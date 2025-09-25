from manim import *
import numpy as np
from numpy import pi
from library.Mechanics.Spring import Compression_Spring as spr

BLU_AUT = "#3349ff"
ROSSO_AUT = "#df0000"
VERDE_AUT = "#76f939"
GIALLO_AUT = "#f3fd17"

"""
Author: Ivan Archetti   
Creation date: 10/09/2025


Collection of python classes about valve actuators
"""

# ======================================================================================================================

class electric_actuator():
    """
    Coil actuator for directional valves
    """

    arguments = {"actuator_stroke_color": GREY_E,
                 "actuator_fill_color": GREY_A}
    
    def __init__(self, position=ORIGIN, height=2, position_side=LEFT, **kwargs):
        # initialization
        self.h = height
        self.w = height
        self.position = position
        self.actuator_stroke_color = self.arguments["actuator_stroke_color"]
        self.actuator_fill_color = self.arguments["actuator_fill_color"]
        
        self.actuator = VGroup()

        self.actuator.add(self.set_coil_actuator(position_side=position_side))

    # ----------------------------------------------------------------------------------------------------------------------        

    def set_coil_actuator(self, position_side=LEFT):
        """
        Drawing the general coil actuator for the valve
        position_side: indicates in which side is the translation
        """
        
        # initialization
        h = self.h
        w = self.w
        position = self.position

        actuator = VGroup()
        actuator.add(Rectangle(width=w, height=h/2, color=self.actuator_stroke_color, fill_color=self.actuator_fill_color, 
                               fill_opacity=0.3).shift(w/2*position_side + h/4*UP))

        actuator.add(Line(start=actuator.get_top()+1/8*w*(-position_side), end=actuator.get_bottom()+1/8*w*position_side, 
                          stroke_width=3, color=BLACK))
        
        # set actuator position respect to the valve
        actuator.shift(position)
        
        return actuator

# ======================================================================================================================

class manual_actuator():
    """
    Manual actuator for directional valves
    """

    arguments = {"actuator_stroke_color": GREY_E,
                 "actuator_fill_color": GREY_A}
    
    def __init__(self, position=ORIGIN, height=2, position_side=LEFT, actuator_type=0, **kwargs):
        # initialization
        self.h = height
        self.w = height
        self.position = position
        self.actuator_stroke_color = self.arguments["actuator_stroke_color"]
        self.actuator_fill_color = self.arguments["actuator_fill_color"]
        
        self.actuator = VGroup()

        self.actuator.add(self.set_manual_actuation(position_side=position_side, actuator_type=actuator_type))

    # ----------------------------------------------------------------------------------------------------------------------

    def set_manual_actuation(self, position_side=LEFT, actuator_type=0):
        """
        Drawing the manual actuation for the valve
        position_side: indicates in which side is the translation
        actuator_type: which type of maual actuation is chosen
        #0 lever hand
        #1 push button
        """
        
        # initialisation
        h = self.h
        w = self.w
        position = self.position

        actuator = VGroup()

        if actuator_type == 0: # lever hand
            a = 4/7
            b = 4/5
            c = 1/10
            r = h/8
            angle = pi/12
            tg = np.tan(angle)
            sin = np.sin(angle)
            cos = np.cos(angle)

            # body of the lever
            actuator.add(Line(start=(a+c*tg)*w*position_side + h*c*UP, end=(a+(1/4+c)*tg)*w*position_side + (c+1/4)*h*UP, color=self.actuator_stroke_color))
            actuator.add(Line(start=ORIGIN, end=((a+(1/4+c)*tg)*w*(-position_side)), color=self.actuator_stroke_color).shift(actuator[0].get_end()))
            actuator.add(Line(start=ORIGIN, end=1/4*h*DOWN, color=self.actuator_stroke_color).shift(actuator[1].get_end()))
            actuator.add(Line(start=actuator[2].get_end(), end=actuator[0].get_start(), color=self.actuator_stroke_color))
            # body lever shade
            points = []
            for i in actuator:
                points.append(i.get_start())
            actuator.add(Polygon(*points, color=self.actuator_stroke_color, fill_color=self.actuator_fill_color, fill_opacity=0.3, stroke_width=0))

            # lever
            actuator.add(Line(start=a*w*position_side, end=(a+b*sin)*h*position_side + cos*b*h*UP, color=self.actuator_stroke_color))
            actuator.add(Circle(radius=r, color=self.actuator_stroke_color, fill_color=self.actuator_fill_color,
                                fill_opacity=0.3).shift((a*w+sin*(b*h+r))*position_side + cos*(b*h+r)*UP))

        elif actuator_type == 1: # bush button
            # main part
            actuator.add(Rectangle(width=w, height=h/4, color=self.actuator_stroke_color, fill_color=self.actuator_fill_color, 
                                   fill_opacity=0.3).shift(w/2*position_side + h/4*UP))
            # lines
            actuator.add(Line(start=1/4*h*UP, end=1/4*h*DOWN, color=self.actuator_stroke_color).shift(w/2*position_side + actuator[0].get_center()))
            actuator.add(Line(start=ORIGIN, end=-w/4*position_side, color=self.actuator_stroke_color).shift(actuator[-1].get_top()))
            actuator.add(Line(start=ORIGIN, end=-w/4*position_side, color=self.actuator_stroke_color).shift(actuator[-2].get_bottom()))
        
        # set actuator position respect to the valve
        actuator.shift(position)
            
        return actuator
    
    # ----------------------------------------------------------------------------------------------------------------------

    def set_push_button_compression(self, motion_direction=RIGHT):
        """
        Show the compression of the push button
        motion_direction: direction of the actuator motion
        """

        # initialization
        w = self.w
        actuator_fill_color = self.actuator_fill_color

        pos = np.sign(self.position[0])
        dir = np.sign(motion_direction[0])
        stretch_factor = 2

        functions = []

        # if valve closes the pneumatic circuit
        if pos*dir < 0:
            fill_color = ROSSO_AUT
            
        # if valve opens the pneumatic circuit
        elif pos*dir > 0:
            fill_color = actuator_fill_color

        functions.append(self.actuator.animate().shift(5/4*w*motion_direction).set_fill(fill_color).stretch(stretch_factor**(pos*dir), dim=0))

        return functions

