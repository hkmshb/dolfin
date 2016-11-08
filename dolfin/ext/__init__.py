"""
Redirects imports for extensions. This module basically makes it possible to
import `dolfin_name` as `dolfin.ext.name`.

:note: extracted from flask.
"""

def setup():
    from ..exthook import ExtensionImporter
    importer = ExtensionImporter(['dolfin_%s'], __name__)
    importer.install()


setup()
del setup
