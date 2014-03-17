import re

import sublime
import sublime_plugin


class IndentListItemCommand(sublime_plugin.TextCommand):
    bullet_pattern = r'([-+*]|([(]?(\d+|#|[a-y]|[A-Y]|[MDCLXVImdclxvi]+))([).]))'
    bullet_pattern_re = re.compile(bullet_pattern)
    line_pattern_re = re.compile(r'^\s*' + bullet_pattern)
    spaces_re = re.compile(r'^\s*')

    def run(self, edit, reverse=False):
        for region in self.view.sel():
            if region.a != region.b:
                continue

            line = self.view.line(region)
            line_content = self.view.substr(line)

            new_line = line_content

            m = self.line_pattern_re.match(new_line)
            if not m:
                return

            # Determine how to indent (tab or spaces)
            tab_str = self.view.settings().get('tab_size', 4) * ' '
            sep_str = ' ' if m.group(4) else ''

            prev_line = self.view.line(sublime.Region(line.begin() - 1, line.begin() - 1))
            prev_line_content = self.view.substr(prev_line)

            prev_prev_line = self.view.line(sublime.Region(prev_line.begin() - 1, prev_line.begin() - 1))
            prev_prev_line_content = self.view.substr(prev_prev_line)

            if not reverse:
                # Do the indentation
                new_line = self.bullet_pattern_re.sub(tab_str + sep_str + r'\1', new_line)

                # Insert the new item
                if prev_line_content:
                    new_line = '\n' + new_line

            else:
                if not new_line.startswith(tab_str):
                    continue
                # Do the unindentation
                new_line = re.sub(tab_str + sep_str + self.bullet_pattern, r'\1', new_line)

                # Insert the new item
                if prev_line_content:
                    new_line = '\n' + new_line
                else:
                    prev_spaces = self.spaces_re.match(prev_prev_line_content).group(0)
                    spaces = self.spaces_re.match(new_line).group(0)
                    if prev_spaces == spaces:
                        line = sublime.Region(line.begin() - 1, line.end())

            endings = ['.', ')']

            # Transform the bullet to the next/previous bullet type
            if self.view.settings().get('list_indent_auto_switch_bullet', True):
                bullets = self.view.settings().get('list_indent_bullets', ['*', '-', '+'])

                def change_bullet(m):
                    bullet = m.group(1)
                    try:
                        return bullets[(bullets.index(bullet) + (1 if not reverse else -1)) % len(bullets)]
                    except ValueError:
                        pass
                    n = m.group(2)
                    ending = endings[(endings.index(m.group(4)) + (1 if not reverse else -1)) % len(endings)]
                    if n.isdigit():
                        return '${1:a}' + ending
                    elif n != '#':
                        return '${1:0}' + ending
                    return m.group(2) + ending
                new_line = self.bullet_pattern_re.sub(change_bullet, new_line)

            self.view.replace(edit, line, '')
            self.view.run_command('insert_snippet', {'contents': new_line})

    def is_enabled(self):
        return bool(self.view.score_selector(self.view.sel()[0].a, 'text.restructuredtext'))
