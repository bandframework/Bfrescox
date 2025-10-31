import os
import shutil
from pathlib import Path

from ._fill_in_template import fill_in_template_file


class Configuration(object):
    """
    Class representing a Frescox input configuration.
    """

    @classmethod
    def from_NML(cls, filename: Path):
        """
        Parameters:
            filename (str or Path): Path to Frescox Fortran namelist input
            file

        Returns:
            Configuration object constructed from contents of given
            |frescox| Fortran namelist input file
        """
        return cls(filename)

    @classmethod
    def from_template(
        cls,
        template_path: Path,
        output_path: Path,
        parameters: dict,
        overwrite: bool = False,
    ):
        """
        Read in a template nml file, replace '@key@' placeholders with
        corresponding values from parameters, and write result to
        output_path.

        For example, if one has a Frescox template file with a line like
        this:
        ```
        &POT kp=1 type=1  p1=@V@ p2=@r@ p3=@a@ p4=@W@ p5=@rw@ p6=@aw@ /
        ```

        Then the `parameters` dict should have the keys `V`, `r`, `a`,
        `W`, `rw`, and `aw`.

        Placeholders may be repeated in multiple places in the template
        file.

        Parameters:
            template_path (Path): Path to the template NML file.
            output_path (Path): Path to write the modified NML file.
            parameters (dict): Dictionary of parameters to replace in
                the template. Keys should match placeholders in the
                template, corresponding values are the desired
                replacements in the output file.
        overwrite (bool): Whether to overwrite output_path if it already
            exists.

        Raises:
            ValueError: If keys exist in the template that are not in
                parameters.
            ValueError: If keys exist in parameters that are not in the
                template file

        Returns:
            Configuration object
        """
        fill_in_template_file(
            template_path,
            output_path,
            parameters,
            overwrite=overwrite,
        )
        return cls(output_path)

    @classmethod
    def from_json(cls, filename: Path):
        """
        Parameters:
            filename (str or Path): Path to Frescox |bfrescox| format JSON
            file

        Returns:
            Configuration object constructed from contents of given
            |bfrescox| format JSON file
        """
        raise NotImplementedError("from_json not implemented yet")

    def __init__(self, filename: Path):
        """
        Parameters:
            filename (str or Path): Path to Frescox Fortran namelist input
            file

        Raises:
            TypeError: If filename is not a str or Path
            ValueError: If filename does not exist or is not a file
        """
        super().__init__()

        # ----- ERROR CHECK ARGUMENTS
        if (not isinstance(filename, str)) and (not isinstance(filename, Path)):
            raise TypeError("Given filename is not a str or Path")
        fname = Path(filename).resolve()
        if not fname.is_file():
            msg = "Configuration file does not exist or is not a file"
            raise ValueError(msg)

        # ----- STORE CONFIGURATION
        # No loading or checking to be done if Frescox NML file
        self.__nml = fname

    def write_to_nml(self, filename: Path, overwrite: bool = False):
        """
        Write configuration to Frescox Fortran namelist input file.
        Parameters:
            filename (str or Path): Path to write Frescox Fortran
                namelist input file
            overwrite (bool): Whether to overwrite filename if it
                already exists.
        Raises:
            TypeError: If filename is not a str or Path
            RuntimeError: If filename already exists and overwrite is
                False
        """
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
