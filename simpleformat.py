import sublime
import sublime_plugin


class SurroundCommand(sublime_plugin.TextCommand):
    """
    Base class to surround the selection with text.
    """
    surround = ''

    def run(self, edit):
        for sel in self.view.sel():
            len_surround = len(self.surround)
            sel_str = self.view.substr(sel)
            rsel = sublime.Region(sel.begin() - len_surround, sel.end() + len_surround)
            rsel_str = self.view.substr(rsel)
            print((sel_str[:len_surround], sel_str[-len_surround:]))
            if sel_str[:len_surround] == self.surround and sel_str[-len_surround:] == self.surround:
                replacement = sel_str[len_surround:-len_surround]
            else:
                replacement = "%s%s%s" % (self.surround, sel_str, self.surround)
            if rsel_str == replacement:
                self.view.sel().subtract(sel)
                self.view.replace(edit, rsel, sel_str)
                self.view.sel().add(sublime.Region(rsel.begin(), rsel.begin() + len(sel_str)))
            else:
                self.view.replace(edit, sel, replacement)


class StrongemphasisCommand(SurroundCommand):
    surround = "**"


class EmphasisCommand(SurroundCommand):
    surround = "*"


class LiteralCommand(SurroundCommand):
    surround = "``"


class SubstitutionCommand(SurroundCommand):
    surround = "|"
