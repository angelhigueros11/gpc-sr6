# Graficas por computador
# Angel Higueros - 20460
# SR6

import struct

from cube import *
from texture import *
from vector import *
from utils import *
from matrices import *
from math import *

# Métodos de escritura


def char(c):
    return struct.pack('=c', c.encode('ascii'))


def word(w):
    return struct.pack('=h', w)


def dword(d):
    return struct.pack('=l', d)


def color(r, g, b):
    return bytes([b, g, r])


def cross(v1, v2):
    return V3(
        v1.y * v2.z - v1.z * v2.y,
        v1.z * v2.x - v1.x * v2.z,
        v1.x * v2.y - v1.y * v2.x,
    )


def bounding_box(v1, v2, v3):
    x = [v1.x, v2.x, v3.x]
    y = [v1.y, v2.y, v3.y]

    x.sort()
    y.sort()

    return V3(x[0], y[0], 0), V3(x[-1], y[-1], 0)


def barycentric(v1, v2, v3, v4):
    c = cross(
        V3(v2.x - v1.x, v3.x - v1.x, v1.x - v4.x),
        V3(v2.y - v1.y, v3.y - v1.y, v1.y - v4.y)
    )

    if c.z == 0:
        return -1, -1, -1

    return (
        c.x / c.z, c.y / c.z,
        1 - ((c.x + c.y) / c.z)
    )


