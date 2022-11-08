"""Sphinx configuration."""
project = "Gridworks Timecoordinator"
author = "Jessica Millar"
copyright = "2022, Jessica Millar"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
