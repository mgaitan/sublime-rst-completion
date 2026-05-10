SublimeText ♥ reStructuredText
==============================

``sublime-rst-completion`` is a group of snippets and commands to facilitate writing restructuredText
with SublimeText.


Demo
----

(image links to a Youtube video)

.. image:: http://img.youtube.com/vi/otM_tjIi_vY/0.jpg
   :target: http://www.youtube.com/watch?v=otM_tjIi_vY



.. contents::
   :depth: 2
   :local:


Install
-------

The easiest way to install is via `Sublime Package Control <http://wbond.net/sublime_packages/package_control>`_ . Just look for *"Restructured Text (RST) Snippets"*

Otherwise you can:

- Clone the repository into
  your `packages folder <http://sublimetext.info/docs/en/basic_concepts.html#the-packages-directory>`_::

      git clone git@github.com:mgaitan/sublime-rst-completion.git

- Or download the `.zip`_ file and unzip it into your ST2/ST3/ST4 packages
  directory.

Optionally, to use the `Render preview`_ feature, you need to install at least one of
Pandoc_, docutils_ or rst2pdf_ and they should be accessible in your ``PATH``. (Copy the ``command_path`` variable from the package's settings file to your user settings file and add paths to your local installations to it.)  In debian/ubuntu you can install them via ``apt-get``::

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
| ``h1``                 | Header level 1                     | see `Headers`_             |
+------------------------+------------------------------------+----------------------------+
| ``h2``                 | Header level 2                     |                            |
+------------------------+------------------------------------+----------------------------+
| ``h3``                 | Header level 3                     |                            |
+------------------------+------------------------------------+----------------------------+
| ``e``                  | emphasis                           | ``ctrl+alt+i``             |
|                        |                                    | (``super+shift+i`` on Mac) |
+------------------------+------------------------------------+----------------------------+
| ``se``                 | strong emphasis (bold)             | ``ctrl+alt+b``             |
|                        |                                    | (``super+shift+b`` on Mac) |
+------------------------+------------------------------------+----------------------------+
| ``lit`` or ``literal`` | literal text (inline code)         | ``ctrl+alt+k``             |
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


Render preview
--------------

You can preview your document in different formats converted with different tools
pressing ``ctrl+shift+r``.

The *Quick Window* will offer the format and tool and the result will be automatically open
after the conversion.

By the way, it can use Pandoc_, rst2pdf_, or ``rst2*.py`` tools (included with
docutils_) to produce ``html``, ``pdf``, ``odt`` or ``docx`` output formats.

Each time you select a different ``format + tool`` option, it reverts to its default
settings for subsequent page renderings.

.. note::

    The original code is from the `SublimePandoc <https://github.com/jclement/SublimePandoc>`_
    project.


Magic Tables
------------

There is a particular *magic* expansion for tables. Here is how it works:


Grid tables
+++++++++++

1. Create some kind of table outline, separating columns with two or more spaces::


      This is the paragraph text *before* the table is created.

      Column 1  Column 2
      Foo  Put two (or more) spaces as a field separator.
      Bar  Even very very long lines like these are fine, as long as you do not put in line endings here.

2. Put your cursor somewhere in the content.
3. Press ``ctrl+t, enter`` (Linux or Windows) or ``super+shift+t, enter`` (Mac)
   to convert it to a table.  The output will look something like this::

      This is the paragraph *after* the table is created.

      +----------+---------------------------------------------------------+
      | Column 1 | Column 2                                                |
      +==========+=========================================================+
      | Foo      | Put two (or more) spaces as a field separator.          |
      +----------+---------------------------------------------------------+
      | Bar      | Even very very long lines like these are fine, as long  |
      |          | as you do not put in line endings here.                 |
      +----------+---------------------------------------------------------+


Now suppose you add some text in two cells like this::

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


Alternately, if you want the table to keep its dimensions, you can **reflow** the
table by pressing ``ctrl+t, r`` (``super+shift+t, r`` on Mac). The result will look
like this::

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


With the base trigger combination and the arrow keys you can do simple cell merges.
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

.. note::

   The original code of `wcwidth <https://github.com/jquast/wcwidth>`_ was taken to solve alignment issue with CJK characters.


Simple tables
+++++++++++++

A simpler table style is also supported if you prefer it. Here is how it works:

1. Create some kind of table outline, separating column with two or more spaces::


      This is paragraph *before* the table is created.

      Column 1  Column 2
      Foo  Put two (or more) spaces as a field separator.
      Bar  Even very very long lines like these are fine, as long as you do not put in line endings here.

2. Put your cursor somewhere in the content.
3. Press ``ctrl+t, s`` (Linux or Windows) or ``super+shift+t, s`` (Mac) to convert it
4. to a table. The output will look something like this::

      This is paragraph text *after* the table is created.

      ==========  ================================================================================================
      Column 1    Column 2
      ==========  ================================================================================================
      Foo         Put two (or more) spaces as a field separator.
      Bar         Even very very long lines like these are fine, as long as you do not put in line endings here.
      ==========  ================================================================================================


Now suppose you add some text in a cell::

      ==========  ================================================================================================
      Column 1    Column 2
      ==========  ================================================================================================
      Foo is longer now         Put two (or more) spaces as a field separator.
      Bar         Even very very long lines like these are fine, as long as you do not put in line endings here.
      ==========  ================================================================================================


Press the same trigger: magically, the structure will be fixed::

      ===================  ================================================================================================
      Column 1             Column 2
      ===================  ================================================================================================
      Foo is longer now    Put two (or more) spaces as a field separator.
      Bar                  Even very very long lines like these are fine, as long as you do not put in line endings here.
      ===================  ================================================================================================


.. note::

   The original code of this feature was taken from
   `Vincent Driessen's vim-rst-tables <https://github.com/nvie/vim-rst-tables>`_ :


Smart lists
-----------

Ordered or unordered lists patterns are automatically detected. When you type something
like this::

  1. Some item
  2. Another|

When you press ``enter``, the new line will prefixed with the logical next list-item prefix::

  ...
  2. Another
  3. |

If you press ``enter`` when the item is empty, the markup is erased keeping
the same indent as the previous line, in order to allow multi-line items.
Also note that ordered lists also work with alphabetic or Roman numerals
suffixed with a period, e.g.
(``a. b. c. ...``, ``A. B. C. ...``, ``i. ii. iii. iv. ...``, ``X. XI. XII. ...``, ``#.``);
surrounded by parentheses, e.g.
(``(a) (b) (c) ...``, ``(A) (B) (C) ...``, ``(i) (ii) (iii) (iv) ...``, ``(X) (XI) (XII) ...``, ``(#)``);
or suffixed with a right-parenthesis.
(``a) b) c) ...``, ``A) B) C) ...``, ``i) ii) iii) iv) ...``, ``X) XI) XII) ...``, ``#)``);

