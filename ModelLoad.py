from functools import reduce
from typing import List

import pywavefront
import numpy as np


def load_obj(path):
    obj_wf = pywavefront.Wavefront(path)
    obj_wf.parse()
    for name, material in obj_wf.materials.items():
        vertices = np.array(material.vertices, dtype=np.float32)
        vertices.resize((vertices.size // 6, 6))
        vertices[:, [0, 1, 2, 3, 4, 5]] = vertices[:, [3, 4, 5, 0, 1, 2]]
        vertices.resize(vertices.size)
        return vertices


# def load_obj_file(path):
#     vertices, normals, texture_coords = [], [], []
#     obj_data = {0: vertices, 1: normals, 2: texture_coords}
#     vertices_data = []
#     with open(path, 'r') as f:
#         model_data = f.readlines()
#     for line in model_data:
#         s = line.rstrip().split()
#         if s[0] == '#':
#             continue
#         if s[0] == 'mtllib':
#             pass
#         elif s[0] == 'v':
#             vertices.append(s[1:])
#         elif s[0] == 'vn':
#             normals.append(s[1:])
#         elif s[0] == 'vt':
#             texture_coords.append(s[1:])
#         elif s[0] == 's':
#             pass
#         elif s[0] == 'usemtl':
#             pass
#         elif s[0] == 'f':
#             surface = s[1:]
#             surface_data = []
#             for surface_vertices in surface:
#                 for index, value in enumerate(surface_vertices.split('/')):
#                     if value != '':
#                         surface_data.extend(obj_data[index][int(value) - 1])
#             vertices_data.append(surface_data)
#     return np.array(vertices_data, dtype=np.float32)


if __name__ == '__main__':
    tmp = load_obj('resources/models/hand.obj')
    print(tmp)
