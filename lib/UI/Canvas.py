import pygame
from lib.const import*

class Canvas:
    def __init__(self, posx, posy, width, height):
        self.posx, self.posy = posx, posy
        self.HSize = width
        self.VSize = height
        self.frames = list()
        self.frame = 0
        self.thickness = 5
        self.borderThickness = 10
        self.color = BLACK
        self.current_color = BLACK
        self.cursor_color = BLACK
        self.mouseinc = False
        self.FPS = 1
        self.isexporting = False
        self.recordedPts = [[-1, -1], [-1, -1], 0]
        self.onionSurface = None
        self.addFrame()
        self.borderSurface = pygame.Surface((self.HSize, self.VSize))
        self.borderSurface.fill(BLACK)
    
    def setTool(self, tool:str):
        if tool == "pen":
            self.color = self.current_color
            self.cursor_color = self.color
        elif tool == "eraser":
            self.color = WHITE 
            self.cursor_color = BLACK

    def __mouseInCanvas(self):
        mx, my = pygame.mouse.get_pos()
        if (self.posx + self.thickness // 2 <= mx <= self.posx + self.HSize - self.thickness // 2):
            if (self.posy + self.thickness // 2 <= my <= self.posy + self.VSize - self.thickness // 2):
                self.mouseinc = True
                return
        self.mouseinc = False

    def frameExists(self):
        if self.frame < len(self.frames):
            return True
        return False

    def updateOnionSkin(self):
        if self.frame > 0:
            self.onionSurface = self.frames[self.frame - 1].copy()
            self.onionSurface.set_colorkey((255, 255, 255), pygame.RLEACCEL)
            self.onionSurface.set_alpha(50)
        else:
            self.onionSurface = None

    def addFrame(self):
        self.frames.append( pygame.Surface((self.HSize - 2 * self.borderThickness,
        self.VSize - 2 * self.borderThickness,)) )
        self.frames[self.frame].fill(WHITE)

    def handleEvents(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                pygame.display.toggle_fullscreen()
        self.__mouseInCanvas()
        if event.type == pygame.MOUSEBUTTONUP:
            self.recordedPts = [[-1, -1], [-1, -1], 0]
        if self.mouseinc:
            pygame.mouse.set_visible(False)
            if event.type == pygame.MOUSEWHEEL:
                self.thickness += event.y
                if self.thickness < 1:
                    self.thickness = 1
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    self.recordedPts[self.recordedPts[2]][0] = (
                        pygame.mouse.get_pos()[0] - self.borderThickness
                    )
                    self.recordedPts[self.recordedPts[2]][1] = (
                        pygame.mouse.get_pos()[1] - self.posy - self.borderThickness
                    )

                    if self.recordedPts[1] != [-1, -1]:
                        pygame.draw.line(
                            self.frames[self.frame],
                            self.color,
                            self.recordedPts[0],
                            self.recordedPts[1],
                            self.thickness,
                        )
                        pygame.draw.circle(
                            self.frames[self.frame],
                            self.color,
                            self.recordedPts[1],
                            self.thickness // 2,
                        )
                        self.recordedPts[0] = self.recordedPts[1].copy()

                    elif self.recordedPts[0] != [-1, -1]:
                        self.recordedPts[2] = 1

                elif pygame.mouse.get_pressed()[2]:
                    self.frames[self.frame].fill(WHITE)
        else:
            pygame.mouse.set_visible(True)

    def show(self, frame):
        frame.window.blit(self.borderSurface, (0, self.posy))
        frame.window.blit(
            self.frames[self.frame],
            (self.posx + self.borderThickness, self.posy + self.borderThickness),
        )
        if self.onionSurface != None and not self.isexporting:
            frame.window.blit(
                self.onionSurface,
                (self.posx + self.borderThickness, self.posy + self.borderThickness),
            )

        if self.mouseinc:
            pygame.draw.circle(frame.window,
                self.cursor_color,
                pygame.mouse.get_pos(),
                self.thickness,
            )
