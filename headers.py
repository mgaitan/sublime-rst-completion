# py3 import compatibility. Better way to do this?
try:
    from .helpers import BaseBlockCommand
except ValueError:
    from helpers import BaseBlockCommand    # NOQA


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
            title_lenght = len(title.encode("utf-8"))
            strike = adornment_char * title_lenght
            if head_lines == 2:
                result = title + '\n' + strike + '\n'
            else:
                result = strike + '\n' + title + '\n' + strike + '\n'
            self.view.replace(edit, region, result)
