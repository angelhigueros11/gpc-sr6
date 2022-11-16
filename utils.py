# Graficas por computador
# Angel Higueros - 20460
# SR6

from vector import *
from math import *
from matrices import *

light = V3(0, 0, 1)


def cross(v1, v2):
    return V3(
        v1.y * v2.z - v1.z * v2.y,
        v1.z * v2.x - v1.x * v2.z,
        v1.x * v2.y - v1.y * v2.x,
    )


def load_triangle_3(face, transform_vertex, obj, texture, triangle):
    f1 = face[0][0] - 1
    f2 = face[1][0] - 1
    f3 = face[2][0] - 1

    v1 = transform_vertex(obj.vertex[f1])
    v2 = transform_vertex(obj.vertex[f2])
    v3 = transform_vertex(obj.vertex[f3])

    bright = (normalize(cross((v2 - v1), (v3 - v1))) @ light)

    if texture:

        fa = face[0][1] - 1
        fb = face[1][1] - 1
        fc = face[2][1] - 1

        t1 = V3(*obj.tvertex[fa])
        t2 = V3(*obj.tvertex[fb])
        t3 = V3(*obj.tvertex[fc])

        triangle(
            v2, v1, v3,
            cords=(t1, t3, t2),
            light=bright
        )

    elif bright >= 0:
        triangle(
            v1, v2, v3,
            bytes([bright, bright, bright])
        )


def load_triangle_4(face, transform_vertex, obj, texture, triangle):
    f1 = face[0][0] - 1
    f2 = face[1][0] - 1
    f3 = face[2][0] - 1
    f4 = face[3][0] - 1

    v1 = transform_vertex(obj.vertex[f1])
    v2 = transform_vertex(obj.vertex[f2])
    v3 = transform_vertex(obj.vertex[f3])
    v4 = transform_vertex(obj.vertex[f4])

    bright = (normalize(cross((v2 - v1), (v3 - v1))) @ light)

    if texture:
        fa = face[0][1] - 1
        fb = face[1][1] - 1
        fc = face[2][1] - 1
        f42 = face[3][1] - 1

        t1 = V3(*obj.tvertex[fa])
        t2 = V3(*obj.tvertex[fb])
        t3 = V3(*obj.tvertex[fc])
        t4 = V3(*obj.tvertex[f42])

        triangle(
            v1, v3, v2,
            cords=(t1, t3, t2),
            light=bright
        )
        triangle(
            v1, v4, v3,
            cords=(t1, t4, t3),
            light=bright
        )

    else:
        triangle(
            v1, v3, v2,
            bytes([bright, bright, bright])
        )
        triangle(
            v1, v4, v3,
            bytes([bright, bright, bright])
        )


def load_matrix(translate_factor, scale_factor, rotate):
    translate_factor = V3(*translate_factor)
    scale_factor = V3(*scale_factor)
    rotate = V3(*rotate)

    transition_matrix = [
        [1, 0, 0, translate_factor.x],
        [0, 1, 0, translate_factor.y],
        [0, 0, 1, translate_factor.z],
        [0, 0, 0, 1]
    ]

    scale_matrix = [
        [scale_factor.x, 0, 0, 0],
        [0, scale_factor.y, 0, 0],
        [0, 0, scale_factor.z, 0],
        [0, 0, 0, 1]
    ]

    a = rotate.x
    rotation_x = [
        [1, 0, 0, 0],
        [0, cos(a), -sin(a), 0],
        [0, sin(a), cos(a), 0],
        [0, 0, 0, 1]
    ]

    a = rotate.y
    rotation_y = [
        [cos(a), 0, sin(a), 0],
        [0, 1, 0, 0],
        [-sin(a), 0,  cos(a), 0],
        [0, 0, 0, 1]
    ]

    a = rotate.z
    rotation_z = [
        [cos(a), -sin(a), 0, 0],
        [sin(a), cos(a), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]

    first = mult(rotation_x, rotation_y)
    rotation_matrix = mult(first, rotation_z)

    second = mult(transition_matrix, rotation_matrix)
    return mult(second, scale_matrix)
