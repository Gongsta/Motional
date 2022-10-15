name = "Pong"

import pygame
from pygame import draw, Rect
from random import randint
from math import radians, sin, cos, tan, pi, inf

pygame.init()
window = pygame.display.set_mode((800, 600))

gametime= pygame.time.Clock()
pygame.display.set_caption(name)

tick_speed_increase = 4  
default_tick_speed  = 30
cool_down_timer     = 20
victory_score       = 1 #inf is good though
enable_line         = None #None means automatic decision
enable_score        = True
enable_rgb          = True

seed      = 0
controls  = [[ord("a"),ord("z")],
             [ord("k"),ord("m")]]

class ball:
    def __init__(self):
        self.loc           = [0, 0]
        self.trail         = [[],[],[]]
        self.u             = 8
        self.v             = [0, 0]
        self.reset()
        return

    def reset(self):
        self.v      = [0, 0]
        self.loc    = [392, randint(120, 480)]
        self.trail  = [self.loc, self.loc, self.loc]
        return

    def pitch(self):
        direction = randint(0,1) # 0 right, 1 left
        negative  = randint(0,1) # effectively a bool
        angle     = randint(2,9) * 5
        angle     = (radians(angle) if (negative == 1) else - radians(angle))
        # sOh  cAh  tOa
        # O=sh A=ch
        self.v[0] = self.u * cos(angle)
        self.v[1] = self.u * sin(angle)

        self.v[0] = (self.v[0] if (direction == 0) else - self.v[0])
        return

    def change_loc(self):
        self.loc = [int(self.loc[0] + self.v[0]),
                    int(self.loc[1] + self.v[1])]
        return

    def move(self, paddle_0, paddle_1):
        
        self.change_loc()
        x = self.collide(paddle_0[1], paddle_1[1])
        
        self.trail.append(self.loc)
        self.trail.pop(0)
        return (tick_speed_increase if (x == 1) else 0)

    def collide(self, p0, p1): #MAYBE add bouncing off corners
        if self.loc[1] < 8:
            self.v   = [self.v[0], -self.v[1]]
            self.loc  = [self.loc[0], 8]

        elif self.loc[1] >= 592 - 16:
            self.v   = [self.v[0], -self.v[1]]
            self.loc  = [self.loc[0], 592 - 16]

        if self.loc[0] < 32:
            #print("l",p0)
            if self.loc[1] > p0 -8 and self.loc[1] <= p0 + 96 + 8:
                #print("LEFT BOUNCE")
                self.v    = [-self.v[0], self.v[1]]
                self.loc  = [32, self.loc[1]]
                return 1
            
        elif self.loc[0] >= 768 - 16:
            #print("r",p1)
            if self.loc[1] > int(p1 - 8) and self.loc[1] <= int(p1 + 96 + 8):
                #print("RIGHT BOUNCE")
                self.v   =  [-self.v[0], self.v[1]]
                self.loc  = [768 - 16, self.loc[1]]
                return 1
        return

    def check_alive(self):
        if self.loc[0] < 0:
            #print("left player loses")
            return [False, "l"]
        elif self.loc[0] > 800 - 16:
            #print("right player loses")
            return [False, "r"]
        elif self.v[1] == 0:
            #print("reset")
            return [False, "n"]
        return [True, "n"] 
    
    def draw(self):
        for i in range(len(self.trail)):
            r = self.trail[i]
            draw.rect(window, cc_ball[i], Rect(r[0], r[1], 16, 16))
        return

"5 PADDLE OBJECT FUNCTIONS"
class paddle:
    def __init__(self, startposition):
        self.step   = 8
        self.length = 96
        hori_loc    = (16 if (startposition == 0) else 768)
        vert_loc    = int(300 - (self.length/2))
        self.loc    = [hori_loc, vert_loc]
        return

    def move(self, cd):#can be "u"(up) or "d"(down) or " "(none)
        if cd == "u":
            vert_loc = self.loc[1] - self.step
        elif cd == "d":
            vert_loc =  self.loc[1] + self.step
        else:
            vert_loc = self.loc[1]
        
        if vert_loc >= 10 and vert_loc < 590 - self.length:
            self.loc = [self.loc[0], vert_loc]  
        return

    def draw(self):
        draw.rect(window, cc_paddle, Rect(self.loc[0], self.loc[1], 16, self.length))
        return
    
