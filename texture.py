# Graficas por computador
# Angel Higueros - 20460
# SR6

import contextlib
import struct


def color(r, g, b):
    return bytes([b, g, r])


class Texture:
    def __init__(self, filename):
        self.filename = filename
        self.read()

    def read(self):
        with open(self.filename, "rb") as image:
            image.seek(2 + 4 + 4)
            header_size = struct.unpack("=l", image.read(4))[0]
            image.seek(2 + 4 + 4 + 4 + 4)

            self.width = struct.unpack("=l", image.read(4))[0]
            self.height = struct.unpack("=l", image.read(4))[0]

            image.seek(header_size)

            self.pixels = []
            for y in range(self.height):
                self.pixels.append([])
                for _ in range(self.width):
                    b = ord(image.read(1))
                    g = ord(image.read(1))
                    r = ord(image.read(1))
                    self.pixels[y].append(color(b, g, r))

    def get_color(self, tx, ty):
        x = int(tx * self.width)
        y = int(ty * self.height)

        return self.pixels[y][x]

    def get_color_with_intensity(self, tx, ty, intensity):
        x = round(tx * self.width)
        y = round(ty * self.height)

        with contextlib.suppress(Exception):
            int_values = list(self.pixels[y][x])

            b = round(int_values[0] * intensity)
            g = round(int_values[1] * intensity)
            r = round(int_values[2] * intensity)

            r = max(r, 0)
            g = max(g, 0)
            b = max(b, 0)

            return color(b, g, r)

# t = Texture('./model.bmp')
# r = Render()
# r.glInit('sr5-textures.bmp')
# r.glCreateWindow(1024, 1024)
# r.glViewPort(0,0, 1024, 1024)
# r.glClearColor(0, 0, 0)
# r.glClear()
# r.glColor(255,255,255)


# def load_model():
#     obj = Obj('./model.obj')
#     for face in obj.faces:
#             if len(face) == 3:
#                 f1 = face[0][1] - 1
#                 f2 = face[1][1] - 1
#                 f3 = face[2][1] - 1

#                 vt1 = V3(
#                     obj.tvertices[f1][0] * t.width,
#                     obj.tvertices[f1][1] * t.height,
#                     )
#                 vt2 = V3(
#                     obj.tvertices[f2][0] * t.width,
#                     obj.tvertices[f2][1] * t.height,
#                     )
#                 vt3 = V3(
#                     obj.tvertices[f3][0] * t.width,
#                     obj.tvertices[f3][1] * t.height,
#                     )

#                 r.line(vt1, vt2)
#                 r.line(vt2, vt3)
#                 r.line(vt3, vt1)


# r.framebuffer = t.pixels
# load_model()
# r.glFinish()
