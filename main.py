import pygame as pg
from classes import *
from map import Map_Object
pg.init()

class Main:
    def __init__(self):
        self.win = pg.display.set_mode((WIDTH,HEIGHT))
        self.clock = pg.time.Clock()
        self.run = True
        self.screens = {"default":Screen()}
        self.current_screen = "default"
    def change_screen(self,ID):
        if ID in self.screens.keys():
            self.last_screen = self.current_screen
            self.current_screen = ID
            pg.display.set_caption(f"{TITLE}/{ID}")
        else:
            raise ValueError("Given ID is not valid - no screen with given ID")
    def screen(self):
        if self.current_screen != None:
            return self.screens[self.current_screen]
        else:
            raise ValueError("Screens are not handled properly.")
    def confirm_fin(self,v,r):
        self.change_screen(self.last_screen)
        r[0]=v
    def confirm_over(self,q,t,f,r):
        self.screens["__confirm__"] = Screen()
        back = Image((0,0),(WIDTH,HEIGHT),self.win)
        black = pg.Surface((WIDTH,HEIGHT),pg.SRCALPHA,32)
        black.fill((0,0,0,150))
        back.surface.blit(black,(0,0))
        self.screens["__confirm__"].objects.append(back)
        font_ = pg.font.SysFont(FONT,12) 
        self.screens["__confirm__"].objects.append(Label((WIDTH//2-100,HEIGHT//2-150),(200,100),q))
        self.screens["__confirm__"].objects.append(Button((WIDTH//2-250,HEIGHT//2),(200,100),t,lambda a: self.confirm_fin(True,r)))
        self.screens["__confirm__"].objects.append(Button((WIDTH//2+50,HEIGHT//2),(200,100),f,lambda a: self.confirm_fin(False,r)))
        self.change_screen("__confirm__")
        del font_
        del black
    def __call__(self):
        while self.run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.run = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for obj in [x for x in self.screen().objects if "click" in x.tag]:
                            if obj.const_rect().collidepoint(pg.mouse.get_pos()): obj.click(pg.mouse.get_pos())   
                if event.type == pg.KEYDOWN:
                    for obj in [x for x in self.screen().objects if "keyboard" in x.tag]:
                        obj.key(event.key) 
            for obj in [x for x in self.screen().objects if "over" in x.tag]:
                if obj.const_rect().collidepoint(pg.mouse.get_pos()): obj.over(True,pos=pg.mouse.get_pos())
                else: obj.over(False)
            self.win.fill(BACKGROUND_COLOR)
            [x.draw(self.win) for x in self.screen().objects]
            pg.display.update()
            self.clock.tick(60)
    def turn_off(self):
        self.run = False

if __name__ == "__main__":
    M = Main()
    test_value = [0]
    pg.display.set_caption(f"{TITLE}/{M.current_screen}")
    M.screens["map"]=Screen()
    M.screens["default"].objects.append(Button((10,10),(100,50),"MAP",lambda self: M.change_screen("map")))
    M.screens["default"].objects.append(Button((10,420),(100,50),"EXIT",lambda self: M.turn_off()))
    map_o = Map_Object((WIDTH-395,10),(385,385),M)
    map_o.load_file("./pointers.json")
    print(map_o.map)
    #map_o.gen_conf()
    M.screens["map"].objects.append(map_o)
    M.screens["map"].objects.append(Button((10,420),(100,50),"Back",lambda self: M.change_screen("default")))
    M.screens["map"].objects.append(Label((10,10),(100,50),map_o.coords))
    M.screens["map"].objects.append(Label((10,300),(100,50),test_value))
    M.screens["map"].objects.append(Button((10,360),(100,50),"Test",lambda self: M.confirm_over("Do you want to change camera position?","Yes","No",test_value)))
    M.screens["map"].objects.append(Dynamic_Table((10,10),(160,280),map_o.get_legend,16))
    M()
