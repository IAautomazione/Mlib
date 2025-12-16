from manim import *
import numpy as np
from numpy import pi
from Mlib.Graphics.Colors import *

"""
Author: Ivan Archetti   
Creation date: 25/09/2025


Collection of python classes of conveyor_belts
"""


# ======================================================================================================================

class Converyor_belt():
    arguments = {}

    def __init__(self, height=1, length=4, belt_color=BLUE_AUT, rotation=-1, **kwargs):
        """
        rotation: direction of rotation -1 counterclockwise, clockwise = 1 
        """
        
        # initialization
        self.height = height
        self.length = length
        self.r = self.height/2
        self.rotation = rotation

        self.belt_color = belt_color

        self.conveyor_belt = VGroup()

        self.belt = self.set_belt()
        
        self.left_pulley = self.set_pulley(center=self.belt[0].get_start()[0]*LEFT)
        
        self.right_pulley = self.set_pulley(center=self.belt[0].get_end()[0]*RIGHT)

        self.frame = self.set_frame()


        self.conveyor_belt.add(self.left_pulley, self.belt, self.right_pulley, self.frame)


# ----------------------------------------------------------------------------------------------------------------------      

    def set_frame(self):
        """
        Create the frame of the conveyor belt
        """
        
        # initialization
        h = self.height
        r = self.r*1.05
        rotation = self.rotation

        start_angle = 3/4*pi
        angle = pi/2
        
        u = [np.cos(start_angle), np.sin(start_angle)]
        A = r*(u[0]*RIGHT + u[1]*UP) + self.right_pulley.get_center()
        B = r*(u[0]*LEFT + u[1]*UP) + self.left_pulley.get_center()
        C = r*(u[0]*LEFT - u[1]*UP) + self.left_pulley.get_center()
        D = r*(u[0]*RIGHT - u[1]*UP) + self.right_pulley.get_center()
        
        frame = VGroup()
        #0 right arc
        frame.add(Arc(radius=r, start_angle=-start_angle, angle=-angle, stroke_width=1, color=GREY_D).shift(self.right_pulley.get_center()))
        # upper line
        frame.add(Line(start=A, end=B, stroke_width=1, color=GREY_D))
        # left arc
        frame.add(Arc(radius=r, start_angle=pi-start_angle, angle=-angle, stroke_width=1, color=GREY_D).shift(self.left_pulley.get_center()))
        # lower line
        frame.add(Line(start=C, end=D, stroke_width=1, color=GREY_D))

        #4 internal area
        arc_points_left = frame[0].get_points()
        arc_points_right = frame[2].get_points()
        points = [*arc_points_left, *arc_points_right]
        frame.add(Polygon(*points, color=GREY_D, fill_color=GREY_D, fill_opacity=0.9, stroke_width=0))

        #5 direction arrows
        l_arrow = np.abs(self.left_pulley.get_center()[0] - self.right_pulley.get_center()[0])/2
        
        frame.add(Line(start=(l_arrow-r/3)*LEFT, end=1.2*r*LEFT, stroke_width=2*h, 
                       color=GREY_A).shift(self.right_pulley.get_center() + rotation*1/6*h*DOWN))
        frame[-1].add_tip(tip_length=h/6, tip_width=h/6)
        
        frame.add(Line(start=(l_arrow-r/3)*RIGHT, end=1.2*r*RIGHT, stroke_width=2*h,
                       color=GREY_A).shift(self.left_pulley.get_center() + rotation*1/6*h*UP))
        frame[-1].add_tip(tip_length=h/6, tip_width=h/6)

        return frame

# ----------------------------------------------------------------------------------------------------------------------      

    def set_belt(self):
        """
        Create the bel of the coveyor
        """
        
        # initialization
        h = self.height
        r = self.r # radius of the belt
        l = self.length

        # define thickness of the belt
        stroke_width = np.clip(8*h, 1, 8)
        
        belt_color = self.belt_color

        belt = VGroup()

        # first arc
        belt.add(Arc(radius=r, start_angle=-pi/2, angle=pi, color=belt_color, stroke_width=stroke_width))

        # upper side
        belt.add(Line(start=ORIGIN, end=l*LEFT, color=belt_color, stroke_width=stroke_width).shift(r*UP))

        # second arc
        belt.add(Arc(radius=r, start_angle=pi/2, angle=pi, color=belt_color, stroke_width=stroke_width).shift(l*LEFT))

        # lower side
        belt.add(Line(start=l*LEFT, end=ORIGIN, color=belt_color, stroke_width=stroke_width).shift(r*DOWN))

        # center the belt to the screen
        belt.shift(l/2*RIGHT)

        # insert the teeth on the belt
        self.teeth = VGroup()
    

        belt.add(self.teeth)

        return belt
    
    # ----------------------------------------------------------------------------------------------------------------------

    def set_pulley(self, center=ORIGIN):
        """
        Create the pulley for the belt
        center: where to put the pulley respect the space
        """
        
        # initialization
        h = self.height
        r_out = self.r*0.9
        r_in = self.r*0.3
        r_med = (r_out+r_in)/2
        pulley = VGroup()

        # main circle
        pulley.add(AnnularSector(inner_radius=r_in, outer_radius=r_out, angle=2*pi, color=GREY_D))

        # center circle
        pulley.add(Circle(radius=self.r*0.2, fill_opacity = 1, color=BLACK))
        
        # add the other interna circle
        n_circle = 8
        r_circle = r_out/7
        angle = 2*pi/n_circle
        stroke_width = np.clip(h, 1, 2)

        for i in range(n_circle):
            u = [np.cos(i*angle)*RIGHT, np.sin(i*angle)*UP]
            pulley.add(Circle(radius=r_circle, color=GREY_A, stroke_width=stroke_width).shift(r_med*(u[0]+u[1])))

        pulley.shift(center)

        return pulley
    
    # ----------------------------------------------------------------------------------------------------------------------

    def move_belt(self, n_turn=0.5, run_time=3):
        """
        Simulate the motion of the belt
        n_turn: number of turns
        run_time: simulation time
        """
        
        # initialization
        rotation = self.rotation

        functions = []
        
        # rotate the pulleys
        functions.append(Rotate(self.left_pulley, angle=rotation*n_turn*2*pi, run_time=run_time))
        functions.append(Rotate(self.right_pulley, angle=rotation*n_turn*2*pi, run_time=run_time))
        # activate the direction arrows
        functions.append(Indicate(self.frame[5], scale_factor=1.05, color=RED_AUT, run_time=run_time))
        functions.append(Indicate(self.frame[6], scale_factor=1.05, color=RED_AUT, run_time=run_time))

        return functions

