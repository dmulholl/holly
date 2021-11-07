# Carbon

[1]: https://github.com/dmulholl/ivy
[2]: http://www.dmulholl.com/demos/holly/
[3]: https://github.com/dmulholl/holly
[4]: https://fonts.google.com/specimen/Crimson+Text

A simple, blog-style theme for [Ivy][1] with support for post and tag indexes.

* [Demo][2]

This theme is designed to be used with the [Holly][3] blog-engine plugin.
It will display the following attributes from the site's `config.py` file in the site header:

* `title`
* `tagline`

If a node has an `intro` attribute, this will be used as the snippet shown on index pages;
otherwise a snippet of text from the node's first paragraph will be used.

If a node has an `image` attribute containing the name of an image file stored in an `@root/images/` directory, this will be used as the node's featured image.

This theme supports the following includes:

* `menu`

    This file will be used to construct the theme's main menu. It should contain
    a list of links, optionally with nested sub-lists.

* `head`

    If a `head.html` file is present in the includes folder its content will be
    included at the end of each page's `<head>` section. This file can be used
    to add custom CSS or JavaScript to a site without directly editing the
    theme's template files.

* `foot`

    If a `foot.html` file is present in the includes folder its content will
    be included at the end of each page's `<body>` section. This file can be
    used to add custom JavaScript to a site without directly editing the
    theme's template files.

This theme is distributed under the following license:

* All code has been placed in the public domain.
* The bundled [Crimson Text][4] font is distributed under the SIL Open Font License.
