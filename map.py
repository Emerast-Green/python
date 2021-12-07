import pygame as pg
import json

from classes import FONT, FONT_SIZE, Base
'''
TODO: Make point manager, so it will automatically distribute various colours and show names in legend.
Legend is of course separate object referenced in code with function
'''

class Map_Object(Base):
    def __init__(self,pos,size,parent=None):
        super().__init__(pos,size,["keyboard","over","click"],parent)
        self.maps = {}
        self.map = "default"
        self.camera = [0,0]
        self.coords = [0,0]
        self.win = pg.Surface(self.size)
        self.overlay = pg.Surface(size,pg.SRCALPHA,32)
        self.osz = 40 #over_size
    def load_file(self,path):
        a = open(path,"r")
        b = json.load(a)
        a.close()
        self.camera = b["default_position"]
        self.maps = b["worlds"]
        self.map = tuple(b["worlds"].keys())[0]
        self.camera = [-self.camera[0]*2//32,self.camera[1]*2//32]
        del b
    def gen_conf(self):
        self.maps["default"]=[
            ["t1",100,100],
            ["t2",-50,25]
        ]
        self.camera = [0,0]
    def key(self,key):
        if key == pg.K_d:
            self.camera[0]-=1
        if key == pg.K_a:
            self.camera[0]+=1
        if key == pg.K_w:
            self.camera[1]+=1
        if key == pg.K_s:
            self.camera[1]-=1
        self.coords[0],self.coords[1] = self.camera[0]*-16,self.camera[1]*16
    def click(self):
        pass
    def gen_map(self):
        self.win = pg.Surface(self.size)
        self.win.fill((0,120,0))
        for x in range(self.size[0]//32+2):
            pg.draw.line(self.win,(255,255,255),(x*32,0),(x*32,self.size[1]+4))
        for y in range(self.size[1]//32+2):
            pg.draw.line(self.win,(255,255,255),(0,y*32),(self.size[0]+4,y*32))
        self.set_at((0,0),(255,0,0))
        self.set_at((16,16),(0,255,0))
    def set_at(self,pos,colour):
        pg.draw.rect(self.win,colour,pg.Rect(
            1*pos[0]*2+self.camera[0]*32+self.size[0]//2-1,
            -1*pos[1]*2+self.camera[1]*32+self.size[1]//2-1,
            4,4)
        )
    def colour_manager(self,r,g,b):
        a = 0
        jump = 75
        limit = 225
        if a == 0 and r == g == b < limit:
            r += jump
            a = 1
        if a == 0 and r > g == b < limit:
            g += jump
            a = 1
        if a == 0 and r == g > b < limit:
            b += jump
            a = 1
        del a
        return r,g,b
    def get_legend(self):
        r,g,b = 0,0,0
        re = []
        for p in self.maps[self.map]:
            r,g,b = self.colour_manager(r,g,b)
            re.append([p[0],(r,g,b)])
        return re
    def draw_points(self):
        r,g,b = 0,0,0
        for p in self.maps[self.map]:
            r,g,b = self.colour_manager(r,g,b)
            self.set_at((p[1],p[2]),(r,g,b))
        del r,g,b
    def draw(self,win):
        self.gen_map()
        self.draw_points()
        win.blit(self.win,self.pos)
        win.blit(self.overlay,(self.pos[0]-self.osz,self.pos[1]-self.osz))
        self.overlay = pg.Surface((self.size[0]+self.osz*2,self.size[1]+self.osz*2),pg.SRCALPHA,32)
    def hover(self,pos,**kwargs):
        pg.draw.line(self.overlay,(255,255,255),
            (pos[0]-40-self.pos[0]+self.osz,
            pos[1]-10-self.pos[1]+self.osz),
            (pos[0]+40-self.pos[0]+self.osz,
            pos[1]-10-self.pos[1]+self.osz)
        )
        font_ = pg.font.SysFont(FONT,FONT_SIZE-2)
        self.overlay.blit(font_.render(str(pos),1,(0,0,0)),(
            pos[0]-font_.size(str(pos))[0]//2-self.pos[0]+self.osz,
            pos[1]-30-self.pos[1]+self.osz
        ))
        # ADDITIONALLY RENDER NAMES OF POINTS NEARBY CURSOR
        del font_
    def click(self,pos):
        print(f"CLICKED AT {pos}")
