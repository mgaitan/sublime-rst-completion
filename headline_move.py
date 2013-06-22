import sublime
import sublime_plugin
import re
from collections import namedtuple

ADORNEMENTS = r"[\!\"\#\$\%\&\\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\\\]\\^\_\`\{\|\}\~]"
PATTERN = r"^(%s*)\n(?P<title>.+)\n(?P<underline>%s+)" % (ADORNEMENTS,ADORNEMENTS)

Header = namedtuple('Header', "level start end adornement title raw")


class RstHeaderTree(object):

    def __init__(self, text):
        self.headers = self._parse(text)
        self._text_lenght = len(text)

    def _parse(self, text):
        """
        Given a chunk of restructuredText, returns a list of tuples
        (level, start, end, adornement, title, raw) for each header found.


        level: int (zero-based). the "weight" of the header.
        start: index where the header starts
        end: index where the header ends
        adornement: one (just underlined) or two char (over and underline) string
                    that represent the adornement,
        title: the parsed title
        raw : the raw parsed header text, including breaks.

        """

        candidates = re.findall(PATTERN, text, re.MULTILINE)
        headers = []
        levels = []

        for candidate in candidates:
            (over, title, under) = candidate
            # validate
            if (over == '' or over == under) and len(under) >= len(title):
                # encode the adornement of the header to calculate its level
                adornement = under[0] * (2 if over else 1)
                if adornement not in levels:
                    levels.append(adornement)
                level = levels.index(adornement)
                raw = "\n".join(candidate)
                start = text.find(raw)
                end = start + len(raw)
                h = Header(level, start, end, adornement, title, raw)
                headers.append(h)
        return headers

    def belong_to(self, pos):
        """
        given a cursor position, return the deeper header
        that contains it
        """
        match = []
        for h in self.headers:
            start, end = self.region(h)
            if start <= pos <= end:
                match.append(h)
        try:
            return sorted(match, key=lambda h: h.level, reverse=True)[0]
        except IndexError:
            return None


    def level(self, level):
        """filter headers by level"""
        return [h for h in self.headers if h.level == level]


    def region(self, header):
        """
        determines the (start, end) region under the given header
        A region ends when a header of the same or higher level (i.e lower number)
        is found or at the EOF
        """

        try:
            index = self.headers.index(header)
        except ValueError:
            return

        start = header.start
        if index == len(self.headers) - 1:     # last header
            return (start, self._text_lenght)

        for next_h in self.headers[index + 1:]:
            if next_h.level <= header.level:
                return (start, next_h.start - 1)

        return (start, self._text_lenght)

    def next(self, header, same_level=False):
        """given a header returns the closer header
           (down direction)

           If same_level is true, only move to headline with the same level
           or higher level.
        """
        if same_level:
            headers = [h for h in self.headers
                       if h.level <= header.level]
        else:
            headers = self.headers[:]

        index = headers.index(header)
        print [(h.level, h.title) for h in headers][index:]
        try:
            return headers[index + 1]
        except IndexError:
            return None

    def prev(self, header, same_level=False):
        """same than next, but in reversed direction
        """
        if same_level:
            headers = [h for h in self.headers
                       if h.level <= header.level]

        else:
            headers = self.headers[:]

        index = headers.index(header)
        if index == 0:
            return None
        return headers[index - 1]


class HeadlineMoveCommand(sublime_plugin.TextCommand):
    # inspired on the code of Muchenxuan Tong in
    # https://github.com/demon386/SmartMarkdown

    def run(self, edit, forward=True, same_level=True):
        """Move between headlines, forward or backward.

        If same_level is true, only move to headline with the same level
        or higher level.

        """
        cursor_pos = self.view.sel()[0].begin()
        region = sublime.Region(0, self.view.size())
        tree = RstHeaderTree(self.view.substr(region))
        parent_belong = tree.belong_to(cursor_pos)

        if forward:
            h = tree.next(parent_belong, same_level)
        else:
            h = tree.prev(parent_belong, same_level)
        if h:
            self.jump_to(h.end - len(h.raw.split('\n')[-1]) -1 )

    def jump_to(self, pos):
        region = sublime.Region(pos, pos)
        self.view.sel().clear()
        self.view.sel().add(region)
        self.view.show(region)



if __name__ == '__main__':

    rst = """

***
h1
***

fddsfa



h2
---

h3
**

h2 2
-----

+++
h4
+++

h5
$$

"""
    tree = RstHeaderTree(rst)
    print "lenght", tree._text_lenght
    for h in tree.headers:
        print h
        print tree.region(h)

