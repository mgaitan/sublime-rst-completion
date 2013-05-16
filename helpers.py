import re

from sublime import Region
import sublime_plugin


class BaseBlockCommand(sublime_plugin.TextCommand):

    def _get_row_text(self, row):

        if row < 0 or row > self.view.rowcol(self.view.size())[0]:
            raise RuntimeError('Cannot find table bounds.')

        point = self.view.text_point(row, 0)
        region = self.view.line(point)
        text = self.view.substr(region)
        return text

    def get_cursor_position(self):
        return self.view.rowcol(self.view.sel()[0].begin())

    def get_block_bounds(self):
        """given the cursor position as started point,
           returns the limits and indentation"""
        row, col = self.get_cursor_position()
        upper = lower = row

        try:
            while self._get_row_text(upper - 1).strip():
                upper -= 1

        except Exception as e:
            print e
            pass
        else:
            upper += 1

        try:
            while self._get_row_text(lower + 1).strip():
                lower += 1
        except Exception as e:
            print e
            pass
        else:
            lower -= 1

        block_region = Region(self.view.text_point(upper - 1, 0),
                              self.view.text_point(lower + 2, 0))
        lines = [self.view.substr(region) for region in self.view.lines(block_region)]
        indent = re.match('^(\s*).*$', self._get_row_text(upper - 1)).group(1)
        return block_region, lines, indent
