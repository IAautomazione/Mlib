from manim import *
import numpy as np
from numpy import pi
from Mlib.Graphics.Colors import *


"""
Author: Ivan Archetti   
Creation date: 09/09/2025


Collection of python classes about connections (Pipe, cable, tube, etc etc...)
"""

# ======================================================================================================================

class Pipe_connection():
    """
    Connection between pneumatic elements (pipe/hose)
    """

    arguments = {"pipe_color": BLACK,
                 "radius": 0.1,
                 "stroke": 4}

    def __init__(self, pos=ORIGIN, l_len=[1], directions=[RIGHT], color=BLACK, **kwargs):
        """
        l_len: is the sequence of the lenghts of each pipe part
        directions: has the same number of elements of L_len and define the direction of each 
                    element
        """
       
        # initialization of the pipe line
        self.pipe_color = color
        self.stroke = self.arguments["stroke"]
        self.r = self.arguments["radius"]
        self.pos = pos
        self.l_len = l_len
        self.dir = directions
              
        self.pipe_connection = self.set_pipe_connection()

    # ----------------------------------------------------------------------------------------------------------------------        

    def set_pipe_connection(self):
        """
        Procedure the creates the connection/pipe 
        """

        l_len = self.l_len
        dir = self.dir

        pipe_connection = VGroup()
        # check if the lengths and direction quantity are the same
        if len(l_len) == len(dir):
            # add first segment
            pipe_connection.add(Line(start=ORIGIN, end=l_len[0]*dir[0], color=self.pipe_color, stroke_width=self.stroke).shift(self.pos))
            # add from second to the last segment
            for j, k, l in zip(l_len[1:], dir[:-1], dir[1:]):
                # if pipe are more than one I'll add the others
                if len(self.l_len) > 1:
                    # check if the pipe are adjacent
                    if k[0] != np.abs(l[0]) or k[1] != np.abs(l[1]):
                        if k[0] != 0: # verify is the pipe is horizontal to determine the angle of the curve
                            start_angle = -pi/2*l[1]
                            angle = pi/2*l[1]*k[0]
                        if k[1] != 0: # verify is the pipe is vertical to determine the angle of the curve
                            start_angle = pi/2*(l[0]+1)
                            angle = -pi/2*l[0]*k[1]
                        
                        # add curved pipe
                        pipe_connection.add(Arc(radius=self.r, start_angle=start_angle, angle=angle, color=self.pipe_color,
                                                stroke_width=self.stroke).next_to(pipe_connection[-1], direction=k, buff=0).shift(self.r/2*l))
                    
                        # add straight connection
                        pipe_connection.add(Line(start=ORIGIN, end=j*l, color=self.pipe_color, 
                                                 stroke_width=self.stroke).next_to(pipe_connection[-1], direction=l, buff=0).shift(self.r/2*k))
                    else:
                        print("\n Two adjacent straight lines with same direction! \n")
        else:
            print("\n Quantity of lengths and direction mismatched!  \n")        
    
        return pipe_connection