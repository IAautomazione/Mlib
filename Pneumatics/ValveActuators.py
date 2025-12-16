from manim import *
import numpy as np
from numpy import pi
from Mlib.Mechanics.Spring import Compression_Spring as spr
from Mlib.Graphics.Colors import *


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
    
    def __init__(self, position=ORIGIN, height=2, position_side=LEFT, actuator_type=0, actuated=False, **kwargs):
        # initialization
        self.h = height
        self.w = height
        self.position = position
        self.actuator_stroke_color = self.arguments["actuator_stroke_color"]
        self.actuator_fill_color = self.arguments["actuator_fill_color"]
        
        self.actuator = VGroup()

        self.actuator.add(self.set_coil_actuator(position_side=position_side))

        # initialization of actuator status (compressed or not)
        if actuated:
            self.actuation_init(actuator_type=actuator_type)

    # ----------------------------------------------------------------------------------------------------------------------

    def create_coil(self, position_side=LEFT):
        """
        create coil actuator
        position_side: indicates in which side is the translation
        """

        # initialization
        h = self.h
        w = self.w
        stroke_width = 2*h

        coil = VGroup()
        coil.add(Rectangle(width=w, height=h/2, color=self.actuator_stroke_color, stroke_width=stroke_width,
                               fill_color=self.actuator_fill_color, fill_opacity=0.3).shift(w/2*position_side + h/4*UP))

        coil.add(Line(start=coil.get_top()+1/8*w*(-position_side), end=coil.get_bottom()+1/8*w*position_side, 
                          stroke_width=stroke_width, color=BLACK))
        
        return coil

    # ----------------------------------------------------------------------------------------------------------------------        

    def set_coil_actuator(self, position_side=LEFT, actuator_type=0, animated=True):
        """
        Drawing the general coil actuator for the valve
        position_side: indicates in which side is the translation
        """
        
        # initialization
        position = self.position
        
        actuator = VGroup()

        if actuator_type == 0: # lever hand
            actuator = self.create_coil(position_side=position_side)
        
        # set actuator position respect to the valve
        actuator.shift(position)
        
        return actuator
    
    # ----------------------------------------------------------------------------------------------------------------------

    def actuation_init(self, actuator_type=0):
        """
        Defines the actuation status (compressed or not compressed)
        actuator_type: which type of actuation is chosen
        """

        if actuator_type==0: # coil
            self.set_coil_actuator(animated=False)
            
        elif actuator_type==1: 
            pass

# ======================================================================================================================

