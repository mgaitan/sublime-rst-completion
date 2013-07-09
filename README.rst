Sublime Text Restructured Text Code Completion (rst)
=======================================================

A group of snippets and commands to facilitate writing restructuredText
with Sublime text editor. This plugin will hopefully evolve to make
Sublime a useful documentation toolkit.

.. contents::

Install
-------

The easiest way to install is via `Sublime Package Control <http://wbond.net/sublime_packages/package_control>`_ . Just look for *"Restructured Text (RST) Snippets"*

Otherwise you can:

- Clone the repository into
  your `packages folder <http://sublimetext.info/docs/en/basic_concepts.html#the-packages-directory>`_::

      git clone git@github.com:dbousamra/sublime-rst-completion.git

- Or download the `.zip`_ file and unzip it into your ST2 packages
  directory.

Optionally, to use the `preview rendering`_ feature, you need to install at least one of
Pandoc_, docutils_ or rst2pdf_ and they should be accesibles in your ``PATH``.
In debian/ubuntu you can install them via ``apt-get``::

    $ sudo apt-get install pandoc docutils rst2pdf

.. _Pandoc: http://johnmacfarlane.net/pandoc/
.. _rst2pdf: http://rst2pdf.ralsina.com.ar/
.. _docutils: http://docutils.sourceforge.net/

Usage
-----

Simple snippets work as tab-triggered shortcuts: type the shortcut and press ``<TAB>`` to
replace it with the snippet. If the snippet has placeholders, you can jump between them
using tab.

+------------------------+------------------------------------+----------------------------+
| shortcut               | result                             | key binding                |
+========================+====================================+============================+
| ``h1``                 | Header level 1                     | see `Header completion`_   |
+------------------------+------------------------------------+----------------------------+
| ``h2``                 | Header level 2                     |                            |
+------------------------+------------------------------------+----------------------------+
| ``h3``                 | Header level 3                     |                            |
+------------------------+------------------------------------+----------------------------+
| ``e``                  | emphasis                           | ``ctrl+i``                 |
|                        |                                    | (``super+shift+i`` on Mac) |
+------------------------+------------------------------------+----------------------------+
| ``se``                 | strong emphasis (bold)             | ``ctrl+b``                 |
|                        |                                    | (``super+shift+b`` on Mac) |
+------------------------+------------------------------------+----------------------------+
| ``lit`` or ``literal`` | literal text (inline code)         | ``ctrl+k``                 |
|                        |                                    | (``super+shift+k`` on Mac) |
+------------------------+------------------------------------+----------------------------+
| ``list``               | unordered list                     | see `Smart Lists`_         |
+------------------------+------------------------------------+----------------------------+
| ``listn``              | ordered list                       |                            |
+------------------------+------------------------------------+----------------------------+
| ``listan``             | auto ordered list                  |                            |
+------------------------+------------------------------------+----------------------------+
| ``def``                | term definition                    |                            |
+------------------------+------------------------------------+----------------------------+
| ``code``               | code-block directive (sphinx)      |                            |
+------------------------+------------------------------------+----------------------------+
| ``source``             | preformatted (``::`` block)        |                            |
+------------------------+------------------------------------+----------------------------+
| ``img``                | image                              |                            |
+------------------------+------------------------------------+----------------------------+
| ``fig``                | figure                             |                            |
+------------------------+------------------------------------+----------------------------+
| ``table``              | simple table                       | ``ctrl+t`` see `Magic      |
|                        |                                    | Tables`_                   |
+------------------------+------------------------------------+----------------------------+
| ``link``               | refered hyperlink                  |                            |
+------------------------+------------------------------------+----------------------------+
| ``linki``              | embeded hyperlink                  |                            |
+------------------------+------------------------------------+----------------------------+
| ``fn`` or ``cite``     | autonumbered footnote or cite      | ``alt+shift+f`` see        |
|                        |                                    | `Magic Footnotes`_         |
+------------------------+------------------------------------+----------------------------+
| ``quote``              | Quotation (``epigraph`` directive) |                            |
+------------------------+------------------------------------+----------------------------+

Also standard admonitions are expanded:

+---------------+
| shortcut      |
+===============+
| ``attention`` |
+---------------+
| ``caution``   |
+---------------+
| ``danger``    |
+---------------+
| ``error``     |
+---------------+
| ``hint``      |
+---------------+
| ``important`` |
+---------------+
| ``note``      |
+---------------+
| ``tip``       |
+---------------+
| ``warning``   |
+---------------+


.. _preview rendering:

Render preview
---------------

You can preview your document in different formats converted with different tools
pressing ``ctrl+shift+r``.

The *Quick Window* will offer the format and tool and the result will be automatically open
after the conversion.

By the moment, it can use Pandoc_, rst2pdf_, or ``rst2*.py`` tools (included with
docutils_) to produce ``html``, ``pdf``, ``odt`` or ``docx`` output formats.

Each time you select a ``format + tool`` option, it turns the default the following times.

.. note::

    The original code is from the `SublimePandoc <https://github.com/jclement/SublimePandoc>`_
    project.


.. _tables:

Magic Tables
------------

There is a particular *magic* expansion for tables. Here is how it works:

1. Create some kind of table outline, separating column with two or more spaces::


      This is paragraph text *before* the table.

      Column 1  Column 2
      Foo  Put two (or more) spaces as a field separator.
      Bar  Even very very long lines like these are fine, as long as you do not put in line endings here.

      This is paragraph text *after* the table.

