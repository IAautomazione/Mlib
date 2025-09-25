from manim import *
from numpy import pi


import Mlib.Pneumatics.PneumaticCylinders as cyl
import Mlib.Pneumatics.DirectionalValves as vls
import Mlib.Mechanics.GeneralConnections as conn
import Mlib.Pneumatics.FunctionalValves as f_vls
import Mlib.Instruments.MeasuringInstruments as m_ins
from Mlib.Graphics.Colors import *




# To watch one of these scenes, run the following:
# python -m manim example_scenes.py SquareToCircle -pl
#
# Use the flat -l for a faster rendering at a lower
# quality.
# Use -s to skip to the end and just save the final frame
# Use the -p to have the animation (or image, if -s was
# used) pop up once done.
# Use -n <number> to skip ahead to the n'th animation of a scene.
# special chars \\\'{a} \\`{e}


#----------------------------------------------
config.background_color = WHITE
config.frame_height = 16
config.frame_width = 9
config.pixel_height = 1600
config.pixel_width = 900


class ScenaShort1(Scene):
    def construct(self):
        
        title1 = Text("Cilindro doppio effetto", color=GREY).scale(1).align_on_border(LEFT, buff=.7).align_on_border(UP, buff=.7)        
        line1 = Underline(title1, color=BLUE_AUT, stroke_width=3, buff=0.05)
        title2 = Text("regolazione velocità", background_stroke_color=WHITE, color=WHITE).scale(0.55).align_on_border(LEFT, buff=.85).align_on_border(UP, buff=1.5)
        rect2 = RoundedRectangle(height=0.4, width=title2.width+1.5, corner_radius=0.1, color=WHITE, fill_opacity=1, stroke_width=0.2).align_on_border(LEFT, buff=.7).align_on_border(UP, buff=1.47)
        rect2.set_color_by_gradient([WHITE, RED_AUT, RED_AUT])

        self.play(Write(title1), Write(line1))
        self.play(FadeIn(rect2, shift=RIGHT), FadeIn(title2, shift=RIGHT))

        # inserisco un cilindro doppio effetto centrale
        cilindro1 = cyl.Pneumatic_cylinder_double_acting(height=2*1.5, width=3*1.5, angle=pi/2)
        cilindro1.switch_updown_fitting_position()
        cilindro1.cylinder.shift(0.5*DOWN)

        cilindro2 = cyl.Pneumatic_cylinder_double_acting(height=2, width=3, angle=pi/2)
        cilindro2.switch_updown_fitting_position()
        cilindro2.cylinder.shift(2*LEFT + 0.5*UP)

        self.play(Write(cilindro1.cylinder))
        self.play(AnimationGroup(cilindro1.open_close_cylinder(perc_stroke=0.75), 
                                 AnimationGroup(Flash(point=cilindro1.barrel[0].get_top() + cilindro1.barrel.width/4*LEFT),
                                                Flash(point=cilindro1.barrel[0].get_top() + cilindro1.barrel.width/4*RIGHT)),
                  run_time=0.8,
                  lag_ratio=0.1))

        self.wait(0.5)
        self.play(AnimationGroup(cilindro1.open_close_cylinder(perc_stroke=0.75), 
                                 AnimationGroup(Flash(point=cilindro1.barrel[0].get_bottom(), flash_radius=0.2)),
                  run_time=0.8,
                  lag_ratio=0.1))

        # sposto il cilindro e aggiungo la valvola 5_2 e i collegamenti
        valvola1 = vls.Pneumatic_valve_5_2(height=1, left_actuator_choice="Push button", right_actuator_choice="Compression spring")
        valvola1.valve.shift(4*DOWN)
        self.wait(0.5)

        self.play(ReplacementTransform(cilindro1.cylinder, cilindro2.cylinder))
        self.wait(0.5)

        tubo1_A = conn.Pipe_connection(pos=cilindro2.fittings[0].get_right(), l_len=[0.69, 2.65], directions=[RIGHT, DOWN], color=BLUE_E)
        tubo2_A = conn.Pipe_connection(pos=cilindro2.fittings[1].get_right(), l_len=[1.19, 5.25], directions=[RIGHT, DOWN], color=BLUE_A)
        input_air1 = Triangle(fill_opacity=0.5, color=BLUE_E).scale(0.1).rotate(pi).next_to(valvola1.get_input_5(chamber=valvola1.right_chamber), direction=DOWN, buff=0.1)
        input_air2 = Triangle(fill_opacity=0.5, color=BLUE_A).scale(0.1).next_to(valvola1.get_input_1(chamber=valvola1.right_chamber), direction=DOWN, buff=0.1)
        input_air3 = Triangle(fill_opacity=0.5, color=BLUE_A).scale(0.1).next_to(valvola1.get_input_3(chamber=valvola1.right_chamber), direction=DOWN, buff=0.1)
        
        self.play(Write(tubo1_A.pipe_connection),
                  Write(tubo2_A.pipe_connection))
        self.wait(0.5)
        self.play(Write(valvola1.valve))
        self.wait(0.5)
        self.play(Write(input_air1),
                  Write(input_air2),
                  Write(input_air3))
        self.wait(1)
        
        # muovo nuovamente il cilindro
        self.play(*valvola1.slide_valve(motion_direction=RIGHT))
        self.play(AnimationGroup(cilindro2.open_close_cylinder(perc_stroke=0.75), 
                                 tubo1_A.pipe_connection.animate().set_color(BLUE_A),
                                 tubo2_A.pipe_connection.animate().set_color(BLUE_E),
                                 input_air1.animate().rotate(pi).set_color(BLUE_A),
                                 input_air3.animate().rotate(pi).set_color(BLUE_E),
                                 AnimationGroup(Flash(point=cilindro2.barrel[0].get_top() + cilindro2.barrel.width/4*LEFT),
                                                Flash(point=cilindro2.barrel[0].get_top() + cilindro2.barrel.width/4*RIGHT)),
                                run_time=0.8,
                                lag_ratio=0.1))
        self.wait()
        self.play(*valvola1.slide_valve(motion_direction=LEFT))
        self.play(AnimationGroup(cilindro2.open_close_cylinder(perc_stroke=0.75),
                                 input_air1.animate().rotate(pi).set_color(BLUE_E),
                                 input_air3.animate().rotate(pi).set_color(BLUE_A),
                                 tubo1_A.pipe_connection.animate().set_color(BLUE_E),
                                 tubo2_A.pipe_connection.animate().set_color(BLUE_A),
                                 AnimationGroup(Flash(point=cilindro2.barrel[0].get_bottom(), flash_radius=0.2)),
                                 run_time=0.8,
                                 lag_ratio=0.1))
        self.wait()

        # modifico il circuito e aggiungo le valvole di regolazione del flusso, prima una poi l'altra
        func_valve1 = f_vls.OneWay_flow_control_valve(height=1.5, flip=1)
        func_valve1.valve.shift(3*DOWN + 0.63*RIGHT)
        func_valve2 = f_vls.OneWay_flow_control_valve(height=1.5, flip=1)
        func_valve2.valve.next_to(func_valve1.valve, direction=RIGHT, buff=0.5)

        self.play(cilindro2.cylinder.animate().shift(UP),
                  VGroup(valvola1.valve, input_air1, input_air2, input_air3).animate().shift(1.5*DOWN),
                  FadeOut(tubo1_A.pipe_connection, tubo2_A.pipe_connection))
        self.play(Write(func_valve1.valve),
                  Write(func_valve2.valve))
        
        # inserisco i nuovi collegamenti e il sensore di portata
        sensoreflusso1 = m_ins.FlowSensor(height=1, um="Flow")
        sensoreflusso1.flowsensor.next_to(func_valve1.get_input_1(), direction=UP, buff=0.4)

        sensoreflusso2 = m_ins.FlowSensor(height=1, um="Flow")
        sensoreflusso2.flowsensor.next_to(func_valve2.get_input_1(), direction=UP, buff=0.4)

        tubo1_A = conn.Pipe_connection(pos=cilindro2.fittings[0].get_right(), l_len=[0.69, 0.55], directions=[RIGHT, DOWN], color=BLUE_E)
        tubo2_A = conn.Pipe_connection(pos=cilindro2.fittings[1].get_right(), l_len=[2.69, 3.12], directions=[RIGHT, DOWN], color=BLUE_A)
        tubo1_B = conn.Pipe_connection(pos=sensoreflusso1.get_fitting_BOTTOM(), l_len=[0.4], directions=[DOWN], color=BLUE_E)
        tubo2_B = conn.Pipe_connection(pos=sensoreflusso2.get_fitting_BOTTOM(), l_len=[0.4], directions=[DOWN], color=BLUE_A)
        tubo1_C = conn.Pipe_connection(pos=func_valve1.get_output_2(), l_len=[1.25], directions=[DOWN], color=BLUE_E)
        tubo2_C = conn.Pipe_connection(pos=func_valve2.get_output_2()+0.03*DOWN, l_len=[0.2, 1.3, 0.8], directions=[DOWN, LEFT, DOWN], color=BLUE_A)

        sotto_titolo1 = Text("Riduzione di flusso\n\rin scarico", line_spacing=-1.1, color=BLACK).scale(0.5).next_to(func_valve1.valve, direction=LEFT, buff=0.6)
        frame_sotto_titolo1 = SurroundingRectangle(sotto_titolo1, corner_radius=0.1, stroke_width=2, color=RED_AUT)
        
        self.play(FadeIn(sensoreflusso1.flowsensor),
                  FadeIn(sensoreflusso2.flowsensor))
        self.play(*sensoreflusso1.update_screen(number=0),
                  *sensoreflusso2.update_screen(number=0))

        self.play(Write(tubo1_A.pipe_connection),
                  Write(tubo2_A.pipe_connection),
                  Write(tubo1_B.pipe_connection),
                  Write(tubo2_B.pipe_connection),
                  Write(tubo1_C.pipe_connection),
                  Write(tubo2_C.pipe_connection))
        
        # primo caso: doppia strozzatura e doppia riduzione di velocità
        self.play(Write(sotto_titolo1),
                  Write(frame_sotto_titolo1))
        
        # evidenzio una valvola funzionale poi l'altra
        opacity = 0.05
        clear_color = LIGHT_GREY_AUT
        func_valve1.valve.save_state()
        func_valve2.valve.save_state()
        self.play(func_valve1.valve[0][:9].animate().set_opacity(opacity),
                  func_valve1.valve[0][9].animate().set_color(clear_color),
                  func_valve1.valve[0][10:13].animate().set_opacity(opacity),
                  func_valve1.valve[0][12:].animate().set_color(clear_color))
        self.wait()
        self.play(Restore(func_valve1.valve),
                  func_valve2.valve[0][:9].animate().set_opacity(opacity),
                  func_valve2.valve[0][9].animate().set_color(clear_color),
                  func_valve2.valve[0][10:13].animate().set_opacity(opacity),
                  func_valve2.valve[0][12:].animate().set_color(clear_color))
        self.wait()
        self.play(Restore(func_valve2.valve))

        # attivo le valvole di regolazione di flusso dell'aria
        self.play(func_valve1.active_choke(active_color=BLUE_E),
                  func_valve1.active_not_return(active=0, closed_color=BLUE_E),
                  func_valve2.active_not_return(active=1, open_color=BLUE_A),)
        #self.wait()

        # azzero la posizione delle valvole funzionali
        self.play(func_valve2.active_not_return(active=-1),
                  func_valve1.active_not_return(active=-1),
                  func_valve1.active_choke(active=-1))
        
        # muovo la valvola direzionale
        self.play(*valvola1.slide_valve(motion_direction=RIGHT))
        
        # modifico l'orientamento degli ingressi
        self.play(input_air1.animate().rotate(pi).set_color(BLUE_A),
                  input_air3.animate().rotate(pi).set_color(BLUE_E))
       
        # muovo il cilindro in maniera più lenta in avanti
        self.play(AnimationGroup(cilindro2.open_close_cylinder(perc_stroke=0.75),
                                 VGroup(tubo1_A.pipe_connection, tubo1_B.pipe_connection, tubo1_C.pipe_connection).animate().set_color(BLUE_A),
                                 VGroup(tubo2_A.pipe_connection, tubo2_B.pipe_connection, tubo2_C.pipe_connection).animate().set_color(BLUE_E),
                                 func_valve1.active_not_return(active=1, open_color=BLUE_A),
                                 func_valve2.active_not_return(active=0, closed_color=BLUE_E),
                                 func_valve2.active_choke(active=1, active_color=BLUE_E),
                                 run_time = 4),
                  AnimationGroup(*sensoreflusso1.update_screen(number=100),
                                 *sensoreflusso2.update_screen(number=100),
                                 run_time = 1)
                  )
        
        # azzero la posizione delle valvole funzionali
        self.play(func_valve1.active_not_return(active=-1),
                  func_valve2.active_not_return(active=-1),
                  func_valve2.active_choke(active=-1),
                  *sensoreflusso1.update_screen(number=0),
                  *sensoreflusso2.update_screen(number=0))
        
        # muovo indietro il cilindro
        self.play(*valvola1.slide_valve(motion_direction=LEFT),
                  input_air1.animate().rotate(pi).set_color(BLUE_E),
                  input_air3.animate().rotate(pi).set_color(BLUE_A))
        
        self.play(AnimationGroup(cilindro2.open_close_cylinder(perc_stroke=0.75),
                                 VGroup(tubo1_A.pipe_connection, tubo1_B.pipe_connection, tubo1_C.pipe_connection).animate().set_color(BLUE_E),
                                 VGroup(tubo2_A.pipe_connection, tubo2_B.pipe_connection, tubo2_C.pipe_connection).animate().set_color(BLUE_A),
                                 func_valve1.active_not_return(active=0, closed_color=BLUE_E),
                                 func_valve2.active_not_return(active=1, open_color=BLUE_A),
                                 func_valve1.active_choke(active=1, active_color=BLUE_E),
                                 run_time = 2),
                  AnimationGroup(*sensoreflusso1.update_screen(number=200),
                                 *sensoreflusso2.update_screen(number=200),
                                 run_time = 2)
                  )
        #self.wait()
        self.play(func_valve1.active_not_return(active=-1, closed_color=BLUE_E),
                  func_valve1.active_choke(active=-1, active_color=BLUE_E),
                  func_valve2.active_not_return(active=-1),
                  *sensoreflusso1.update_screen(number=0),
                  *sensoreflusso2.update_screen(number=0))
        #self.wait()

        # riorganizzo lo schema
        self.play(FadeOut(VGroup(sotto_titolo1, frame_sotto_titolo1), shift=LEFT),
                  FadeOut(sensoreflusso1.flowsensor, shift=LEFT),
                  FadeOut(sensoreflusso2.flowsensor, shift=RIGHT),)
        

        # secondo caso: spinta di sollevamento
        # Riorganizzo tolgo i tubi 
        func_valve3 = f_vls.OneWay_flow_control_valve(height=1.5)
        func_valve3.valve.next_to(func_valve1.valve, direction=UP, buff=0.4)

        massa1 = VGroup()
        massa1.add(RoundedRectangle(width=1.5, height=0.5, corner_radius=0.05, color=GREY_D, fill_opacity=0.9))
        massa1.add(Text("m", color=WHITE).scale(0.5))
        massa1.next_to(cilindro2.rod_stem[1].get_top(), direction=UP, buff=0.04)
        massa1.add_updater(lambda m: m.next_to(cilindro2.rod_stem[1].get_top(), direction=UP, buff=0.04))

        tubo2_D = conn.Pipe_connection(pos=tubo2_A.pipe_connection[-1].get_end(), 
                                       l_len=[tubo2_A.pipe_connection.get_bottom()[1]-tubo2_C.pipe_connection.get_top()[1]], 
                                       directions=[DOWN], color=BLUE_A)
        
        self.play(ReplacementTransform(func_valve2.valve, func_valve3.valve),
                  ReplacementTransform(tubo2_B.pipe_connection, tubo2_D.pipe_connection),
                  FadeIn(massa1, shift=LEFT))
        self.wait()

        # muovo la valvola
        self.play(*valvola1.slide_valve(motion_direction=RIGHT),
                  input_air1.animate().rotate(pi).set_color(BLUE_A),
                  input_air3.animate().rotate(pi).set_color(BLUE_E))
        
        sotto_titolo2 = Text("Regolazione spinta\n\rdi sollevamento", line_spacing=-1.1, 
                             color=BLACK).scale(0.5).next_to(cilindro2.cylinder, direction=DOWN, buff=1.7).shift(0.3*LEFT)
        frame_sotto_titolo2 = SurroundingRectangle(sotto_titolo2, corner_radius=0.1, stroke_width=2, color=RED_AUT)
        
        # apro il cilindro
        self.play(cilindro2.open_close_cylinder(perc_stroke=0.75),
                                 VGroup(tubo1_A.pipe_connection, tubo1_B.pipe_connection, tubo1_C.pipe_connection).animate().set_color(BLUE_A),
                                 VGroup(tubo2_A.pipe_connection, tubo2_B.pipe_connection, tubo2_C.pipe_connection).animate().set_color(BLUE_E),
                                 func_valve1.active_not_return(active=1, open_color=BLUE_A),
                                 func_valve3.active_not_return(active=0, closed_color=BLUE_A),
                                 func_valve3.active_choke(active=1, active_color=BLUE_A),
                                 Write(VGroup(sotto_titolo2, frame_sotto_titolo2)),
                                 run_time = 4)
        


        self.wait(4)
        
   