"""Sphinx configuration."""

from importlib.metadata import version as _version

project = "advantage-play"
author = "Daniele Cucurachi"
copyright = "2026, Daniele Cucurachi"
release = _version("advantage-play")

extensions = [
    "myst_parser",  # Markdown sources
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",  # generates the API pages from the package
    "sphinx.ext.napoleon",  # Google-style docstrings
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_autodoc_typehints",
]

myst_enable_extensions = ["dollarmath", "colon_fence"]  # $EV = \sum p_i x_i$ and ::: fences

autosummary_generate = True
autodoc_default_options = {"members": True, "show-inheritance": True}
napoleon_google_docstring = True
napoleon_numpy_docstring = False

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable", None),
    "pandas": ("https://pandas.pydata.org/docs", None),
}

html_theme = "furo"
html_title = f"{project} {release}"
exclude_patterns = ["_build"]
