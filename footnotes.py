import sublime
import sublime_plugin
import re

DEFINITION_KEY = 'footnote-definitions'
REFERENCE_KEY = 'footnote-references'
REFERENCE_REGEX = r'\[(\d+)\]\_'
DEFINITION_REGEX = r"^\.\.\s\[(\d+)\]"


def get_footnote_references(view):
    ids = {}
    for ref in view.get_regions(REFERENCE_KEY):
        view.substr(view.line(ref))
        if not re.match(DEFINITION_REGEX, view.substr(view.line(ref))):
            id = re.findall(r'\d+', view.substr(ref))[0]
            if id in ids:
                ids[id].append(ref)
            else:
                ids[id] = [ref]
    return ids


def get_footnote_definition_markers(view):
    ids = {}
    for defn in view.get_regions(DEFINITION_KEY):
        id = view.substr(defn).strip()[4:-2]
        ids[id] = defn
    return ids


def get_footnote_identifiers(view):
    ids = get_footnote_references(view).keys()
    ids.sort()
    return ids


def get_last_footnote_marker(view):
    ids = sorted([int(a) for a in get_footnote_identifiers(view) if a.isdigit()])
    if len(ids):
        return int(ids[-1])
    else:
        return 0


def get_next_footnote_marker(view):
    return get_last_footnote_marker(view) + 1


def is_footnote_definition(view):
    line = view.substr(view.line(view.sel()[-1]))
    return re.match(DEFINITION_REGEX, line)


def is_footnote_reference(view):
    refs = view.get_regions(REFERENCE_KEY)
    for ref in refs:
        if ref.contains(view.sel()[0]):
            return True
    return False


def strip_trailing_whitespace(view, edit):
    tws = view.find('\s+\Z', 0)
    if tws:
        view.erase(edit, tws)


class Footnotes(sublime_plugin.EventListener):
    def update_footnote_data(self, view):
        view.add_regions(REFERENCE_KEY,
                         view.find_all(REFERENCE_REGEX),
                         '', 'cross',
                         )
        view.add_regions(DEFINITION_KEY,
                         view.find_all(DEFINITION_REGEX),
                         '',
                         'cross',
                         )

    def on_modified(self, view):
        self.update_footnote_data(view)

    def on_load(self, view):
        self.update_footnote_data(view)


class InsertFootnoteCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        edit = self.view.begin_edit()
        startloc = self.view.sel()[-1].end()
        markernum = get_next_footnote_marker(self.view)
        if bool(self.view.size()):
            targetloc = self.view.find('(\s|$)', startloc).begin()
        else:
            targetloc = 0
        self.view.insert(edit, targetloc, '[%s]_' % markernum)
        self.view.insert(edit, self.view.size(), '\n.. [%s] ' % markernum)
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(self.view.size()))
        self.view.end_edit(edit)

    def is_enabled(self):
        return self.view.sel()
