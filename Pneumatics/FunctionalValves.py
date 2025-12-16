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
        """
        
        h = self.h
        w = self.w
        r_nr = self.r_nr 
        angle = self.angle
        
        line_stroke = 2*h
        
        body = VGroup()
        #0 external body
        body.add(Rectangle(width=w, height=h, color=self.valve_stroke_color, fill_color=self.valve_fill_color, stroke_width=line_stroke, fill_opacity=0.5))
        
        # internal simbol
        #1 input/output line
        body.add(Line(start=w/4*LEFT + 1/2*h*UP, end=w/4*LEFT + 1/3*h*UP, color=BLACK, stroke_width=line_stroke)) # first vertical left line
        body.add(Line(start=w/4*LEFT + 1/3*h*UP, end=w/4*LEFT + 1/3*h*DOWN, color=BLACK, stroke_width=line_stroke)) # second vertical left line
        body.add(Line(start=w/4*LEFT + 1/3*h*DOWN, end=w/4*LEFT + 1/2*h*DOWN, color=BLACK, stroke_width=line_stroke)) # third vertical left line

        #4 dots connections
        body.add(Dot(radius=h/40, color=BLACK).shift(h/4*LEFT + 1/3*h*UP))
        body.add(Dot(radius=h/40, color=BLACK).shift(h/4*LEFT + 1/3*h*DOWN))
        
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
    
# ======================================================================================================================

class Piloted_check_valve():
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
        self.w = height/1.8
        self.u = (np.cos(angle), np.sin(angle))
        self.r_nr = self.h/10 # radius of not return sphere
        self.angle = angle
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
        
        """
        
        h = self.h
        w = self.w
        r_nr = self.r_nr 
        angle = self.angle
        
        line_stroke = 2*h
        
        body = VGroup()
        #0 external body
        body.add(Rectangle(width=w, height=h, color=self.valve_stroke_color, fill_color=self.valve_fill_color, stroke_width=line_stroke, fill_opacity=0.5))
        # internal simbol
        #1
        body.add(Line(start=1/2*h*UP, end=3/10*h*UP, color=BLACK, stroke_width=line_stroke)) 
        #2 
        body.add(Line(start=ORIGIN, end=(1/2+2**(1/2))*r_nr*(LEFT+DOWN), color=BLACK, stroke_width=line_stroke).shift(1.5/5*h*UP)) # left "hat"
        body.add(Line(start=ORIGIN, end=(1/2+2**(1/2))*r_nr*(RIGHT+DOWN), color=BLACK, stroke_width=line_stroke).shift(1.5/5*h*UP)) # right "hat"
        body.add(Circle(radius=r_nr, color=BLACK, stroke_width=line_stroke).shift((3/10*h-(1+2**(1/2)/2)*r_nr)*UP)) # central sphere
        #5
        body.add(Line(start=body[-1].get_bottom(), end=h/2*DOWN, color=BLACK, stroke_width=line_stroke))
        #6 line of command
        body.add(Line(start=ORIGIN, end=h/8*RIGHT, color=BLACK, stroke_width=line_stroke).shift(body[0].get_left()+0.25*h*UP))
        body.add(Line(start=body[-1].get_right(), end=body[2].get_center(), color=BLACK, stroke_width=line_stroke))
        
        if visible_connections:
            #8 tag numbers
            body.add(Text("1", color=BLACK).scale(0.3*h).next_to(body[1].get_top(), direction=UL, buff=0.05*h).rotate(-angle))
            body.add(Text("2", color=BLACK).scale(0.3*h).next_to(body[5].get_bottom(), direction=DL, buff=0.05*h).rotate(-angle))
            body.add(Text("3", color=BLACK).scale(0.3*h).next_to(body[6].get_left(), direction=UL, buff=0.05*h).rotate(-angle))

        # rotate respect to the angle
        body.rotate(angle=angle)

        return body
    
    # ----------------------------------------------------------------------------------------------------------------------        

    def __flip(self):
        """
        Flip the body of the valve
        """
        
        self.body.flip(axis=LEFT)
        self.body[-1].flip(axis=UP)
        self.body[-2].flip(axis=UP)
        self.body[-3].flip(axis=UP)
        self.body.rotate(pi)

    # ----------------------------------------------------------------------------------------------------------------------        

    def active_not_return(self, active=1, open_color=BLUE_E, closed_color=BLUE_A):
        """
        Show the movement of the not return sphere
        active: set whether the valve function is active (1 active / -1 not active/ 0 neutral)
        """
        
        # initialization
        h = self.h
        u = self.u
        k = 0

        functions = []

        l = 1.2/5*h # length of vertical line upper the sphere
        
        if active == 1: # open
            color = open_color
            opacity = 0.1
            k = 1

        elif active == 0:
            color = closed_color # closed  
            opacity = 0.1
            k = 0

        elif active == -1: # normal
            color = BLACK
            opacity = 0
            k = -1

            # check the previous status to restore the correct position of the sphere
            if self.not_return_status == 0:
                k = 0
            elif self.not_return_status == 1:
                k = -1

        scale_factor = (5/7)**k # reduction factor to move the vertical line
        direction = k*(1-(scale_factor)**k)*l*(DOWN*u[0]+RIGHT*u[1])

        # set horizontal and vertical input lines color
        # move sphere
        functions.append(self.body[4].animate().set_color(color).set_fill(opacity=opacity).shift(2*direction))
        # rescale vertical
        functions.append(self.body[5].animate().set_color(color).scale(scale_factor).shift(direction))
        # color vertical line
        functions.append(self.body[1].animate().set_color(color))
       
        # update status
        self.not_return_status = active

        return functions

    # ----------------------------------------------------------------------------------------------------------------------

    def get_input_1(self):
        """
        Get input number 1 of the valve (FESTO numeration)
        """

        input_1 = self.valve[0].get_top()
        return input_1
    
    # ----------------------------------------------------------------------------------------------------------------------

    def get_input_3(self):
        """
        Get input number 3 of the valve, controll input (FESTO numeration)
        """

        input_3 = self.valve[0][6].get_start()
        return input_3

    
