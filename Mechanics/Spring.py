from manim import *
import numpy as np
from numpy import pi

BLU_AUT = "#3349ff"
ROSSO_AUT = "#df0000"
VERDE_AUT = "#76f939"
GIALLO_AUT = "#f3fd17"

"""
Author: Ivan Archetti   
Creation date: 07/09/2025


Collection of python classes of springs
"""


#----------------------------------------------

class Compression_Spring():
    arguments = {"fill_color": GREY_C,
                 "geometric_ratio": 1/20,
                 "scala_lunghezza_libera": 1,
                 "scala_note_secondarie": 0.5}

    def __init__(self, d_ext=1, height=None, coil_angle=None, n_coils=10, angle=0, color=GREY_B,**kwargs):
        # initialization
        # set the minimum number of coils (3 coils) to be a spring
        self.n_coils = np.clip(int(n_coils), 3, None)
        self.coil_angle = coil_angle # angle of the coils respect to the horizontal line
        self.height = height # total height of the spring when is not compressed
        self.d_ext = d_ext
        self.fill_color = self.arguments["fill_color"]
        self.color = color
        self.r = self.d_ext*self.arguments["geometric_ratio"] 
        self.d_coil = self.r*2
        self.angle = angle
        self.u = [np.cos(self.angle), np.sin(self.angle)]

        self.spring = VGroup()
        
        # define the way to create the spring or by coil angle or by height
        if coil_angle != None:
            self.coils = self.set_spring_by_coil_angle(coil_angle=self.coil_angle)
        if height != None:
            self.coils = self.set_spring_by_height(height=self.height)

        self.spring.add(self.coils)
        

    # ----------------------------------------------------------------------------------------------------------------------        

    def set_spring_by_coil_angle(self, coil_angle=pi/10):
        """
        Create the n coils of the spring with n_coils and coil angle (height will be calculated)
        """

        # initialization
        d_coil = self.d_coil
        d_ext = self.d_ext
        angle = self.angle
        n_coils = self.n_coils
        u_coil = self.u_coil = [np.cos(coil_angle), np.sin(coil_angle)]
        d_ext_correct = d_ext/u_coil[0]

        body = VGroup()

        # calculate vertical translation 
        spring_lead = (d_ext_correct/2-d_coil)*u_coil[1]
         
        position = ORIGIN
        
        # create spring body
        for i in range(n_coils):
            if i == 0: # create the spring base
                k = 0
                p = 1
            elif i > 0 and i < n_coils-1 or n_coils == 2: # set hight of the first coil from the base
                k = -1
                p = 2
            elif  i == n_coils-1: # create the last coil
                k = 0
                position = position - spring_lead*UP

            # create coils
            body.add(self.__create_coil().rotate(angle=coil_angle*k).shift(position))
            position = position + p*spring_lead*UP
            coil_angle = -coil_angle
        
            # set color and position for the "frontal" coils 
            if i%2 == 1:
                body[i].set_z_index(body[-1].z_index + 1)
                body[i].set_color(self.color)
                body[i].set_stroke(BLACK)
        
        # rotate the spring respect the base coil
        body.rotate(about_point=body[0].get_center(), angle=angle)

        return body
    
    # ----------------------------------------------------------------------------------------------------------------------        

    def set_spring_by_height(self, height=1):
        """
        Create the n coils of the spring with n_coils and height (coil angle will be calculated)
        height: total height required for the spring
        """
        
        # initialization
        d_coil = self.d_coil
        d_ext = self.d_ext
        n_coils = self.n_coils
        h = height
        
        # height of the spring from the center of base coil and center of last coil
        h_star = h - d_coil

        # calculate the pitch of coil angle and then the coil angle
        spring_lead = h_star/(n_coils-2)
        coil_angle = np.arctan(spring_lead/(d_ext-2*d_coil))

        body = self.set_spring_by_coil_angle(coil_angle=coil_angle)
        self.coil_angle = coil_angle

        return body

    # ----------------------------------------------------------------------------------------------------------------------        

    def __create_coil(self):
        """
        Create a single coil
        """

        d_coil = self.d_coil
        r = self.r
        d_ext = self.d_ext
        fill_color = self.fill_color
        u_coil = self.u_coil

        d_spring = d_ext/u_coil[0]

        coil = RoundedRectangle(corner_radius=r, height=d_coil, width=d_spring-d_coil, 
                                stroke_width=1, stroke_color=fill_color, 
                                fill_color=fill_color, fill_opacity=1, color=BLACK)
        return coil

    # ----------------------------------------------------------------------------------------------------------------------        

    def set_compression(self, shift_position=ORIGIN, perc_comp=0.5):    
        """
        Set the compression of the spring
        perc_comp: percentage of the initial length
        """
        
        # initialization
        coil_angle = self.coil_angle
        d_coil = self.d_coil
        n_coils = self.n_coils
        d_ext = self.d_ext
        u = self.u

        functions = []

        # rescale the new angle ()
        comp_angle = np.arcsin(perc_comp*np.sin(coil_angle))
        # calculate the vertical movement
        translation = (d_ext/2-d_coil)*np.tan(comp_angle) 
        
        # calculate the new position
        position = translation*(u[0]*DOWN + u[1]*RIGHT) + shift_position #************ bisogna muovere anche il primo anello  ************

        # define position of first coil (0)
        functions.append(self.coils[0].animate().shift(shift_position))

        # define position from 1 to n coils
        for i, j in enumerate(self.coils[1:]):
            if i == n_coils - 2: # the last coil has not rotation and different translation
                 comp_angle = 0
                 position = position - translation*(u[0]*DOWN + u[1]*RIGHT) 
                
            functions.append(j.animate().rotate(angle=-comp_angle).shift(position))
            position = position + 2*translation*(u[0]*DOWN + u[1]*RIGHT)
            comp_angle = -comp_angle

        return functions
    
    # ----------------------------------------------------------------------------------------------------------------------        

    def get_spring_legth(self):
        """
        Calculate the total height of the spring
        """
        
        # initialization
        d_coil = self.d_coil
        
        h = self.coils[-1].get_center()[1] - self.coils[0].get_center()[1]
        b = self.coils[-1].get_center()[0] - self.coils[0].get_center()[0]

        hypot = np.hypot(h, b)

        len = d_coil + hypot

        return len
    
    


       