class Render(object):
    def __init__(self, filename):
        self.filename = filename
        self.width = 100
        self.height = 100
        self.width_vertex = 100
        self.height_vertex = 100
        self.current_color = color(255, 255, 255)  # por defecto blanco
        self.framebuffer = []
        self.background_color = color(0, 0, 0)  # por defecto negro
        self.x_vertex = None
        self.y_vertex = None
        self.Model = None
        self.Texture = None
        self.projection = []
        self.glClear()

    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height

    def glClear(self):
        self.framebuffer = [[self.background_color for _ in range(
            self.width)] for _ in range(self.height)]
        self.zbuffer = [
            [-99999 for _ in range(self.width)] for _ in range(self.height)]

    def glVertex(self, cords):
        vertex_x = (self.width_vertex / 2) + (cords[0] * self.width_vertex / 2)
        vertex_y = (self.height_vertex / 2) + \
            (-cords[1] * self.height_vertex / 2)
        x = self.x_vertex + vertex_x
        y = self.y_vertex + vertex_y

        self.framebuffer[
            int(x)][int(y)
                    ] = self.current_color

    def glViewPort(self, cords, width, height):
        self.width_vertex, self.height_vertex = width - 1, height - 1
        self.x_vertex, self.y_vertex = cords

    def point(self, x, y):
        if 0 < x < self.width and 0 < y < self.height:
            self.framebuffer[x][y] = self.current_color

    def line(self, v1, v2):
        x0 = round(v1.x)
        y0 = round(v1.y)
        x1 = round(v2.x)
        y1 = round(v2.y)

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dy = abs(y1 - y0)
        dx = x1 - x0

        offset = 0
        threshold = dx
        y = y0

        for x in range(x0, x1 + 1):
            if steep:
                self.point(x, y)
            else:
                self.point(y, x)

            offset += dy * 2

            if offset >= threshold:
                y += 1 if y0 < y1 else -1
                # threshold += 1 * dx * 2
                threshold += dx * 2

    def glColor(self, r, g, b):
        self.current_color = color(r, g, b)

    def lookAt(self, eye, center, up):
        eye = V3(*eye)
        center = V3(*center)
        up = V3(*up)

        z = normalize(eye - center)
        x = normalize(cross(up, z))
        y = normalize(cross(z, x))

        m = [
            [x.x, x.y, x.z, 0],
            [y.x, y.y, y.z, 0],
            [z.x, z.y, z.z, 0],
            [0, 0, 0, 1]
        ]

        o = [
            [1, 0, 0, -center.x],
            [0, 1, 0, -center.y],
            [0, 0, 1, -center.z],
            [0, 0, 0, 1]
        ]

        self.view = mult(m, o)

        self.projection = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, -0.001, 1]
        ]

        d = self.width_vertex / 4
        l = self.height_vertex / 4

        self.Viewport = [
            [d, 0, 0, d],
            [0, l, 0, l],
            [0, 0, 128, 128],
            [0, 0, 0, 1]
        ]

    def glFinish(self):
        with open(self.filename, 'bw') as f:
            # Pixel header
            f.write(char('B'))
            f.write(char('M'))
            # tamaño archivo = 14 header + 40  info header + resolucion
            f.write(dword(14 + 40 + self.width * self.height * 3))
            f.write(word(0))
            f.write(word(0))
            f.write(dword(14 + 40))

            # Info header
            f.write(dword(40))  # tamaño header
            f.write(dword(self.width))  # ancho
            f.write(dword(self.height))  # alto
            f.write(word(1))  # numero de planos (siempre 1)
            f.write(word(24))  # bits por pixel (24 - rgb)
            f.write(dword(0))  # compresion
            # tamaño imagen sin header
            f.write(dword(self.width * self.height * 3))
            f.write(dword(0))  # resolucion
            f.write(dword(0))  # resolucion
            f.write(dword(0))  # resolucion
            f.write(dword(0))  # resolucion

            for y in range(self.height-1, -1, -1):
                for x in range(self.width):
                    f.write(self.framebuffer[x][y])

    def triangle(self, v1, v2, v3, cords, light):

        m, n = bounding_box(v1, v2, v3)

        # a, b, c = vertices

        # if self.texture:
        #     ta, tb, tc = tvertices

        # luz = V3(0, 0, 1)
        # n = (b - a) * (c - a)
        # i = n.norm() @ luz.norm()

        # if i < 0:
        #     return

        # grey = round(255 * i)
        # self.glColor(grey,  grey, grey)

        for x in range(m.x, n.x):
            for y in range(m.y, n.y):
                w, v, u = barycentric(v1, v2, v3, V3(x, y))

                if w < 0 or v < 0 or u < 0:
                    continue

                if self.Texture:
                    tx = (cords[0].x * w) + (cords[1].x * v) + (cords[2].x * u)
                    ty = (cords[0].y * w) + (cords[1].y * v) + (cords[2].y * u)

                    self.current_color = self.Texture.get_color_with_intensity(
                        tx, ty, light
                    )

                z = (v1.z * w) + (v2.z * v) + (v3.z * u)

                # if (self.zBuffer[x][y] < z):
                #     self.zBuffer[x][y] = z

                #     if self.texture:
                #         tx = ta.x * w + tb.x + u + tc.x * v
                #         ty = ta.y * w + tb.y + u + tc.y * v

                #         self.current_color = self.texture.get_color_with_intensity(tx, ty, i)

                #         self.get_
                #     self.point(y, x)
                if z > self.zbuffer[
                        int(
                        self.x_vertex +
                        (self.width_vertex/2) +
                        (x / self.width * self.width_vertex / 2))
                    ][
                        int(self.y_vertex + (self.height_vertex / 2) +
                            (-y / self.height * self.height_vertex / 2))
                ]:
                    self.zbuffer[
                        int(
                            self.x_vertex +
                            (self.width_vertex/2) +
                            (x / self.width * self.width_vertex/2))
                    ][
                        int(self.y_vertex +
                            (self.height_vertex/2) +
                            (-y / self.height * self.height_vertex/2))
                    ] = z
                    self.glVertex((x / self.width, y / self.height))

    def transform_vertex(self, vertex):
        t_vertex = multmv(
            self.Viewport,
            multmv(
                self.projection,
                multmv(
                    self.view,
                    multmv(
                        self.Model, [
                            vertex[0],
                            vertex[1],
                            vertex[2],
                            1
                        ]
                    )
                )
            )
        )
        return V3(
            round(t_vertex[0] / t_vertex[3]),
            round(t_vertex[1] / t_vertex[3]),
            round(t_vertex[2] / t_vertex[3]),
        )

    def load_model(self, filename, scale_factor, translate_factor, rotate_factor):
        obj = Obj(filename)
        self.Model = load_matrix(translate_factor, scale_factor, rotate_factor)

        for face in obj.faces:

            if len(face) == 3:
                load_triangle_3(face, self.transform_vertex,
                                obj, self.Texture, self.triangle)

            if len(face) == 4:
                load_triangle_4(face, self.transform_vertex,
                                obj, self.Texture, self.triangle)


# IMPLEMENTACION
r = Render('normal.bmp')
r.glCreateWindow(600, 600)
r.glViewPort((0, 0), 600, 600)
r.glClear()

r.Texture = Texture('./model.bmp')
render_config = {
    "normal": {
        "type": ([0, 0, 1], [0, 0, 0], [0, 1, 0]),
        "scale": (2, 2, 2),
        "translate": (-1, -1, 0),
        "rotate": (0, 0, 0),
    }
}

type_render = "normal"
r.lookAt(*render_config[type_render]["type"])
r.load_model(
    './model.obj',
    render_config[type_render]["scale"],
    render_config[type_render]["translate"],
    render_config[type_render]["rotate"]
)
r.glFinish()
