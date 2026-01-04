import pygame
from lib.const import*

class MenuEntry:
    def __init__(self, menu, text, color, fontSize):
        self.font = pygame.font.Font("freesansbold.ttf", size=fontSize)
        self.text = text
        self.color = color
        self.antialiased = True
        self.textImg = None
        self.menu = menu
        self.width, self.height = self.font.size(self.text)
        self.__renderText()

    def __renderText(self):
        self.textImg = self.font.render(self.text, self.antialiased, self.color)

    def setColor(self, color):
        self.color = color
        self.__renderText()
        self.width, self.height = self.font.size(self.text)
        self.menu.update(self)

    def setSize(self, fontSize):
        self.font = pygame.font.Font("freesansbold.ttf", size=fontSize)
        self.__renderText()
        self.width, self.height = self.font.size(self.text)
        self.menu.update(self)


class UIBox:
    def __init__(self, identifier, posx, posy, thickness, HMargin, VMargin, HSize=None, VSize=None):
        self.id = identifier
        self.thickness = thickness
        if HSize != None:
            self.HSize = HSize
        else:
            self.HSize = self.thickness
        if VSize != None:
            self.VSize = VSize
        else:
            self.VSize = self.thickness
        self.HMargin, self.VMargin = HMargin, VMargin
        self.posx, self.posy = posx, posy
        self.onHoverf = None
        self.notOnHoverf = None
        self.onClickf = None
        self.notOnClickf = None
        self.onResizef = None
        self.entries = list()
        self.entry_index = 0
        self.previous_entry = None
        self.borderSurface = pygame.Surface((self.HSize, self.VSize))
        self.boxSurface = pygame.Surface((0, 0))

    def addEntry(self, text, color, fontSize):
        entry = MenuEntry(self, text, color, fontSize)
        self.entries.append(entry)
        self.HSize += entry.width + (self.HMargin + self.thickness*2)
        self.update(entry)
        return entry
    
    def resizeBar(self):
        new_width = self.HSize-2*self.thickness
        new_height = self.VSize-2*self.thickness
        if new_width > 0 and new_height > 0:
            self.borderSurface = pygame.Surface((self.HSize, self.VSize))
            self.boxSurface = pygame.Surface((new_width, new_height))
            self.borderSurface.fill(BLACK)
            self.boxSurface.fill(BOXGRAY)
            self.__renderText()
    
    def __renderText(self):
        HOffset = 0
        for entry in self.entries:
            self.boxSurface.blit(entry.textImg,(HOffset + self.HMargin, self.VMargin))
            HOffset += (self.HMargin  + entry.textImg.get_width())

    def update(self, entry):
        fontWidth = entry.width
        fontHeight = entry.height
        change = True
        for entry in self.entries:
            if fontHeight < entry.font.get_height():
                change = False
                break
        if change:
            self.VSize = fontHeight + (self.VMargin + self.thickness) * 2
            self.resizeBar()
            self.__renderText()
    
    def onResize(self, function):
        self.onResizef = function

    def onClick(self, function):
        self.onClickf = function

    def notOnClick(self, function):
        self.notOnClickf = function

    def onHover(self, function):
        self.onHoverf = function

    def notOnHover(self, function):
        self.notOnHoverf = function

    def __mouseOnEntry(self, entry, mx, my, hoffset):
        entryw, entryh = entry.textImg.get_size()
        if hoffset + self.posx + self.thickness <= mx <= self.thickness + hoffset + entryw + self.posx:
            if self.thickness + self.posy <= my <= entryh + self.posy + self.thickness:
                return True
        return False

    def __mouseOnBar(self, mx, my):
        if self.posx <= mx <= self.posx + self.HSize:
            if self.posy <= my <= self.posy + self.VSize:
                return True
        return False

    def handleEvents(self, event):
        mousex, mousey = pygame.mouse.get_pos()
        clicked = False
        events = {"clicked": False}
        entry, onhover = None, None
        HOffset = self.HMargin
        if self.onResizef != None:
            if event.type == (pygame.WINDOWRESIZED or pygame.WINDOWMAXIMIZED or pygame.WINDOWMINIMIZED):
                self.onResizef(self)

        if self.__mouseOnBar(mousex, mousey):
            for entry_element in self.entries:
                onhover = self.__mouseOnEntry(entry_element, mousex, mousey, HOffset)
                entry = entry_element
                if onhover:
                    if self.onHoverf != None:
                        self.onHoverf(self,entry)

                    if self.onClickf != None:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if not events["clicked"]:
                                self.onClickf(self,entry)
                            events["clicked"] = True
                        if event.type == pygame.MOUSEBUTTONUP:
                            events["clicked"] = False

                    if self.notOnClickf != None:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            events["clicked"] = True
                        if event.type == pygame.MOUSEBUTTONUP:
                            if clicked:
                                self.notOnClickf(self,entry)
                            events["clicked"] = False
                
                elif self.notOnHoverf != None:
                    self.notOnHoverf(self,entry)

                HOffset += (self.HMargin + entry.textImg.get_width())
        self.previous_entry = entry
      
    def show(self, frame):
       frame.window.blit(self.borderSurface,(self.posx, self.posy))
       frame.window.blit(self.boxSurface,(self.posx+self.thickness, self.posy+self.thickness))