class text:
    def get_3x5_row():
        rows = [[0,0,0],[1,0,0],[0,1,0],[0,0,1],[1,1,0],[1,0,1],[0,1,1],[1,1,1]]
        return rows

    def get_3x5_col():
        letters     = {"0": [7,5,5,5,7],
                       "1": [3,3,3,3,3],
                       "2": [7,3,7,1,7],
                       "3": [7,3,7,3,7],
                       "4": [5,5,7,3,3],
                       "5": [7,1,7,3,7],
                       "6": [7,1,7,5,7],
                       "7": [7,3,3,3,3],
                       "8": [7,5,7,5,7],
                       "9": [7,5,7,3,3],
                       "a": [7,5,7,5,5],
                       "b": [4,5,4,5,4],
                       "c": [7,1,1,1,7],
                       "d": [4,5,5,5,4],
                       "e": [7,1,7,1,7],
                       "f": [7,1,7,1,1],
                       "g": [7,1,5,5,7],
                       "h": [5,5,7,5,5],
                       "i": [7,2,2,2,7],
                       "j": [7,2,2,2,4],
                       "k": [5,5,4,5,5],
                       "l": [1,1,1,1,7],
                       "m": [5,7,5,5,5],
                       "n": [7,5,5,5,5],
                       "o": [7,5,5,5,7],
                       "p": [7,5,7,1,1],
                       "r": [7,5,7,4,5],
                       "s": [7,1,7,3,7],
                       "t": [7,2,2,2,2],
                       "u": [5,5,5,5,7],
                       "v": [5,5,5,5,2],
                       "w": [5,5,5,7,5],
                       "x": [5,5,2,5,5],
                       "y": [5,5,7,2,2],
                       "z": [7,3,2,1,7],
                       " ": [0,0,0,0,0],
                       ">": [1,2,3,2,1],
                       "<": [3,2,1,2,3],
                       "[": [6,2,2,2,6],
                       "]": [4,2,2,2,4],
                       "/": [1,4,2,6,3],
                       "(": [3,2,2,2,3],
                       ")": [1,2,2,2,1],
                       "/": [1,4,2,6,3],
                       ":": [0,2,0,2,0],
                       "-": [0,0,7,0,0],
                       ".": [0,0,0,0,2]}
        return letters

    def get_5x9_row():
        rows    = [[0,0,0,0,0],                                                 #5c0 #00
                   
                   [1,0,0,0,0],[0,1,0,0,0],[0,0,1,0,0],[0,0,0,1,0],[0,0,0,0,1], #5c1 #01,02,03,04,05
                   
                   [1,1,0,0,0],[1,0,1,0,0],[1,0,0,1,0],[1,0,0,0,1],[0,1,1,0,0], #5c2 #06,07,08,09,10 
                   [0,1,0,1,0],[0,1,0,0,1],[0,0,1,1,0],[0,0,1,0,1],[0,0,0,1,1], #5c2 #11,12,13,14,15

                   [1,1,1,0,0],[1,1,0,1,0],[1,1,0,0,1],[1,0,1,1,0],[1,0,1,0,1], #5c3 #16,17,18,19,20
                   [0,1,1,1,0],[0,1,1,0,1],[1,0,0,1,1],[0,1,0,1,1],[0,0,1,1,1], #5c3 #21,22,23,24,25

                   [1,1,1,1,0],[1,1,1,0,1],[1,1,0,1,1],[1,0,1,1,1],[0,1,1,1,1], #5c4 #26,27,28,29,30

                   [1,1,1,1,1]]                                                 #5c5 #31
        return rows

    def get_5x9_col():
        letters = { "a": [ 0, 0, 0, 0,31, 9,31, 9, 9],
                    "C": [31, 1, 1, 1, 1, 1, 1, 1,31],
                    "c": [ 0, 0, 0, 0,31, 1, 1, 1,31],
                    "e": [ 0, 0, 0, 0,31, 1,31, 1,31],
                    "f": [ 0, 0, 0, 0,31, 1,31, 1, 1],
                    "G": [31, 1, 1, 1,23, 9, 9, 9,31],
                    "g": [ 0, 0, 0, 0,31, 1,23, 9,31],
                    "H": [ 9, 9, 9, 9,31, 9, 9, 9, 9],
                    "h": [ 0, 0, 0, 0, 9, 9,31, 9, 9],
                    "I": [31, 3, 3, 3, 3, 3, 3, 3,31],
                    "i": [ 0, 0, 0, 0,31, 3, 3, 3,31],
                    "k": [ 0, 0, 0, 0, 9, 8,16, 8, 9],
                    "L": [ 1, 1, 1, 1, 1, 1, 1, 1,31],
                    "l": [ 0, 0, 0, 0, 1, 1, 1, 1,31],
                    "m": [ 0, 0, 0, 0, 9,28,20, 9, 9],
                    "n": [ 0, 0, 0, 0, 9,18,20,23, 9],
                    "o": [ 0, 0, 0, 0,31, 9, 9, 9,31],
                    "P": [31, 9, 9, 9,31, 1, 1, 1, 1],
                    "p": [ 0, 0, 0, 0,31, 9,31, 1, 1],
                    "R": [31, 9, 9, 9,31, 6, 7, 8, 9],
                    "r": [ 0, 0, 0, 0,31, 9,31, 8, 9],
                    "S": [31, 1, 1, 1,31, 5, 5, 5,31],
                    "s": [ 0, 0, 0, 0,31, 1,31, 5,31],
                    "t": [ 0, 0, 0, 0,31, 3, 3, 3, 3],
                    "u": [ 0, 0, 0, 0, 9, 9, 9 ,9,31],
                    "W": [ 9, 9, 9, 9,20,20,20,20,31],
                    "x": [ 0, 0, 0, 0, 9,11, 3,11, 9],
                    "y": [ 0, 0, 0, 0, 9, 9,31, 3, 3],
                    "z": [ 0, 0, 0, 0,31, 4, 3, 2,31],
                    " ": [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   }
        return letters
         

    def display(start, scale, string, char_rows, char_letters, char_width, colour):
        try:
            size = char_width + 1
            letter  =  [start[0],start[1]]
            for i in string:
                #print("\t\t",i)
                column  = letter[0]
                row     = letter[1]
                for j in char_letters[i]:
                    #print("\t",j)
                    for k in char_rows[j]:
                        #print(k)
                        if k == 1:
                            draw.rect(window, colour, Rect(column, row, scale, scale)) 
                        column += scale
                    row   += scale
                    column = letter[0]
                    #print(row,column)  
                letter = [(letter[0] + size*scale),start[1]]
        except Exception:
            window.fill(cc_bg)
            text.error(2)
        return
    

    def display_small(start, scale, string, colour=None):
        if colour == None: colour = cc_text
        sub_rows    = text.get_3x5_row()
        sub_letters = text.get_3x5_col()               
        text.display(start, scale, string, sub_rows, sub_letters, 3, colour)
        return
        

    def display_big(start, scale, string, colour=None):
        if colour == None: colour = cc_text
        title_rows    = text.get_5x9_row()
        title_letters = text.get_5x9_col()
        text.display(start, scale, string, title_rows, title_letters, 5, colour)
        return


    def subtitle(arrows):
        if arrows >= 0:
            string = "> press space to start game <"
        else:
            string = "press space to start game"
        scale      = 4
        med        = ((len(string)*4)-1)/2
        start      = [400 - int(scale * med), 400]
        text.display_small(start, scale, string)
        arrows -= 1
        if arrows == - default_tick_speed: arrows = default_tick_speed
        return arrows

    def subtitle_2(position=400):
        scale      = 4
        string     = "press space to continue or esc to exit"
        med        = ((len(string)*4)-1)/2
        start      = [400 - int(scale * med), position]
        text.display_small(start, scale, string)
        return

    def error(no=0):
        scale      = 6
        stringlist = ["error: page not found","error: icon not found","error: character does not exist"]
        string     = stringlist[no]
        med        = ((len(string)*4)-1)/2
        start      = [400 - int(scale * med), 300 - int((scale / 2) * 5)]
        text.display_small(start, scale, string)
        return

    def reset():
        scale      = 3
        string     = "The game has been reset!"
        med        = ((len(string)*4)-1)/2
        start      = [400 - int(scale * med), 300 - int((scale / 2) * 5)]
        text.display_small(start, scale, string)
        return

    def bottom(n):
        scale      = 4
        stringlist = ["press h for help","press esc to return to menu","press backspace to go back","press g for advanced colour settings","press space to save settings"]
        string     = stringlist[n]
        start      = [792-(len(string)*scale*4), 592 - scale * 6]
        text.display_small(start, scale, string)
        return

    def version():
        scale      = 2
        ### CHANGE VERSION NAME HERE ###
        version    = 0
        stringlist = ["","stable release version","wip version","alpha version","beta version"]
        string     = stringlist[version] 
        start      = [792-(len(string)*scale*4), 12]
        text.display_small(start, scale, string)
        return

    def victory(winner, style=1):
        if style == 0:
            scale      = 6
            string     = winner + " Player Wins"
            start      = [400 - int((scale * ((len(string)* 6) -1))/2), 160]
            text.display_big(start, scale, string)
            text.subtitle_2(400)
        elif style == 1:
            scale      = 10
            string     = winner + " Player"
            start      = [400 - int((scale * ((len(string)* 6) -1))/2), 148]
            text.display_big(start, scale, string)
            string     = "Wins"
            start      = [400 - int((scale * ((len(string)* 6) -1))/2), 148 + scale * 14]
            text.display_big(start, scale, string)
            text.subtitle_2(480)
        return

    def logo():
        scale      = 20
        start      = [400 - int(scale * (23/2)), 120]
        string     = name
        text.display_big(start, scale, string)
        return

    def dot():
        coords = [392,56]
        draw.rect(window, c_line, Rect(coords[0], coords[1], 16, 16))
        return

    def score(value, line = False):
        scale = 16
        ##if line == False: 
        ##    text.dot()

        #Left
        start = [400,24]
        start[0] -= (len(str(value[0])) * scale * 4) + scale
        text.display_small(start, scale, str(value[0]))
        #Right
        start = [400,24]
        start[0] += (len(str(value[1])) * scale) + scale
        text.display_small(start, scale, str(value[1]))
        return

    def title(string):
        scale      = 8
        start      = [400 - int((scale * ((len(string)* 6) -1))/2), 16]
        text.display_big(start, scale, string)
        return

    def multiple(start, scale, strings):
        text.display_big(start, scale, strings[0])
        space = scale * 20
        start = [start[0] + space, start[1] + scale * 4]
        text.display_small(start, scale, strings[1])
        return

    def page_help(screen):
        scale = 4
        start = [144,100]
        lines = []
        space = scale * 3 * 4
        if screen == 0:
            text.title("Help")
            lines = [["h","to open help prompt [this]"],["c","to show in-game controls"],["s","to edit gameplay settings"],["g","to open advanced settings"],
                     ["r","to reset all settings"],["i","to view game info"],["e","to exit game"]]
        if screen == 1:
            text.title("Controls")
            lines = [["left player",""],["a","move paddle up"],["z","move paddle down"],[" "," "],["right player",""],["k","move paddle up"],["m","move paddle down"]]
            string = "first player to "+str(victory_score)+" points wins"
            pos    = [start[0], 500]
            text.display_small(pos, scale, ("first player to "+str(victory_score)+" points wins"))

        for line in lines:
            text.multiple(start, scale, line)
            start[1] += space
        return



class colour:
    def save():
        global cc_ball
        cc_ball    = [pygame.Color(c_ball1[0],c_ball1[1],c_ball1[2]),
                      pygame.Color(c_ball2[0],c_ball2[1],c_ball2[2]),
                      pygame.Color(c_ball3[0],c_ball3[1],c_ball3[2])]
        global cc_bg
        cc_bg      =  pygame.Color(c_bg[0],c_bg[1],c_bg[2])
        global cc_text
        cc_text    =  pygame.Color(c_text[0],c_text[1],c_text[2])
        global cc_wall
        cc_wall    =  pygame.Color(c_wall[0],c_wall[1],c_wall[2])
        global cc_line
        cc_line    =  pygame.Color(c_line[0],c_line[1],c_line[2])
        global cc_paddle
        cc_paddle  =  pygame.Color(c_paddle[0],c_paddle[1],c_paddle[2])
        global cc_hlight
        cc_hlight  =  pygame.Color(c_hlight[0],c_hlight[1],c_hlight[2])
        return

    def cycle():
        global seed

        if rgb_style == "secret":
            rgb_r = int(64 + 63 * sin((seed*pi/180)))
            rgb_g = int(64 + 63 * sin((seed*pi/180)+(2*pi/3)))
            rgb_b = int(64 + 63 * sin((seed*pi/180)+(4*pi/3)))

        elif rgb_style == "1337": #not normally available
            rgb_r = int(64 + 63 * sin((seed*pi/180)))
            rgb_g = int(191 + 63 * sin((seed*pi/180)))
            rgb_b = int(64 + 63 * sin((seed*pi/180)))

        elif rgb_style == "dark":
            rgb_r = int(32 + 31 * sin((seed*pi/360)))
            rgb_g = int(32 + 31 * sin((seed*pi/360)+(2*pi/3)))
            rgb_b = int(32 + 31 * sin((seed*pi/360)+(4*pi/3)))

        elif rgb_style == "jumpy": #Not good
            rgb_r = 25 * int( 5 * (1 + sin((seed*pi/360))))
            rgb_g = 25 * int( 5 * (1 + sin((seed*pi/360)+(2*pi/3))))
            rgb_b = 25 * int( 5 * (1 + sin((seed*pi/360)+(4*pi/3))))

        elif rgb_style == "standard": #ie SQUARED
            rgb_r = int(255 * (sin((seed*pi/360))**2))
            rgb_g = int(255 * (sin((seed*pi/360)+(2*pi/3))**2))
            rgb_b = int(255 * (sin((seed*pi/360)+(4*pi/3))**2))

        elif rgb_style == "cycle": #ie FAST
            rgb_r = int(255 * (sin(4 * ((seed*pi/360)))**2))
            rgb_g = int(255 * (sin(4 * ((seed*pi/360)+(2*pi/3)))**2))
            rgb_b = int(255 * (sin(4 * ((seed*pi/360)+(4*pi/3)))**2))

        elif rgb_style == "fade": #ie SLOW
            rgb_r = int(255 * (sin(0.2 * ((seed*pi/360)))**2))
            rgb_g = int(255 * (sin(0.2 * ((seed*pi/360)+(2*pi/3)))**2))
            rgb_b = int(255 * (sin(0.2 * ((seed*pi/360)+(4*pi/3)))**2))

        elif rgb_style == "flash":
            rgb_x = [0,0,0]
            for i in range(len(rgb_x)):
                rgb_x[i] = int(16 + 2 * (tan((seed*pi/360)+((i*2*pi)/3))**2))
                if rgb_x[i] > 255: rgb_x[i] = 255
                if rgb_x[i] < 0:   rgb_x[i] = 0
            rgb_r = rgb_x[0]
            rgb_g = rgb_x[1]
            rgb_b = rgb_x[2]

        elif rgb_style == "legacy": #ie STANDARD
            rgb_r = int(128 + 127 * sin((seed*pi/180)))
            rgb_g = int(128 + 127 * sin((seed*pi/180)+(2*pi/3)))
            rgb_b = int(128 + 127 * sin((seed*pi/180)+(4*pi/3)))

        else:
            rgb_r = c_wall[0]
            rgb_g = c_wall[1]
            rgb_b = c_wall[2]

        seed += 1
        global cc_wall
        cc_wall =  pygame.Color(rgb_r, rgb_g, rgb_b)
        return

    def update():
        colour.presets(preset)
        colour.save()

    def presets(name="standard"): ### GO HERE TO ADD THEMES
        if True:
            global c_ball1
            global c_ball2
            global c_ball3
            global c_bg
            global c_text
            global c_wall
            global c_line
            global c_paddle
            global c_hlight
            global enable_rgb
            global enable_line
            global preset
            global rgb_style
        #standard, inverted, classic, legacy, 1337, dark

        if name == "standard":
            c_ball1     =  [127,127,127]
            c_ball2     =  [191,191,191]
            c_ball3     =  [255,255,255]
            c_bg        =  [  0,  0,  0]
            c_text      =  [255,255,255]
            c_wall      =  [255,255,255]
            c_line      =  [255,255,255]
            c_paddle    =  [255,255,255]
            c_hlight    =  [127,127,127]
            enable_rgb  =  True
            enable_line =  False
            preset      =  "standard"
            rgb_style   =  "standard"

        elif name == "inverted":
            c_ball1     =  [127,127,127]
            c_ball2     =  [ 63, 63, 63]
            c_ball3     =  [  0,  0,  0]
            c_bg        =  [255,255,255]
            c_text      =  [  0,  0,  0]
            c_wall      =  [  0,  0,  0] 
            c_line      =  [  0,  0,  0]
            c_paddle    =  [  0,  0,  0]
            c_hlight    =  [127,127,127]
            enable_rgb  =  True
            enable_line =  False
            preset      =  "inverted"
            rgb_style   =  "standard"

        elif name == "classic":
            c_ball1     =  [127,127,127]
            c_ball2     =  [191,191,191]
            c_ball3     =  [255,255,255]
            c_bg        =  [  0,  0,  0]
            c_text      =  [255,255,255]
            c_wall      =  [255,255,255]
            c_line      =  [255,255,255]
            c_paddle    =  [255,255,255]
            c_hlight    =  [127,127,127]
            enable_rgb  =  False
            enable_line =  True
            preset      =  "classic"
            rgb_style   =  "legacy"

        elif name == "legacy":
            c_ball1     =  [127,127,127]
            c_ball2     =  [191,191,191]
            c_ball3     =  [255,255,255]
            c_bg        =  [  0,  0,  0]
            c_text      =  [255,255,255]
            c_wall      =  [  0,255,255]
            c_line      =  [255,255,255]
            c_paddle    =  [255,255,255]
            c_hlight    =  [  0,255,255]
            enable_rgb  =  False
            enable_line =  False
            preset      =  "legacy"
            rgb_style   =  "legacy"

        elif name == "1337":
            c_ball1     =  [  0,127,  0]
            c_ball2     =  [  0,191,  0]
            c_ball3     =  [  0,255,  0]
            c_bg        =  [  0,  0,  0]
            c_text      =  [  0,127,  0]
            c_wall      =  [  0, 63,  0]
            c_line      =  [  0, 63,  0]
            c_paddle    =  [  0,127,  0]
            c_hlight    =  [  0,255,  0]
            enable_rgb  =  False
            enable_line =  True
            preset      =  "1337"
            rgb_style   =  "1337"

        elif name == "dark":
            c_ball1     =  [ 63, 63, 63]
            c_ball2     =  [127,127,127]
            c_ball3     =  [191,191,191]
            c_bg        =  [  0,  0,  0]
            c_text      =  [ 63, 63, 63]
            c_wall      =  [ 63, 63, 63]
            c_line      =  [ 63, 63, 63]
            c_paddle    =  [ 63, 63, 63]
            c_hlight    =  [127,127,127]
            enable_rgb  =  False
            enable_line =  True
            preset      =  "dark"
            rgb_style   =  "dark"

        else: preset = "custom"
        colour.save()
        return

"8 SETTINGS"
class settings:
    def __init__(self):
        self.refresh()
        self.selection = 0
        self.key       = ""
        self.max       = len(self.stringlist) - 1
        return

    def refresh(self):
        self.stringlist = [["playing to:           ",str(victory_score)+" points"],
                           ["tick speed:           ",str(default_tick_speed)],
                           ["speed increase:       ",str(tick_speed_increase)],
                           ["cool down:            ",str(cool_down_timer)+" ticks"],
                           ["enable score display: ",str.lower(str(enable_score))],
                           ["enable midway line:   ",str.lower(str(enable_line))],
                           ["enable rgb:           ",str.lower(str(enable_rgb))],
                           ["graphics preset:      ",str.lower(preset)]]
        return

    def directory(self, s):
        if s == 0:
            self.change_vicscore()
        elif s == 1:
            self.change_tickspeed()
        elif s == 2:
            self.change_generic(0)
        elif s == 3:
            self.change_generic(1)
        elif s == 4:
            self.change_bool(0)
        elif s == 5:
            self.change_bool(1)
        elif s == 6:
            self.change_bool(2)
        elif s == 7:
            self.change_preset()
        self.refresh()
        return


    def change_vicscore(self):
        scores = [inf, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ,11, 12, 13, 14 ,15 ,16, 17, 18, 19, 20, 25, 30, 32, 40, 50 ,60, 64, 70, 80, 90, 100, 120, 125, 128, 144, 150, 196 ,200, 250, 256, 300]
        global victory_score
        no = scores.index(victory_score)

        if self.key == "LEFT":
            no -= 1
            if no < 0:
                no = len(scores) - 1
        if self.key == "RIGHT":
            no += 1
            if no > len(scores) - 1:
                no = 0

        victory_score = scores[no]
        return
    
    def change_generic(self, mode):
        if mode == 0:
            global tick_speed_increase
            current = tick_speed_increase
        elif mode == 1:
            global cool_down_timer
            current = cool_down_timer
        
        if self.key == "LEFT" and current > 0:
            current -= 1
        if self.key == "RIGHT" and current < 1000:
            current += 1
        
        if mode == 0:
            tick_speed_increase = current
        if mode == 1:
            cool_down_timer = current
        return
    
    def change_bool(self, mode):
        global preset
        if mode == 0:
            global enable_score
            current = enable_score
            preset  = "custom"
        elif mode == 1:
            global enable_line
            current = enable_line
            preset  = "custom"
        elif mode == 2:
            global enable_rgb
            current = enable_rgb
            preset  = "custom"

        if self.key == "LEFT" or self.key == "RIGHT":
            if current == False:
                current = True
            elif current == True:
                current = False

        if mode == 0:
            enable_score = current
        if mode == 1:
            enable_line = current
        if mode == 2:
            enable_rgb = current
        return

    def change_preset(self): ### GO HERE TO ADD THEMES
        options = ["custom","standard","inverted","1337","dark","classic","legacy"]
        global preset
        try:
            no = options.index(preset)
        except Exception:
            preset = "standard"
            no     = options.index(preset)

        if no == 0:
            no = 1
        else:
            if self.key == "LEFT":
                no -= 1
                if no < 1:
                    no = len(options) - 1
            if self.key == "RIGHT":
                no += 1
                if no > len(options) - 1:
                    no = 1

        preset = options[no]
        colour.update()
        return

    def change_tickspeed(self):
        speeds = [10,12,15,16,20,22,24,25,26,28,30,32,34,35,36,38,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,64,65,70,75,80,90,95,100,120,125,128,150,300]
        global default_tick_speed
        no = speeds.index(default_tick_speed)

        if self.key == "LEFT" and no > 0:
            no -= 1

        if self.key == "RIGHT" and no < len(speeds) - 1:
            no += 1

        default_tick_speed = speeds[no]
        return
   

    def submit(self, key):
        self.key = key

        if self.key == "UP":
            self.selection -= 1
            if self.selection < 0:
                self.selection = self.max

        elif self.key == "DOWN":
            self.selection += 1
            if self.selection > self.max:
                self.selection = 0

        if self.key == "LEFT" or self.key == "RIGHT":
            self.directory(self.selection)
        return

    def draw(self):
        scale  = 4
        start  = [144,120]
        space  = scale * 12
        string = "use arrow keys to navigate settings"
        text.display_small(start, scale, string)
        start[1] += space
        for i in range(len(self.stringlist)):
            text.display_small(start, scale, self.stringlist[i][0])
            startx = start[0] + (len(self.stringlist[i][0]) * 4 * scale)

            if self.selection == i:
                c = cc_hlight
            else:
                c = cc_text

            text.display_small([startx, start[1]], scale, self.stringlist[i][1], c) 
            start[1] += space
        return

class customisation:
    def __init__(self):
        self.refresh()
        self.selection = 0
        self.key       = ""
        self.max       = len(self.stringlist1) * 3
        self.edit      = False
        return

    def refresh(self):
        self.stringlist0 = [["rgb preset mode:                          ",rgb_style]]
        
        self.stringlist1 = [["background fill colour:               ",proc(c_bg[0]), proc(c_bg[1]), proc(c_bg[2])],
                            ["normal text colour:                   ",proc(c_text[0]), proc(c_text[1]), proc(c_text[2])],
                            ["highlighted text colour:              ",proc(c_hlight[0]), proc(c_hlight[1]), proc(c_hlight[2])],
                            ["paddle colour:                        ",proc(c_paddle[0]), proc(c_paddle[1]), proc(c_paddle[2])],
                            ["ball colour:                          ",proc(c_ball3[0]), proc(c_ball3[1]), proc(c_ball3[2])],
                            ["ball trail colour 1:                  ",proc(c_ball2[0]), proc(c_ball2[1]), proc(c_ball2[2])],
                            ["ball trail colour 2:                  ",proc(c_ball1[0]), proc(c_ball1[1]), proc(c_ball1[2])],
                            ["wall colour [if enabled]:             ",proc(c_wall[0]), proc(c_wall[1]), proc(c_wall[2])],
                            ["line colour [if enabled]:             ",proc(c_line[0]), proc(c_line[1]), proc(c_line[2])]]

        self.stringlist2 = [["rgb:                                      ",("enabled" if (enable_rgb == True) else "disabled")],
                            ["midway line:                              ",("enabled" if (enable_line == True) else "disabled")],
                            ["score counter:                            ",("enabled" if (enable_score == True) else "disabled")]]
        return

    def directory(self, s):
        if s == 0:
            self.change_preset()
        else:
            for r in range(1,10):
                for c in range(0,3):     
                    if self.selection == (3 * (r - 1)) + (1 + c):
                        self.change_colour(r, c)
        self.refresh()
        return


    def change_colour(self, number, col): 
        if number == 1:
            global c_bg
            c_bg[col] = self.change_value(c_bg[col])
        elif number == 2:
            global c_text
            c_text[col] = self.change_value(c_text[col])
        elif number == 3:
            global c_hlight
            c_hlight[col] = self.change_value(c_hlight[col])
        elif number == 4:
            global c_paddle
            c_paddle[col] = self.change_value(c_paddle[col])
        elif number == 5:
            global c_ball3
            c_ball3[col] = self.change_value(c_ball3[col])
        elif number == 6:
            global c_ball2
            c_ball2[col] = self.change_value(c_ball2[col])
        elif number == 7:
            global c_ball1
            c_ball1[col] = self.change_value(c_ball1[col])
        elif number == 8:
            global c_wall
            c_wall[col] = self.change_value(c_wall[col])
        elif number == 9:
            global c_line
            c_line[col] = self.change_value(c_line[col])
        return

    def change_value(self, n):
        values = [0, 31, 63, 95, 127, 159, 191, 223, 255]
        try:
            no = values.index(n)
        except Exception:
            no = 0

        if self.key == "LEFT" and no > 0:
            no -= 1
        if self.key == "RIGHT" and no < len(values) - 1:
            no += 1

        return values[no]

    def change_preset(self):
        options = ["1337","legacy","standard","cycle","fade","flash","secret","jumpy","dark"]
        global rgb_style
        try:
            no = options.index(rgb_style)
        except Exception:
            rgb_style = "standard"
            no     = options.index(rgb_style)

        if no == 0:
            no = 1
        else:
            if self.key == "LEFT":
                no -= 1
                if no < 1:
                    no = len(options) - 1
            if self.key == "RIGHT":
                no += 1
                if no > len(options) - 1:
                    no = 1

        rgb_style = options[no]
        return


    def submit(self, key):
        self.key = key

        if self.key == "UP":
           self.selection -= 1
           if self.selection < 0:
                self.selection = self.max

        elif self.key == "DOWN":
            self.selection += 1
            if self.selection > self.max:
               self.selection = 0

        if self.key == "LEFT" or self.key == "RIGHT":
            global preset
            preset = "custom"
            self.directory(self.selection)
        return

    def draw(self):
        scale  = 4
        start  = [144,120]
        space  = scale * 12

        string = "use arrow keys to navigate settings"
        text.display_small(start, scale, string)
        start[1] += space

        scale  = 2
        space  = scale * 12
        gap    = scale * 4 * 4

        for i in range(len(self.stringlist0)):
            text.display_small(start, scale, self.stringlist0[i][0])
            if self.selection == 0:
                c1 = cc_hlight
            else:
                c1 = cc_text
            startx = start[0] + (len(self.stringlist0[i][0]) * 4 * scale)
            text.display_small([startx, start[1]], scale, self.stringlist0[i][1],c1)
            start[1] += space
        
        for i in range(len(self.stringlist1)):
            start[1] += space
            text.display_small(start, scale, self.stringlist1[i][0])

            startx = start[0] + (len(self.stringlist1[i][0]) * 4 * scale)
            for j in range(1,4):
                startx += gap

                if self.selection == ((i * 3) + j):
                    c2 = cc_hlight
                else:
                    c2 = cc_text

                text.display_small([startx, start[1]], scale, self.stringlist1[i][j], c2) 

        start[1] += space
        for i in range(len(self.stringlist2)):
            start[1] += space
            text.display_small(start, scale, self.stringlist2[i][0])
            startx = start[0] + (len(self.stringlist2[i][0]) * 4 * scale)
            text.display_small([startx, start[1]], scale, self.stringlist2[i][1]) 
            
        return


"9 MINOR FUNCTIONS"

def background(show_lines=False):
    window.fill(cc_bg)
    draw.rect(window, cc_wall, Rect(0, 592, 800, 8))
    draw.rect(window, cc_wall, Rect(0,   0, 800, 8))
    if show_lines:
        coords = [392,24]
        for i in range(35):
            draw.rect(window, cc_line, Rect(coords[0], coords[1], 16, 16))
            coords[1] += 32
    return

def transition(no=0):
    window.fill(c_bg)
    text.error(no)
    pygame.display.flip()
    return

def setup():
    colour.presets("legacy")
    colour.save()
    return

def reset():
    global tick_speed_increase
    global default_tick_speed
    global cool_down_timer
    global victory_score
    global enable_line
    global enable_score
    global enable_rgb

    tick_speed_increase = 4  #change me!
    default_tick_speed  = 50
    cool_down_timer     = 20
    victory_score       = 10 #inf
    enable_line         = None
    enable_score        = True
    enable_rgb          = True

    colour.presets()
    colour.save()
    
    if enable_rgb: colour.cycle()
    background()
    text.reset()
    pygame.display.flip()
    gametime.tick(1)
    return

def proc(data):
    output = str(data)
    for i in range(3-len(output)):
       output = "0" + output
    return output

def title_screen():
    count = default_tick_speed
    while True:
        for event in pygame.event.get():
            if event.type == 12: #RED X
                return 1

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: #ESC
                   return 1
                if event.key == pygame.K_e: #E #exit
                    return 1

                if event.key == pygame.K_SPACE: #SPACE
                    transition()
                    return 0

                if event.key == pygame.K_r: #R #reset
                    reset()

        background(False)
        text.logo()
        text.version()
        text.bottom(0)

        count = text.subtitle(count)

        if enable_rgb: colour.cycle()

        pygame.display.flip()
        
        gametime.tick(default_tick_speed)
    return

def victory_screen(scores, winner, o1, o2):
    while True:
        for event in pygame.event.get():
            if event.type == 12:
                return 1

            elif event.type == pygame.KEYDOWN:
                # if event.key == pygame.K_ESCAPE:
                #     return 1
                if event.key == pygame.K_ESCAPE:
                     return 1

                if event.key == pygame.K_SPACE:
                     window.fill(c_bg)
                     pygame.display.flip()
                     return 0

        background()
        o1.draw()
        o2.draw()
        text.victory(winner)
        if enable_score == True: text.score(scores)
        if enable_rgb: colour.cycle()

        pygame.display.flip()
        gametime.tick(default_tick_speed)
    return

def game():
    b       = ball()
    p0      = paddle(0)
    p1      = paddle(1)
    cd      = [" ", " "]
    alive   = [False, 0]
    count   = 0
    line    = enable_line
    speed   = 0
    score   = [0,0]
        
    while True:
        if alive[0] == False and count <= 0:
            count = cool_down_timer 
            speed  = 0
            b.reset()
            alive[0] = None
        elif alive[0] == None and count > 0:
            count -= 1
        elif alive[0] == None and count <= 0:
            b.pitch()
            alive[0] = True
            
        for event in pygame.event.get():
            if event.type == 12:
                return 1
                
            elif event.type == pygame.KEYDOWN:
                for i in range(2):
                    if event.key == controls[i][0]:
                        cd[i] = "u"
                    if event.key == controls[i][1]:
                        cd[i] = "d"
        
                if event.key == pygame.K_r: #R #reset
                    reset()

            elif event.type == 3:
                for i in range(2):
                    if event.key == controls[i][0]:
                        cd[i] = " "
                    if event.key == controls[i][1]:
                        cd[i] = " "

        p0.move(cd[0])
        p1.move(cd[1])

        if alive[0] == True:
            speed += b.move(p0.loc, p1.loc)
            alive  = b.check_alive()
            #print(alive)
        
        if alive[1] == "l":
            score[1] += 1
            alive[1]  = 0
            #print(score)
        if alive[1] == "r":
            score[0] += 1
            alive[1]  = 0
            #print(score)

        background(line)
        b.draw()
        p0.draw()
        p1.draw()

        if enable_score == True: text.score(score, line)

        if score[0] == victory_score:
            return victory_screen(score, "Left", p0, p1)

        elif score[1] == victory_score:
            return victory_screen(score, "Right", p0, p1)
            

        pygame.display.flip()
        #print(speed)
        gametime.tick(default_tick_speed + speed)
    return

if __name__ == "__main__":
    setup()
    enable_line = (enable_line if (enable_line != None) else (False if enable_rgb else True))
    while True:
        x = title_screen()
        if x == 0 or x == 2:
            if game() == 1: break
        else:
            break
    pygame.quit()