# ======================================================================================================================

class meccanic_actuator():
    """
    Meccanic actuator for directional valves
    """

    arguments = {"actuator_stroke_color": GREY_E,
                 "actuator_fill_color": GREY_A}
    
    def __init__(self, position=ORIGIN, height=2, position_side=LEFT, actuator_type=0, **kwargs):
        
        # initialization
        self.h = height
        self.w = height
        self.position = position
        self.actuator_stroke_color = self.arguments["actuator_stroke_color"]
        self.actuator_fill_color = self.arguments["actuator_fill_color"]
        
        self.actuator = VGroup()

        self.actuator.add(self.set_meccanic_actuation(position_side=position_side, actuator_type=actuator_type))

    # ----------------------------------------------------------------------------------------------------------------------

    def set_meccanic_actuation(self, position_side=LEFT, actuator_type=0):
        """
        Drawing the meccanic actuation for the valve
        position_side: indicates in which side is the translation
        actuator_type: which type of maual actuation is chosen
        #0 lever
        #1 roller lever
        #2 spring
        """
        
        # initialization
        h = self.h
        w = self.w
        position = self.position

        actuator = VGroup()

        if actuator_type==0: # lever
            a = 1/10
            b = 1/4
            # show the lever
            actuator.add(Line(start=a*h*UP + w*position_side, end=a*h*UP, color=self.actuator_stroke_color))
            actuator.add(Line(start=a*h*UP, end=(a+b)*h*UP, color=self.actuator_stroke_color))
            actuator.add(Line(start=(a+b)*h*UP, end=(a+b)*h*UP + w*position_side, color=self.actuator_stroke_color))
            actuator.add(ArcBetweenPoints(start=(a+b)*h*UP + w*position_side, end=a*h*UP + w*position_side, 
                                          color=self.actuator_stroke_color, radius=-b*h/2*position_side[0]))
            
            # color internal area
            points = []
            for i in actuator:
                points.append(i.get_start())
            actuator.add(Polygon(*points, color=self.actuator_stroke_color, fill_color=self.actuator_fill_color, fill_opacity=0.3, stroke_width=0))

            actuator.add(Polygon(*actuator[3].get_points(), color=self.actuator_stroke_color, 
                                 fill_color=self.actuator_fill_color, fill_opacity=0.3, stroke_width=0))
            
        elif actuator_type==1: # roller lever
            a = 1/10
            b = 1/4
            r = b*h*2/3
            # show the lever
            actuator.add(Line(start=a*h*UP + w*position_side, end=a*h*UP, color=self.actuator_stroke_color))
            actuator.add(Line(start=a*h*UP, end=(a+b)*h*UP, color=self.actuator_stroke_color))
            actuator.add(Line(start=(a+b)*h*UP, end=(a+b)*h*UP + w*position_side, color=self.actuator_stroke_color))
            actuator.add(ArcBetweenPoints(start=(a+b)*h*UP + w*position_side, end=a*h*UP + w*position_side, 
                                          color=self.actuator_stroke_color, radius=r*position_side[0]))
            
            # color internal area
            points = []
            for i in actuator:
                points.append(i.get_start())
            actuator.add(Polygon(*points, color=self.actuator_stroke_color, fill_color=self.actuator_fill_color, fill_opacity=0.3, stroke_width=0))

            # add the roller
            actuator.add(Circle(radius=r, color=self.actuator_stroke_color, fill_color=self.actuator_fill_color, 
                                fill_opacity=0.3).shift((w+r*2/3)*position_side + (a+b/2)*h*UP))
            actuator.add(Dot(radius=h*a*2/3, color=BLACK).shift(actuator[-1].get_center()))

        elif actuator_type==2: # spring
            # initialization of the spring
            spr.arguments["geometric_ratio"] = 1/80
            d_ext = w/3
            n_coils = 10
            height = self.height = 1.2*w
            
            self.spring = spr(color=BLACK, d_ext=d_ext, height=height, n_coils=n_coils, angle=pi/2*position_side[0])
            
            # set the postion respect to the valve
            pos = self.spring.get_spring_legth()*position_side + d_ext/2*UP
            self.spring.spring.shift(pos)
            actuator.add(self.spring.spring)
            
        # set actuator position respect to the valve
        actuator.shift(position)

        return actuator

    # ----------------------------------------------------------------------------------------------------------------------

    def set_spring_compression(self, perc_comp=0.5):
        """
        Set the compression of the actuator spring
        perc_comp: percentage of compression
        """

        return self.spring.set_compression(perc_comp=perc_comp)
        