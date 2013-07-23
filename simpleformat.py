import sublime
import sublime_plugin


class SurroundCommand(sublime_plugin.TextCommand):
    """
    Base class to surround the selection with text.
    """
    surround = ''

    def run(self, edit):
        for sel in self.view.sel():
            replacement = "%s%s%s" % (self.surround, self.view.substr(sel), self.surround)
            self.view.replace(edit, sel, replacement)


class StrongEmphasisCommand(SurroundCommand):
    surround = "**"


class EmphasisCommand(SurroundCommand):
    surround = "*"


class LiteralCommand(SurroundCommand):
    surround = "``"


class SubstitutionCommand(SurroundCommand):
    surround = "|"