# =====================================================================================================================

class AND_valve():
    """
    Logic valve OR function
    """

    arguments = {"valve_stroke_color": GREY_E,
                 "valve_fill_color": GREY_A}

    def __init__(self, height=2, visible_connections=False, actuated=False, position=0, **kwargs):
        """
        visible_connections: show or not tags of connections
        stroke: is the percentage of the total stroke (positive right, negative left)
        """

        # initialization of valve geometry
        self.h = height
        self.w = height

        self.valve_stroke_color = self.arguments["valve_stroke_color"]
        self.valve_fill_color = self.arguments["valve_fill_color"]

        self.valve = VGroup()

        self.body = self.set_body(visible_connections=visible_connections)
        
        if actuated:
            self.switch_valve(position=position, animated=False)

        self.valve.add(self.body)

    # ----------------------------------------------------------------------------------------------------------------------        

    def set_body(self, visible_connections=False):
        """
        Define the body of the valve
        flip: redraw thw body valve flipped of pi respect to the vertical axis
        stroke: is the percentage of the total stroke (positive right, negative left)
        """
        
        h = self.h
        w = 2*self.w
        self.wall_factor = wall_factor = 1/90
        
        stroke_width = 2*h
        
        body = VGroup()
        #0 external body
        body.add(Rectangle(width=w, height=h, color=self.valve_stroke_color, fill_color=self.valve_fill_color, stroke_width=stroke_width, fill_opacity=0.5))

        #1 left diaphragm
        body.add(Line(start=ORIGIN, end=h/5*UP, stroke_width=stroke_width, color=BLACK).shift(w/4*LEFT+h/2*DOWN))
        body.add(Line(start=ORIGIN, end=h/5*DOWN, stroke_width=stroke_width, color=BLACK).shift(w/4*LEFT+h/2*UP))
        #3 right diaphragm
        body.add(Line(start=ORIGIN, end=h/5*UP, stroke_width=stroke_width, color=BLACK).shift(w/4*RIGHT+h/2*DOWN))
        body.add(Line(start=ORIGIN, end=h/5*DOWN, stroke_width=stroke_width, color=BLACK).shift(w/4*RIGHT+h/2*UP))
        
        #5 internal piston
        body.add(Rectangle(width=2/3*w, height=1/5*h, stroke_width=stroke_width, color=BLACK).shift((1/12*w*RIGHT + w*wall_factor*LEFT)))
        body.add(Line(start=2/5*h*DOWN, end=2/5*h*UP, stroke_width=stroke_width, color=BLACK).shift(body[-1].get_left()))
        body.add(Line(start=2/5*h*DOWN, end=2/5*h*UP, stroke_width=stroke_width, color=BLACK).shift(body[-2].get_right()))

        #8 connections
        body.add(Line(start=ORIGIN, end=w/6*LEFT, stroke_width=stroke_width, color=BLACK).shift(body[0].get_left()))
        body.add(Line(start=ORIGIN, end=w/6*UP, stroke_width=stroke_width, color=BLACK).shift(body[0].get_top()))
        body.add(Line(start=ORIGIN, end=w/6*RIGHT, stroke_width=stroke_width, color=BLACK).shift(body[0].get_right()))
        
        if visible_connections:
            #11 tag numbers
            body.add(Text("1", color=BLACK).scale(0.3*h).next_to(body[8].get_top(), direction=UP, buff=h/20))
            body.add(Text("2", color=BLACK).scale(0.3*h).next_to(body[9].get_right(), direction=RIGHT, buff=h/20))
            body.add(Text("3", color=BLACK).scale(0.3*h).next_to(body[10].get_top(), direction=UP, buff=h/20))
            

        return body
    
    # ----------------------------------------------------------------------------------------------------------------------        

    def switch_valve(self, position=0, animated=True, run_time=1):
        """
        Switch internal piston
        stroke: is the percentage of the total stroke (positive right, negative left)
        """

        # initialization
        w = 2*self.w

        movement = (1/6*RIGHT+2*self.wall_factor*LEFT)*w*position

        if animated:
            functions = self.body[5:8].animate(run_time=run_time).shift(movement)
        else:
            functions = self.body[5:8].shift(movement)

        return functions
         
