class Configuration(object):
    def __init__(self):
        """
        Create an object that fully specifies the configuration of a |frescox|
        simulation.

        .. todo::
            * Write this class
        """
        super().__init__()

        raise NotImplementedError("This class will be written soon")

    def write_to_nml(self, filename, overwrite=False):
        """
        Write the object's full simulation specification to a valid |frescox|
        Fortran namelist file.

        :param filename: Name including path of file to write specification to
        :param overwrite: If a file already exists with the given output
            filename, then overwrite the file if True; otherwise, raise an
            error.
        """
        raise NotImplementedError("This class will be written soon")
