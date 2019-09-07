import glm
from GEngine.model import Model
import numpy as np
from typing import List


class bg_model:
    def __init__(self, path, window_size):
        self.path = path
        self.flag = False
        self.Model = None
        self.window_size = window_size


class CameraData:
    def __init__(self, position, rotation):
        self.position = position
        self.rotation = rotation


class Camera:
    def __init__(self, name, bg: bg_model):
        self.name = name
        self.bg = bg


class check_couple:
    def __init__(self, left_camera=None, right_camera=None, left_camera_data=None, right_camera_data=None):
        self.left_camera = left_camera
        self.right_camera = right_camera
        self.left_camera_data = left_camera_data
        self.right_camera_data = right_camera_data


# camera1 = Camera('camera1', bg_model('resources/images/leftCamera.png', (1712.767, 1712.385)),
#                  CameraData(glm.vec3(638.14, 459.54, 2901.81), (-2.04, 2.16, -0.09)))
# camera2 = Camera('camera1', bg_model('resources/images/rightCamera.png', (1760.151, 1752.823)),
#                  CameraData(glm.vec3(257.90, 408.14, 3057.48), (2.17, -1.98, -0.42)))

# left_camera = camera1
# right_camera = camera2
curindex = 0
camera_list = dict()
couple_list: List[check_couple] = list()

img_size = (1920, 1080)
bg_size = np.array([-img_size[0] / 2, img_size[1] / 2, 0, 0, 1,
               img_size[0] / 2, img_size[1] / 2, 0, 1, 1,
               -img_size[0] / 2, -img_size[1] / 2, 0, 0, 0,
               -img_size[0] / 2, -img_size[1] / 2, 0, 0, 0,
               img_size[0] / 2, -img_size[1] / 2, 0, 1, 0,
               img_size[0] / 2, img_size[1] / 2, 0, 1, 1, ], dtype=np.float32)


# left_camera.bg.Model = Model([bg], texture_path=[left_camera.bg.path])
#
# right_camera.bg.Model = Model([bg], texture_path=[right_camera.bg.path])

def change_render(index):
    global curindex
    curindex = index


def init(path=r'D:\PhotoCheck\pythonGUI\Source\2CameraParam.txt'):
    with open(path, 'r') as f:
        camera_data = f.readlines()
    camera_data = [(camera_data[i], camera_data[i + 1], camera_data[i + 2]) for i in range(0, len(camera_data), 3)]
    flag = False
    for item in camera_data:
        if item[0].split(' ')[0] == '%':
            bg_data = [float(i) for i in item[1].split(' ') if i.strip() != '']
            name: str = item[0].split(' ', 1)[1].strip()
            bg = bg_model(item[2].strip(), window_size=(bg_data[0], bg_data[1]))
            bg.Model = Model([bg_size], texture_path=[bg.path])
            cur_camera = Camera(name, bg=bg)
            camera_list[name] = cur_camera
        elif item[0].split(' ')[0] == '$':
            rotation = [float(i) for i in item[1].split(' ') if i.strip() != ''][:3]
            position = [float(i) for i in item[2].split(' ') if i.strip() != ''][:3]
            if flag:
                couple_list[-1].right_camera = camera_list[item[0].split(' ', 1)[1].strip()]
                couple_list[-1].right_camera_data = CameraData(position=position, rotation=rotation)
                flag = False
            else:
                couple_list.append(check_couple())
                couple_list[-1].left_camera = camera_list[item[0].split(' ', 1)[1].strip()]
                couple_list[-1].left_camera_data = CameraData(position=position, rotation=rotation)
                flag = True


if __name__ == '__main__':
    init()
