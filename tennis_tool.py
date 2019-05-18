import math
from textwrap import dedent
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy3dgui.layout3d import Layout3D
from kivy3dgui.layout3d import Node
import sys
import numpy as np
from kivy.base import runTouchApp
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.animation import Animation
from kivy.app import App
import codecs
import csv

sys.setrecursionlimit(100000)


#---------------------------ボールの座標データの調整--------------------------

W_mat = np.zeros((0, 3))
W_bounce_pos = np.zeros((0, 3))

L_mat = np.zeros((0, 3))
L_bounce_pos = np.zeros((0, 3))

FILENAME_W_tr = './ball_data/win_trj.csv'   #軌跡
FILENAME_W_bc = './ball_data/win_bnc.csv'   #バウンド

FILENAME_L_tr = './ball_data/lose_trj.csv'  #軌跡
FILENAME_L_bc = './ball_data/lose_bnc.csv'  #バウンド


with codecs.open(FILENAME_W_tr,encoding = "utf-8") as f:
            reader = csv.reader(f)
            #header = next(reader)  # ヘッダーを読み飛ばしたい時
            
            for row in reader:
                a = np.array([float(row[3]), float(row[2]), float(row[1])])
                W_mat = np.r_[W_mat,a.reshape(1,-1)]

with codecs.open(FILENAME_W_bc,encoding = "utf-8") as f:
            reader = csv.reader(f)
            #header = next(reader)  # ヘッダーを読み飛ばしたい時
            
            for row in reader:
                if row[7] != '':                    
                    a = np.array([float(row[7]), 0, float(row[8])])
                    W_bounce_pos = np.r_[W_bounce_pos,a.reshape(1,-1)]

with codecs.open(FILENAME_L_tr,encoding = "utf-8") as f:
            reader = csv.reader(f)
            #header = next(reader)  # ヘッダーを読み飛ばしたい時
            
            for row in reader:
                a = np.array([float(row[3]), float(row[2]), float(row[1])])
                L_mat = np.r_[L_mat,a.reshape(1,-1)]


