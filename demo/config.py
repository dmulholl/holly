# ------------------------------------------------------------------------------
# Site Configuration File
# ------------------------------------------------------------------------------

theme = "carbon"
title = "Holly Demo"
tagline = "A blog-engine plugin for Ivy."

extensions = ["holly"]

holly = {
    "homepage": {
        "root_urls": ["@root/blog//", "@root/animalia//"],
    },
    "roots": [
        {
            "index_url": "@root/blog//",
        },
        {
            "index_url": "@root/animalia//",
        },
        {
            "index_url": "@root/fakelink//",
            "tag_slug": "tags",
            "sort_func": None,
            "reverse": True,
        },
    ],
}

