# -*- coding: utf-8 -*-
import os
import sublime
import sublime_plugin

RSTPLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))
ERRORS_IN_VIEWS = {}


def lint_external(filename):
    """
    Run rstcheck with external interpreter.
    """
    import subprocess

    # check if active view contains file
    if not filename or not os.path.exists(filename):
        return

    if os.name == 'nt':
        interpreter = 'pythonw'
    else:
        interpreter = 'python'
    # first argument is interpreter
    checker = os.path.join(RSTPLUGIN_DIR, 'rstcheck.py')

    # build checker path for installation from git
    if not os.path.exists(checker):
        checker = os.path.join(
            sublime.packages_path(), 'sublime-rst-completion',
                              'rstcheck.py')

    arguments = [interpreter, checker, filename]

    # place for warnings =)
    warnings = []
    # run subprocess
    proc = subprocess.Popen(arguments, stdout=subprocess.PIPE)

    # parse STDOUT for warnings and errors
    for line in proc.stdout:
        warning = line.strip().split(':', 2)
        warnings.append([int(warning[1]), warning[2], ''])
    # and return them =)
    return warnings


def update_statusbar(view):
    """
    Update status bar with error.
    """
    # get view errors (exit if no errors found)
    view_errors = ERRORS_IN_VIEWS.get(view.id())
    if view_errors is None:
        return

    # get view selection (exit if no selection)
    view_selection = view.sel()
    if not view_selection:
        return

    # get current line (line under cursor)
    current_line = view.rowcol(view_selection[0].end())[0]

    if current_line in view_errors:
        # there is an error on current line
        errors = view_errors[current_line]
        view.set_status('rstchecker',
                        'errors: %s' % ' / '.join(errors))
    else:
        # no errors - clear statusbar
        view.erase_status('rstchecker-tip')


class RstcheckerLintCommand(sublime_plugin.TextCommand):
    """
    Do rstchecker lint on current file.
    """
    def run(self, edit):
        """
        Run rstchecker lint.
        """
        # current file name
        filename = os.path.abspath(self.view.file_name())

        # check if active view contains file
        if not filename:
            return

        # check only rst files
        if not self.view.match_selector(0, 'text.restructuredtext'):
            return

        # we need to always clear regions. three situations here:
        # - we need to clear regions with fixed previous errors
        # - is user will turn off 'highlight' in settings and then run lint
        # - user adds file with errors to 'ignore_files' list
        self.view.erase_regions('rstchecker-errors')

        # we need to always erase status too. same situations.
        self.view.erase_status('rstchecker-tip')

        # save file if dirty
        # if self.view.is_dirty():
        #    self.view.run_command('save')

        # and lint file in subprocess
        self.errors_list = lint_external(filename)

        # show errors
        if self.errors_list:
            self.show_errors()

    def show_errors(self):
        """
        Show all errors.
        """
        errors_to_show = []

        # config vars
        select = []
        ignore = []
        is_highlight = True
        is_popup = True

        regions = []
        view_errors = {}
        errors_list_filtered = []

        for e in self.errors_list:
            current_line = e[0] - 1
            error_text = e[2]

            # get error line
            text_point = self.view.text_point(current_line, 0)
            line = self.view.full_line(text_point)
            full_line_text = self.view.substr(line)
            line_text = full_line_text.strip()


            # build error text
            error = [error_text, u'{0}: {1}'.format(current_line + 1,
                                                    line_text)]
            # skip if this error is already found (with pep8 or rstchecker)
            if error in errors_to_show:
                continue
            errors_to_show.append(error)

            # build line error message
            if is_popup:
                errors_list_filtered.append(e)

            # prepare errors regions
            if is_highlight:
                # prepare line
                line_text = full_line_text.rstrip('\r\n')
                line_length = len(line_text)

                # calculate error highlight start and end positions
                start = text_point + line_length - len(line_text.lstrip())
                end = text_point + line_length

                regions.append(sublime.Region(start, end))

            # save errors for each line in view to special dict
            view_errors.setdefault(current_line, []).append(error_text)

        # renew errors list with selected and ignored errors
        self.errors_list = errors_list_filtered
        # save errors dict
        ERRORS_IN_VIEWS[self.view.id()] = view_errors

        # highlight error regions if defined
        if is_highlight:
            self.view.add_regions('rstchecker-errors', regions,
                                  'invalid.deprecated', '',
                                  sublime.DRAW_OUTLINED)

        if is_popup:
            # view errors window
            self.view.window().show_quick_panel(errors_to_show,
                                                self.error_selected)

    def error_selected(self, item_selected):
        """
        Error was selected - go to error.
        """
        if item_selected == -1:
            return

        # reset selection
        selection = self.view.sel()
        selection.clear()

        # get error region
        error = self.errors_list[item_selected]
        region_begin = self.view.text_point(error[0] - 1, len(error[1]))

        # go to error
        selection.add(sublime.Region(region_begin, region_begin))
        self.view.show_at_center(region_begin)
        update_statusbar(self.view)


class RstcheckerLintBackground(sublime_plugin.EventListener):
    """
    Listen to Sublime Text events.
    """
    def on_post_save(self, view):
        """
        Do lint on file save if not denied in settings.
        """
        view.run_command('rstchecker_lint')

    def on_selection_modified(self, view):
        """
        Selection was modified: update status bar.
        """
        update_statusbar(view)
