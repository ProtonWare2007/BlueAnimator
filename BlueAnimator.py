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
        self.components = list()

    def add(self, component):
        self.components.append(component)
    
    def setTitle(self, title:str):
        pygame.display.set_caption(title)
    
    def resize(self, size):
        self.width, self.height = size
        self.window = pygame.display.set_mode(size, pygame.RESIZABLE)

    def mainloop(self):
        while True:
            self.window.fill(LIGHTGRAY)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                for component in self.components:
                    component.handleEvents(event)

            for component in self.components:
                component.show(self)
            
            self.width, self.height = self.window.get_size()
            pygame.display.update()

def windowResized(bar):
    bar.HSize = app.window.get_size()[0]
    bar.resizeBar()

def tool_box_windowResized(bar):
    bar.posx = app.window.get_size()[0] - bar.HSize
    bar.resizeBar()

def change_size(entry):
    if not entry.text.startswith("Frame") and not entry.text.startswith("FPS"):
        entry.setSize(40)
        if entry.text.startswith(">") or entry.text.startswith("<"):
            entry.setColor(RED)
        else:
            entry.setColor(BLUE)

def tool_box_change(entry):
	entry.setSize(23)
	entry.setColor(BLUE)

def tool_box_reset(entry):
	entry.setSize(20)
	entry.setColor(BLACK)

def tool_box_entryClicked(entry):
	if entry.text == "PenTool":
		canvas.setTool("pen")
	elif entry.text == "EraserTool":
		canvas.setTool("eraser")

def reset_size(entry):
    entry.setSize(30)
    entry.setColor(BLACK)
    
def ui_color_windowResized(color_selector):
	color_selector.posx = app.window.get_size()[0] - color_selector.Size - color_selector.thickness*2

def onColorSelection(color_selector):
	canvas.color = color_selector.selectedColor
	canvas.current_color = canvas.color
	canvas.cursor_color = canvas.color

def entryClicked(entry):
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


def loadDimensions():
	try:
		with open("paper.dim") as file:
			width = int(file.readline())
			height = int(file.readline())
			return (width,height)
	except Exception:
		sys.exit(0x01)

def load():
	uiColorSelector.load()

def loadingView():
    loadingWindow = pygame.display.set_mode((600,400),pygame.NOFRAME)
    pygame.display.set_caption("BlueAnimator - loading")
    icon = pygame.image.load("BlueAnimator.png")
    pygame.display.set_icon(icon)
    font = pygame.font.Font("freesansbold.ttf", size=60)
    textname = font.render("BlueAnimator", True, WHITE)
    font = pygame.font.Font("freesansbold.ttf", size=40)
    textstatus = font.render("is loading", True, WHITE)
    font = pygame.font.Font("freesansbold.ttf", size=30)
    pub = font.render("made by ProtonWare", True, WHITE)
    font = pygame.font.Font("freesansbold.ttf", size=40)
    clock = pygame.time.Clock()
    counter = 1
    while running:
        loadingWindow.fill((0,0,180))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        counter = (counter + 1) % 4
        textstatus = font.render("is loading"+"."*counter, True, WHITE)
        loadingWindow.blit(textname,(60,120))
        loadingWindow.blit(textstatus,(320,200))
        loadingWindow.blit(pub,(20,340))
        clock.tick(10)
        pygame.display.update()
	

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

canvas = Canvas(0, 70, canvas_width, canvas_height)

menu = UIBox(0, 0, 8, 8, 8)
toolBox = UIBox(0, 70, 8, 14, 14)
uiColorSelector = UIColorSelector(0, 200, 8, 14, 14)

menu.addEntry("Export", BLACK, 30)
menu.addEntry("<", BLACK, 30)
frame_entry = menu.addEntry("Frame:1", BLACK, 30)
menu.addEntry(">", BLACK, 30)
menu.addEntry("<<", BLACK, 30)
fps = menu.addEntry("FPS:1", BLACK, 30)
menu.addEntry(">>", BLACK, 30)
menu.addEntry("Exit", BLACK, 30)

toolBox.addEntry("PenTool", BLACK, 20)
toolBox.addEntry("EraserTool", BLACK, 20)

menu.onHover(change_size)
menu.notOnHover(reset_size)
menu.onClick(entryClicked)
menu.onResize(windowResized)

toolBox.onHover(tool_box_change)
toolBox.notOnHover(tool_box_reset)
toolBox.onResize(tool_box_windowResized)
toolBox.onClick(tool_box_entryClicked)

uiColorSelector.onResize(ui_color_windowResized)
uiColorSelector.onColorSelected(onColorSelection)

running = True
loader = threading.Thread(target=load)
loadingViewer = threading.Thread(target=loadingView)
loader.start()
loadingViewer.start()
loader.join()
running = False

app = MainApp((win_width, win_height))
app.setTitle("BlueAnimator")
windowResized(menu)
tool_box_windowResized(toolBox)
ui_color_windowResized(uiColorSelector)
app.add(menu)
app.add(toolBox)
app.add(uiColorSelector)
app.add(canvas)
app.mainloop()