class manual_actuator():
    """
    Manual actuator for directional valves
    """

    arguments = {"actuator_stroke_color": GREY_E,
                 "actuator_fill_color": GREY_A}
    
    def __init__(self, position=ORIGIN, height=2, position_side=LEFT, actuator_type=0, actuated=False, **kwargs):
        # initialization
        self.h = height
        self.w = height
        self.position = position
        self.actuator_stroke_color = self.arguments["actuator_stroke_color"]
        self.actuator_fill_color = self.arguments["actuator_fill_color"]
        
        self.actuator = VGroup()

        self.actuator.add(self.set_manual_actuation(position_side=position_side, actuator_type=actuator_type))

        # initialization of actuator status (compressed or not)
        if actuated:
            self.actuation_init(actuator_type=actuator_type)

    # ----------------------------------------------------------------------------------------------------------------------

    def create_manual_lever(self, position_side=LEFT):
        """
        create lever hand actuator
        position_side: indicates in which side is the translation
        """

        # initialisation
        h = self.h
        w = self.w
        stroke_width = 2*h

        a = 4/7
        b = 4/5
        c = 1/10
        r = h/8
        angle = pi/12
        tg = np.tan(angle)
        sin = np.sin(angle)
        cos = np.cos(angle)

        lever = VGroup()

        # body of the lever
        lever.add(Line(start=(a+c*tg)*w*position_side + h*c*UP, end=(a+(1/4+c)*tg)*w*position_side + (c+1/4)*h*UP, 
                            color=self.actuator_stroke_color, stroke_width=stroke_width))
        lever.add(Line(start=ORIGIN, end=((a+(1/4+c)*tg)*w*(-position_side)), color=self.actuator_stroke_color, 
                            stroke_width=stroke_width).shift(lever[0].get_end()))
        lever.add(Line(start=ORIGIN, end=1/4*h*DOWN, color=self.actuator_stroke_color, 
                            stroke_width=stroke_width).shift(lever[1].get_end()))
        lever.add(Line(start=lever[2].get_end(), end=lever[0].get_start(), 
                            color=self.actuator_stroke_color, stroke_width=stroke_width))
        # body lever shade
        points = []
        for i in lever:
            points.append(i.get_start())
        lever.add(Polygon(*points, color=self.actuator_stroke_color, fill_color=self.actuator_fill_color, fill_opacity=0.3, stroke_width=0))

        # lever
        lever.add(Line(start=a*w*position_side, end=(a+b*sin)*h*position_side + cos*b*h*UP, color=self.actuator_stroke_color, stroke_width=stroke_width))
        lever.add(Circle(radius=r, color=self.actuator_stroke_color, stroke_width=stroke_width, fill_color=self.actuator_fill_color, 
                            fill_opacity=0.3).shift((a*w+sin*(b*h+r))*position_side + cos*(b*h+r)*UP))
        
        return lever

    # ----------------------------------------------------------------------------------------------------------------------

    def create_push_button(self, position_side=LEFT):
        """
        create lever actuator
        position_side: indicates in which side is the translation
        """

        # initialisation
        h = self.h
        w = self.w
        stroke_width = 2*h

        push_button = VGroup()

        # main part
        push_button.add(Rectangle(width=w, height=h/4, color=self.actuator_stroke_color, stroke_width=stroke_width, 
                                fill_color=self.actuator_fill_color, fill_opacity=0.3).shift(w/2*position_side + h/4*UP))
        # lines
        push_button.add(Line(start=1/4*h*UP, end=1/4*h*DOWN, color=self.actuator_stroke_color, stroke_width=stroke_width).shift(w/2*position_side + push_button[0].get_center()))
        push_button.add(Line(start=ORIGIN, end=-w/4*position_side, color=self.actuator_stroke_color, stroke_width=stroke_width).shift(push_button[-1].get_top()))
        push_button.add(Line(start=ORIGIN, end=-w/4*position_side, color=self.actuator_stroke_color, stroke_width=stroke_width).shift(push_button[-2].get_bottom()))

        return push_button

    # ----------------------------------------------------------------------------------------------------------------------

    def set_manual_actuation(self, position_side=LEFT, actuator_type=0):
        """
        Drawing the manual actuation for the valve
        position_side: indicates in which side is the translation
        actuator_type: which type of maual actuation is chosen
        #0 manual lever
        #1 push button
        """
        
        # initialisation
        position = self.position

        actuator = VGroup()

        if actuator_type == 0: # lever hand
            actuator = self.create_manual_lever(position_side=position_side)

        elif actuator_type == 1: # push button
            actuator = self.create_push_button(position_side=position_side)
        
        # set actuator position respect to the valve
        actuator.shift(position)
            
        return actuator
    
    # ----------------------------------------------------------------------------------------------------------------------

    def actuation_init(self, actuator_type=0):
        """
        Defines the actuation status (compressed or not compressed)
        actuator_type: which type of actuation is chosen
        """

        if actuator_type==0: # lever hand
            print('"set_lever_hand_compression" Must be developed yet!!!')
            
        elif actuator_type==1: # push button
            self.set_push_button_compression(animated=False)
            
            
    # ----------------------------------------------------------------------------------------------------------------------

    def set_push_button_compression(self, motion_direction=RIGHT, animated=True, run_time=1):
        """
        Show the compression of the push button
        motion_direction: direction of the actuator motion
        animated: a flag that define whether is in animation mode or in static mode
        """

        # initialization
        w = self.w
        actuator_fill_color = self.actuator_fill_color

        pos = np.sign(self.position[0])
        dir = np.sign(motion_direction[0])
        stretch_factor = 2

        functions = []

        # if valve closes the pneumatic circuit
        if np.sign(pos*dir) < 0:
            fill_color = RED_AUT
            
        # if valve opens the pneumatic circuit
        elif np.sign(pos*dir) > 0:
            fill_color = actuator_fill_color

        if animated:
            functions.append(self.actuator[0][0].animate(run_time=run_time).shift(5/4*w*motion_direction).set_fill(fill_color).stretch(stretch_factor**(pos*dir), dim=0))
            functions.append(self.actuator[0][1:].animate(run_time=run_time).shift(6/4*w*motion_direction).set_fill(fill_color))
        else:
            functions.append(self.actuator[0][0].shift(-1/4*w*motion_direction*pos).set_fill(RED_AUT).stretch(1/stretch_factor, dim=0))
            functions.append(self.actuator[0][1:].shift(-2/4*w*motion_direction*pos))

        return functions