.. tip::

   The very same feature works for  `line blocks <http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#line-blocks>`_,
   i.e. starting lines with ``|``.

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

or this::

    A subtitle
    ---<TAB>


and you'll get::


    *******************
    A longer main title
    *******************

    A subtitle
    ----------

respectively.


Folding/unfolding
+++++++++++++++++

If you put the cursor in a completed header and press ``shift + TAB`` (``alt + TAB`` in Mac),
the section under it will be folded/unfolded.

For example::

    Folding/unfolding
    +++++++++++++++++<TAB>

    If you put the cursor in a completed header and press ``shift + TAB``,
    (``alt + TAB`` in Mac) the section under it will be folded/unfolded.

    Navigation
    ++++++++++

    ...

results in:

    .. image:: https://raw.github.com/dbousamra/sublime-rst-completion/11_foldable_headers/img/folding.png


Nested sections under that section are included.


Navigation
++++++++++

Also, it's possible to jump between headers.
``alt+down`` and ``alt+up`` move the cursor position to the closest next or
previous header respectively.

``alt+shift+down`` and ``alt+shift+up`` do the same, but only between headers
with the same or higher level (i.e. ignoring subsections).

The header level is detected automatically.


Adjust header level
+++++++++++++++++++

With the cursor in a header, pressing ``ctrl + +`` (plus key) and ``ctrl + -`` (minus
key) (``alt + +`` and ``alt + -``, in Mac) will increase and decrease the header level
respectively.  The adornment decoration (underline / overline) is autodetected from the
document and uses the Sphinx conventions from many years ago by default.

For example, you have the cursor in::

    Magic Footnotes|
    ---------------

Which is a header level 2 and want to convert to a level 3, press ``ctrl + -`` to get::

    Magic Footnotes|
    +++++++++++++++

.. note::

    If you wish to customize these to your own standard section-header adornments,
    you can do so by ensuring this Package is installed as a ``.sublime-package``
    file and then overriding the ``headers.py`` file in an file in an
    `Override Package <https://docs.sublimetext.io/guide/extensibility/packages.html#package-types>`__,
    search for ``DEFAULT_HEADERS`` in the ``RstHeaderTree`` class and set it to a list
    of strings where the string at index 0 represents the syntax for your
    highest-level section header  (``<h1>``), and the string at index 5 represents
    the syntax for your lowest-level section header (``<h6>``).  Two matching
    characters together cause the section heading to have over/under adornment.

    Exxample:

    .. code-block:: python

        DEFAULT_HEADERS = '## ** = - ^ "'.split()

    follows the `Sphinx reStructuredText Primer suggestion
    <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#sections>`__
    as of 03-Jun-2025 which is documented as:

    - # with overline, for parts
    - \* with overline, for chapters
    - = for sections
    - \- for subsections
    - ^ for subsubsections
    - \" for paragraphs


Magic Footnotes
---------------

This is the smarter way to add footnotes, grouping them (and keeping count)
in a common region at the bottom of the document.

When you want to add a new footnote, press ``alt+shift+f``.
This will happen:

-  A new ``n+1`` (where ``n`` is the current footnotes count) note reference
   will be added in the current cursor position.
-  The corresponding reference definition will be added
   at the bottom of the *footnotes region*.
-  The cursor will be moved to write the note.

After the footnote directive is created (before, during or after writing the footnote
content), place the caret anywhere on the same line as the ``.. [XX]`` directive
(if it is not already there) and your caret will go back to the footnote reference
with ``shift+up``.

When the cursor is just after a footnote reference (i.e. the caret is just to the
right of the underscore like this ``[XX]_|``) you can jump to the corresponding
footnote definition with ``shift+down`` [1]_.

This feature is based on the code by `J. Nicholas Geist <https://github.com/jngeist>`_
for `MarkdownEditing <https://github.com/ttscoff/MarkdownEditing>`_

Authors
-------

- Most features added by Martín Gaitán (`mgaitan <http://github.com/mgaitan>`_)
- Original idea by Dominic Bou-Samra (`dbousamra`_)
- And some kind contributors_

.. tip::

    Pull requests and bug reports are welcome!

License
-------

This Sublime Text Package is under a
`BSD license <https://github.com/dbousamra/sublime-rst-completion/blob/master/LICENSE>`_ .



.. _.zip: http://github.com/dbousamra/sublime-rst-completion/zipball/master
.. _dbousamra: http://github.com/dbousamra
.. _contributors: https://github.com/dbousamra/sublime-rst-completion/contributors

.. [1]  in fact, you can also jump forward and back between notes with
        the general ``alt+shift+f``
