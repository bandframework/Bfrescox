import os
import shutil
from pathlib import Path

from ._fill_in_template import fill_in_template_file


class Configuration(object):
    @classmethod
    def from_NML(cls, filename):
        """
        :return: Configuration object constructed from contents of given
            |frescox| Fortran namelist input file
        """
        return cls(None, filename)

    @classmethod
    def from_template(
        cls,
        template_path: Path,
        output_path: Path,
        parameters: dict,
        overwrite: bool = False,
    ):
        """
        Read in a template nml file, replace '@key@' placeholders with corresponding
        values from parameters, and write result to output_path.

        For example, if one has a Frescox template file with a line like this:
        ```
        &POT kp=1 type=1  p1=@V@ p2=@r@ p3=@a@ p4=@W@ p5=@rw@ p6=@aw@ /
        ```

        Then the `parameters` dict should have the keys `V`, `r`, `a`, `W`, `rw`, and `aw`.

        Placeholders may be repeated in multiple places in the template file.

        Parameters:
            template_path (Path): Path to the template NML file.
            output_path (Path): Path to write the modified NML file.
            parameters (dict): Dictionary of parameters to replace in the template. Keys
                should match placeholders in the template, corresponding values are
                the desired replacements in the output file.
        overwrite (bool): Whether to overwrite output_path if it already exists.

        Raises:
            ValueError: If keys exist in the template that are not in parameters.
            ValueError: If keys exist in parameters that are not in the template file

        Returns:
            Configuration object
        """
        fill_in_template_file(
            template_path,
            output_path,
            parameters,
            overwrite=overwrite,
        )
        return cls(None, output_path)

    @classmethod
    def from_json(cls, filename):
        """
        :return: Configuration object constructed from contents of given
            |bfrescox| format JSON file
        """
        raise NotImplementedError("Is this a good idea?!")

    def __init__(self, configuration, filename):
        """
        .. todo::
            * Figure this out once we start configuring in earnest.  It does
              seem like a good idea for users to be able to use an NML files
              they have hanging around.
            * Note that this class could double as a translation tool if so
              desired.  A user could load from JSON and write to NML.  If we
              were to add a write_to_JSON, then a user could convert an NML file
              to JSON.

        :param configuration:
        :param filename:
        """
        super().__init__()

        # ----- ERROR CHECK ARGUMENTS
        if configuration is not None:
            raise NotImplementedError("Should this be a dict?")

        if (not isinstance(filename, str)) and (not isinstance(filename, Path)):
            raise TypeError("Given filename is not a str or Path")
        fname = Path(filename).resolve()
        if not fname.is_file():
            msg = "Configuration file does not exist or is not a file"
            raise ValueError(msg)

        # ----- STORE CONFIGURATION
        # No loading or checking to be done if Frescox NML file
        self.__nml = fname

    def write_to_nml(self, filename, overwrite=False):
        """ """
        # ----- ERROR CHECK ARGUMENTS
        if (not isinstance(filename, str)) and (not isinstance(filename, Path)):
            raise TypeError("Given filename is not a str or Path")
        fname_in = Path(filename).resolve()
        if fname_in.exists():
            if overwrite:
                assert fname_in.is_file()
                os.remove(fname_in)
            else:
                raise RuntimeError(f"Input file ({fname_in}) already exists")

        # ----- WRITE CONFIGURATION TO FILE
        # Trivial for NML
        shutil.copy(self.__nml, fname_in)
