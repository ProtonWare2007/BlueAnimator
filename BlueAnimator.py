import pygame, sys
import threading

from lib.ExportEngine import Exporter
from lib.UI.UIBox import UIBox
from lib.UI.UIColorSelector import UIColorSelector
from lib.UI.Canvas import Canvas

from lib.const import*

class MainApp:
    def __init__(self, size: tuple):
        self.width, self.height = size
        self.window = pygame.display.set_mode(size, pygame.RESIZABLE)
        pygame.display.set_caption("BlueAnimator - loading")
        icon = pygame.image.load("BlueAnimator.png")
        pygame.display.set_icon(icon)
        self.components = list()
        self.started = False
        self.clock = pygame.time.Clock()
        font = pygame.font.Font("freesansbold.ttf", size=60)
        self.textname = font.render("BlueAnimator", True, WHITE)
        font = pygame.font.Font("freesansbold.ttf", size=40)
        self.textstatus = font.render("is loading", True, WHITE)
        font = pygame.font.Font("freesansbold.ttf", size=20)
        self.pub = font.render("made by ProtonWare", True, WHITE)
        self.font = pygame.font.Font("freesansbold.ttf", size=40)
        self.loadingBarRect = pygame.Rect(50,self.height - 100,0,40)
        self.counter = 1
        self.running = True

    def add(self, component):
        self.components.append(component)
    
    def setTitle(self, title:str):
        pygame.display.set_caption(title)
    
    def resize(self, size):
        self.width, self.height = size
        self.window = pygame.display.set_mode(size, pygame.RESIZABLE)
    
    def __loading(self):
        self.window.fill((0,0,180))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        self.counter = (self.counter + 1) % 4
        self.textstatus = self.font.render("is loading"+"."*self.counter, True, WHITE)
        self.window.blit(self.textname,(self.width//10,self.height//3))
        self.window.blit(self.textstatus,(self.width//2,self.height//2))
        self.window.blit(self.pub,(20,self.height - 40))
        pygame.draw.rect(self.window,BLACK,((40,self.height-110),(256*2+20,60)),10)
        pygame.draw.rect(self.window,WHITE,self.loadingBarRect)
        self.clock.tick(10)

    def mainloop(self):	
        while self.running:
            if self.started:
                self.window.fill(LIGHTGRAY)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit(0)
                    for component in self.components:
                        component.handleEvents(event)

                for component in self.components:
                    component.show(self)
            else:
                self.__loading()
            self.width, self.height = self.window.get_size()
            #self.loadingBarRect.height = self.height - 100
            pygame.display.update()

def windowResized(bar):
    if bar.id == "menu":
        bar.HSize = app.window.get_size()[0]
    if bar.id == "toolBox1" or bar.id == "toolBox2":
        bar.posx = app.window.get_size()[0] - bar.HSize
    if bar.id == "toolBox2":
        bar.posy = 136	
    bar.resizeBar()

def change_size(box,entry):
    if box.id == "menu":
        if not entry.text.startswith("Frame") and not entry.text.startswith("FPS"):
            entry.setSize(40)
    elif box.id == "toolBox1":
        entry.setSize(23)
    elif box.id == "toolBox2":
        if not entry.text.startswith("Layer"):
            entry.setSize(30)
    if entry.text.startswith(">") or entry.text.startswith("<"):
        entry.setColor(RED)
    else:
        entry.setColor(BLUE)

def reset_size(box,entry):
    if box.id == "menu":
        entry.setSize(30)
    elif box.id == "toolBox1":
	    entry.setSize(20)
    elif box.id == "toolBox2":
        entry.setSize(25)
    entry.setColor(BLACK)
    
def ui_color_windowResized(color_selector):
	color_selector.posx = app.window.get_size()[0] - color_selector.Size - color_selector.thickness*2

def onColorSelection(color_selector):
	canvas.color = color_selector.selectedColor
	canvas.current_color = canvas.color
	canvas.cursor_color = canvas.color

def entryClicked(box,entry):
    if box.id == "menu":
        if entry.text == "Exit":
            pygame.quit()
            sys.exit(0)
        elif entry.text == ">":
            canvas.frame += 1
            if not canvas.frameExists():
                canvas.addFrame()
            frame_entry.text = "Frame:" + str(canvas.frame + 1)
            canvas.updateOnionSkin()
        elif entry.text == "<":
            if canvas.frame > 0:
                canvas.frame -= 1
                frame_entry.text = "Frame:" + str(canvas.frame + 1)
            canvas.updateOnionSkin()
        elif entry.text == ">>":
            canvas.FPS += 1
            fps.text = "FPS:" + str(canvas.FPS)
        elif entry.text == "<<":
            if canvas.FPS > 1:
                canvas.FPS -= 1
                fps.text = "FPS:" + str(canvas.FPS)
        elif entry.text == "Export":
            exporter.export(canvas, app)
    elif box.id == "toolBox2":
        if entry.text == ">":
            canvas.layer += 1
            if not canvas.layerExists():
                canvas.addLayer()
            layer_entry.text = "Layer:" + str(canvas.layer + 1)
            #canvas.updateOnionSkin()
        elif entry.text == "<":
            if canvas.layer > 0:
                canvas.layer -= 1
                layer_entry.text = "Layer:" + str(canvas.layer + 1)
            #canvas.updateOnionSkin()
		
    if entry.text == "PenTool":
        canvas.setTool("pen")
    elif entry.text == "EraserTool":
        canvas.setTool("eraser")

def loadDimensions():
	try:
		with open("paper.dim") as file:
			width = int(file.readline())
			height = int(file.readline())
			return (width,height)
	except Exception:
		sys.exit(0x01)

def resizeUI():
    windowResized(menu)
    windowResized(toolBox1)
    windowResized(toolBox2)
    ui_color_windowResized(uiColorSelector)

canvas_width, canvas_height = loadDimensions()

if canvas_width > 974:
	win_width = canvas_width
else:
	win_width = 974
if canvas_height > 600 - 70:
	win_height = canvas_height + 70
else:
	win_height = 600

pygame.init()
exporter = Exporter()
app = MainApp((win_width, win_height))
canvas = Canvas(0, 70, canvas_width, canvas_height)

menu = UIBox("menu", 0, 0, 8, 8, 8)
toolBox1 = UIBox("toolBox1", 0, 70, 8, 14, 14)
toolBox2 = UIBox("toolBox2", 0, 70, 8, 14, 14)
uiColorSelector = UIColorSelector(0, 210, 8, 14, 14)

menu.addEntry("Export", BLACK, 30)
menu.addEntry("<", BLACK, 30)
frame_entry = menu.addEntry("Frame:1", BLACK, 30)
menu.addEntry(">", BLACK, 30)
menu.addEntry("<<", BLACK, 30)
fps = menu.addEntry("FPS:1", BLACK, 30)
menu.addEntry(">>", BLACK, 30)
menu.addEntry("Exit", BLACK, 30)

toolBox1.addEntry("PenTool", BLACK, 20)
toolBox1.addEntry("EraserTool", BLACK, 20)
toolBox2.addEntry("<", BLACK, 25)
layer_entry = toolBox2.addEntry("Layer:1", BLACK, 25)
toolBox2.addEntry(">", BLACK, 25)

menu.onHover(change_size)
menu.notOnHover(reset_size)
menu.onClick(entryClicked)
menu.onResize(windowResized)

toolBox1.onHover(change_size)
toolBox1.notOnHover(reset_size)
toolBox1.onResize(windowResized)
toolBox1.onClick(entryClicked)

toolBox2.onHover(change_size)
toolBox2.notOnHover(reset_size)
toolBox2.onResize(windowResized)
toolBox2.onClick(entryClicked)

uiColorSelector.onResize(ui_color_windowResized)
uiColorSelector.onColorSelected(onColorSelection)
loader = threading.Thread(target=uiColorSelector.createColorRect,args=(app,resizeUI))
loader.start()

app.add(canvas)
app.add(menu)
app.add(toolBox1)
app.add(toolBox2)
app.add(uiColorSelector)
app.mainloop()
