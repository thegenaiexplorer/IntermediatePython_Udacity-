"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional),diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    # __init__ method has been modified to accept designation, name, diameter
    # and hazardous as parameters
    def __init__(self, designation, name, diameter, hazardous):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to
        the constructor.
        """
        self.designation = str(designation)
        if (len(name) == 0):
            self.name = None
        else:
            self.name = str(name)
        if (len(str(diameter)) == 0):
            self.diameter = float('nan')
        else:
            self.diameter = float(diameter)
        self.hazardous = bool(hazardous)
        self.fullname = ""

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return self.f_name

    @fullname.setter
    def fullname(self, value):
        """Set the Full Name of this NEO."""
        if (self.name is None):
            self.f_name = f'{self.designation}'
        else:
            self.f_name = f'{self.designation} ({self.name})'

    def __str__(self):
        """Return `str(self)`."""
        hazard = "is not"
        if (self.hazardous):
            hazard = "is"
        return f'NEO {self.fullname} has a diameter of {self.diameter:.3f} ' \
               f'km and {hazard} potentially hazardous.'

    def __repr__(self):
        """Return `repr(self)`.

        a computer-readable string representation of this object.
        """
        return f"NearEarthObject(designation={self.designation!r}, " \
               f"name={self.name!r}, diameter={self.diameter:.3f}, " \
               f"hazardous={self.hazardous!r})"


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulats information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    # Constructor of the class has been modified to inlcude designation, time,
    # distance and velocity as parameters.
    def __init__(self, designation, time, distance, velocity):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied
        to the constructor.
        """
        self._designation = str(designation)
        self.time = cd_to_datetime(time)
        self.distance = float(distance)
        self.velocity = float(velocity)

        # Create an attribute for the referenced NEO, originally None.
        self.neo = None
        self.time_str = ""
        self.fullname = ""

    @property
    def time_str(self):
        """Return a formatted representation of this object's approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default
        representation includes seconds - significant figures that don't
        exist in our input data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return self.time_to_str

    @time_str.setter
    def time_str(self, value):
        """Convert datetime object to string."""
        self.time_to_str = datetime_to_str(self.time)

    @property
    def fullname(self):
        """Retrun fullname of the object."""
        return self.f_name

    @fullname.setter
    def fullname(self, value):
        """Set fullname of the Object."""
        if (self.neo is None):
            self.f_name = self._designation
        else:
            self.f_name = self.neo.fullname

    def __str__(self):
        """Return `str(self)`."""
        return f'At {self.time_str}, "{self.fullname}" approaches Earth ' \
               f'at a distance of {self.distance:.2f} au and a velocity ' \
               f'of {self.velocity:.2f} km/s.'

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation.

        of this object.
        """
        return f"CloseApproach(time={self.time_str!r}, " \
               f"distance={self.distance:.2f}, velocity={self.velocity:.2f}," \
               f" neo={self.neo!r})"
