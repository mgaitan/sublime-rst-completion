import re
from collections import namedtuple


ADORNEMENTS = r"[\!\"\#\$\%\&\\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\\\]\\^\_\`\{\|\}\~]"
PATTERN = r"^(%s*)\n(?P<title>.+)\n(?P<underline>%s+)" % (ADORNEMENTS,ADORNEMENTS)


Header = namedtuple('Header', "level start end adornement title raw")


def parse_headers(text):
    """
    Given a chunk of restructuredText, returns a list of tuples
    (level, start, end, adornement, title, raw) for each header found.


    level: int (zero-based). the "weight" of the header.
    start: index where the header starts
    end: index where the header ends
    adornement: one (just underlined) or two char (over and underline) string
                that represent the adornement,
    title: the parsed title
    raw : the raw parsed header text, including breaks.

    """

    candidates = re.findall(PATTERN, text, re.MULTILINE)
    headers = []
    levels = []

    for candidate in candidates:
        (over, title, under) = candidate
        # validate
        if (over == '' or over == under) and len(under) >= len(title):
            # encode the adornement of the header to calculate its level
            adornement = under[0] * (2 if over else 1)
            if adornement not in levels:
                levels.append(adornement)
            level = levels.index(adornement)
            raw = "\n".join(candidate)
            start = text.find(raw)
            end = start + len(raw)
            h = Header(level, start, end, adornement, title, raw)
            headers.append(h)
    return headers


if __name__ == '__main__':

    rst = """

***
h1
***

fddsfa



h2
---

h3
**

h2 2
-----

+++
h4
+++

h5
$$

"""

    for h in parse_headers(rst):
        print h