2. Put your cursor somewhere in the content to convert as table.
3. Press ``ctrl+t, enter`` (Linux or Windows) or ``super+shift+t, enter`` (Mac). The output will look
   something like this::

      This is paragraph text *before* the table.

      +----------+---------------------------------------------------------+
      | Column 1 | Column 2                                                |
      +==========+=========================================================+
      | Foo      | Put two (or more) spaces as a field separator.          |
      +----------+---------------------------------------------------------+
      | Bar      | Even very very long lines like these are fine, as long  |
      |          | as you do not put in line endings here.                 |
      +----------+---------------------------------------------------------+

      This is paragraph text *after* the table.


Now suppose you add some text in a cell::

      +----------+---------------------------------------------------------+
      | Column 1 | Column 2                                                |
      +==========+=========================================================+
      | Foo is longer now     | Put two (or more) spaces as a field separator.          |
      +----------+---------------------------------------------------------+
      | Bar      | Even very very long lines like these are fine, as long  |
      |          | as you do not put in line endings here.                 |
      +----------+---------------------------------------------------------+

Press the same trigger: magically, the structure will be fixed::


      +-------------------+--------------------------------------------------------+
      | Column 1          | Column 2                                               |
      +===================+========================================================+
      | Foo is longer now | Put two (or more) spaces as a field separator.         |
      +-------------------+--------------------------------------------------------+
      | Bar               | Even very very long lines like these are fine, as long |
      |                   | as you do not put in line endings here.                |
      +-------------------+--------------------------------------------------------+


In addition, if you would like to keep the column width fixed, you could **reflow** the table pressing ``ctrl+t, r`` (``super+shift+t, enter`` in Mac). The result would be this::


      +----------+---------------------------------------------------------+
      | Column 1 | Column 2                                                |
      +==========+=========================================================+
      | Foo is   | Put two (or more) spaces as a field separator.          |
      | longer   |                                                         |
      | now      |                                                         |
      +----------+---------------------------------------------------------+
      | Bar      | Even very very long lines like these are fine, as long  |
      |          | as you do not put in line endings here.                 |
      +----------+---------------------------------------------------------+

With the base trigger combination and the cursors you can merge simple cells.
For example, suppose you have this table::

    +----+----+
    | h1 | h2 |
    +====+====+
    | 11 | 12 |
    +----+----+
    | 21 | 22 |
    +----+----+

Move the cursor to the cell ``12`` and press ``ctrl+t, down``. You'll get this::

    +----+----+
    | h1 | h2 |
    +====+====+
    | 11 | 12 |
    +----+    |
    | 21 | 22 |
    +----+----+


.. note::

   The original code of this feature was taken from
   `Vincent Driessen's vim-rst-tables <https://github.com/nvie/vim-rst-tables>`_ :


Smart lists
-----------

Ordered or unordered lists patterns are automatically detected. When you type something
like this::

  1. Some item
  2. Another|

When press ``enter`` the newline will prepended with a logical next item::

  ...
  2. Another
  3. |

If you press ``enter`` when the item is empty, the markup is erased keeping
the same indent as the previous line, in order to allow multilines items.
Also note that orderer list works with an alphabetic pattern or roman numbers pattern
(``a. b. c. ...``, ``A. B. C. ...``, ``i. ii. iii. iv. ...``, ``X. XI. XII. ...``).

.. tip::

   The very same feature works for  `line blocks <http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#line-blocks>`_ starting a line with ``|``.

.. note::

   This feature was proudly stolen from `Muchenxuan Tongh's SmartMarkdown
   <https://github.com/demon386/SmartMarkdown>`_


Headers
--------

.. _header completion:

Autocompletion
+++++++++++++++

You can autocomplete standard headers (over/)underlines with ``TAB``.

For example try this::


    **********<TAB>
    A longer main title
    *******

Or this::

    A subtitle
    ---<TAB>


You'll get::


    *******************
    A longer main title
    *******************

    A subtitle
    ----------

respectively.

Navigation
++++++++++

Also, it's possible to jump between headers.
``ctrl+down`` and ``ctrl+up`` move the cursor position
to the closer next or previous header respectively.

``ctrl+shift+down`` and ``ctrl+shift+up`` to the same, but only
between headers with the same or higher level (i.e. ignore childrens)

The header level is detected automatically.


Magic Footnotes
---------------

This is the smarter way to add footnotes, grouping them (and keepping count)
in a common region at the bottom of the document.

When you want to add a new note, press ``alt+shift+f`` (``super+shift+f`` in Mac).
This will happen:

-  A new ``n+1`` (where ``n`` is the current footnotes count) note reference
   will be added in the current cursor position
-  The corresponding reference definition will be added
   at the bottom of the *footnotes region*
-  The cursor will be moved to write the note

After write the note you can go back to the reference with ``shift+up``. Also, if
the cursor is over a reference (i.e: around something like ``[XX]_``) you can jump to its
definition with ``shift+down`` [1]_.

This feature is based on the code by `J. Nicholas Geist <https://github.com/jngeist>`_
for `MarkdownEditing <https://github.com/ttscoff/MarkdownEditing>`_

Authors
--------

- Most features added by Martín Gaitán (`mgaitan <http://github.com/mgaitan>`_)
- Original idea by Dominic Bou-Samra (`dbousamra`_)
- An few gentle contributors_

.. tip::

    Pull requests and bug reports are welcome!

License
-------

License: Seriously? It's a text editing plugin.


.. _.zip: http://github.com/dbousamra/sublime-rst-completion/zipball/master
.. _dbousamra: http://github.com/dbousamra
.. _contributors: https://github.com/dbousamra/sublime-rst-completion/contributors

.. [1]  in fact, you can also jump forward and back between notes with
        the general ``alt+shift+f``
