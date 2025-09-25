from manim import *
from numpy import pi
from Mlib.Pneumatics import ValveActuators as vact
from Mlib.Graphics.Colors import *


"""
Author: Ivan Archetti   
Creation date: 09/09/2025


Collection of python classes about pneumatic valves
"""

# ======================================================================================================================
# directional valves
# ======================================================================================================================

class Pneumatic_valve_5_2():
    """
    Pneumtic valve with double chamber and 5 input/output for chamber
    """

    arguments = {"output_reduction": 1/10,
                 "valve_stroke_color": GREY_E,
                 "valve_fill_color": GREY_A,
                 "actuator_fill_color": GREY_D}

    def __init__(self, height=2, left_actuator_choice="Coil", right_actuator_choice="Compression spring",  visible_connections=False, **kwargs):
        """
        left_actuator, right_actuator: tags that determinate the type of actuator
                                       
        """
        
        # initialization
        self.h = height
        self.w = self.h
        self.k = self.h*self.arguments["output_reduction"]        
        self.valve_stroke_color = self.arguments["valve_stroke_color"]
        self.valve_fill_color = self.arguments["valve_fill_color"]
        self.actuator_fill_color = self.arguments["actuator_fill_color"]
        self.left_actuator_choice = left_actuator_choice
        self.right_actuator_choice = right_actuator_choice
         
        self.valve = VGroup()
        
        # initialization left valve chamber
        self.left_chamber = self.set_chamber(connections=((1,4), (2,3), (5,5)), visible_connections=visible_connections)
        self.left_chamber.shift(self.w/2*LEFT)

        # initialization right valve chamber
        self.right_chamber = self.set_chamber(connections=((1,2), (4,5), (3,3)), visible_connections=visible_connections)
        self.right_chamber.shift(self.w/2*RIGHT)

        # define dictionary actuator
        self.dict_act = self.dict_actuator()

        # initialization left actuator
        position_side = LEFT
        position = self.w*position_side + self.h/2*DOWN
        self.left_actuator = self.select_actuator(position_side=position_side, position=position, actuator_type=left_actuator_choice)

        # initialization right actuator
        position_side = RIGHT
        position = self.w*position_side + self.h/2*DOWN
        self.right_actuator = self.select_actuator(position_side=position_side, position=position, actuator_type=right_actuator_choice)

        self.valve.add(self.left_actuator.actuator, self.left_chamber, self.right_chamber, self.right_actuator.actuator)

    # ----------------------------------------------------------------------------------------------------------------------    

    def set_chamber(self, connections=((1,1), (2,2), (3,3), (4,4), (5,5)), visible_connections=False):
        """
        Procedure that initialize internal structure of the chamber

        connection: (x, y) tuple of tuples that show the connection to the inputs and outputs
                    if the connection is an arrow the x is where it begins and y where finishes
                    if x and y are the same there is no connection ("T" fitting)
                    if there is a third number z, is a multiple connection, x and y are the beginning and z the finish
        """

        # initialization
        h = self.h
        valve_stroke_color = self.valve_stroke_color
        valve_fill_color = self.valve_fill_color
        
        # set chamber volume
        chamber = VGroup()
        chamber.add(Rectangle(width=h, height=h, color=valve_stroke_color, fill_color=valve_fill_color, fill_opacity=0.5))

        for connection in connections:
            start, angle = self.get_IN_OUT_positions(connection[0])
            end, angle = self.get_IN_OUT_positions(connection[1])
            # verify if an arrow is required
            if connection[0] != connection[1] and len(connection) == 2:
                chamber.add(Arrow(start=start, end=end, stroke_width=3, max_tip_length_to_length_ratio=0.15, color=BLACK, buff=0))
            # if there is no connection is blocked and add T connections
            elif connection[0] == connection[1]:
                # set T connection when there is no air flow
                T_connection = self.set_T_connection()
                chamber.add(T_connection.shift(start).rotate(about_point=T_connection[0].get_start(), angle=angle))
            # connection for center pressure
            elif connection[0] != connection[1] and len(connection) == 3: 
                point, _ = self.get_IN_OUT_positions(connection[2])
                cp_connection = self.__set_center_pressure_connection(start, end, point)
                chamber.add(cp_connection)

             # add tag numbers to the input outpu valve
            if visible_connections:
                for i in range(1, 6):
                    pos = self.get_IN_OUT_positions(i)[0]
                    if i == 1:
                        pos = pos + h/10*DR
                    elif i == 2:
                        pos = pos + h/10*UR
                    elif i == 3:
                        pos = pos + h/10*DR
                    elif i == 4:
                        pos = pos + h/10*UL
                    elif i == 5:
                        pos = pos + h/10*DL
                    
                    chamber.add(Text(f"{i}", color=BLACK).scale(0.3*h).shift(pos))

        return chamber

    # ----------------------------------------------------------------------------------------------------------------------        

    def get_IN_OUT_positions(self, connection):
        """
        Procedure that defines the connection position
        connection: is a number that identify the position as suggested in the drawing below
        """
        
        # Input and output configuration in a valve chamber (FESTO tags number)
        #|-------------|
        #|  |       |  |
        #|  4       2  |
        #|             |
        #|  5   1   3  |
        #|  |   |   |  |
        #|-------------|
        
        x, y = ORIGIN, ORIGIN
        angle = 0
        if connection == 1:
            x, y = ORIGIN, DOWN/2
        elif connection == 2:
            x, y = RIGHT/4, UP/2
            angle = pi
        elif connection == 3:
            x, y = RIGHT/4, DOWN/2
        elif connection == 4:
            x, y = LEFT/4, UP/2
            angle = pi
        elif connection == 5:
            x, y = LEFT/4, DOWN/2
            
        return (x+y)*self.h, angle
    
    # ----------------------------------------------------------------------------------------------------------------------        

    def set_T_connection(self):
        """
        Drawing the "T" connection
        """
        T_connection = VGroup()
        T_connection.add(Line(start=ORIGIN, end=2*self.k*UP, stroke_width=3, color=BLACK))
        T_connection.add(Line(start=self.k*LEFT, end=self.k*RIGHT, stroke_width=3, color=BLACK).shift(T_connection[0].get_top()))
        return T_connection
    
    # ----------------------------------------------------------------------------------------------------------------------        

    def __set_center_pressure_connection(self, out_point1, out_point2, in_point):
        """
        Drawing the connection in the center pressure configuration
        out_point1/2: points where the line goes out
        in_point: point where the line comes in
        """
        
        # initialization
        h = self.h

        cp_connection = VGroup()
        cp_connection.add(Arrow(start=h/2*DOWN, end=ORIGIN, color=BLACK, max_tip_length_to_length_ratio=0.35,
                                max_stroke_width_to_length_ratio=5, stroke_width=5, buff=0).shift(out_point1))
        cp_connection.add(Arrow(start=h/2*DOWN, end=ORIGIN, color=BLACK, max_tip_length_to_length_ratio=0.35,
                                max_stroke_width_to_length_ratio=5, stroke_width=5, buff=0).shift(out_point2))
        cp_connection.add(Line(start=cp_connection[-2].get_start(), end=cp_connection[-1].get_start(), 
                               stroke_width=3, color=BLACK))
        cp_connection.add(Line(start=cp_connection[-1].get_center(), end=in_point, 
                               stroke_width=3, color=BLACK))
        return cp_connection
    
    # ----------------------------------------------------------------------------------------------------------------------        

    def dict_actuator(self):

        dict_actuator = {"Coil" : 0,
                         "Manual lever" : 1,
                         "Push button" : 2,
                         "Simple lever" : 3,
                         "Roller lever" : 4,
                         "Compression spring" : 5}
        
        return dict_actuator
    
    # ----------------------------------------------------------------------------------------------------------------------

    def select_actuator(self, position_side=LEFT, position=ORIGIN, actuator_type="Coil"):
        """
        Select the actuator type to install to the valve
        position_side: which side must be the actuator
        position: position respect the valve
        actuator_type: what type of actuator
        """

        h = self.h
        n_type = self.dict_act[actuator_type]
        
        if n_type == 0: # coil actuator
           actuator = vact.electric_actuator(position=position, height=h, position_side=position_side)
        elif n_type == 1: # lever
            actuator = vact.manual_actuator(position=position, height=h, position_side=position_side, actuator_type=0)
        elif n_type == 2: # push button
            actuator = vact.manual_actuator(position=position, height=h, position_side=position_side, actuator_type=1)
        elif n_type == 3: # simple lever
            actuator = vact.meccanic_actuator(position=position, height=h, position_side=position_side, actuator_type=0)
        elif n_type == 4: # roller lever
            actuator = vact.meccanic_actuator(position=position, height=h, position_side=position_side, actuator_type=1)
        elif n_type == 5: # spring
            actuator = vact.meccanic_actuator(position=position, height=h, position_side=position_side, actuator_type=2)
        else:
            actuator = VGroup() # empty choice

        return actuator
    
    # ----------------------------------------------------------------------------------------------------------------------        

    def slide_valve(self, motion_direction=RIGHT):
        """
        Procedure that animate the cylinder movement
        side: indicates in which side is the translation
        """

        # initialization
        w = self.w
        left_actuator_choice = self.left_actuator_choice
        right_actuator_choice = self.right_actuator_choice

        functions = []
        
        functions.append(*self.__move_actuator(self.left_actuator, left_actuator_choice, motion_direction))
        functions.append(*self.__move_actuator(self.right_actuator, right_actuator_choice, motion_direction))
            
        # move only the valves except the actuators
        functions.append(self.valve[1:-1].animate().shift(w*motion_direction))
        
        return functions
    
    # ----------------------------------------------------------------------------------------------------------------------

    def __move_spring(self, actuator, motion_direction):
        """
        Procedure that define the compression and movement of the spring
        actuator: right or left actuator spring
        motion_direction: the direction of spring during tha translation
        """
       
        # initialization
        w = self.w
        # k indicate the way of motion and compression respect to the position
        k = motion_direction[0]*actuator.position[0]
        
        len = actuator.spring.height
        d_coil = actuator.spring.d_coil
        
        # calculate the compression factor with the original length (height) of the spring
        compression = k*(w+4*d_coil)/len
        
        return actuator.set_spring_compression(perc_comp=compression)
    
    # ----------------------------------------------------------------------------------------------------------------------

    def __move_actuator(self, actuator, actuator_choice, motion_direction):
        """
        Procedure that collects the movement of the actuators during the valve shifting
        actuator: actuator class
        actuator_choice: number taht define the actuator type (electric, mechanic, etc etc...)
        motion_direction: direction of movement (left/right)
        """
        
        # initialization
        w = self.w
        dict_act = self.dict_act

        functions = []

        # select the right or left actuator
        if np.sign(actuator.position[0]) == -1:
            pos = 0 # left
        elif np.sign(actuator.position[0]) == 1:
            pos = -1 # right

        # select the actuator in order to show the correct movement (translation compression, etc etc...)
        if dict_act[actuator_choice] == 5: # Compression spring
            functions.append(self.__move_spring(actuator, w*motion_direction))
        elif dict_act[actuator_choice] == 2: # Push button
            functions.append(actuator.set_push_button_compression(motion_direction=motion_direction))
        else: # translation for the other actuators
            functions.append(self.valve[pos].animate().shift(w*motion_direction))

        return functions
    
    # ----------------------------------------------------------------------------------------------------------------------

    def get_input_1(self, chamber):
        """
        Get input number 1 of the valve (FESTO numeration)
        """

        # sum chamber center and position of connection
        input_1 = chamber[0].get_center() + self.get_IN_OUT_positions(connection=1)[0]
        return input_1
    
    # ----------------------------------------------------------------------------------------------------------------------

    def get_input_3(self, chamber):
        """
        Get input number 3 of the valve (FESTO numeration)
        """

        # sum chamber center and position of connection
        input_3 = chamber[0].get_center() + self.get_IN_OUT_positions(connection=3)[0]
        return input_3
    
    # ----------------------------------------------------------------------------------------------------------------------

    def get_input_5(self, chamber):
        """
        Get input number 5 of the valve (FESTO numeration)
        """

        # sum chamber center and position of connection
        input_5 = chamber[0].get_center() + self.get_IN_OUT_positions(connection=5)[0]
        return input_5


