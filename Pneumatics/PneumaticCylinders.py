from manim import *
import numpy as np
from numpy import pi
from Mlib.Graphics.Colors import *

"""
Author: Ivan Archetti   
Creation date: 09/09/2025


Collection of python classes about pneumatic cylinders and relative methods
"""

# ======================================================================================================================

class Pneumatic_cylinder_double_acting():
    """
    Pneumatic cylinder double acting
    """
    
    arguments = {}
    
    def __init__(self, height=2, width=4, angle=0, **kwargs):
        # initialization of cylinder dimensions
        self.h = height
        self.w = width
        self.angle = angle
        self.r = self.h/20
        self.stroke = self.w-2*self.r # "usefull" stroke
        self.h_offset = self.h/50
        self.w_offset = self.w/12
        self.w_fitting = self.w/40
        self.h_fitting = self.h/10
        self.u = np.array([np.cos(self.angle), np.sin(self.angle), 0.0]) # unit vector of cylinder axis 
        
        self.opened_state = -1 # if self.opened_state is -1 the cylinder is closed
        
        # initialization of cylinder group
        self.cylinder = VGroup()
        
        self.barrel = self.set_barrel()
        
        self.rod_stem = self.set_rod_stem()
        
        self.fittings = self.set_fittings()
        
        self.cylinder.add(self.barrel, self.rod_stem, self.fittings)

        # set orientation
        self.cylinder.rotate(self.angle) 
        # rotate before the elements and then the volume, otherwise will appear the colored areas
        # not in the correct orientation (due to angle)
        
        self.air_area = self.set_air_area()
        
        self.cylinder.add(self.air_area)

# ----------------------------------------------------------------------------------------------------------------------    

    def set_barrel(self):
        """
        Create the external barrel of the cylinder
        """

        barrel = VGroup()
        barrel.add(RoundedRectangle(height=self.h, width=self.w, corner_radius=self.r, color=BLACK))
        return barrel

# ----------------------------------------------------------------------------------------------------------------------    

    def set_rod_stem(self):
        """
        Create the rod and stem of the cylinder
        """

        # initialization
        h = self.h
        w = self.w
        r = self.r
        stroke = self.stroke

        rod_stem = VGroup()
        # head cylinder stem
        rod_stem.add(RoundedRectangle(height=0.99*h, width=w/8, fill_opacity=1, corner_radius=r/2, 
                                      stroke_width=0, color=GREY_C).shift((stroke/2 - w/8)*LEFT))
        # cylinder stem
        rod_stem.add(RoundedRectangle(height=h/5, width=w*0.85, corner_radius=r/2, fill_opacity=1, color=GREY).next_to(rod_stem[-1], direction=RIGHT, buff=0))
        
        return rod_stem

# ----------------------------------------------------------------------------------------------------------------------    

    def set_fittings(self):
        """
        Create fittings of the cylinder (where the air flows in and out)
        """

        #initialization
        h = self.h_fitting
        w = self.w_fitting
        h_offset = self.h_offset
        w_offset = self.w_offset

        fittings = VGroup()
        # fitting 1
        fittings.add(Rectangle(height=h, width=w, fill_opacity=1, color=GREY_B).next_to(self.barrel[0], 
                               direction=UL, buff=0).shift(w_offset*RIGHT + h_offset))
        # fitting 2
        fittings.add(Rectangle(height=h, width=w, fill_opacity=1, color=GREY_B).next_to(self.barrel[0], 
                               direction=UR, buff=0).shift(w_offset*LEFT +h_offset))
        return fittings

# ----------------------------------------------------------------------------------------------------------------------    

    def set_air_area(self):
        """
        Set the blue areas that simulate air flow in the cylinder
        """

        air_area = VGroup()
        # left volume
        air_area.add(self.make_area(LEFT).set_z_index(self.fittings.get_z() - 1))
        # right volume
        air_area.add(self.make_area(RIGHT).set_z_index(self.fittings.get_z() - 1))

        return air_area

# ----------------------------------------------------------------------------------------------------------------------    
    
    def make_area(self, side):
        """
        Procedure to create the dynamic blue area that simulate air flow in the cylinder
        side: where the area must be create (right or left side)
        """

        # initialization
        w = float(self.w)
        h = float(self.h)
        piston_thick = float(self.w/8)

        def updater():
            body_cyl_center = self.barrel[0].get_center()

            # rotated axis cylinder
            u_rot = rotate_vector(RIGHT, self.angle)

            # cylinder axis rotated
            piston_center = self.rod_stem[0].get_center()
            s = float(np.dot(piston_center - body_cyl_center, u_rot))  # coord. lungo asse

            # determination of contact point
            sgn = side[0] 
            s_face = sgn * s + piston_thick / 2
            width_axis = np.clip(w/2 - s_face, 0.0, w)
            center_offset = sgn * (w/2 - width_axis/2)

            # mask dimensions
            Hmask = float(np.hypot(w, h))
            Wmask = max(float(width_axis), 1e-6)

            # create mask (it follows tanslations because body_cyl_center is updated)
            mask_center = body_cyl_center + u_rot * center_offset

            # create mask
            mask = Rectangle(width=Wmask, height=Hmask)
            mask.move_to(mask_center)
            mask.rotate(self.angle)

            # color interpolation
            alpha = float(np.clip(width_axis / w, 0.0, 1.0))
            color = interpolate_color(BLUE_E, BLUE_A, alpha)

            # effective area
            area = Intersection(self.barrel[0], mask)
            area.set_fill(color, opacity=0.6).set_stroke(opacity=0)
            return area

        return always_redraw(updater)

# ----------------------------------------------------------------------------------------------------------------------    
    
    def open_close_cylinder(self, perc_stroke=0.75):
        """
        Actuation of linear movement of the cylinder
        perc_stroke: is the percentage of ideal stroke of linear movement
        """
        
        vertical_stroke = UP*self.u[1]
        horizontal_stroke = RIGHT*self.u[0]

        # switch state position everytime the function is called
        self.opened_state = -self.opened_state

        return self.rod_stem.animate().shift(self.opened_state*self.stroke*perc_stroke*(horizontal_stroke + vertical_stroke))
    
# ----------------------------------------------------------------------------------------------------------------------    

    def switch_updown_fitting_position(self):
        """
        Reverse fitting position from top to bottom or viceversa
        """
        
        for i in range(2):
            self.fittings[i].shift((DOWN*self.u[0] + RIGHT*self.u[1])*(self.h + self.h_fitting + 2*self.h_offset))


# ======================================================================================================================

class Pneumatic_cylinder_single_acting():
    """
    Pneumatic cylinder single acting
    """
    
    arguments = {}
    
    def __init__(self, **kwargs):
        pass