import math
from textwrap import dedent
from kivy.lang import Builder
from kivy3dgui.layout3d import Layout3D
from kivy3dgui.layout3d import Node
from kivy.base import runTouchApp
from kivy.uix.gridlayout import GridLayout
from kivy.app import App


class Minimal3dApp(App):
    
    def build(self):
        #カメラ（視点の向き）
        self.move_camera = True   
        self.cam_distance = 10
        self.super = []
        
        init_dist = []
        rad = 70.0
        azimuth = 0 #0 to 2PI
        polar = 90 #0 to PI
        
        self.m_sx = 0

        x = rad * math.cos(azimuth) * math.sin(polar)                     
        y = rad * math.sin(azimuth) * math.sin(polar)                     
        z = rad * math.cos(polar)

        self.rad = rad
        self.azimuth = azimuth
        self.polar = polar                  
        
        self.layout3d_str = '''
                    #:kivy 1.0
                    #: import Layout3D kivy3dgui.layout3d
                    #: import Animation kivy.animation.Animation
                    
                    Layout3D:  #①光や影の調整など
                        id: board3d
                        #look_at: [0, 0, 10, 0, 0, -20, 0, 1, 0]
                        canvas_size: (1920, 1080)
                        #shadow_offset: 2
                        light_position: [-24.5, 150, 100]
                        #shadow_origin: [-4,  1., -20.]
                        #shadow_target: [-4.01, 0., -23.0]                  
                        #shadow_threshold: 0.3 
                        post_processing: True  

                        shadow_threshold: 0.3 
                        post_processing: True

                        Node:  #手前の壁
                            id: front
                            rotate: (0, 0, 1, 0)
                            scale: (1.0, 1.2, 0.8)
                            translate: (0, 0, -80)
                            min_light_intensity: 1.0
                            receive_shadows: True                            
                            meshes: ("./meshes/2dbox.obj",)
                            Button:
                                id: bottom_floor
                                text: "Player B"
                                font_size: 50
                                background_normal: ''
                                background_color: 0.000 , 0.000 , 0.000, 1.000

                        Node:  #奥の壁
                            id: back
                            rotate: (-180, 0, 1, 0)
                            scale: (1.0, 1.0, 0.8)
                            translate: (0, 0, 80)
                            min_light_intensity: 1.0                          
                            meshes: ("./meshes/2dbox.obj",)
                            Button:
                                id: bottom_floor
                                text: "Player A"
                                font_size: 50
                                background_normal: ''
                                background_color: 0.000 , 0.000 , 0.000, 1.000
                       
                        Node:
                            id: Ball
                            name: 'Node 0'
                            min_light_intensity: 1.0
                            scale: (0.025, 0.025, 0.025)   #ボールの大きさ
                            translate: (0, 0, -0.5)
                            effect: True
                            meshes: ("./data/obj/sphere.obj", ) 
                            Button:
                                canvas:
                                    Color:
                                        rgb: 1.000 ,0.9608 ,0.2980
                                    Rectangle:
                                        size: self.size
                                        pos: self.pos 
                        
                                        
                        Node:
                            id: Net
                            name: 'Node 2'
                            #rotate: (45, 10, 15, 0)
                            scale: (2, 2, 2)
                            translate: (0, 0, 0)
                            effect: True
                            meshes: ("./data/obj/tennis_net.obj",)
                            Button:
                                text: "Hello"
                                canvas:
                                    Color:
                                        rgb: 0.6588 ,0.6588 ,0.7216
                                    Rectangle:
                                        size: self.size
                                        pos: self.pos
                                        Line:
                                            width:10
                                            points: 0, 0, 0, 1

                        Node:
                            id: TennisCourt
                            name: 'Node 1'
                            #rotate: (45, 10, 15, 0)
                            scale: (2, 2, 2)
                            translate: (0, 0, 0)
                            min_light_intensity: 1.0
                            receive_shadows: True 
                            effect: True
                            meshes: ("./data/obj/tennis_court.obj",)
                            Button:
                                canvas:
                                    Color:
                                        rgb: 0.0, 0.6196, 0.321
                                    Rectangle:
                                        size: self.center   
                                        pos: 0, 0
                                        source: "./data/imgs/tenniscourt.jpg"


                        Node:
                            id: CourtLines
                            name: 'Node l'
                            #rotate: (45, 10, 15, 0)
                            scale: (2, 2, 2)
                            translate: (0, 0, 0)
                            #effect: True
                            meshes: ("./data/obj/courtlines.obj",)
                            Button:
                                canvas:
                                    Color:
                                        rgb: 0.000, 0.000, 0.000
                                    Rectangle:
                                        size: self.size
                                        pos: self.pos
                                        Line:
                                            width:10
                                            points: 0, 0, 0, 1
                        
                        Node:
                            id: CourtLines2
                            name: 'Node l2'
                            #rotate: (45, 10, 15, 0)
                            scale: (2, 2, 2)
                            translate: (0, 0, 0)
                            #effect: True
                            meshes: ("./data/obj/courtlines_2.obj",)
                            Button:
                                canvas:
                                    Color:
                                        rgb: 0.000, 0.000, 0.000
                                    Rectangle:
                                        size: self.size
                                        pos: self.pos
                                        Line:
                                            width:10
                                            points: 0, 0, 0, 1

                        

                    '''
        


        layout3d = Builder.load_string(dedent(self.layout3d_str))
        layout3d.bind(on_touch_move = self.on_touch_move)
        self.layout3d = layout3d
        self.baselayout = layout3d
        self.layout3d.f_type = 0
        layout3d.bind(on_motion=self.on_motion)       

        grid = GridLayout(cols=2)
        grid.add_widget(self.layout3d)
        self.grid = grid
        
        return self.grid
        #return layout3d
        

    def _keyboard_released(self, window, keycode):
        self.super = []

    def _keyboard_on_key_down(self, window, keycode, text, super):
        print("Values ", self.super)
        if 'lctrl' in self.super and keycode[1] == 'z':
            #self.super = []
            self.undo()
            return False
        elif 'lctrl' not in self.super:
            self.super.append('lctrl')
            return False
        else:
            self.super = []
            return False    
               
    def on_motion(self, etype, motionevent):
        print(etype)
        pass
    
        

    def get_camera_pos(self):
        rad = self.rad
        azimuth = math.radians(self.azimuth)
        polar = math.radians(self.polar)
        x = rad * math.sin(azimuth) * math.sin(polar)                     
        y = rad * math.cos(polar)
        z = rad * math.cos(azimuth) * math.sin(polar)                               
        return [x, y, z]
        

    def on_button_touch_up(self, *args):
        self.move_camera = True
        
    
        
    def on_touch_move(self, widget, touch):
        if not self.move_camera:
            return True
        polar_angle = (touch.dy / self.layout3d.height) * 360        
        azimuth_angle = (touch.dx / self.layout3d.width) * -360
        
        self.azimuth += azimuth_angle
        self.polar += polar_angle
        if self.polar >= 180:
            self.polar = 180
        if self.polar <= 0:
            self.polar = 0.01
        if self.azimuth >= 360:
           self.azimuth = 0
            
        x,y,z = self.get_camera_pos()
        self.layout3d.look_at = [x, y, z-10, 0, 0, -10, 0, 1, 0]

    
if __name__ == '__main__':
    Minimal3dApp().run()

