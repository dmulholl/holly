# ------------------------------------------------------------------------------
# Site Configuration File
# ------------------------------------------------------------------------------

theme = "carbon"
title = "Holly Demo"
tagline = "A blog-engine plugin for Ark."

extensions = ["holly"]

holly = {
    "homepage": {
        "root_urls": ["@root/blog//", "@root/animalia//"],
    },
    "roots": [
        {
            "root_url": "@root/blog//",
        },
        {
            "root_url": "@root/animalia//",
        },
    ],
}

