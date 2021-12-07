import pygame as pg
from pygame import font

WIDTH, HEIGHT = 640,480
LABEL_COLOUR = (50,50,50)
BUTTON_COLOUR = (80,80,80)
BUTTON_COLOUR2 = (50,50,50)
BACKGROUND_COLOR = (20,20,20)
FONT = "dejavusans"
FONT_SIZE = 16
TITLE = "Minecraft"

class Base:
    def __init__(self,pos,size,tags=[],parent=None):
        self.tag = tags
        self.pos = pos
        self.size = size
        self.parent = parent
    def get_adopted(self,parent):
        self.parent = parent
    def const_rect(self):
        return pg.Rect(self.pos[0],self.pos[1],self.size[0],self.size[1])
    def over(self,v,**kwargs):
        if v and "pos" in tuple(kwargs.keys()): self.hover(**kwargs)
    def tick(self,**kwargs):
        pass
    def hover(self,pos):
        pass
    def draw(self,win):
        pg.draw.rect(win,BUTTON_COLOUR2,self.const_rect())
    def click(self,pos):
        pass

class Image(Base):
    def __init__(self,pos,size,surface=None,parent=None):
        super().__init__(pos,size,[],parent)
        if surface == None:
            self.surface = pg.Surface(self.size)
        else:
            self.surface = pg.Surface(self.size)
            self.surface.blit(surface,(0,0))
    def draw(self,win):
        win.blit(self.surface,self.pos)

class Label(Base):
    def __init__(self,pos,size,text,fontsize=FONT_SIZE,colour=LABEL_COLOUR,parent=None):
        super().__init__(pos,size,[],parent)
        self.text = text
        self.fontsize = fontsize
        self.bc = colour
    def draw(self,win):
        pg.draw.rect(win,self.bc,self.const_rect())
        font = pg.font.SysFont(FONT,self.fontsize)
        win.blit(font.render(str(self.text),1,(255,255,255)),
            (
                self.pos[0] + self.size[0]//2 - font.size(str(self.text))[0]//2
                ,
                self.pos[1] + self.size[1]//2 - font.size(str(self.text))[1]//2
            )
        )
    def const_rect(self):
        return pg.Rect(self.pos[0],self.pos[1],self.size[0],self.size[1])

class Button(Label):
    def __init__(self,pos,size,text,func,fontsize=FONT_SIZE,colour=BUTTON_COLOUR,colour2=BUTTON_COLOUR2,parent=None):
        super().__init__(pos,size,text,fontsize,colour,parent)
        self.func = func
        self.bc2 = colour2
        self.over_ = False
        self.tag = ["click","over"]
    def over(self,state,**kwargs):
        if self.over_ != state:
            self.over_ = state
            self.bc,self.bc2 = self.bc2,self.bc
    def click(self,pos,**kwargs):
        self.func(self)

class Screen:
    def __init__(self):
        self.objects = []
    def load(self):
        pass

class Dynamic_Table(Base):
    def __init__(self,pos,size,func,font_size=FONT_SIZE,parent=None):
        super().__init__(pos,size,["tick"],parent)
        self.func = func
        self.bc = BUTTON_COLOUR2
        self.font_size = font_size
    def draw(self,win):
        data = self.func()
        font_ = pg.font.SysFont("dejavusans",self.font_size)
        pg.draw.rect(win,self.bc,self.const_rect())
        for x,p in enumerate(data):
            if len(p) > 1:
                win.blit(font_.render(p[0],1,p[1]),(self.pos[0]+5,self.pos[1]+5+x*font_.size(p[0])[1]))
            else:
                win.blit(font_.render(p[0],1,(255,255,255)),(self.pos[0]+5,self.pos[1]+5+x*font_.size(p[0])[1]))
        del data, font_
    def const_rect(self):
        return pg.Rect(self.pos[0],self.pos[1],self.size[0],self.size[1])