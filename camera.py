#!/usr/bin/python
"""A Camera Class
This module is responsible for keeping track of camera-related details
"""

from point2d import Point2d
from point3d import Point3d

class Camera(object):
    """Creates a camera with the given specifications

    Parameters
    ----------
    focal_len: float
        focal length of the camera.
    dpi: float
        dots-per-inch of the camera.
    fov: float
        distance to which the camera can see. field of vision
    """

    def __init__(self, focal_len, dpi, fov, x_min, x_max, obj_width, focal_point):
        self.dpi = dpi
        self.focal_len = self.convert_to_px(focal_len)
        self.fov = self.convert_to_px(fov)
        self.retina_width = (self.focal_len * self.convert_to_px(obj_width))/self.fov
        self.u_vector = Point2d()
        self.v_vector = Point2d()
        self.focal_point = focal_point
        self.rect = []

    def convert_to_px(self, value):
        """Camera specifications are given in millimeters, but need to be
        converted to pixels in order to work with image values

        Parameters
        ----------
        value: float
            value in millimeters to convert to pixels

        Note
        ----
        Possible update: change to convert to/from various measurements used
        in images and photography
        """
        return (value * self.dpi)/25.4

    def is_within_view(self, w_vector, dimensions=2, rect=None):
        """Determines if a given point on an object is within a cone of vision
        as determined by two points created from the camera's view.

        Parameters
        ----------
        u, v: Point2d
            Points from with a cone is created
        w: Point2d
            Point to determine if is within the view point of 'u' and 'v'
        dimension: int
            Number of dimensions of the plane; 2 by default
        rect: array-like
            List of Point3d objects that form a rectangle; None by default.
            Only necessary if 'dimensions' is 3

        Returns
        -------
        bool:
            True if 'w' is within cone, otherwise False

        Note
        ----
        Points for the 'rect' variable must be input in the following order
        Point 1 - x_max, y_min
        Point 2 - x_min, y_min
        Point 3 - x_min, y_max
        Point 4 - x_max, y_max
        """
        if dimensions == 2:
            if(self.u_vector.left_normal() * w_vector > 0) and (self.v_vector.left_normal() * w_vector < 0):
                return True
            else:
                return False
        elif dimensions == 3:
            #TODO: find a way enforce rect if dimensions is 3
            norm_rect = []
            for index in range(len(rect)):
                norm_rect.append(rect[index], rect[(index+1) % len(rect)])

            for vector in norm_rect:
                if vector * w_vector > 0:
                    return False
            return True
        else:
            raise ValueError('A %d plane does not exist. Please enter a dimension of 2 or 3' %dimensions)

    def object_view2d(self, x_min, x_max, width):
        """Creates the object's current cone of view (provides values for
        vectors u & v).
        Sets up the u and v vectors for within view

        Parameters
        ----------
        x_min: int
            Minimum x value for the object
        x_max: int
            Maximum x value for the object
        width: int
            width of the image seen. This will eventually be a class variable
        """
        a_vector = Point2d(-self.retina_width/2 + (x_min * self.retina_width)/width, -self.focal_len)
        self.u_vector = self.focal_point - a_vector

        b_vector = Point2d(-self.retina_width/2 + (x_max * self.retina_width)/ width, -self.focal_len)
        self.v_vector = self.focal_point - b_vector
