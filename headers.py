import sublime
import sublime_plugin
import re
from collections import namedtuple
# py3 import compatibility. Better way to do this?
try:
    from .helpers import BaseBlockCommand
except ValueError:
    from helpers import BaseBlockCommand    # NOQA


# reference:
#   http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#sections
ADORNEMENTS = r"""[!"#$%&'\\()*+,\-./:;<=>?@\[\]\^_`{|}~]"""
PATTERN = r"^(%s*)\n(?P<tit>.+)\n(?P<under>%s+)" % (ADORNEMENTS,
                                                    ADORNEMENTS)

Header = namedtuple('Header', "level start end adornement title raw")


class RstHeaderTree(object):
    # based on sphinx's header conventions
    DEFAULT_HEADERS = {0: '**', 1: '=', 2:'-', 3:'^', 4:'"', 5:'+',
                       6:'~', 7:'#', 8:"'", 9:':'}

    def __init__(self, text):
        # add a ficticius break as first line
        # to allow catching a very first header without overline.
        # This imply any position returned (Header.start, Header.end)
        # must be decremented one character

        self.headers = self._parse('\n' + text)
        self._text_lenght = len(text)

    def _parse(self, text):
        """
        Given a chunk of restructuredText, returns a list of tuples
        (level, start, end, adornement, title, raw) for each header found.


        level: int (zero-based). the "weight" of the header.
        start: index where the header starts
        end: index where the header ends
        adornement: one (just underlined) or two char
                    (over and underline) string
                    that represent the adornement,
        title: the parsed title
        raw : the raw parsed header text, including breaks.

        """

        candidates = re.findall(PATTERN, text, re.MULTILINE)
        headers = []
        levels = []

        for candidate in candidates:
            (over, title, under) = candidate
            # validate.
            if ((over == '' or over == under) and len(under) >= len(title)
                    and len(set(under)) == 1):
                # encode the adornement of the header to calculate its level
                adornement = under[0] * (2 if over else 1)
                if adornement not in levels:
                    levels.append(adornement)
                level = levels.index(adornement)
                raw = "\n".join(candidate)
                start = text.find(raw) - 1    # see comment on __init__
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

    def region(self, header):
        """
        determines the (start, end) region under the given header
        A region ends when a header of the same or higher level
        (i.e lower number) is found or at the EOF
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

    def _index(self, header, same_or_high=False):
        """
        helper method that returns the absolute index
        of the header in the tree or a filteredr tree
        If same_or_high is true, only move to headline with the same level
        or higher level.

        returns (index, headers)
        """
        if same_or_high:
            headers = [h for h in self.headers
                       if h.level <= header.level]
        else:
            headers = self.headers[:]
        return headers.index(header), headers

    def next(self, header, same_or_high=False):
        """
        given a header returns the closer header
        (down direction)
        """
        index, headers = self._index(header, same_or_high)
        try:
            return headers[index + 1]
        except IndexError:
            return None

    def prev(self, header, same_or_high=False, offset=-1):
        """same than next, but in reversed direction
        """
        index, headers = self._index(header, same_or_high)
        if index == 0:
            return None
        return headers[index + offset]

    def levels(self):
        """ returns the heading adornement map"""
        levels = RstHeaderTree.DEFAULT_HEADERS.copy()
        for h in self.headers:
            levels[h.level] = h.adornement
        return levels

    @classmethod
    def make_header(cls, title, adornement, force_overline=False):
        title_lenght = len(title.encode("utf-8"))
        strike = adornement[0] * title_lenght
        if force_overline or len(adornement) == 2:
            result = strike + '\n' + title + '\n' + strike + '\n'
        else:
            result = title + '\n' + strike + '\n'
        return result



class HeaderChangeLevelCommand(sublime_plugin.TextCommand):
    """
    increase or decrease the header level,
    The level markup is autodetected from the document,
    and use sphinx's convention by default.
    """

    def run(self, edit, offset=-1):
        cursor_pos = self.view.sel()[0].begin()
        region = sublime.Region(0, self.view.size())
        tree = RstHeaderTree(self.view.substr(region))
        levels = tree.levels()

        parent = tree.belong_to(cursor_pos)
        hregion = sublime.Region(parent.start + 1, parent.end + 1)
        if not (parent.start < cursor_pos <= parent.end):
            return

        if offset == -1 and parent.level == 0:
            return

        if offset == 1 and parent.level == max(levels.keys()):
            return

        adornement = levels[parent.level + offset]
        new_header = RstHeaderTree.make_header(parent.title, adornement)
        self.view.replace(edit, hregion, new_header)



class HeadlineMoveCommand(sublime_plugin.TextCommand):
    # briefly inspired on the code of Muchenxuan Tong in
    # https://github.com/demon386/SmartMarkdown

    def run(self, edit, forward=True, same_or_high=True):
        """Move between headlines, forward or backward.

        If same_or_high is true, only move to headline with the same level
        or higher level.

        """
        cursor_pos = self.view.sel()[0].begin()
        region = sublime.Region(0, self.view.size())
        tree = RstHeaderTree(self.view.substr(region))
        parent = tree.belong_to(cursor_pos)

        if forward:
            h = tree.next(parent, same_or_high)
        else:
            is_in_header = parent.start <= cursor_pos <= parent.end
            offset = -1 if is_in_header else 0
            h = tree.prev(parent, same_or_high, offset)
        if h:
            self.jump_to(h.end - len(h.raw.split('\n')[-1]) - 1)

    def jump_to(self, pos):
        region = sublime.Region(pos, pos)
        self.view.sel().clear()
        self.view.sel().add(region)
        self.view.show(region)


class SmartFoldingCommand(sublime_plugin.TextCommand):
    """Smart folding is used to fold / unfold headline at the point.

    It's designed to bind to TAB key, and if the current line is not
    a headline, a \t would be inserted.

    """
    def run(self, edit):

        cursor_pos = self.view.sel()[0].begin()
        region = sublime.Region(0, self.view.size())
        tree = RstHeaderTree(self.view.substr(region))
        parent = tree.belong_to(cursor_pos)
        is_in_header = parent.start <= cursor_pos <= parent.end
        if is_in_header:
            start, end = tree.region(parent)
            start += len(parent.raw) + 1
            region = sublime.Region(start, end)
            if any([i.contains(region) for i in
                    self.view.folded_regions()]):
                self.view.unfold(region)
            else:
                self.view.fold(region)
        else:
            for r in self.view.sel():
                self.view.insert(edit, r.a, '\t')
                self.view.show(r)


class SmartHeaderCommand(BaseBlockCommand):
    def run(self, edit):
        for region in self.view.sel():
            region, lines, indent = self.get_block_bounds()
            head_lines = len(lines)
            adornment_char = lines[-1][0]

            if (head_lines not in (2, 3) or
                    head_lines == 3 and lines[-3][0] != adornment_char):
                # invalid header
                return

            title = lines[-2]
            force_overline = head_lines == 3
            result = RstHeaderTree.make_header(title, adornment_char, force_overline)
            self.view.replace(edit, region, result)
