#!/usr/bin/python
"""A Grid class
This module is responsible for creating a grid for use in conjunction with
tactical"""

from point2d import Point2d

class Grid(object):
    """Creates a Grid of the given interval based on the camera height, width
    and a starting value

    Parameters
    ----------
    interval: int
        distance between the grid points
    height, width: int
        will be replaced in later implementations from camera input
    start_val: int
        value at which the grid should start. 0 by default
    cam: Camera
        camera object on which the grid will be based
    """

    def __init__(self, interval, height, width, start_val=0, cam=None):
        self.interval = interval
        self.height = height
        self.width = width
        self.start = start_val
        self.gridpoints = self.build_grid()
        self.cam = cam

    def build_grid(self):
        """Creates the points for the grid

        Returns
        -------
        array-like:
            Point2d objects representing each point on the grid
        """

        points = []
        delta_x = self.width/self.interval
        delta_y = self.height/self.interval

        for y_val in range(self.start, self.height + delta_y, delta_y):
            for x_val in range(self.start, self.width + delta_x, delta_x):
                point = Point2d(x_val, y_val)
                if point not in points:
                    points.append(point)

        return points

    def __remove__(self, value):
        """Overrides the remove method of the list class for use with the
        grid class.
        Will remove the points from the 'gridpoints' class member"""
        self.gridpoints.remove(value)

    #TODO: create a setitem, getitem, so that we can use in for loops?
    #if index >= len(grid_points) raise error

    def draw(self, mode=0):
        """Uses matplotlib to produce a graphical representation of the grid

        Parameters
        ----------
        mode: int
            A 'mode' value of 0 will draw only the grid.
            A 'mode' value of 1 will draw the grid + object (cone) view

        TODO: create mode as an enumerated type.
        """
        import matplotlib.pyplot as plt
        fig = plt.figure()
        plt.plot([g[0] for g in self.gridpoints], [g[1] for g in self.gridpoints], 'o')
        #plt.xlim(self.start, self.width)
        #plt.ylim(self.start, self.height)

        if mode == 1:
            from matplotlib.lines import Line2D
            axis = fig.add_subplot(111)
            plt.plot(self.cam.u_vector[0], self.cam.u_vector[1], 'x', color='m')
            plt.plot(self.cam.v_vector[0], self.cam.v_vector[1], 'o', color='m')
            line1 = Line2D([self.start, self.cam.u_vector[0], self.cam.u_vector[0]*100], [self.start, self.cam.u_vector[1], self.cam.u_vector[1] * 100])
            line2 = Line2D([self.start, self.cam.v_vector[0], self.cam.v_vector[0]*100], [self.start, self.cam.v_vector[1], self.cam.v_vector[1] * 100])
            axis.add_line(line1)
            axis.add_line(line2)

        plt.show()

if __name__ == '__main__':
    testgrid = Grid(10, 480, 640)
    testgrid.draw()

    from camera import Camera
    cam2d = Camera(3.97, 640, 95, 120, 400, 48, Point2d())
    cam2d.object_view2d(120, 400, 640)
    conetestgrid = Grid(10, 480, 640, cam=cam2d)
    conetestgrid.draw(1)

    for gp in conetestgrid.gridpoints[:]:
        if cam2d.is_within_view(gp):
            conetestgrid.gridpoints.remove(gp)
    conetestgrid.draw(1)
