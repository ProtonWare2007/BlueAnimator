import pygame

class Exporter:
    def __init__(self):
        pass

    def export(self, canvas, app):
        posx, posy = canvas.posx, canvas.posy
        width, height = canvas.HSize - 2 * canvas.borderThickness,\
			canvas.VSize - 2 * canvas.borderThickness
        frames = canvas.frames
        data = bytearray(list())
        data.append(canvas.FPS)
        bytedata = width.to_bytes(2, "big")
        
        for index in range(0, len(bytedata), 1):
            data.append(bytedata[index])
        bytedata = height.to_bytes(2, "big")
        for index in range(0, len(bytedata), 1):
            data.append(bytedata[index])
        
        canvas.isexporting = True
        
        for frameindex in range(0, len(frames), 1):
            canvas.frame = frameindex
            canvas.show(app)
            pygame.display.update()
            for y in range(0, height, 1):
                for x in range(0, width, 1):
                    pixel = frames[frameindex].get_at((x, y))
                    for value_index in range(0,3,1):
                        data.append(pixel[value_index])
        
        canvas.isexporting = False
        
        with open("./output.smedia", "wb") as output:
            output.write(data)
