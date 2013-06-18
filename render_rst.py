import sublime
import sublime_plugin
import webbrowser
import tempfile
import os
import re
import os.path
import sys
import subprocess
from subprocess import PIPE


class RenderRstCommand(sublime_plugin.TextCommand):

    TARGETS = ['html (pandoc)', 'html (rst2html)', 'pdf (pandoc)', 'pdf (rst2pdf)',
               'odt (pandoc)', 'odt (rst2odt)', 'docx (pandoc)']

    def is_enabled(self):
        return True

    def is_visible(self):
        return True

    def run(self, edit):
        if not hasattr(self, 'targets'):
            self.targets = RenderRstCommand.TARGETS[:]
        self.view.window().show_quick_panel(self.targets, self.convert,
                                            sublime.MONOSPACE_FONT)

    def convert(self, target_index):
        target, tool = re.match(r"(.*) \((.*)\)", self.targets[target_index]).groups()

        # update targets: last used turns the first option
        self.targets.insert(0, self.targets.pop(target_index))
        encoding = self.view.encoding()
        if encoding == 'Undefined':
            encoding = 'UTF-8'
        elif encoding == 'Western (Windows 1252)':
            encoding = 'windows-1252'
        contents = self.view.substr(sublime.Region(0, self.view.size()))
        contents = contents.encode(encoding)

        file_name = self.view.file_name()
        if file_name:
            os.chdir(os.path.dirname(file_name))

        # write buffer to temporary file
        # This is useful because it means we don't need to save the buffer
        with tempfile.NamedTemporaryFile(delete=False, suffix=".rst") as tmp_rst:
            tmp_rst.write(contents)

        # output file...
        suffix = "." + target
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as output:
            output.close()
            output_name = output.name

        self.run_tool(tmp_rst.name, output_name, tool)
        self.open_result(output_name, target)

    def run_tool(self, infile, outfile, tool):
        if tool in ("pandoc", "rst2pdf"):
            cmd = [tool, infile, "-o", outfile]
        else:
            cmd = ["%s.py" % tool, infile, outfile]

        try:
            # Use the current directory as working dir whenever possible
            file_name = self.view.file_name()
            if file_name:
                working_dir = os.path.dirname(file_name)
                p = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE,
                                     cwd=working_dir)
            else:
                p = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE)
            p.wait()
            out, err = p.communicate()
            if err:
                raise Exception("Command: %s\n" % " ".join(cmd) + "\nErrors: " + err)
        except Exception as e:
            sublime.error_message("Fail to generate output.\n{0}".format(e))

    def open_result(self, outfile, target):
        if target == "html":
            webbrowser.open_new_tab(outfile)
        elif sys.platform == "win32":
            os.startfile(outfile)
        elif "mac" in sys.platform or "darwin" in sys.platform:
            os.system("open %s" % outfile)
            print(outfile)
        elif "posix" in sys.platform or "linux" in sys.platform:
            os.system("xdg-open %s" % outfile)