# ======================================================================================================================


class Pneumatic_valve_5_3(Pneumatic_valve_5_2):
    """
    Pneumatic valve with triple chamber and 5 input/output for chamber
    """

    def __init__(self, height=2, center_selection=0, left_actuator_choice="Coil", right_actuator_choice="Compression spring", 
                 visible_connections=False, **kwargs):
        
        # initialization
        super().__init__(height=height, left_actuator_choice=left_actuator_choice, right_actuator_choice=right_actuator_choice, 
                         visible_connections=visible_connections)
        
        h = self.h
        
        # create the space between left and right chamber to draw valve 5/3 from valve 5/2
        self.valve[0:2].shift(1/2*h*LEFT)
        self.valve[2:4].shift(1/2*h*RIGHT)

        # initialization central chamber
        if center_selection == 0:
            # center open
            self.central_chamber = self.set_chamber(connections=((5,4), (1,1), (3,2)), visible_connections=visible_connections)
        elif center_selection == 1:
            # center closed
            self.central_chamber = self.set_chamber(connections=((1,1), (2,2), (3,3), (4,4), (5,5)), visible_connections=visible_connections)
        else:
            # center pressure
            self.central_chamber = self.set_chamber(connections=((3,3), (5,5), (4,2,1)), visible_connections=visible_connections)

        self.valve.insert(2, self.central_chamber)




    






                