with codecs.open(FILENAME_L_bc,encoding = "utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)  # ヘッダーを読み飛ばしたい時
            
            for row in reader:
                if row[7] != '':                    
                    a = np.array([float(row[7]), 0, float(row[8])])
                    L_bounce_pos = np.r_[L_bounce_pos,a.reshape(1,-1)]

#----------------------------------------------------------------------------

#---------------------アニメーションの動きを変数に格納する------------------------

W_animate = Animation(translate=(W_mat[0][0]*2,W_mat[0][1]*2,W_mat[0][2]*2))
i = 1
while i < len(W_mat):
    W_animate += Animation(translate=(W_mat[i][0]*2,W_mat[i][1]*2,W_mat[i][2]*2), duration=0.005)

    i += 1


L_animate = Animation(translate=(L_mat[0][0]*2,L_mat[0][1]*2,L_mat[0][2]*2))
i = 1
while i < len(L_mat):
    L_animate += Animation(translate=(L_mat[i][0]*2,L_mat[i][1]*2,L_mat[i][2]*2), duration=0.005)

    i += 1
#-----------------------------------------------------------------------------

#----------------------------アプリケーションクラス------------------------------
 
class Minimal3dApp(App):
    index = NumericProperty(0)
    j = NumericProperty(0)
    remove_list = []

    def win_rally_start(self):     
        W_animate.start(self.layout3d.ids["Ball"])

    def lose_rally_start(self):
        L_animate.start(self.layout3d.ids["Ball"])
    
    def build(self):   #アプリケーション自体をBuildする関数
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
        
        #↓レイアウトの定義↓
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
                            meshes: ("./data/obj/2dbox.obj",)
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
                            meshes: ("./data/obj/2dbox.obj",)
                            Button:
                                id: bottom_floor
                                text: "Player A"
                                font_size: 50
                                background_normal: ''
                                background_color: 0.000 , 0.000 , 0.000, 1.000
                       
                        Node:   #黄色いボール
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
                        
                                        
                        Node:   #ネット
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

                        Node:   #テニスコートの緑の面
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

                        Button:
                            id: Button1
                            size_hint: (0.2, 0.1)
                            text: "Winning Pattern"
                            font_size: 20
                            background_normal: ''
                            background_color: 1, .3, .4, .85
                            on_release:
                                app.win_rally_start()                          

                        Button:
                            id: Button2
                            size_hint: (0.15, 0.1)
                            pos_hint: {"x": 0.2, "y": 0}
                            text: "Trajectory"
                            font_size: 20

                        Button:
                            id: Button3
                            size_hint: (0.15, 0.1)
                            pos_hint: {"x": 0.35, "y": 0}
                            text: "Bounce"
                            font_size: 20
                            
                        
                        Button:
                            id: Button4
                            size_hint: (0.2, 0.1)
                            pos_hint: {"x": 0.5, "y": 0}
                            text: "Losing Pattern"
                            font_size: 20
                            background_normal: ''
                            background_color: 0.000 , 0.000 , 1.000, .85
                            on_release:
                                app.lose_rally_start()                          

                        Button:
                            id: Button5
                            size_hint: (0.15, 0.1)
                            pos_hint: {"x": 0.7, "y": 0}
                            text: "Trajectory"
                            font_size: 20

                        Button:
                            id: Button6
                            size_hint: (0.15, 0.1)
                            pos_hint: {"x": 0.85, "y": 0}
                            text: "Bounce"
                            font_size: 20

                        Button:
                            id: ClearButton
                            size_hint: (0.15, 0.1)
                            pos_hint: {"x":0.0, "y":0.9}
                            text: "Clear"
                            font_size: 20
                            #on_release:
                                #app.bottom_touch.clear()

                    '''

        self.box_str = '''
            Node: 
                min_light_intensity: 1.0
                receive_shadows: True 
                effect: True
                scale: (0.2, 0.2, 0.2)
                translate: (1, 1, 1)
                meshes: ("./data/obj/ballmark.obj", ) 
                Button:
                    canvas:
                        Color:
                            rgba: 1.000,1.000, 1.000, 1.000
                        Rectangle:
                            size: self.center   
                            pos: 0, 0                 
            '''

        self.redbox_str = '''
            Node: 
                min_light_intensity: 1.0
                receive_shadows: True 
                effect: True
                scale: (0.2, 0.2, 0.2)
                translate: (1, 1, 1)
                meshes: ("./data/obj/ballmark.obj", ) 
                Button:
                    canvas:
                        Color:
                            rgba: 1.000 ,0.000 ,0.000, 1.000
                        Rectangle:
                            size: self.center   
                            pos: 0, 0
                             
            '''

        self.redball_str = '''
            Node:
                id: RedBall
                name: 'Node 0'
                min_light_intensity: 1.0
                scale: (0.025, 0.025, 0.025)   #ボールの大きさ
                translate: (0, 0, 22)
                effect: True
                meshes: ("./data/obj/sphere.obj", ) 
                Button:
                    text: "Hello"
                    canvas:
                        Color:
                            rgb: 1.000 ,0.000 ,0.000
                        Rectangle:
                            size: self.size
                            pos: self.pos
            '''

        self.orangeball_str = '''
            Node:
                id: RedBall
                name: 'Node 0'
                min_light_intensity: 1.0
                scale: (0.025, 0.025, 0.025)   #ボールの大きさ
                translate: (0, 0, 22)
                effect: True
                meshes: ("./data/obj/sphere.obj", ) 
                Button:
                    text: "Hello"
                    canvas:
                        Color:
                            rgb: 1.000 ,0.5059 ,0.000
                        Rectangle:
                            size: self.size
                            pos: self.pos
            '''


        #layout3d.add_widget(aaa)
        layout3d = Builder.load_string(dedent(self.layout3d_str))
        layout3d.bind(on_touch_move = self.on_touch_move)  #canvasをぐりぐり動かせるようにする
        layout3d.ids.Button2.bind(on_touch_up = self.bottom_touch_w)  #Button2に軌道描画を反映
        layout3d.ids.Button3.bind(on_touch_up = self.bottom_touch_w_2) #Button3にバウンド位置プロットを反映
        layout3d.ids.Button5.bind(on_touch_up = self.bottom_touch)   #Button5に軌道描画を反映
        layout3d.ids.Button6.bind(on_touch_up = self.bottom_touch_2) #Button6にバウンド位置プロットを反映
        layout3d.ids.ClearButton.bind(on_touch_up = self.clear_canvas)
        self.layout3d = layout3d
        self.baselayout = layout3d
        self.layout3d.f_type = 0
        layout3d.bind(on_motion=self.on_motion)       
        


        grid = GridLayout(cols=2)
        grid.add_widget(self.layout3d)
        self.grid = grid
        
        return self.grid
        #return layout3d
        
    def clear_canvas(self, widget, obj):
        self.grid.ids.board3d.remove_widget(self.ids.Ball)

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
     
    
    def on_ball_pos_w(self, widget):       
        if self.index < len(W_mat)-1:
            self.index += 1
            self.a = W_mat[self.index][0]*2
            self.b = W_mat[self.index][1]*2
            self.c = W_mat[self.index][2]*2

            if self.index > 201 and self.index < 258:
                redbox = Builder.load_string(dedent(self.redbox_str))
                redbox.translate = (self.a, self.b, self.c)
                self.layout3d.add_widget(redbox)
            else:
                box = Builder.load_string(dedent(self.box_str))
                box.translate = (self.a, self.b, self.c)
                self.layout3d.add_widget(box)
                       
    
    def bottom_touch_w(self, widget, touch):
        Clock.schedule_interval(self.on_ball_pos_w, 0.01)


    def on_ball_bounce_w(self, widget):
        if self.j < len(W_bounce_pos)-1:
            self.j += 1
            self.aa = W_bounce_pos[self.j][0]*2
            self.bb = W_bounce_pos[self.j][1]*2
            self.cc = W_bounce_pos[self.j][2]*2
            if self.j == 3:
                redball = Builder.load_string(dedent(self.redball_str))
                redball.translate = (self.aa, self.bb, self.cc)
                self.layout3d.add_widget(redball)
            else:
                orangeball = Builder.load_string(dedent(self.orangeball_str))
                orangeball.translate = (self.aa, self.bb, self.cc)
                self.layout3d.add_widget(orangeball)

    def bottom_touch_w_2(self, widget, touch):
        orangeball = Builder.load_string(dedent(self.orangeball_str))
        orangeball.translate = (W_bounce_pos[0][0]*2, W_bounce_pos[0][1]*2, W_bounce_pos[0][2]*2)
        self.layout3d.add_widget(orangeball)
        Clock.schedule_interval(self.on_ball_bounce_w, 1) 



    def on_ball_pos(self, widget):       
        if self.index < len(L_mat) - 2:
            self.index += 2
            self.a = L_mat[self.index][0]*2
            self.b = L_mat[self.index][1]*2
            self.c = L_mat[self.index][2]*2

            if self.index > 331 and self.index < 405:
                redbox = Builder.load_string(dedent(self.redbox_str))
                redbox.translate = (self.a, self.b, self.c)
                self.layout3d.add_widget(redbox)
            else:
                box = Builder.load_string(dedent(self.box_str))
                box.translate = (self.a, self.b, self.c)
                self.layout3d.add_widget(box)        
    
    def bottom_touch(self, widget, touch):
        Clock.schedule_interval(self.on_ball_pos, 0.01)


    def on_ball_bounce(self, widget):
        if self.j < len(L_bounce_pos)-1:
            self.j += 1
            self.aa = L_bounce_pos[self.j][0]*2
            self.bb = L_bounce_pos[self.j][1]*2
            self.cc = L_bounce_pos[self.j][2]*2

            if self.j == 5:
                redball = Builder.load_string(dedent(self.redball_str))
                redball.translate = (self.aa, self.bb, self.cc)
                self.layout3d.add_widget(redball)
            else:
                orangeball = Builder.load_string(dedent(self.orangeball_str))
                orangeball.translate = (self.aa, self.bb, self.cc)
                self.layout3d.add_widget(orangeball)

    def bottom_touch_2(self, widget, touch):
        orangeball = Builder.load_string(dedent(self.orangeball_str))
        orangeball.translate = (L_bounce_pos[0][0]*2, L_bounce_pos[0][1]*2, L_bounce_pos[0][2]*2)
        self.layout3d.add_widget(orangeball)
        Clock.schedule_interval(self.on_ball_bounce, 1) 

        

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

