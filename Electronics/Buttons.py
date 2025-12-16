from manim import *
import numpy as np
from numpy import pi
from Mlib.Graphics.Colors import *

"""
Author: Ivan Archetti   
Creation date: 01/10/2025


Collection of python classes about buttons and commands 
"""


# ======================================================================================================================

class Button_ON_OFF():  
    """
    Button with two state On and OFF
    """

    arguments = {"frame_color": GREY_B,
                 "ON_color": PURE_RED,
                 "OFF_color": RED_E,}

    def __init__(self, radius=1, active=0, tag="", **kwargs):
        """
        active: is the state of activation of the button (0 not activate, 1 activate)
        tag: description under the button
        """

        # initialization
        self.frame_color = self.arguments["frame_color"]
        self.ON_color = self.arguments["ON_color"]
        self.OFF_color = self.arguments["OFF_color"]
        
        self.r = radius
        self.active = active
        self.tag = tag
        
        self.frame_button = self.set_button()

        self.button = VGroup()

        self.button.add(self.frame_button)

    # ----------------------------------------------------------------------------------------------------------------------

    def set_button(self):
        """
        Set the button's frame and structure
        """
        
        # initialization
        r_in = self.r
        r_out = 1.2*self.r
        active = self.active
        
        frame_color = self.frame_color
        ON_color = self.ON_color
        OFF_color = self.OFF_color
        tag = self.tag

        button = VGroup()
        
        #0 external frame
        button.add(Annulus(inner_radius=r_in, outer_radius=r_out, color=frame_color))
        
        #1 internal button
        if active:
            color = ON_color
        else:
            color = OFF_color
        
        button.add(Circle(radius=r_in, color=color, fill_color=color, fill_opacity=0.9))

        #2 add decription tag
        button.add(Text(tag, color=GREY_D).scale(r_in).next_to(button[0], direction=DOWN, buff=r_in/3))
        
        return button

    # ----------------------------------------------------------------------------------------------------------------------

    def activation(self, active=0):
        """
        Set the button's status
        active: is the state of activation of the button (0 not activate, 1 activate) 
        """

        ON_color = self.ON_color
        OFF_color = self.OFF_color

        if active:
            color = ON_color
        else:
            color = OFF_color
            
        return self.frame_button[1].animate().set_color(color)


# ======================================================================================================================

class Button_start(Button_ON_OFF):  
    """
    Start button with two state On and OFF
    """

    def __init__(self, radius=1, active=0, **kwargs):
        tag="start"

        self.arguments["ON_color"] = GREEN_AUT
        self.arguments["OFF_color"] = GREEN_E

        super().__init__(radius=radius, active=active, tag=tag)

# ======================================================================================================================

class Button_stop(Button_ON_OFF):  
    """
    Start button with two state On and OFF
    """

    def __init__(self, radius=1, active=0, **kwargs):
        tag="stop"

        self.arguments["ON_color"] = PURE_RED
        self.arguments["OFF_color"] = RED_E

        super().__init__(radius=radius, active=active, tag=tag)

# ======================================================================================================================