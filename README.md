# Bfrescox

[![Check standard conformance](https://github.com/bandframework/Bfrescox/actions/workflows/check_standards.yml/badge.svg?branch=main)](https://github.com/bandframework/Bfrescox/actions/workflows/check_standards.yml)

[![Test manual bfrescox installation](https://github.com/bandframework/Bfrescox/actions/workflows/test_bfrescox_sdist.yml/badge.svg?branch=main)](https://github.com/bandframework/Bfrescox/actions/workflows/test_bfrescox_sdist.yml)
[![Test manual bfrescoxpro installation](https://github.com/bandframework/Bfrescox/actions/workflows/test_bfrescoxpro_sdist.yml/badge.svg?branch=main)](https://github.com/bandframework/Bfrescox/actions/workflows/test_bfrescoxpro_sdist.yml)
[![codecov](https://codecov.io/gh/bandframework/Bfrescox/graph/badge.svg?token=U3X4WBQJ67)](https://codecov.io/gh/bandframework/Bfrescox)

[![Build documentation](https://github.com/bandframework/Bfrescox/actions/workflows/build_docs.yml/badge.svg?branch=main)](https://github.com/bandframework/Bfrescox/actions/workflows/build_docs.yml)
[![Build & publish Jupyter book](https://github.com/bandframework/Bfrescox/actions/workflows/publish_book.yml/badge.svg?branch=main)](https://github.com/bandframework/Bfrescox/actions/workflows/publish_book.yml)
[![Jupyter book](https://jupyterbook.org/badge.svg)](https://bandframework.github.io/Bfrescox)


Bfrescox is a Python package wrapping [Frescox](https://github.com/LLNL/Frescox) (see also the [official website](https://www.fresco.org.uk/frescox.htm)), a Fortran application for coupled-reaction-channels calculations in nuclear physics.  To get started, please see the [user and developer guides](https://bfrescox.readthedocs.io) and the [Jupyter book of examples](https://bandframework.github.io/Bfrescox).

## Support

To report potential problems with Bfrescox, please check if the problem has already been reported and recorded as an [Issue](https://github.com/bandframework/Bfrescox/issues).  If not or to request changes or new features, please open a new issue.  For all other communication needs, please email the Bfrescox development team.

* beyerk@frib.msu.edu
* catacora@frib.msu.edu
* joneal@anl.gov

## Documentation

The [user and developer guides](https://bfrescox.readthedocs.io) are available on ReadTheDocs.  Examples are available as a [Jupyter book](https://bandframework.github.io/Bfrescox).

Please refer to the [Frescox documentation](https://github.com/LLNL/Frescox) for all information regarding the use of Frescox. There is also a comprehensive website documenting the FrescoX namelist input [here](https://www.fresco.org.uk/xinput7a/frescox-namelist-manual/index.html).

## Citation

Please refer to the [Frescox documentation](https://github.com/LLNL/Frescox) for any information on citing the use of their software.

Please use the following to cite the use of either Bfrescox or Bfrescoxpro:


```
@techreport{bfrescox2025,
 author      = {Kyle Beyer and Manuel Catacora-Rios and Jared O'Neal},
 title       = {{Bfrescox} Users Manual},
 institution = {Michigan State University and Argonne National Laboratory},
 number      = {Version Alpha},
 year        = {2025},
 url         = {https://bfrescox.readthedocs.io/}
}
```

Bfrescox is part of the [BAND Framework](https://bandframework.github.io/). Please consider also citing the following:

    @techreport{bandframework,
        title       = {{BANDFramework: An} Open-Source Framework for {Bayesian} Analysis of Nuclear Dynamics},
        author      = {Kyle Beyer and Landon Buskirk and Manuel Catacora Rios and Moses Y-H. Chan and Tyler H. Chang and Troy Dasher 
        and Richard James DeBoer and Christian Drischler and Richard J. Furnstahl and Pablo Giuliani and
        Kyle Godbey and Kevin Ingles and Sunil Jaiswal and An Le and Dananjaya Liyanage and Filomena M. Nunes
        and Daniel Odell and David O'Gara and Jared O'Neal and Daniel R. Phillips and Matthew Plumlee
        and Matthew T. Pratola and Scott Pratt and Oleh Savchuk and Alexandra C. Semposki and \"Ozge S\"urer and 
        Stefan M. Wild and John C. Yannotty},
        institution = {},
        number      = {Version 0.5.0},
        year        = {2025},
        url         = {https://github.com/bandframework/bandframework}
    }
    
    @article{Phillips:2020dmw,
        author = "Phillips, D. R. and others",
        title = "{Get on the BAND Wagon: A Bayesian Framework for Quantifying Model Uncertainties in Nuclear Dynamics}",
        eprint = "2012.07704",
        archivePrefix = "arXiv",
        primaryClass = "nucl-th",
        doi = "10.1088/1361-6471/abf1df",
        journal = "J. Phys. G",
        volume = "48",
        number = "7",
        pages = "072001",
        year = "2021"
    }


