# BAND SDK v0.2 Community Policy Compatibility for Bfrescox and Bfrescoxpro

This document summarizes the efforts of the Bfrescox and Bfrescoxpro BAND member packages to achieve compatibility with the BAND SDK community policies.  Additional details on the BAND SDK are available [here](https://github.com/bandframework/bandframework/tree/main/resources/sdkpolicies/bandsdk.md). The most recent template for this form exists [here](https://github.com/bandframework/bandframework/tree/main/resources/sdkpolicies/template.md).

To suggest changes to these requirements or obtain more information, please contact [BAND](https://bandframework.github.io/team).

Details on citing the current version of the BAND Framework can be found in the [README](https://github.com/bandframework/bandframework).


**Website:** https://github.com/bandframework/Bfrescox

**Contact:** The Bfrescox development team, whose contact details are provided in the project's [README](README.md).

**Icon:** https://github.com/bandframework/Bfrescox/blob/main/docs/logo.png

**Description:**  Bfrescox and Bfrescoxpro are Python packages that provide a Python interface for the [Frescox](https://github.com/LLNL/Frescox) coupled-channels simulation software.

### Mandatory Policies

**BAND SDK**
| #  | Policy                |Support| Notes                   |
|----|-----------------------|-------|-------------------------|
| 1. | Support BAND community GNU Autoconf, CMake, or other build options. |Full| The Meson build system is integrated into the `setup.py` files of the two packages for automatic building of the underlying Frescox binaries |
| 2. | Have a README file in the top directory that states a specific set of testing procedures for a user to verify the software was installed and run correctly. |Full| README points users to [RTD documentation](https://bfrescox.readthedocs.io) that contains installation and test procedures |
| 3. | Provide a documented, reliable way to contact the development team. |Full| __PENDING__ |
| 4. | Come with an open-source license. |Full| [BSD-2-Clause](https://github.com/bandframework/Bfrescox/blob/main/LICENSE) |
| 5. | Provide a runtime API to return the current version number of the software. |Full| Accessible via the standard `__version__` package variable. |
| 6. | Provide a BAND team-accessible repository. |Full| https://github.com/bandframework/Bfrescox |
| 7. | Must allow installing, building, and linking against an outside copy of all imported software that is externally developed and maintained. |Full| The installation of each package automatically downloads the source code of the current compatible version of the Frescox software from its official GitHub repository and builds a dedicated binary.  All other external dependencies are publicly available Python packages that should be obtained automatically as part of the package's installation process.  However, users have the possibility of installing each dependence as desired before installing a Bfrescox package so long as it satisfies the package's version requirements. |
| 8. | Have no hardwired print or IO statements that cannot be turned off. |Full| __PENDING__ |

### Recommended Policies

| # | Policy                 |Support| Notes                   |
|---|------------------------|-------|-------------------------|
|**R1.**| Have a public repository. |Full| https://github.com/bandframework/Bfrescox |
|**R2.**| Free all system resources acquired as soon as they are no longer needed. |Full| Our packages cannot control the resources allocated by Frescox, but we assume that they are deallocated appropriately when the binary terminates.  Otherwise, the packages rely on Python's automatic garbage collection system. |
|**R3.**| Provide a mechanism to export ordered list of library dependencies. |Partial| While `python -m pip info bfrescox` and `python -m pip info bfrescoxpro` do report dependencies, they are not necessarily reported in an ordered fashion.  Users can run `bfrescox.print_information()` and `bfrescoxpro.print_information()` to get the external dependencies of their Frescox internal binary so long as macOS users have `otool` installed and in the PATH; Linux users, `ldd`. Here as well, there is no guarantee on ordering. |
|**R4.**| Document versions of packages that it works with or depends upon, preferably in machine-readable form. |None| None. |
|**R5.**| Have SUPPORT, LICENSE, and CHANGELOG files in top directory. |Partial| License provided as indicated in M4.  Support information is included in the main README. |
|**R6.**| Have sufficient documentation to support use and further development. |Full| Both user and developer guides are available publicly via ReadTheDocs.  Examples are available publicly as a Jupyter book hosted on the Bfrescox GitHub page. |
|**R7.**| Be buildable using 64-bit pointers; 32-bit is optional. |None| __WHAT TO DO HERE?__ |
|**R8.**| Do not assume a full MPI communicator; allow for user-provided MPI communicator. |None|  MPI communicator use is decided by the Frescox code, which is outside our control. |
|**R9.**| Use a limited and well-defined name space (e.g., symbol, macro, library, include). |Full| All functions, classes, and package-wide variables are contained within the package'    s namespace. |
|**R10.**| Give best effort at portability to key architectures. |Full| __PENDING__ |
|**R11.**| Install headers and libraries under `<prefix>/include` and `<prefix>/lib`, respectively. |N/a| None. |
|**R12.**| All BAND compatibility changes should be sustainable. |Full| None. |
|**R13.**| Respect system resources and settings made by other previously called packages. |Full| None. |
|**R14.**| Provide a comprehensive test suite for correctness of installation verification. |Full| __PENDING__ |
