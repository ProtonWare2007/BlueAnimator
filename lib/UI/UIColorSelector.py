import pygame,math,time
from lib.const import*

class UIColorSelector:
    def __init__(self, posx, posy, thickness, HMargin, VMargin):
        self.thickness = thickness
        self.Size = 256
        self.HMargin, self.VMargin = HMargin, VMargin
        self.posx, self.posy = posx, posy
        self.colorSurfaces = list()
        self.colorIndex = 0
        self.onResizef = None
        self.onColorSelectionf = None
        self.selectedColor = BLACK
        self.borderSurface = pygame.Surface((self.thickness*2+self.Size,self.thickness*2+self.Size))
        self.borderSurface.fill(BLACK)

    def createColorRect(self,app,resizeUI):
        for blue in range(0, 256, 1):
            colorImg = pygame.Surface((256, 256))
            colorImg.lock()
            for green in range(0, 256, 1):
                for red in range(0, 256, 1):
                    colorImg.set_at((red, green), (red, green, blue))
            colorImg.unlock()
            self.colorSurfaces.append(colorImg)
            app.loadingBarRect.width += 2
        app.setTitle("BlueAnimator v0.5 alpha")
        app.started = True
        resizeUI()
    
    def __mouseOnRect(self, mousex, mousey):
        if self.posx + self.thickness <= mousex <= self.posx + self.thickness + self.Size:
            if self.posy + self.thickness <= mousey <= self.posy + self.thickness + self.Size:
                return True
        return False

    def onResize(self, func):
        self.onResizef = func
	
    def onColorSelected(self, func):
        self.onColorSelectionf = func

    def handleEvents(self, event):
        mx, my = pygame.mouse.get_pos()
        
        if self.onResizef != None:
            if event.type == (pygame.WINDOWRESIZED or pygame.WINDOWMAXIMIZED or pygame.WINDOWMINIMIZED):
                self.onResizef(self)
        
        if self.__mouseOnRect(mx, my):
            if event.type == pygame.MOUSEWHEEL:
                if event.y == 1 and self.colorIndex < len(self.colorSurfaces) - 1:
                    self.colorIndex += 1
                elif event.y == -1 and self.colorIndex > 0:
                    self.colorIndex -= 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                px, py = mx - self.posx - self.thickness, my - self.posy - self.thickness
                self.selectedColor = self.colorSurfaces[self.colorIndex].get_at((px,py))
                if self.onColorSelectionf != None:
                     self.onColorSelectionf(self)

    def show(self, frame):
        frame.window.blit(self.borderSurface,(self.posx,self.posy))
        frame.window.blit(self.colorSurfaces[self.colorIndex], (self.posx + self.thickness, self.posy + self.thickness))
