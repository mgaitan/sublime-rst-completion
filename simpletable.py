# -*- coding: utf-8 -*-

import re
try:
    from .helpers import BaseBlockCommand
except ValueError:
    from helpers import BaseBlockCommand


class SimpletableCommand(BaseBlockCommand):

    _SEPARATOR = '  '

    def get_result(self, indent, table):
        result = '\n'.join(self._draw_table(indent, table))
        result += '\n'
        return result

    def run(self, edit):
        region, lines, indent = self.get_block_bounds()
        table = self._parse_table(lines)
        result = self.get_result(indent, table)
        self.view.replace(edit, region, result)

    def _split_table_cells(self, row_string):
        return re.split(r'\s\s+', row_string.strip())

    def _parse_table(self, raw_lines):
        parsed_lines = []
        for row_string in raw_lines:
            if not self._row_is_separator(row_string):
                parsed_lines.append(self._split_table_cells(row_string))
        return parsed_lines

    def _row_is_separator(self, row):
        return re.match('^[\t =]+$', row)

    def _table_header_line(self, widths):
        linechar = '='
        parts = []
        for width in widths:
            parts.append(linechar * width)
        return SimpletableCommand._SEPARATOR.join(parts)

    def _get_column_max_widths(self, table):
        widths = []
        for row in table:
            num_fields = len(row)
            # dynamically grow
            if num_fields >= len(widths):
                widths.extend([0] * (num_fields - len(widths)))
            for i in range(num_fields):
                field_width = len(row[i])
                widths[i] = max(widths[i], field_width)
        return widths

    def _pad_fields(self, row, width_formats):
        """ Pad all fields using width formats """
        new_row = []
        for i in range(len(row)):
            col = row[i]
            col = width_formats[i] % col
            new_row.append(col)
        return new_row

    def _draw_table(self, indent, table):
        if not table:
            return []
        col_widths = self._get_column_max_widths(table)
        # Reserve room for separater
        len_sep = len(SimpletableCommand._SEPARATOR)
        sep_col_widths = [(col + len_sep) for col in col_widths]
        width_formats = [('%-' + str(w) + 's' + SimpletableCommand._SEPARATOR) for w in col_widths]

        header_line = self._table_header_line(sep_col_widths)
        output = [indent + header_line]
        first = True
        for row in table:
            # draw the lines (num_lines) for this row
            row = self._pad_fields(row, width_formats)
            output.append(indent + SimpletableCommand._SEPARATOR.join(row))
            # draw the under separator for header
            if first:
                output.append(indent + header_line)
                first = False

        output.append(indent + header_line)
        return output
