Sublime Text Restructured Text Code Completion (rst)
=======================================================

Some convenience snippets and completion hints for Sublime text editor.
This plugin will hopefully evolve to make Sublime a useful documentation
toolkit.

Install
-------

The easiest way to install is via `Sublime Package Control <http://wbond.net/sublime_packages/package_control>`_ . Just look for *"Restructured Text (RST) Snippets"*

Otherwise you can:

- Clone the repository into
  your `packages folder <http://sublimetext.info/docs/en/basic_concepts.html#the-packages-directory>`_::

      git clone git@github.com:dbousamra/sublime-rst-completion.git

or

- Download the `.zip`_ file and unzip it into your ST2 packages
  directory.

Usage
-----

Most features work as tab-triggered shortcuts: type the shortcut and press ``<TAB>`` to
replace it with the snippet. If the snippet has placeholders, you can jump between them
using tab.

+------------------------+------------------------------------+--------------------------+
| shortcut               | result                             | key binding              |
+========================+====================================+==========================+
| ``h1``                 | Header level 1                     | see `Header completion`_ |
+------------------------+------------------------------------+                          +
| ``h2``                 | Header level 2                     |                          |
+------------------------+------------------------------------+                          +
| ``h3``                 | Header level 3                     |                          |
+------------------------+------------------------------------+--------------------------+
| ``e``                  | emphasis                           | ``ctrl+i``               |
+------------------------+------------------------------------+--------------------------+
| ``se``                 | strong emphasis (bold)             | ``ctrl+b``               |
+------------------------+------------------------------------+--------------------------+
| ``lit`` or ``literal`` | literal text (inline code)         | ``control+k``            |
+------------------------+------------------------------------+--------------------------+
| ``list``               | unordered list                     | see `Smart Lists`_       |
+------------------------+------------------------------------+                          +
| ``listn``              | ordered list                       |                          |
+------------------------+------------------------------------+                          +
| ``listan``             | auto ordered list                  |                          |
+------------------------+------------------------------------+--------------------------+
| ``def``                | term definition                    |                          |
+------------------------+------------------------------------+--------------------------+
| ``code``               | code-block directive (sphinx)      |                          |
+------------------------+------------------------------------+--------------------------+
| ``source``             | preformatted (``::`` block)        |                          |
+------------------------+------------------------------------+--------------------------+
| ``img``                | image                              |                          |
+------------------------+------------------------------------+--------------------------+
| ``fig``                | figure                             |                          |
+------------------------+------------------------------------+--------------------------+
| ``table``              | simple table                       | ``ctrl+t`` see `Magic    |
|                        |                                    | Tables`_                 |
+------------------------+------------------------------------+--------------------------+
| ``link``               | refered hyperlink                  |                          |
+------------------------+------------------------------------+--------------------------+
| ``linki``              | embeded hyperlink                  |                          |
+------------------------+------------------------------------+--------------------------+
| ``fn`` or ``cite``     | autonumbered footnote or cite      |                          |
+------------------------+------------------------------------+--------------------------+
| ``quote``              | Quotation (``epigraph`` directive) |                          |
+------------------------+------------------------------------+--------------------------+

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


.. _below:

Magic Tables
+++++++++++++

There is a particular *magic* expansion for tables, adapted from
`Vincent Driessen's vim-rst-tables <https://github.com/nvie/vim-rst-tables>`_ :


1. Create some kind of table outline, separating column with two or more spaces::


      This is paragraph text *before* the table.

      Column 1  Column 2
      Foo  Put two (or more) spaces as a field separator.
      Bar  Even very very long lines like these are fine, as long as you do not put in line endings here.
      Qux  This is the last line.

      This is paragraph text *after* the table.

2. Put your cursor somewhere in the content to convert as table.
3. Press ``ctrl+t`` (Linux or Windows) or ``super+shift+t`` (Mac). The output will look
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
      | Qux      | This is the last line.                                  |
      +----------+---------------------------------------------------------+

      This is paragraph text *after* the table.


Now change something in the generated table and run ``ctrl+t`` again: Magically,
the structure will be fixed.

Also you can press ``ctrl+r`` (Linux or Windows) or ``super+shift+r+t`` (Mac)
to reflows the table keeping the current columns width fixed.

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
Also note that orderer list works with an alphabetic pattern
(``a. b. c. ...`` or ``A. B. C. ...``).

.. tip::

   The very same feature works for  `line blocks <http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#line-blocks>`_ starting a line with ``|``.

.. note::

   This feature was proudly stolen from `Muchenxuan Tongh's SmartMarkdown
   <https://github.com/demon386/SmartMarkdown>`_


Header completion
-----------------

You can autocomplete standard headers (over/)underlines with TAB.

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


Authors
--------

Dominic Bou-Samra (`dbousamra`_) with the active contribution of Martín Gaitán
(`mgaitan <http://github.com/mgaitan>`_) and others_

.. tip::

    Pull requests and bug reports are welcome!

License
-------

License: Seriously? It's a text editing plugin.


.. _.zip: http://github.com/dbousamra/sublime-rst-completion/zipball/master
.. _dbousamra: http://github.com/dbousamra
.. _others: https://github.com/dbousamra/sublime-rst-completion/contributors