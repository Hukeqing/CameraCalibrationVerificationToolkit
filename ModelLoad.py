import pywavefront
import numpy as np


def load_obj(path, resize=500):
    obj_wf = pywavefront.Wavefront(path)
    obj_wf.parse()
    for name, material in obj_wf.materials.items():
        tmp = np.array(material.vertices, dtype=np.float)
        tmp.resize((tmp.size // 6, 6))
        for index, item in enumerate(tmp):
            tmp[index][0], tmp[index][1], tmp[index][2], tmp[index][3], tmp[index][4], tmp[index][5] = item[3] / resize, item[4] / resize, item[
                5] / resize, item[0], item[1], item[2]
        return tmp


if __name__ == '__main__':
    tmp = load_obj('resources/models/hand.obj')
    tmp.resize((tmp.size // 6, 6))
    print(tmp)
