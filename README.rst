jqpm
====

jQuery Package Manager. Or, package manager for jQuery plugins.

Or just `jqpm`.


Wait, what?
***********

Yep, that's correct. While jQuery might not have a central plugin repository
(`yet <http://plugins.jquery.com/>`_), there is always `GitHub <http://github.com>`_.

jqpm will use it to find plugins you request and install them. For example::

    $ jqpm install flot

installs the `Flot <http://code.google.com/p/flot/>`_ charting library, placing
``jquery.flot.js`` inside current directory.


Okay...
*******

Like any package manager worth its salt, jqpm also lets you keep up with changes
to stuff you have installed::

    $ jqpm update

To accomplish that, a ``.jqpm`` directory is created that holds information about
installed plugins. Make sure it's part of version control!


Is that even serious?
*********************

Maybe :-) I implemented it mostly for fun, as an experiment and simple exercise
in several technologies I wanted to try out. But hey, it's totally possible
it proves to be at least somewhat useful!


And if I want to try it...
**************************

\...you should have *node.js* and *npm*.

The preferred way for jqpm is to install it globally::

    $ sudo npm install jqpm -g

Alternatively, you can install it locally and add symlink/alias to ``jqpm`` binary::

    $ cd ~
    $ npm install jqpm

::

    $ ln -s ~/node_modules/jqpm/bin/jqpm ~/bin/jqpm  # provided ~/bin is in $PATH
    $ echo "alias jqpm=~/node_modules/jqpm/bin/jqpm" >> ~/.bash_aliases