# ======================================================================================================================

class mechanic_actuator():
    """
    Meccanic actuator for directional valves
    """

    arguments = {"actuator_stroke_color": GREY_E,
                 "actuator_fill_color": GREY_A}
    
    def __init__(self, position=ORIGIN, height=2, position_side=LEFT, actuator_type=0, actuated=False, **kwargs):
        
        # initialization
        self.h = height
        self.w = height
        self.position = position
        self.actuated = actuated
        self.position_side = position_side
        self.actuator_stroke_color = self.arguments["actuator_stroke_color"]
        self.actuator_fill_color = self.arguments["actuator_fill_color"]
        
        self.actuator = VGroup()

        self.actuator.add(self.set_mechanic_actuation(position_side=position_side, actuator_type=actuator_type))

        # initialization of actuator status (compressed or not)
        if actuated:
            self.actuation_init(actuator_type=actuator_type)

    # ----------------------------------------------------------------------------------------------------------------------

    def create_lever(self, position_side=LEFT):
        """
        create lever actuator
        position_side: indicates in which side is the translation
        """

        h = self.h
        w = self.w
        stroke_width = 2*h

        lever = VGroup()

        a = 1/10
        b = 1/4
        # show the lever
        lever.add(Line(start=a*h*UP + w*position_side, end=a*h*UP, color=self.actuator_stroke_color, stroke_width=stroke_width))
        lever.add(Line(start=a*h*UP, end=(a+b)*h*UP, color=self.actuator_stroke_color, stroke_width=stroke_width))
        lever.add(Line(start=(a+b)*h*UP, end=(a+b)*h*UP + w*position_side, color=self.actuator_stroke_color, stroke_width=stroke_width))
        lever.add(ArcBetweenPoints(start=(a+b)*h*UP + w*position_side, end=a*h*UP + w*position_side, 
                                        color=self.actuator_stroke_color, radius=-b*h/2*position_side[0], stroke_width=stroke_width))
        
        # color internal area
        points = []
        for i in lever:
            points.append(i.get_start())
        lever.add(Polygon(*points, color=self.actuator_stroke_color, fill_color=self.actuator_fill_color, fill_opacity=0.3, stroke_width=0))

        lever.add(Polygon(*lever[3].get_points(), color=self.actuator_stroke_color, 
                           fill_color=self.actuator_fill_color, fill_opacity=0.3, stroke_width=0))
        
        return lever
    
    # ----------------------------------------------------------------------------------------------------------------------

    def create_roller_lever(self, position_side=LEFT):
        """
        Create roller lever actuator
        position_side: indicates in which side is the translation
        """
        
        h = self.h
        w = self.w
        stroke_width = 2*h

        roller_lever = VGroup()

        a = 1/10
        b = 1/4
        r = b*h*2/3
        # show the lever
        roller_lever.add(Line(start=a*h*UP + w*position_side, end=a*h*UP, color=self.actuator_stroke_color, stroke_width=stroke_width))
        roller_lever.add(Line(start=a*h*UP, end=(a+b)*h*UP, color=self.actuator_stroke_color, stroke_width=stroke_width))
        roller_lever.add(Line(start=(a+b)*h*UP, end=(a+b)*h*UP + w*position_side, color=self.actuator_stroke_color, stroke_width=stroke_width))
        roller_lever.add(ArcBetweenPoints(start=(a+b)*h*UP + w*position_side, end=a*h*UP + w*position_side, 
                                        color=self.actuator_stroke_color, radius=r*position_side[0], stroke_width=stroke_width))
        
        # color internal area
        points = []
        for i in roller_lever:
            points.append(i.get_start())
        roller_lever.add(Polygon(*points, color=self.actuator_stroke_color, fill_color=self.actuator_fill_color, fill_opacity=0.3, stroke_width=0))

        # add the roller
        roller_lever.add(Circle(radius=r, color=self.actuator_stroke_color, stroke_width=stroke_width, 
                            fill_color=self.actuator_fill_color, fill_opacity=0.3).shift((w+r*2/3)*position_side + (a+b/2)*h*UP))
        roller_lever.add(Dot(radius=h*a*2/3, color=BLACK).shift(roller_lever[-1].get_center()))

        return roller_lever
    
    # ----------------------------------------------------------------------------------------------------------------------

    def create_spring(self, position_side=LEFT):
        """
        Procedure that defines the compression and movement of the spring
        position_side: indicates in which side is the translation
        """

        w = self.w
        self.len_spring_factor = 1.2
        
        # initialization of the spring
        spr.arguments["geometric_ratio"] = 1/80
        d_ext = w/3
        n_coils = 10
        height = self.height = self.len_spring_factor*w
        
        spring = spr(color=BLACK, d_ext=d_ext, height=height, n_coils=n_coils, angle=pi/2*position_side[0])

        # set the postion respect to the valve
        pos = spring.get_spring_legth()*position_side + d_ext/2*UP
        spring.spring.shift(pos)
        
        return spring
    
    # ----------------------------------------------------------------------------------------------------------------------

    def set_mechanic_actuation(self, position_side=LEFT, actuator_type=0):
        """
        Initializes the mechanic actuation for the valve
        position_side: indicates in which side is the translation
        actuator_type: which type of actuation is chosen
        #0 lever
        #1 roller lever
        #2 spring
        """
        
        # initialization
        position = self.position

        actuator = VGroup()

        if actuator_type==0: # lever
            actuator = self.create_lever(position_side=position_side)
            
        elif actuator_type==1: # roller lever
            actuator = self.create_roller_lever(position_side=position_side)

        elif actuator_type==2: # spring
            self.spring = self.create_spring(position_side=position_side)
            actuator = self.spring.spring
            
        # set actuator position respect to the valve
        actuator.shift(position)

        return actuator
    
    # ----------------------------------------------------------------------------------------------------------------------

    def actuation_init(self, actuator_type=0):
        """
        Defines the actuation status (compressed or not compressed)
        actuator_type: which type of actuation is chosen
        """

        if actuator_type==0: # lever
            print('"set_lever_compression" Must be developed yet!!!')
            
        elif actuator_type==1: # roller lever
            self.set_roller_lever_compression(animated=False)
            
        elif actuator_type==2: # spring
            self.set_spring_compression(animated=False)
            
    # ----------------------------------------------------------------------------------------------------------------------

    def set_roller_lever_compression(self, motion_direction=RIGHT, animated=True, run_time=1):
        """
        Show the compression of the roller lever
        motion_direction: direction of the actuator motion
        animated: a flag that define whether is in animation mode or in static mode
        """

        # initialization
        w = self.w
        actuator_fill_color = self.actuator_fill_color

        pos = np.sign(self.position[0])
        dir = np.sign(motion_direction[0])
        stretch_factor = 2

        functions = []

        # if valve closes the pneumatic circuit
        if np.sign(pos*dir) < 0:
            fill_color = RED_AUT
            
        # if valve opens the pneumatic circuit
        elif np.sign(pos*dir) > 0:
            fill_color = actuator_fill_color

        if animated:
            # animated compression
            functions.append(self.actuator[0][0:3].animate(run_time=run_time).shift(5/4*w*motion_direction).stretch(stretch_factor**(np.sign(pos*dir)), dim=0))
            functions.append(self.actuator[0][3].animate(run_time=run_time).shift((5/4 + 1/(2*stretch_factor))*w*motion_direction))
            functions.append(self.actuator[0][4].animate(run_time=run_time).shift(5/4*w*motion_direction).stretch(stretch_factor**(pos*dir), dim=0))
            functions.append(self.actuator[0][5].animate(run_time=run_time).shift((5/4 + 1/(2*stretch_factor))*w*motion_direction).set_fill(fill_color))
            functions.append(self.actuator[0][6].animate(run_time=run_time).shift((5/4+ 1/(2*stretch_factor))*w*motion_direction))
        else:
            # not animated compression
            self.actuator[0][0:3].shift(pos*1/4*w*LEFT).stretch(1/stretch_factor, dim=0)
            self.actuator[0][3].shift(pos*(1/4 + 1/(2*stretch_factor))*w*LEFT)
            self.actuator[0][4].shift(pos*1/4*w*LEFT).stretch(1/stretch_factor, dim=0)
            self.actuator[0][5].shift(pos*(1/4 + 1/(2*stretch_factor))*w*LEFT).set_fill(RED_AUT)
            self.actuator[0][6].shift(pos*(1/4+ 1/(2*stretch_factor))*w*LEFT)

        return functions

    # ----------------------------------------------------------------------------------------------------------------------

    def set_spring_compression(self, motion_direction=RIGHT, animated=True, run_time=1):
        """
        Set the compression of the actuator spring
        perc_comp: percentage of compression
        animated: a flag that define whether is in animation mode or in static mode
        """

        # initialization
        w = self.height
        d_coil = self.spring.d_coil
        
        # k indicate the way of motion and compression respect to the position
        if animated:
            k = np.sign(motion_direction[0]*self.position[0])
        else:
            k = 1
            self.spring.spring.shift(-w/self.len_spring_factor*self.position_side)
        
        # calculate the compression factor with the original length (height) of the spring
        compression = k*(w/self.len_spring_factor + 4*d_coil)/w

        return self.spring.set_compression(perc_comp=compression, animated=animated, run_time=run_time)

