from manim import *
import numpy as np
from numpy import pi
from library.Graphics.Colors import *

"""
Author: Ivan Archetti   
Creation date: 19/09/2025


Collection of python classes about displays 
"""


# ======================================================================================================================

class Display_7_segments():  
    """
    Seven segments display
    """

    arguments = {"display_stroke_color": GREY_E,
                 "display_stroke_width": 1,
                 "display_fill_color": GREY_A,
                 "display_on": RED_C,
                 "brightness_ON": 1,
                 "brightness_OFF": 0.1}

    def __init__(self, height=1, **kwargs):

        # initialization
        self.display_stroke_color = self.arguments["display_stroke_color"]
        self.display_stroke_width = self.arguments["display_stroke_width"]
        self.display_fill_color = self.arguments["display_fill_color"]
        self.display_on = self.arguments["display_on"]
        self.brightness_ON = self.arguments["brightness_ON"]
        self.brightness_OFF = self.arguments["brightness_OFF"]
        
        self.h = height
        self.w = height

        self.segment_matrix = self.set_segments_matrix()

        self.display = VGroup()

        self.seven_segments = self.set_seven_segments()

        self.display.add(self.seven_segments)

    # ----------------------------------------------------------------------------------------------------------------------

    def set_seven_segments(self):
        """
        Set the seven segments in order to create a singol display
        """
        
        # initialization
        w = self.w
        a = w/5

        seven_segments = VGroup()
        
        central_segment = self.set_central_segment()
        vertical_segment_UR = self.set_vertical_segment()
        vertical_segment_DR = self.set_vertical_segment()
        vertical_segment_UL = self.set_vertical_segment()
        vertical_segment_DL = self.set_vertical_segment()
        horizontal_segment_UP = self.set_horizontal_segment()
        horizontal_segment_DOWN = self.set_horizontal_segment()

        # add central segment
        seven_segments.add(central_segment)

        # add vertical right segments   
        seven_segments.add(vertical_segment_UR.rotate(pi/2).shift((w/2)*RIGHT + w/2*UP))
        seven_segments.add(vertical_segment_DR.rotate(-pi/2).shift((w/2)*RIGHT + w/2*DOWN).flip())

        # add vertical right segments   
        seven_segments.add(vertical_segment_UL.rotate(pi/2).shift((w/2)*LEFT + w/2*UP).flip())
        seven_segments.add(vertical_segment_DL.rotate(-pi/2).shift((w/2)*LEFT + w/2*DOWN))

        # add horizontal upper
        seven_segments.add(horizontal_segment_UP.shift((w-a*3**(1/2)/4)*UP)) 

        # add horizontal lower
        seven_segments.add(horizontal_segment_DOWN.shift((w-a*3**(1/2)/4)*DOWN).flip(axis=RIGHT))

        return seven_segments

    # ----------------------------------------------------------------------------------------------------------------------

    def set_central_segment(self):
        """
        Definition of the central segment of the display
        """

        # initialization
        display_fill_color = self.display_fill_color
        brightness = self.brightness_OFF

        w = self.w
        a = w/5
        alpha = pi/6
        tan = np.tan(alpha)
        s = w/2 - a*(3**(1/2) - 1.2)
        l = a/(2*tan)

        central_segment = VGroup()

        # points of the segment 
        A = s*RIGHT + a/2*DOWN
        B = (l+s)*RIGHT 
        C = s*RIGHT + a/2*UP
        D = s*LEFT + a/2*UP
        E = (l+s)*LEFT
        F = s*LEFT + a/2*DOWN

        points = [F, A, B, C, D, E, F] # loop of the segment
        
        # filling the segment
        central_segment.add(Polygon(*points, color=display_fill_color, fill_opacity=brightness, stroke_width=0))

        return central_segment

    # ----------------------------------------------------------------------------------------------------------------------

    def set_vertical_segment(self):
        """
        Definition of the central segment of the display
        """

        # initialization
        display_fill_color = self.display_fill_color
        brightness = self.brightness_OFF

        w = self.w
        a = w/5
        alpha = pi/3
        tan = np.tan(alpha)
        s = a*3**(1/2)/2

        v_segment = VGroup()

        # points of the segment 
        A = (w/2-(s-a/2)*tan)*RIGHT
        B = w/2*RIGHT + (s-a/2)*UP 
        C = (w/2-s)*RIGHT + s*UP
        D = (w/2-a/2)*LEFT + s*UP
        E = w/2*LEFT

        points = [E, A, B, C, D, E] # loop of the segment

        # filling the segment
        v_segment.add(Polygon(*points, color=display_fill_color, fill_opacity=brightness, stroke_width=0)).shift(3**(1/2)/4*a*DOWN)

        return v_segment
    
    # ----------------------------------------------------------------------------------------------------------------------

    def set_horizontal_segment(self):
        """
        Definition of the central segment of the display
        """

        # initialization
        display_fill_color = self.display_fill_color
        brightness = self.brightness_OFF

        w = self.w
        a = w/5
        s =  a*3**(1/2)/2

        h_segment = VGroup()

        # points of the segment 
        A = (w/2 - a/2)*RIGHT 
        B = (w/2)*RIGHT + s*UP
        C = (w/2)*LEFT + s*UP
        D = (w/2 - a/2)*LEFT

        points = [D, A, B, C, D] # loop of the segment

        # filling the segment
        h_segment.add(Polygon(*points, color=display_fill_color, fill_opacity=brightness, stroke_width=0)).shift(3**(1/2)/4*a*DOWN)

        return h_segment
    
    # ----------------------------------------------------------------------------------------------------------------------

    def set_segments_matrix(self):
        """
        Matrix that set the segments of the the display
        """

        #     5    
        #   -----
        # 3|     |
        #  |  0  |1 
        #   -----
        # 4|     |
        #  |     |2
        #   -----
        #     6


        # column references    0  1  2  3  4  5  6
        # R = reset all segments
        segments_matrix = {0: (0, 1, 1, 1, 1, 1, 1),
                           1: (0, 1, 1, 0, 0, 0, 0),
                           2: (1, 1, 0, 0, 1, 1, 1),
                           3: (1, 1, 1, 0, 0, 1, 1),
                           4: (1, 1, 1, 1, 0, 0, 0),
                           5: (1, 0, 1, 1, 0, 1, 1),
                           6: (1, 0, 1, 1, 1, 1, 1),
                           7: (0, 1, 1, 0, 0, 1, 0),
                           8: (1 ,1 ,1 ,1, 1, 1, 1),
                           9: (1, 1, 1, 1, 0, 1, 1),
                           "R": (0, 0, 0, 0, 0, 0, 0)}
        
        return segments_matrix
    
    # ----------------------------------------------------------------------------------------------------------------------

    def select_segments(self, number=0):
        """
        Activate the number indicate in number
        """
        
        # initialization
        brightness_ON = self.brightness_ON
        brightness_OFF = self.brightness_OFF

        functions = []
        sequences = self.segment_matrix[number]

        for i, segment in enumerate(sequences):
            if segment == 0:
                segment_color = self.display_fill_color
                brightness = brightness_OFF
            elif segment == 1:
                segment_color = self.display_on
                brightness = brightness_ON 
            functions.append(self.seven_segments[i].animate().set_color(segment_color).set_fill(opacity=brightness))
        
        return functions
    
    # ----------------------------------------------------------------------------------------------------------------------

    def reset_display(self):
        """
        Reset all the segments
        """

        return self.select_segments(number="R")
