from manim import *
import numpy as np
from numpy import pi

from Mlib.Graphics.Colors import *


"""
Author: Ivan Archetti   
Creation date: 10/09/2025


Collection of python classes about functional valves
"""


# ======================================================================================================================

class OneWay_flow_control_valve():
    """
    One-way flow control valve
    """

    arguments = {"valve_stroke_color": GREY_E,
                 "valve_fill_color": GREY_A}

    def __init__(self, height=2, angle=0, flip=-1, visible_connections=False, **kwargs):
        """
        flip: 1 body is flipped -1 body is not flipped
        """

        # initialization of valve geometry
        self.h = height
        self.w = height
        self.r_nr = self.h/15 # radius of not return sphere
        self.angle = angle
        self.u = (np.cos(angle), np.sin(angle))
        self.not_return_status = 0 # status of not return device

        self.valve_stroke_color = self.arguments["valve_stroke_color"]
        self.valve_fill_color = self.arguments["valve_fill_color"]

        self.valve = VGroup()

        self.body = self.set_body(visible_connections=visible_connections)

        if flip==1:
            self.__flip()

        self.valve.add(self.body)

    # ----------------------------------------------------------------------------------------------------------------------        

    def set_body(self, visible_connections=False):
        """
        Define the body of the valve
        flip: redraw thw body valve flipped of pi respect to the vertical axis
        """
        
        h = self.h
        w = self.w
        r_nr = self.r_nr 
        angle = self.angle
        
        line_stroke = 3
        
        body = VGroup()
        #0 external body
        body.add(Rectangle(width=w, height=h, color=self.valve_stroke_color, fill_color=self.valve_fill_color, fill_opacity=0.5))
        
        # internal simbol
        #1 input/output line
        #body.add(Line(start=w/4*LEFT + 1/2*h*UP, end=w/4*LEFT + 1/2*h*DOWN, color=BLACK, stroke_width=line_stroke)) # vertical left line
        body.add(Line(start=w/4*LEFT + 1/2*h*UP, end=w/4*LEFT + 1/3*h*UP, color=BLACK, stroke_width=line_stroke)) # first vertical left line
        body.add(Line(start=w/4*LEFT + 1/3*h*UP, end=w/4*LEFT + 1/3*h*DOWN, color=BLACK, stroke_width=line_stroke)) # second vertical left line
        body.add(Line(start=w/4*LEFT + 1/3*h*DOWN, end=w/4*LEFT + 1/2*h*DOWN, color=BLACK, stroke_width=line_stroke)) # third vertical left line

        #4 dots connections
        body.add(Dot(radius=h/40, color=BLACK).shift(h/4*LEFT + 1/3*h*UP))
        body.add(Dot(radius=h/40, color=BLACK).shift(h/4*LEFT + 1/3*h*DOWN))
        #body.add(Line(start=body[2].get_center()+h/40*DOWN, end=body[3].get_center()+h/40*UP, color=BLACK, stroke_width=line_stroke)) # extra vertical left line
        
        #6 not return line
        body.add(Line(start=w/4*LEFT + 1/3*h*UP, end=w/4*RIGHT + 1/3*h*UP, color=BLACK, stroke_width=line_stroke))
        body.add(Line(start=w/4*RIGHT + 1/3*h*UP, end=w/4*RIGHT + 2**(1/2)*r_nr*UP, color=BLACK, stroke_width=line_stroke))

        body.add(Line(start=2**(1/2)*r_nr*UP, end=(1/2+2**(1/2))*r_nr*LEFT + 1/2*r_nr*DOWN, color=BLACK, stroke_width=line_stroke).shift(h/4*RIGHT)) # left "hat"
        body.add(Line(start=2**(1/2)*r_nr*UP, end=(1/2+2**(1/2))*r_nr*RIGHT+ 1/2*r_nr*DOWN, color=BLACK, stroke_width=line_stroke).shift(h/4*RIGHT)) # right "hat"
        body.add(Circle(radius=h/14, color=BLACK, stroke_width=line_stroke).shift(h/4*RIGHT)) # central sphere
        
        body.add(Line(start=w/4*RIGHT + r_nr*DOWN, end=w/4*RIGHT + 1/3*h*DOWN, color=BLACK, stroke_width=line_stroke))
        body.add(Line(start=w/4*RIGHT + 1/3*h*DOWN, end=w/4*LEFT + 1/3*h*DOWN, color=BLACK, stroke_width=line_stroke))

        #13 choke valve
        body.add(Arc(radius=h/3, start_angle=5/6*pi, angle=1/3*pi, color=BLACK, stroke_width=line_stroke).shift(body[2].get_center() + (1/3+1/20)*h*RIGHT))
        body.add(Arc(radius=h/3, start_angle=1/6*pi, angle=-1/3*pi, color=BLACK, stroke_width=line_stroke).shift(body[2].get_center() + (1/3+1/20)*h*LEFT))
        arrow_angle = pi/6
        body.add(Arrow(start=h/6*(np.sin(arrow_angle)*DOWN+np.cos(arrow_angle)*LEFT), end=h/4*(np.sin(arrow_angle)*UP+np.cos(arrow_angle)*RIGHT), 
                       color=BLACK, stroke_width=line_stroke, buff=0).shift(body[2].get_center()))
        
        if visible_connections:
            #15 tag numbers
            body.add(Text("2", color=BLACK).scale(0.3*h).next_to(body[1].get_top(), direction=DL, buff=0.15).rotate(-angle))
            body.add(Text("1", color=BLACK).scale(0.3*h).next_to(body[3].get_bottom(), direction=UL, buff=0.15).rotate(-angle))

        # rotate respect to the angle
        body.rotate(angle=angle)

        return body
    
    # ----------------------------------------------------------------------------------------------------------------------        

    def __flip(self):
        """
        Flip the body of the valve
        """
        
        self.body.flip(axis=UP)
        self.body[-1].flip(axis=LEFT)
        self.body[-2].flip(axis=LEFT)
        self.body.rotate(pi)
        self.u = (np.cos(self.angle+pi), -np.sin(self.angle+pi))

    # ----------------------------------------------------------------------------------------------------------------------        

    def active_choke(self, active=1, active_color=BLUE_E):
        """
        Actives the valve and shows the choke
        active: set whether the valve function is active (1 active / -1 not active)
        """

        if active==1:
            color = active_color
            line_stroke = 6
        else:
            color = BLACK
            line_stroke = 3

        functions = []
        functions.append(self.body[2].animate().set_color(color).set_stroke(width=line_stroke))
        functions.append(self.body[13:16].animate().set_color(color))

        return functions
    
    # ----------------------------------------------------------------------------------------------------------------------        

    def active_not_return(self, active=1, open_color=BLUE_E, closed_color=BLUE_A):
        """
        Show the movement of the not return sphere
        active: set whether the valve function is active (1 active / -1 not active/ 0 neutral)
        """
        
        # initialization
        h = self.h
        u = self.u
        r_nr = self.r_nr
        k = 0

        functions = []

        l = (1/3*h-r_nr) # length of vertical line under the sphere
        
        if active == 1: # open
            color = open_color
            opacity = 0.3
            k = 1
            limit = 6
        elif active == 0:
            color = closed_color # closed
            opacity = 0.3
            k = 0
            limit = 8
        elif active == -1: # normal
            color = BLACK
            opacity = 0
            k = -1
            limit = 6

            # check the previous status to restore the correct position of the sphere
            if self.not_return_status == 0:
                k = 0
            elif self.not_return_status == 1:
                k = -1

        scale_factor = (5/7)**k # reduction factor to move the vertical line
        direction = k*(1-(scale_factor)**k)*l*(DOWN*u[0]+RIGHT*u[1])

        # set horizontal and vertical input lines color
        # move sphere
        functions.append(self.body[10].animate().set_color(color).set_fill(opacity=opacity).shift(direction))
        # rescale vertical
        functions.append(self.body[11].animate().set_color(color).scale(scale_factor).shift(direction/2))

        # color the not return line
        functions.append(self.body[1].animate().set_color(color))
        functions.append(self.body[3].animate().set_color(color))
        functions.append(self.body[limit:10].animate().set_color(color))
        functions.append(self.body[12].animate().set_color(color))
        

        # update status
        self.not_return_status = active

        return functions
    
    # ----------------------------------------------------------------------------------------------------------------------

    def get_output_2(self):
        """
        Get output number 2 of the valve (FESTO numeration)
        """

        # sum chamber center and position of connection
        output_2 = self.body[1].get_start() 
        return output_2
    
     # ----------------------------------------------------------------------------------------------------------------------

    def get_input_1(self):
        """
        Get input number 1 of the valve (FESTO numeration)
        """

        # sum chamber center and position of connection
        input_1 = self.body[3].get_end() 
        return input_1
    
     # ----------------------------------------------------------------------------------------------------------------------