# ======================================================================================================================

class pneumatic_actuator():
    """
    Pneumatic actuator for directional valves
    """

    arguments = {"actuator_stroke_color": GREY_E,
                 "actuator_fill_color": GREY_A}
    
    def __init__(self, position=ORIGIN, height=2, position_side=LEFT, actuator_type=0, actuated=False, **kwargs):
        
        # initialization
        self.h = height
        self.w = height
        self.position = position
        self.actuator_stroke_color = self.arguments["actuator_stroke_color"]
        self.actuator_fill_color = self.arguments["actuator_fill_color"]
        self.actuated = actuated
        self.status = -1 # flag that defines the actuator status
        
        self.actuator = VGroup()

        self.actuator.add(self.set_pneumatic_actuation(position_side=position_side, actuator_type=0))

        # initialization of actuator status (compressed or not)
        if actuated:
            self.actuation_init(actuator_type=actuator_type)

    # ----------------------------------------------------------------------------------------------------------------------

    def create_pneumatic_signal(self, position_side=LEFT):
        """
        Procedure that defines the compression and movement of the spring
        position_side: indicates in which side is the translation
        """

        # initialization
        h = self.h
        stroke_width = 2*h
        scale_factor = h/5
        actuator_fill_color = self.actuator_fill_color
        actuator_stroke_color = self.actuator_stroke_color

        signal = VGroup()

        # set rotation of triangle
        if position_side[0] == 1:
            rotation = pi/6 + pi
        else:
            rotation = pi/6 

        signal.add(Line(start=ORIGIN, end=h/3*position_side, color=actuator_stroke_color, stroke_width=stroke_width))
        signal.add(Triangle(color=BLACK, stroke_width=stroke_width, fill_color=actuator_fill_color,
                                fill_opacity=0.3).scale(scale_factor).rotate(rotation).next_to(signal[-1], direction=position_side, buff=0))
        signal.add(Line(start=ORIGIN, end=h/6*position_side, color=BLACK, stroke_width=stroke_width).next_to(signal[-1], direction=position_side, buff=0))

        return signal

    # ----------------------------------------------------------------------------------------------------------------------

    def set_pneumatic_actuation(self, position_side=LEFT, actuator_type=0, animated=True):
        """
        Drawing the pneumatic actuation for the valve
        position_side: indicates in which side is the translation
        actuator_type: which type of actuation is chosen
        #0 signal
        """
        
        # initialization
        h = self.h
        position = self.position

        actuator = VGroup()

        if actuator_type==0: # signal
            actuator = self.create_pneumatic_signal(position_side=position_side)

        actuator.shift(position + h/3*UP)

        return actuator
    
    # ----------------------------------------------------------------------------------------------------------------------
    
    def actuation_init(self, actuator_type=0):
        """
        Defines the actuation status (compressed or not compressed)
        actuator_type: which type of actuation is chosen
        """

        if actuator_type==0: # pneumatic signal
            self.set_pneumatic_signal_compression(animated=False)
            
        elif actuator_type==1: 
            pass

    def set_pneumatic_signal_compression(self, motion_direction=RIGHT, animated=True, run_time=1):
        """
        Show the compression (atuation) of pneumatic signal
        motion_direction: direction of the actuator motion
        animated: a flag that define whether is in animation mode or in static mode
        """

        #initialization
        w = self.w
        functions = []

        if self.status==-1:
            color = RED_AUT
        elif self.status==1:
            color = self.actuator_fill_color


        if animated:
            functions.append(self.actuator[0][0].animate(run_time=run_time).shift(w*motion_direction))
            functions.append(self.actuator[0][1].animate(run_time=run_time).shift(w*motion_direction).set_color(color))
            functions.append(self.actuator[0][2].animate(run_time=run_time).shift(w*motion_direction))
        else:
            functions.append(self.actuator[0][1].set_color(RED_AUT))

        self.status = -self.status

        return functions

# ======================================================================================================================