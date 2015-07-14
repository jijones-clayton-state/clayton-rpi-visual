#!/usr/bin/python
"""A 3D Point Class
This module is a representation of a three-dimensional point class
Very much based on the Point2d class
"""

class Point3d(object):
    """Creates a 3d vector, defaulting to <0, 0, 0>

    Parameters
    ----------
    x: float
        x-coordinate; 0 by default
    y: float
        y-coordinate; 0 by default
    z: float
        z-coordinate; 0 by default

    """
    def __init__(self, x=0, y=0, z=0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __repr__(self):
        return 'Point3d: <%f, %f, %f>' %(self.x, self.y, self.z)

    def __neg__(self):
        return Point3d(-self.x, -self.y, -self.z)

    def __sub__(self, term):
        """Componentwise subtraction; overrides the - operator.

        Example
        -------
        >>> a = Point3d(1, -2, 0)
        >>> b = Point3d(3, 5, 0)
        >>> print b - a
        Point3d: <2.000000, 7.000000, 0.000000>
        """
        x = self.x - term.x
        y = self.y - term.y
        z = self.z - term.z

        return Point3d(x, y, z)

    def __mul__(self, term):
        """Dot product; overrides the * operator.

        Example
        -------
        >>> a = Point3d(1, -2, 0)
        >>> b = Point3d(3, 5, 0)
        >>> print a * b
        -7
        """
        return (self.x * term.x) + (self.y * term.y) + (self.z * term.z)

    def cross(self, term):
        """Cross product

        Example
        -------
        >>> a = Point3d(1, -2, 0)
        >>> b = Point3d(3, 5, 0)
        >>> print a.cross(b)
        Point3d: <0.000000, 0.000000, 11.000000>
        """
        #return [u[1] * v[2] - v[1] * u[2], v[0] * u[2] - u[0] * v[2],
        #u[0] * v[1] - v[0] * u[1]]
        #thought process: u == self, v == term
                        #x, y, z indexed from 0
        #is this a correct assumption?
        x = self.y * term.z - term.y * self.z
        y = term.x * self.z - self.x * term.z
        z = self.x * term.y - term.x * self.y

        return Point3d(x, y, z)

    def __getitem__(self, index):
        """Vector components; indexed starting at 0.
        Example
        -------
        >>> a = Point3d(1, -2, 0)
        >>> a[0]
        1
        >>> a[1]
        -2
        >>> a[2]
        0
        """
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        elif index == 2:
            return self.z
        else:
            raise KeyError('Point3d %s has no component %d' %(self, index))

    def __setitem__(self, index, value):
        """Allows a value to be assigned to each vector component;
        indexed starting at 0.

        Example
        -------
        >>> a = Point3d(1, -2, 0)
        >>> print a
        Point3d: <1.000000, -2.000000, 0.000000>
        >>> a[0] = 3
        >>> print a
        Point3d: <3.000000, -2.000000, 0.000000>
        >>> a[1] = 4
        >>> print a
        Point3d: <3.000000, 4.000000, 0.000000>
        >>> a[2] = 1
        >>> print a
        Point3d: <3.000000, 4.000000, 1.000000>
        """
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        elif index == 2:
            self.z = value
        else:
            raise KeyError('Point3d %s has no component %d' %(self, index))

    def left_normal(self):
        """Normal vector"""
        #still the left-facing normal vector or is it something else now?
        k = Point3d(0, 0, 1)
        return self.cross(k, self)
