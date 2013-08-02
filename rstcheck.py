#!/usr/bin/env python

import sys
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO
from docutils.core import publish_doctree
from docutils import nodes
from docutils import io
from docutils import utils


class CaptureStdIO(object):

    def __enter__(self):
        self._orig_stdin = sys.stdin
        self._orig_stdout = sys.stdout
        self._orig_stderr = sys.stderr

        self.stdin = sys.stdin = StringIO()
        self.stdout = sys.stdout = StringIO()
        self.stderr = sys.stderr = StringIO()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdin = self._orig_stdin
        sys.stdout = self._orig_stdout
        sys.stderr = self._orig_stderr

    def read_stdout(self):
        self.stdout.seek(0)
        return self.stdout.read()

    def read_stderr(self):
        self.stderr.seek(0)
        return self.stderr.read()


def getlevel(nd):
    return TYPE_TO_LEVEL[nd.attributes['type']]

TYPE_TO_LEVEL = dict((l, i) for (i, l) in enumerate(utils.Reporter.levels))


def head(lst):
    return lst[0] if lst else None


def rstflakes(file, report, normal):
    with CaptureStdIO() as stdio:
        doctree = publish_doctree(
            source=None,
            source_path=file,
            source_class=io.FileInput,
            )

    if normal:
        sys.stdout.write(stdio.read_stdout())
        sys.stderr.write(stdio.read_stderr())
    else:
        error = '{0}:{1}: {2} ({3})'.format
        warn = '{0}:{1}: WARNING {2} ({3})'.format
        for smsg in doctree.traverse(nodes.system_message):
            level = getlevel(smsg)
            if level >= report:
                # see: docutils.nodes.system_message
                body = head(smsg.traverse(nodes.Text))
                body = body.replace("\n", " ")
                if 'Unknown directive type' in body:
                    continue
                if 'Unknown interpreted text role' in body:
                    continue
                if 'Substitution definition contains illegal element' in body:
                    # there will be error message for the contents it
                    # self so let's ignore it.
                    continue
                path = smsg.attributes['source']
                line = smsg.get('line', '')
                if level >= TYPE_TO_LEVEL['ERROR']:
                    print error(path, line, body, level)
                else:
                    print warn(path, line, body, level)


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser(
        description='ReST checker for flymake')
    parser.add_argument(
        'file', help='ReST file')
    parser.add_argument(
        '--report', '-r', default=2,
        help='report level (0<=level<=5; default: %(default)s)')
    parser.add_argument(
        '--normal', '-n', action='store_true',
        help='print normal rst2* output')
    args = parser.parse_args()
    rstflakes(**vars(args))


if __name__ == '__main__':
    main()
