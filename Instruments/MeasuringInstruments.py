from manim import *
import numpy as np
from numpy import pi
from Mlib.Electronics.Displays import Display_7_segments as dsp7
from Mlib.Graphics.Colors import *


"""
Author: Ivan Archetti   
Creation date: 09/09/2025


Collection of python classes about instruments for measuring
"""

# ======================================================================================================================

class Gauge():  
    """
    Pressure gauge
    """

    arguments = {"notches": 40}

    def __init__(self, radius=1, um='', **kwargs):
        
        # initialization
        self.radius = radius
        self.start_notch_angle = 7/6*pi
        self.notch_angle = -4/3*pi
        self.notches = self.arguments["notches"] # number of notches
        self.um = um # unit of measurement (e.g. bar, Pa, atm, etc etc...)

        self.gauge = VGroup()

        self.body = self.set_body()

        self.gage = self.set_gage()

        self.arrow = self.set_arrow()
        
        self.gauge.add(self.body, self.gage, self.arrow)
        
    # ----------------------------------------------------------------------------------------------------------------------        

    def set_body(self):
        """
        Create circular body and fitting of the gauge
        """

        # initiialization
        r = self.radius
        angle = pi/12 # angle that determinate fitting width
        u1 = [np.cos(3/2*pi-angle), np.sin(3/2*pi-angle)]
        u2 = [np.cos(3/2*pi+angle), np.sin(3/2*pi+angle)]

        body = VGroup()
        # external body
        body.add(Circle(radius=r, color=BLACK, fill_color=GREY_A, fill_opacity=0.3, stroke_width=4))
        
        # fitting
        body.add(Arc(radius=r, start_angle=3/2*pi-angle, angle=2*angle, stroke_width=2, color=BLACK))
        body.add(Line(start=ORIGIN, end=r/3*DOWN, stroke_width=2, color=BLACK).shift(r*(u1[0]*RIGHT + u1[1]*UP)))
        body.add(Line(start=r*u1[0]*RIGHT, end=r*u2[0]*RIGHT, stroke_width=2, color=BLACK).shift(body[-1].get_bottom()[1]*UP))
        body.add(Line(start=ORIGIN, end=r/3*DOWN, stroke_width=2, color=BLACK).shift(r*(u2[0]*RIGHT + u2[1]*UP)))
        
        element_A = body[1].get_points() # arc points
        element_B = body[3].get_points()[::-1] # horizontal line points
        points = [*element_A, *element_B]  # closed path
        body.add(Polygon(*points, color=GREY_C, fill_opacity=0.5, stroke_width=0))
        
        return body
    
    # ----------------------------------------------------------------------------------------------------------------------        
    
    def set_gage(self):
        """
        Set number and notches of the gage
        """
        
        # initialization
        d_angle = self.notch_angle/self.notches
        r = self.radius
        um = self.um
        
        start = self.radius*0.9
        end = self.radius*0.7
        number_pos = self.radius*0.6
        
        gage = VGroup()
        
        for i in range(self.notches+1):
            # notches vector
            u = [np.cos(self.start_notch_angle + i*d_angle)*RIGHT, np.sin(self.start_notch_angle + i*d_angle)*UP]
            
            # define notches length
            if i%5 == 0:
                start = self.radius*0.9
                # add numbers
                gage.add(Text(f"{int(i/5)}", color=BLACK).scale(0.3*r).shift(number_pos*(u[0] + u[1])))
            else:
                start = r*0.8
            end = r*0.7
            
            # add notch
            gage.add(Line(start=start*(u[0] + u[1]), end=end*(u[0] + u[1]), color=BLUE_AUT, stroke_width=2))
        # add unit of measurement
        gage.add(Text(um, color=BLUE_AUT).scale(0.25*self.radius).shift(self.body[0].get_center() + 0.6*r*DOWN))

        return gage
    
    # ----------------------------------------------------------------------------------------------------------------------        

    def set_arrow(self):
        """
        Create the central arrow of the cursor
        """
        
        r = self.radius
        a = 1/15
        b = 1/3
        c = 1/10
        
        arrow = VGroup()
        # create arrow (in vertical position)
        triangle = Polygon([-a*r, -b*r, 0], [0, 2*b*r, 0], [a*r, -b*r, 0])
        circle = Circle(radius=r*c)
        arrow.add(Union(triangle, circle))
        arrow[-1].set_fill(BLUE_AUT, opacity=1)
        arrow[-1].set_stroke(color=BLUE_AUT, width=0)
        arrow.add(Intersection(triangle, circle))
        arrow[-1].set_fill(BLUE_AUT, opacity=1)
        arrow[-1].set_stroke(color=BLUE_AUT, width=0)
        # add central point
        arrow.add(Dot(radius=r*c/3, color=GREY_B))

        # set initial position (must be compensated vertical position)
        arrow.rotate(angle=self.start_notch_angle-pi/2, about_point=arrow[-1].get_center())
        
        return arrow
    
    # ----------------------------------------------------------------------------------------------------------------------        

    def set_gage_value(self, gage_perc=0):
        """
        Rotate the central arrow forward and backward respect the notch angle (from -100% to 100%)
        gage_perc: percentage of max value that rotates the arrow
        
        """
        
        gage_perc = np.clip(gage_perc, -100, 100)
        angle = self.notch_angle*gage_perc/100
        return Rotating(self.arrow, radians=angle, about_point=self.body[0].get_center())
    

# ======================================================================================================================

