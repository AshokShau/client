import os
import sys
from datetime import datetime

# Add your project to the Python path
sys.path.insert(0, os.path.abspath('..'))

project = 'pytdbot'
copyright = f'{datetime.now().year}, AshokShau'
author = 'AshokShau'
release = '1.0.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx_autodoc_typehints',
]

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_use_keyword = True

# Autodoc settings
autodoc_default_options = {
    'members': True,
    'member-order': 'groupwise',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__',
    'show-inheritance': True,
}
autodoc_member_order = 'groupwise'
autodoc_typehints = 'description'
autodoc_typehints_format = 'short'

# HTML theme settings
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'navigation_depth': 4,
    'collapse_navigation': False,
    'titles_only': False,
    'style_external_links': True,
}

# HTML static path
html_static_path = ['_static']

# CSS overrides
html_css_files = [
    'custom.css',
]

# Exclude patterns
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Source suffixes
source_suffix = {
    '.rst': 'restructuredtext',
}

# Master document
master_doc = 'index'


# Suppress warnings
suppress_warnings = [
    'autodoc.import_object',
]