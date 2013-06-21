"""
inspired on the code of Muchenxuan Tong in
https://github.com/demon386/SmartMarkdown
"""

import sublime
import sublime_plugin

try:
    from .headers_utils import parse_headers
except ValueError:
    from headers_utils import parse_headers


class HeadlineMoveCommand(sublime_plugin.TextCommand):
    def run(self, edit, forward=True, same_level=True):
        """Move between headlines, forward or backward.

        If same_level is true, only move to headline with the same level
        or higher level.

        """
        cursor_pos = self.view.rowcol(self.view.sel()[0].begin())
        region = sublime.Region(0, self.view.size())
        rst = self.view.substr(region)
        headers = parse_headers(rst)
        print headers
        return

        for region in self.view.sel():
            if same_level:
                _, level = headline.headline_and_level_at_point(self.view,\
                                                                region.a,
                                                                search_above_and_down=True)
                if level is None:
                    return
            else:
                level = headline.ANY_LEVEL

            match_region, _ = headline.find_headline(self.view, \
                                                     region.a, \
                                                     level, \
                                                     forward, \
                                                     level_type, \
                                                     skip_headline_at_point=True,\
                                                     skip_folded=True)

            if is_region_void(match_region):
                return
            new_sel.append(sublime.Region(match_region.a, match_region.a))

        self.adjust_view(new_sel)

    def adjust_view(self, new_sel):
        self.view.sel().clear()
        for region in new_sel:
            self.view.sel().add(region)
            self.view.show(region)
