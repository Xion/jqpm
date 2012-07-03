jqpm
====

jQuery Package Manager. Or, package manager for jQuery plugins.

Or just `jqpm`.


Installation
************

Requires *node.js* and *npm*.

::

    $ npm install jqpm

Usage
*****

Installing a plugin::

    $ jqpm install xarea

This will download ``jquery.xarea.js`` and put it inside current directory.
Additionally, an ``.jqpm`` subdirectory will be created to hold the information
about installed plugins, their version and date of last update.

