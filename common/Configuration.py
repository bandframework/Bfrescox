import os
import shutil
from os import PathLike
from pathlib import Path
from typing import Union

from ._fill_in_template import fill_in_template_file


class Configuration(object):
    @classmethod
    def from_NML(cls, filename: Union[str, PathLike]) -> "Configuration":
        """
        Args:
            filename (Union[str, PathLike]): Path to Frescox Fortran
                namelist input file

        Returns:
            Configuration: constructed from contents of given |frescox|
                Fortran namelist input file
        """
        return cls(filename)

    @classmethod
    def from_template(
        cls,
        template_path: Union[str, PathLike],
        output_path: Union[str, PathLike],
        parameters: dict,
        overwrite: bool = False,
    ) -> "Configuration":
        """
        Read in a template nml file, replace '@key@' placeholders with
        corresponding values from parameters, and write result to
        output_path. The set of possible keys in the template file must
        exactly match the keys in `parameters`, or a ValueError will be
        raised.

        For example, if one has a Frescox template file with a line like
        this defining a potential:
        ```
        &POT kp=1 type=1  p1=@V@ p2=@r@ p3=@a@ p4=@W@ p5=@rw@ p6=@aw@ /
        &POT kp=1 type=2  p1=@Vs@ p2=@rw@ p3=@aw@ p4=@Ws@ p5=@rw@ p6=@aw@ /
        ```

        Then the `parameters` dict should have the keys `V`, `r`, `a`,
        `W`, `rw`, `aw`, `Vs` and `Ws`. Notice that `rw` and `aw` are
        used in multiple places in the template file. The corresponding
        values in `parameters` will be substituted into each location
        where the placeholder appears.

        Args:
            template_path (Union[str, PathLike]): Path to the template
                NML file.
            output_path (Union[str, PathLike]): Path to write the
                modified NML file.
            parameters (dict): Dictionary of parameters to replace in
                the template. Keys should match placeholders in the
                template, corresponding values are the desired replacements
                in the output file.
            overwrite (bool): Whether to overwrite output_path if it
                already exists.

        Raises:
            TypeError: If template_path or output_path are not str or
                PathLike
            ValueError: If keys exist in the template that are not in
                `parameters`.
            ValueError: If keys exist in `parameters` that are not in
                the template file
        """
        if not isinstance(template_path, (str, PathLike)):
            raise TypeError("template_path must be str or PathLike")
        if not isinstance(output_path, (str, PathLike)):
            raise TypeError("output_path must be str or PathLike")

        fill_in_template_file(
            Path(template_path),
            Path(output_path),
            parameters,
            overwrite=overwrite,
        )
        return cls(Path(output_path))

    @classmethod
    def from_json(cls, filename: Union[str, PathLike]) -> "Configuration":
        """
        Args:
            filename (Union[str, PathLike]): Path to Frescox |bfrescox| format
                JSON file

        Returns:
            Configuration : constructed from contents of given
                w|bfrescox| format JSON file
        """
        raise NotImplementedError("from_json not implemented yet")

    def __init__(self, filename: Union[str, PathLike]):
        """
        Class representing a Frescox input configuration.

        Args:
            filename (Union[str, PathLike]): Path to Frescox Fortran namelist
                input file

        Raises:
            TypeError: If filename is not a str or Path
            ValueError: If filename does not exist or is not a file
        """
        super().__init__()

        # ----- ERROR CHECK ARGUMENTa
        if not isinstance(filename, (str, PathLike)):
            raise TypeError("filename must be a str or PathLike")
        fname = Path(filename).resolve()
        if not fname.is_file():
            msg = f"Configuration file {fname} does not exist or is not a file"
            raise ValueError(msg)

        # ----- STORE CONFIGURATION
        # No loading or checking to be done if Frescox NML file
        self.__nml = fname

    def write_to_nml(
        self, filename: Union[str, PathLike], overwrite: bool = False
    ) -> None:
        """
        Write configuration to Frescox Fortran namelist input file.

        Args:
            filename (Union[str, PathLike]): Path to write Frescox Fortran
                namelist input file
            overwrite (bool): Whether to overwrite filename if it
                already exists.

        Raises:
            TypeError: If filename is not a str or Path
            RuntimeError: If filename already exists and overwrite is False
        """
        # ----- ERROR CHECK ARGUMENTS
        if not isinstance(filename, (str, PathLike)):
            raise TypeError("filename must be a str or PathLike")
        fname_in = Path(filename).resolve()
        if fname_in.exists():
            if fname_in == self.__nml:
                return  # No action needed
            if overwrite:
                assert fname_in.is_file()
                os.remove(fname_in)
            else:
                raise RuntimeError(f"Input file ({fname_in}) already exists")

        # ----- WRITE CONFIGURATION TO FILE
        # Trivial for NML
        shutil.copy(self.__nml, fname_in)
