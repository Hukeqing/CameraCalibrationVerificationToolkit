from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
from GEngine.shader import ShaderProgram
from GEngine.model import Model, ModelFromExport, generate_grid_mesh
import glm
from GEngine.camera3D import Camera3D
# from GEngine.input_process import InputProcess, keys
from GEngine.window import GWindow

import threading
import OpenGLtkinter
import data

import time

# import cv2

SCR_WIDTH = int(1920 * 0.5) * 2
SCR_HEIGHT = int(1080 * 0.5)

camera = Camera3D(glm.vec3(0.0, 0, 30.0))

# window = GWindow(b"demo", SCR_WIDTH, SCR_HEIGHT, InputProcess(camera), keep_mouse_stay=False)
window = GWindow("demo", SCR_WIDTH, SCR_HEIGHT, camera, keep_mouse_stay=False)


# image_size = (1920, 1080)
# light_color = (1.0, 1.0, 1.0)
# hand_color = (0.9, 0.9, 0.9)
# light_position = (-1000, -700, 1000)

# model_position = [
#     glm.vec3(1.0, 1.0, 1.0),
#     [[0, glm.vec3(1.0, 0.0, 0.0)], [0, glm.vec3(0.0, 1.0, 0.0)], [0, glm.vec3(0.0, 0.0, 1.0)]],
#     glm.vec3(500, 500.0, 0.0)
# ]

# left_camera_intrinsic = np.loadtxt(image_path + "left/Intrinsic.txt")
#
# right_camera_intrinsic = np.loadtxt(image_path + "/right/Intrinsic.txt")

# stereo_left_index = 48
# stereo_right_index = stereo_left_index

# left_camera_extrinsic = np.loadtxt(image_path + "left/ExtrinsicCameraPars.txt")
#
# right_camera_extrinsic = np.loadtxt(image_path + "right/ExtrinsicCameraPars.txt")


def init():
    # grid_vertices, grid_mesh = generate_grid_mesh(-10, 10, step=0.5)

    # bg = np.array([-1, 1, 0, 0, 1,
    #                1, 1, 0, 1, 1,
    #                -1, -1, 0, 0, 0,
    #                -1, -1, 0, 0, 0,
    #                1, -1, 0, 1, 0,
    #                1, 1, 0, 1, 1
    #                ], dtype=np.float32)

    scale = 120
    img_size = (1920 / scale, 1080 / scale)
    # img_size = (20, 20)
    # img_size = (2, 2)
    bg = np.array([-img_size[0] / 2, img_size[1] / 2, 0, 0, 1,
                   img_size[0] / 2, img_size[1] / 2, 0, 1, 1,
                   -img_size[0] / 2, -img_size[1] / 2, 0, 0, 0,
                   -img_size[0] / 2, -img_size[1] / 2, 0, 0, 0,
                   img_size[0] / 2, -img_size[1] / 2, 0, 1, 0,
                   img_size[0] / 2, img_size[1] / 2, 0, 1, 1, ],
                  dtype=np.float32)

    # global shader_program
    # shader_program = ShaderProgram("resources/shaders/shader.vs", "resources/shaders/shader.fg")
    # shader_program.init()

    # global bg_model_left
    # bg_model_left = Model([bg], texture_path=[image_path + "left/left" + str(stereo_left_index + 1) + ".png"])
    # bg_model_left = Model([bg], texture_path=[image_path + "leftCamera.png"])
    data.bg_model_left.Model = Model([bg], texture_path=[data.bg_model_left.path])

    # global bg_model_right
    # bg_model_right = Model([bg], texture_path=[image_path + "right/right" + str(stereo_right_index + 1) + ".png"])
    # bg_model_right = Model([bg], texture_path=[image_path + "rightCamera.png"])
    data.bg_model_right.Model = Model([bg], texture_path=[data.bg_model_right.path])

    global bg_shader_program
    bg_shader_program = ShaderProgram("resources/shaders/bg_shader.vs", "resources/shaders/bg_shader.fg")
    bg_shader_program.init()

    glEnable(GL_DEPTH_TEST)


def render_background_image(bg_model):
    # glDisable(GL_DEPTH_TEST)
    bg_shader_program.use()
    m = glm.mat4(1.0)
    m = glm.scale(m, glm.vec3(2))
    bg_shader_program.set_matrix("model", glm.value_ptr(m))

    view = camera.get_view_matrix()
    bg_shader_program.set_matrix("view", glm.value_ptr(view))

    projection = camera.get_projection(1920 / 2, 1080 / 2)
    bg_shader_program.set_matrix("projection", glm.value_ptr(projection))
    bg_shader_program.un_use()
    bg_model.draw(bg_shader_program, draw_type=GL_TRIANGLES)
    # glEnable(GL_DEPTH_TEST)


def render():
    glClearColor(1.0, 1.0, 1.0, 0.0)
    glClearDepth(1.0)
    glPointSize(5)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glViewport(0, 0, int(window.window_width / 2), window.window_height)
    render_background_image(data.bg_model_left.Model)
    # render_side_view(left_camera_intrinsic, left_camera_extrinsic, window.window_width / 2, window.window_height,
    #                  stereo_left_index)
    if data.bg_model_left.flag:
        data.bg_model_left.Model.change_mesh(data.bg_model_left.path)
        data.bg_model_left.flag = False

    glViewport(int(window.window_width / 2), 0, int(window.window_width / 2), window.window_height)
    render_background_image(data.bg_model_right.Model)
    # render_side_view(right_camera_intrinsic, right_camera_extrinsic, window.window_width / 2, window.window_height,
    #                  stereo_right_index)
    if data.bg_model_right.flag:
        data.bg_model_right.Model.change_mesh(data.bg_model_right.path)
        data.bg_model_right.flag = False


def main_render():
    init()
    window.set_render_function(render)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    msg_handle = threading.Thread(target=OpenGLtkinter.tkinterwindow, args=())
    msg_handle.daemon = True
    msg_handle.start()

    window.start_window_loop()


if __name__ == '__main__':
    main_render()
