Sublime Text Restructured Text Code Completion (rst)
=======================================================

Some convenience snippets and completion hints for Sublime text editor.
This plugin will hopefully evolve to make Sublime a useful documentation
toolkit.

Installation
------------

The easiest way to install is via `Sublime Package Control <http://wbond.net/sublime_packages/package_control>`_ .

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

+------------------------+------------------------------------+-----------------------+
| shortcut               | result                             | key binding           |
+========================+====================================+=======================+
| ``h1``                 | Header level 1                     |                       |
+------------------------+------------------------------------+-----------------------+
| ``h2``                 | Header level 2                     |                       |
+------------------------+------------------------------------+-----------------------+
| ``h3``                 | Header level 3                     |                       |
+------------------------+------------------------------------+-----------------------+
| ``e``                  | emphasis                           | ``ctrl+i``            |
+------------------------+------------------------------------+-----------------------+
| ``se``                 | strong emphasis (bold)             | ``ctrl+b``            |
+------------------------+------------------------------------+-----------------------+
| ``lit`` or ``literal`` | literal text (inline code)         | ``control+k``         |
+------------------------+------------------------------------+-----------------------+
| ``list``               | unordered list                     |                       |
+------------------------+------------------------------------+-----------------------+
| ``listn``              | ordered list                       |                       |
+------------------------+------------------------------------+-----------------------+
| ``listan``             | auto ordered list                  |                       |
+------------------------+------------------------------------+-----------------------+
| ``def``                | term definition                    |                       |
+------------------------+------------------------------------+-----------------------+
| ``code``               | code-block directive (sphinx)      |                       |
+------------------------+------------------------------------+-----------------------+
| ``source``             | preformatted (``::`` block)        |                       |
+------------------------+------------------------------------+-----------------------+
| ``img``                | image                              |                       |
+------------------------+------------------------------------+-----------------------+
| ``fig``                | figure                             |                       |
+------------------------+------------------------------------+-----------------------+
| ``table``              | simple table                       | ``ctrl+t`` see below_ |
+------------------------+------------------------------------+-----------------------+
| ``link``               | refered hyperlink                  |                       |
+------------------------+------------------------------------+-----------------------+
| ``linki``              | embeded hyperlink                  |                       |
+------------------------+------------------------------------+-----------------------+
| ``fn`` or ``cite``     | autonumbered footnote or cite      |                       |
+------------------------+------------------------------------+-----------------------+
| ``quote``              | Quotation (``epigraph`` directive) |                       |
+------------------------+------------------------------------+-----------------------+


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



Authors
--------

Dominic Bou-Samra (`dbousamra`_) with contribution of Martín Gaitán (`mgaitan <http://github.com/mgaitan>`_) and others_

.. tip::

    Pull requests are welcome!


License
-------

License: Seriously? It's a text editing plugin.


.. _Sublime Text Restructured Text Code Completion (rst):
.. _.zip: http://github.com/dbousamra/sublime-rst-completion/zipball/master
.. _dbousamra: http://github.com/dbousamra
.. _others: https://github.com/dbousamra/sublime-rst-completion/contributors