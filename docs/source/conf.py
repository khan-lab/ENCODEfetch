# -- Project information -----------------------------------------------------
project = 'ENCODEfetch'
author = 'Aziz Khan'
copyright = '2025, Aziz Khan'

# -- General configuration ---------------------------------------------------
extensions = [
    'myst_parser',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.viewcode',
    'sphinx_autodoc_typehints',
    'sphinx.ext.todo',
    'sphinx_copybutton',
]

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "fieldlist",
    "tasklist",
]

templates_path = ['_templates']
exclude_patterns = ['_build']

# Use Markdown via MyST
source_suffix = {'.rst': 'restructuredtext', '.md': 'markdown'}
master_doc = 'index'

# Type hints in descriptions
autodoc_typehints = "description"
always_document_param_types = True

# -- Options for HTML output -------------------------------------------------
html_theme = 'furo'
html_title = 'ENCODEfetch'
html_static_path = ['_static']
html_logo = '../logo.png'  # expects repo logo at docs root or adjust path
html_favicon = '../logo.png'

# -- Path setup so autodoc can find the package ------------------------------
import os, sys, pathlib
DOCS_DIR = pathlib.Path(__file__).resolve().parent
REPO_ROOT = DOCS_DIR.parent.parent  # assumes docs/ at repo root
sys.path.insert(0, str(REPO_ROOT))

# If building on a machine without deps, mock heavy imports here (not needed now)
autodoc_mock_imports = []