# =====================================================================================================================

class OR_valve():
    """
    Logic valve OR function
    """

    arguments = {"valve_stroke_color": GREY_E,
                 "valve_fill_color": GREY_A}

    def __init__(self, height=2, visible_connections=False, actuated=False, position=0, **kwargs):
        """
        visible_connections: show or not tags of connections
        animated: a flag that defines whether is in animation mode or in static mode
        actuated: a flag that defines whether the position of sphere must change
        """

        # initialization of valve geometry
        self.h = height
        self.w = height

        self.valve_stroke_color = self.arguments["valve_stroke_color"]
        self.valve_fill_color = self.arguments["valve_fill_color"]

        self.valve = VGroup()

        self.body = self.set_body(visible_connections=visible_connections)

        if actuated:
            self.switch_valve(position=position, animated=False)

        self.valve.add(self.body)

    # ----------------------------------------------------------------------------------------------------------------------        

    def set_body(self, visible_connections=False):
        """
        Define the body of the valve
        visible_connections: shows or not the tags of connections
        """
        
        h = self.h
        w = 2*self.w

        stroke_width = 2*h
        
        body = VGroup()
        #0 external body
        body.add(Rectangle(width=w, height=h, color=self.valve_stroke_color, fill_color=self.valve_fill_color, stroke_width=stroke_width, fill_opacity=0.5))

        #1 internal connection LEFT
        body.add(Line(start=ORIGIN, end=w/8*RIGHT, stroke_width=stroke_width, color=BLACK).shift(body[0].get_left()))
        body.add(Line(start=ORIGIN, end=w/8*(RIGHT+UP), stroke_width=stroke_width, color=BLACK).shift(body[-1].get_right()))
        body.add(Line(start=ORIGIN, end=w/8*(RIGHT+DOWN), stroke_width=stroke_width, color=BLACK).shift(body[-2].get_right()))

        #4 upper connection
        body.add(Line(start=ORIGIN, end=h/2*DOWN, stroke_width=stroke_width, color=BLACK).shift(body[0].get_top()))
        body.add(Dot(radius=0.025*h, color=BLACK).shift(body[-1].get_bottom()))

        #6 internal connection RIGHT
        body.add(Line(start=ORIGIN, end=w/8*LEFT, stroke_width=stroke_width, color=BLACK).shift(body[0].get_right()))
        body.add(Line(start=ORIGIN, end=w/8*(LEFT+UP), stroke_width=stroke_width, color=BLACK).shift(body[-1].get_left()))
        body.add(Line(start=ORIGIN, end=w/8*(LEFT+DOWN), stroke_width=stroke_width, color=BLACK).shift(body[-2].get_left()))

        #9 internal sphere
        body.add(Circle(radius=h/8, color=BLACK, stroke_width=stroke_width).shift((w*3/16+w/8*np.cos(pi/4))*LEFT)) 
        body.add(Line(start=body[1].get_right(), end=body[9].get_left(), stroke_width=stroke_width, color=BLACK))
        body.add(Line(start=body[9].get_right(), end=body[6].get_left(), stroke_width=stroke_width, color=BLACK))
        
        #12 connections
        body.add(Line(start=ORIGIN, end=w/6*LEFT, stroke_width=stroke_width, color=BLACK).shift(body[0].get_left()))
        body.add(Line(start=ORIGIN, end=w/6*UP, stroke_width=stroke_width, color=BLACK).shift(body[0].get_top()))
        body.add(Line(start=ORIGIN, end=w/6*RIGHT, stroke_width=stroke_width, color=BLACK).shift(body[0].get_right()))
        
        if visible_connections:
            #14 tag numbers
            body.add(Text("1", color=BLACK).scale(0.3*h).next_to(body[12].get_top(), direction=UP, buff=h/20))
            body.add(Text("2", color=BLACK).scale(0.3*h).next_to(body[13].get_right(), direction=RIGHT, buff=h/20))
            body.add(Text("3", color=BLACK).scale(0.3*h).next_to(body[14].get_top(), direction=UP, buff=h/20))

        return body
    
    # ----------------------------------------------------------------------------------------------------------------------        

    def switch_valve(self, position=0, animated=True, run_time=1):
        """
        Switch internal sphere
        position: relative position of the internal sphere (-1 left,  1 right)
        """


        # initializations
        w = 2 * self.w

        functions = []

        # defines elements
        sphere = self.body[9]
        left_line = self.body[10]
        right_line = self.body[11]

        # defines the shift amount (position = -1 left, +1 right)
        shift_amount = (3 + 2*np.cos(np.pi/4))*w/8*position*RIGHT

        # creates the new lines thatconnect the sphere 
        new_left_line = Line(start=self.body[1].get_right(), end=sphere.get_left() + shift_amount,
                             stroke_width=left_line.stroke_width, color=left_line.color)

        new_right_line = Line(start=sphere.get_right() + shift_amount, end=self.body[6].get_left(),
                              stroke_width=right_line.stroke_width, color=right_line.color)

        if animated:
            functions.append(sphere.animate(run_time=run_time).shift(shift_amount))
            functions.append(Transform(left_line, new_left_line, run_time=run_time))
            functions.append(Transform(right_line, new_right_line,run_time=run_time ))
        else:
            functions.append(sphere.shift(shift_amount))
            functions.append(left_line.become(new_left_line))
            functions.append(right_line.become(new_right_line))

        return functions
    
    # =====================================================================================================================

    