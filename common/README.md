The files in this directory are the set of functionality that is shared
between the `bfrescox` and `bfrexcoxpro` packages. They are symlinked
into the respective package directories under the same names they take
here. This allows for relative imports, both between these files and
from these files into the package-specific code.

This implies that names of files that should be in the private interface
of both packages should contain a leading underscore, which is
meaningful within the scope of the package.

