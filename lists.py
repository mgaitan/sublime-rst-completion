# -*- coding: utf-8 -*-

"""Smart list is used to automatially continue the current list."""
# Author: Muchenxuan Tong <demon386@gmail.com>

# Original from https://github.com/demon386/SmartMarkdown with this patch:
# https://github.com/vovkkk/SmartMarkdown/commit/bb1bb76179771212c1f21883d9b64d0a299fc98c
# roman number conversion from Mark Pilgrim's "Dive into Python"

# Modified by Martín Gaitán <gaitan@gmail.com>

import re

import sublime
import sublime_plugin
try:
    from .helpers import BaseBlockCommand
except ValueError:
    from helpers import BaseBlockCommand    # NOQA



ORDER_LIST_PATTERN = re.compile(r"(\s*[(]?)(\d+|[a-y]|[A-Y])([.)]\s+)(.*)")
UNORDER_LIST_PATTERN = re.compile(r"(\s*(?:[-+|*]+|[(]?#[).]))(\s+)\S+")
EMPTY_LIST_PATTERN = re.compile(r"(\s*)([-+*]|[(]?(?:\d+|[a-y]|[A-Y]|#|[MDCLXVImdclxvi]+)[.)])(\s+)$")
NONLIST_PATTERN = re.compile(r"(\s*[>|%]+)(\s+)\S?")
ROMAN_PATTERN = re.compile(r"(\s*[(]?)(M{0,4}CM|CD|D?C{0,3}XC|XL|L?X{0,3}IX|IV|V?I{0,3})([.)]\s+)(.*)",
                           re.IGNORECASE)
#Define digit mapping
ROMAN_MAP = (('M', 1000),
             ('CM', 900),
             ('D', 500),
             ('CD', 400),
             ('C', 100),
             ('XC', 90),
             ('L', 50),
             ('XL', 40),
             ('X', 10),
             ('IX', 9),
             ('V', 5),
             ('IV', 4),
             ('I', 1))

#Define exceptions
class RomanError(Exception): pass
class NotIntegerError(RomanError): pass
class InvalidRomanNumeralError(RomanError): pass


def to_roman(n):
    """convert integer to Roman numeral"""
    if not (0 < n < 5000):
        raise Exception("number out of range (must be 1..4999)")
    result = ""
    for numeral, integer in ROMAN_MAP:
        while n >= integer:
            result += numeral
            n -= integer
    return result

def from_roman(s):
    """convert Roman numeral to integer"""
    result = 0
    index = 0
    for numeral, integer in ROMAN_MAP:
        while s[index:index + len(numeral)] == numeral:
            result += integer
            index += len(numeral)
    return result


class SmartListCommand(BaseBlockCommand):


    def run(self, edit):

        def update_ordered_list(lines):
            new_lines = []
            next_num = None
            kind = lambda a: a
            for line in lines:
                match = ORDER_LIST_PATTERN.match(line)
                if not match:
                    new_lines.append(line)
                    continue
                new_line = match.group(1) + \
                              (kind(next_num) or match.group(2)) + \
                              match.group(3) + match.group(4)
                new_lines.append(new_line)

                if not next_num:
                    try:
                        next_num = int(match.group(2))
                        kind = str
                    except ValueError:
                        next_num = ord(match.group(2))
                        kind = chr
                next_num += 1
            return new_lines

        def update_roman_list(lines):
            new_lines = []
            next_num = None
            kind = lambda a: a
            for line in lines:
                match = ROMAN_PATTERN.match(line)
                if not match:
                    new_lines.append(line)
                    continue
                new_line = match.group(1) + \
                              (kind(next_num) or match.group(2)) + \
                              match.group(3) + match.group(4)
                new_lines.append(new_line)

                if not next_num:
                    actual = match.group(2)
                    next_num = from_roman(actual.upper())

                    if actual == actual.lower():
                        kind = lambda a: to_roman(a).lower()
                    else:
                        kind = to_roman
                next_num += 1
            return new_lines



        for region in self.view.sel():
            line_region = self.view.line(region)
            # the content before point at the current line.
            before_point_region = sublime.Region(line_region.a,
                                                 region.a)
            before_point_content = self.view.substr(before_point_region)
            # Disable smart list when folded.
            folded = False
            for i in self.view.folded_regions():
                if i.contains(before_point_region):
                    self.view.insert(edit, region.a, '\n')
                    folded = True
            if folded:
                break

            match = EMPTY_LIST_PATTERN.match(before_point_content)
            if match:
                insert_text = match.group(1) + \
                              re.sub(r'\S', ' ', str(match.group(2))) + \
                              match.group(3)
                self.view.erase(edit, before_point_region)
                self.view.insert(edit, line_region.a, insert_text)
                break

            match = ROMAN_PATTERN.match(before_point_content)
            if match:
                actual = match.group(2)
                next_num = to_roman(from_roman(actual.upper()) + 1)
                if actual == actual.lower():
                    next_num = next_num.lower()

                insert_text = match.group(1) + \
                              next_num + \
                              match.group(3)
                self.view.insert(edit, region.a, "\n" + insert_text)

                # backup the cursor position
                pos = self.view.sel()[0].a

                # update the whole list
                region, lines, indent = self.get_block_bounds()
                new_list = update_roman_list(lines)
                self.view.replace(edit, region, '\n'.join(new_list) + '\n')
                # restore the cursor position
                self.view.sel().clear()
                self.view.sel().add(sublime.Region(pos, pos))
                self.view.show(pos)

                break


            match = ORDER_LIST_PATTERN.match(before_point_content)
            if match:
                try:
                    next_num = str(int(match.group(2)) + 1)
                except ValueError:
                    next_num = chr(ord(match.group(2)) + 1)

                insert_text = match.group(1) + \
                              next_num + \
                              match.group(3)
                self.view.insert(edit, region.a, "\n" + insert_text)

                # backup the cursor position
                pos = self.view.sel()[0].a

                # update the whole list
                region, lines, indent = self.get_block_bounds()
                new_list = update_ordered_list(lines)
                self.view.replace(edit, region, '\n'.join(new_list) + '\n')
                # restore the cursor position
                self.view.sel().clear()
                self.view.sel().add(sublime.Region(pos, pos))
                self.view.show(pos)
                break

            match = UNORDER_LIST_PATTERN.match(before_point_content)
            if match:
                insert_text = match.group(1) + match.group(2)
                self.view.insert(edit, region.a, "\n" + insert_text)
                break

            match = NONLIST_PATTERN.match(before_point_content)
            if match:
                insert_text = match.group(1) + match.group(2)
                self.view.insert(edit, region.a, "\n" + insert_text)
                break

            self.view.insert(edit, region.a, '\n' + \
                             re.sub(r'\S+\s*', '', before_point_content))
        self.adjust_view()

    def adjust_view(self):
        for region in self.view.sel():
            self.view.show(region)