class FlowSensor():  
    """
    Flow sensor
    """

    arguments = {"body_color": GREY_D,
                 "indication_color": WHITE}

    def __init__(self, height=1, um='', **kwargs):

        # initialization
        self.body_color = self.arguments["body_color"]
        self.indication_color = self.arguments["indication_color"]
        self.um = um

        self.h = height
        self.w = 2/3*height

        self.flowsensor = VGroup()

        self.body = self.set_body()

        self.screen, self.digits = self.set_screen()

        self.flowsensor.add(self.body, self.screen)

    # ----------------------------------------------------------------------------------------------------------------------        

    def set_body(self):
        """
        Create the rectangular body and fittings of the sensor
        """

        # initiialization
        h_body = self.h
        w_body = 2/3*h_body
        h_botton = h_body/10
        um = self.um

        body_color = self.body_color
        indication_color = self.indication_color
        w_botton = w_body/7
        h_botton = w_body/4
        r = h_body/100

        body = VGroup()

        #0 main body
        body.add(Rectangle(height=h_body, width=w_body, color=body_color, fill_color=body_color, fill_opacity=1))

        #1 um indication
        body.add(Text(um, color=indication_color).scale(1/(6*h_body)).shift(h_botton/3*UP))

        #2 fittings
        body.add(Rectangle(height=h_body/5, width=w_body/3, color=BLACK, fill_color=BLACK, stroke_width=0, fill_opacity=0.8).next_to(body[0], direction=UP, buff=0))
        body.add(Rectangle(height=h_body/25, width=w_body/3.5, color=BLUE_AUT, fill_color=BLUE_AUT, stroke_width=0, fill_opacity=0.8).next_to(body[-1], direction=UP, buff=0))

        body.add(Rectangle(height=h_body/5, width=w_body/3, color=BLACK, fill_color=BLACK, stroke_width=0, fill_opacity=0.8).next_to(body[0], direction=DOWN, buff=0))
        body.add(Rectangle(height=h_body/25, width=w_body/3.5, color=BLUE_AUT, fill_color=BLUE_AUT, stroke_width=0, fill_opacity=0.8).next_to(body[-1], direction=DOWN, buff=0))

        #6 buttons
        body.add(RoundedRectangle(corner_radius=r, height=h_botton, width=w_botton, color=BLUE_AUT, fill_color=BLUE_AUT, fill_opacity=1).shift(w_body/4*LEFT + h_body/6*DOWN))
        body.add(Arrow(start=h_botton/2*DOWN, end=h_botton/2*UP, max_tip_length_to_length_ratio=0.4, color=GRAY_B, buff=0.1).shift(body[-1].get_center()))
        body.add(Text("A", color=indication_color).scale(h_body/8).next_to(body[-2], direction=DOWN, buff=h_body/20))
        body.add(RoundedRectangle(corner_radius=r, height=h_botton, width=w_botton, color=BLUE_AUT, fill_color=BLUE_AUT, fill_opacity=1).shift(w_body/4*RIGHT + h_body/6*DOWN))
        body.add(Arrow(start=h_botton/2*UP, end=h_botton/2*DOWN, max_tip_length_to_length_ratio=0.4, color=GRAY_B, buff=0.1).shift(body[-1].get_center()))
        body.add(Text("B", color=indication_color).scale(h_body/8).next_to(body[-2], direction=DOWN, buff=h_body/20))

        return body

    # ----------------------------------------------------------------------------------------------------------------------        

    def set_screen(self):
        """
        Create the display of the sensor
        """

        # initiialization
        h = self.body[0].height
        w = self.body[0].width
        h_screen = h/4
        w_screen = w*4/5
        h_display = h/10
        a = w_screen/8
        positions = (3*a, a, -a, -3*a)
        r = h/100
        
        screen = VGroup()
        digits = []
        # screen
        screen.add(RoundedRectangle(corner_radius=r, height=h_screen, width=w_screen, color=BLUE_AUT, fill_color=BLUE_AUT, fill_opacity=1).shift(0.3*h*UP))

        # seven segments display
        for i, pos in enumerate(positions):
            digits.append(dsp7(height=h_display))
            # update screen
            screen.add(digits[i].display)
            # set the position of each display
            screen[1+i].shift(pos*RIGHT + screen[0].get_center())

        return screen, digits
    
    # ----------------------------------------------------------------------------------------------------------------------      

    def update_screen(self, number=0):
        """
        Print the number on the screen
        """

        # initialization
        functions = []

        str_number = str(number)

        # filter the number of the digits from the screen
        start_digit = 0
        free_digits = len(str_number) - len(self.digits)
        
        if free_digits>0:
            start_digit = free_digits
        elif free_digits<0: # reset the digits where there is no numbers
            for j in range(1-free_digits):
                functions.append(self.digits[-j].select_segments(number="R"))
        
        # read only 4 digits and set the single display with the correct digit
        for i, digit in enumerate(reversed(str_number[start_digit:])):
            functions.append(self.digits[i].select_segments(number=int(digit)))

        return functions
    
    # ----------------------------------------------------------------------------------------------------------------------

    def reset_screen(self):
        """
        Reset all the digits of the screen (empty screen)
        """

        functions = []

        for digit in self.digits:
            functions.append(digit.reset_display())
            
        return functions
    
    # ----------------------------------------------------------------------------------------------------------------------

    def get_fitting_TOP(self):
        """
        Get fitting position on top
        """

        # sum chamber center and position of connection
        fitting = self.body[3].get_top() 
        return fitting
    
    # ----------------------------------------------------------------------------------------------------------------------

    def get_fitting_BOTTOM(self):
        """
        Get fitting position on bottom
        """

        # sum chamber center and position of connection
        fitting = self.body[5].get_bottom() 
        return fitting



    
    
    
    
    