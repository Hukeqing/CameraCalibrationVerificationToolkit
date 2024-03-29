import cv2
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
import ModelLoad
import glfw

SCR_WIDTH = int(1920 * 0.5)
SCR_HEIGHT = int(1080 * 0.5)

camera = Camera3D(glm.vec3(0.0, 0, 1000.0))

ortho_camera = Camera3D(glm.vec3(0, 0, 1000))
bg_view = ortho_camera.get_view_matrix()

# window = GWindow(b"demo", SCR_WIDTH, SCR_HEIGHT, InputProcess(Camera), keep_mouse_stay=False)
window = GWindow("demo", SCR_WIDTH * 2, SCR_HEIGHT, camera, keep_mouse_stay=False)

light_color = (1.0, 1.0, 1.0)
hand_color = (1, 0, 0)
light_position = (-5000, -5000, 5000)

hand_position = glm.vec3(0)
hand_rotation = glm.vec3(0)

move_nor_speed = 1000
move_add_speed = 2000
move_sub_speed = 500

rotate_nor_speed = 90
rotate_add_speed = 180
rotate_sub_speed = 45

data.init(r'resources\models\data.txt')


def init():
    global bg_shader_program
    bg_shader_program = ShaderProgram("resources/shaders/bg_shader.vs", "resources/shaders/bg_shader.fg")
    bg_shader_program.init()

    global hand_shader_program
    hand_shader_program = ShaderProgram("resources/shaders/hand_shader.vs", "resources/shaders/hand_shader.fg")
    hand_shader_program.init()

    global hand_model
    v = ModelLoad.load_obj('resources/models/hand.obj')
    hand_model = Model([v], vertex_format='VN')
    # hand_model = ModelFromExport("resources/models/hand.obj", vertex_format="VN")

    # glEnable(GL_DEPTH_TEST)


def render_background_image(bg_model, camera_view=None, fx=1920):
    # glDisable(GL_DEPTH_TEST)
    bg_shader_program.use()
    m = glm.mat4(1.0)
    rescale = 45 / camera.zoom
    m = glm.scale(m, glm.vec3(rescale))

    fov = 2 * glm.atan(1080 / 2 / fx) / 3.14159 * 180
    fov *= camera.zoom / 45

    projection = camera.get_projection(fov, SCR_WIDTH, SCR_HEIGHT)
    bg_ortho = glm.ortho(-SCR_WIDTH * 0.5, SCR_WIDTH * 0.5, -SCR_HEIGHT * 0.5, SCR_HEIGHT * 0.5, 0.3, 5000)

    bg_shader_program.set_matrix("model", glm.value_ptr(m))

    # view = camera.get_view_matrix()
    bg_shader_program.set_matrix("view", glm.value_ptr(bg_view))

    bg_shader_program.set_matrix("projection", glm.value_ptr(bg_ortho))
    bg_shader_program.un_use()
    bg_model.draw(bg_shader_program, draw_type=GL_TRIANGLES)
    # glEnable(GL_DEPTH_TEST)

    hand_shader_program.use()
    hand_shader_program.set_matrix("projection", glm.value_ptr(projection))
    hand_shader_program.set_matrix("view", glm.value_ptr(camera_view))
    # hand_shader_program.set_matrix("view", glm.value_ptr(view))
    m = glm.mat4(1.0)
    m = glm.translate(m, hand_position)
    m = glm.rotate(m, glm.radians(hand_rotation.x), glm.vec3(1, 0, 0))
    m = glm.rotate(m, glm.radians(hand_rotation.y), glm.vec3(0, 1, 0))
    m = glm.rotate(m, glm.radians(hand_rotation.z), glm.vec3(0, 0, 1))

    hand_shader_program.set_matrix("model", glm.value_ptr(m))
    hand_shader_program.set_uniform_3f("lightColor", light_color)
    hand_shader_program.set_uniform_3f("lightPos", light_position)
    hand_shader_program.set_uniform_3f("handColor", hand_color)
    hand_shader_program.un_use()

    glEnable(GL_CULL_FACE)
    hand_model.draw(hand_shader_program, draw_type=GL_TRIANGLES)
    glDisable(GL_CULL_FACE)


def render_view(cur_camera: data.Camera, cur_camera_data: data.CameraData):
    camera.position = cur_camera_data.position

    tmp = tuple([- i for i in cur_camera_data.rotation])
    # tmp = tuple(cur_camera_data.rotation)
    view = cv2.Rodrigues(tmp)[0]
    # camera.yaw = cur_camera.camera_data.yaw - 90
    # camera.pitch = cur_camera.camera_data.pitch

    view = glm.mat4x4(*view[0], 0, *view[1], 0, *view[2], 0, -camera.position[0], -camera.position[1], -camera.position[2], 1)
    # print(view)
    # render_background_image(cur_camera.bg.Model, window_width=cur_camera.bg.window_size[0],
    #                         window_height=cur_camera.bg.window_size[1], camera_view=view)
    render_background_image(cur_camera.bg.Model, camera_view=view, fx=cur_camera.bg.window_size[0])
    # render_side_view(left_camera_intrinsic, left_camera_extrinsic, window.window_width / 2, window.window_height,
    #                  stereo_left_index)
    if cur_camera.bg.flag:
        cur_camera.bg.Model.change_mesh(cur_camera.bg.path)
        cur_camera.bg.flag = False


def render():
    glClearColor(1.0, 1.0, 1.0, 0.0)
    glClearDepth(1.0)
    glPointSize(5)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    global hand_position
    global hand_rotation

    move_speed = move_nor_speed
    rotate_speed = rotate_nor_speed
    if glfw.get_key(window.window, glfw.KEY_LEFT_CONTROL) == glfw.PRESS:
        move_speed = move_add_speed
        rotate_speed = rotate_add_speed
    elif glfw.get_key(window.window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS:
        move_speed = move_sub_speed
        rotate_speed = rotate_sub_speed
    # hand move
    if glfw.get_key(window.window, glfw.KEY_A) == glfw.PRESS:
        hand_position.y += move_speed * window.delta_time
    if glfw.get_key(window.window, glfw.KEY_D) == glfw.PRESS:
        hand_position.y -= move_speed * window.delta_time
    if glfw.get_key(window.window, glfw.KEY_W) == glfw.PRESS:
        hand_position.x -= move_speed * window.delta_time
    if glfw.get_key(window.window, glfw.KEY_S) == glfw.PRESS:
        hand_position.x += move_speed * window.delta_time
    if glfw.get_key(window.window, glfw.KEY_Q) == glfw.PRESS:
        hand_position.z -= move_speed * window.delta_time
    if glfw.get_key(window.window, glfw.KEY_E) == glfw.PRESS:
        hand_position.z += move_speed * window.delta_time

    if glfw.get_key(window.window, glfw.KEY_J) == glfw.PRESS:
        hand_rotation.x += rotate_speed * window.delta_time
    if glfw.get_key(window.window, glfw.KEY_L) == glfw.PRESS:
        hand_rotation.x -= rotate_speed * window.delta_time
    if glfw.get_key(window.window, glfw.KEY_I) == glfw.PRESS:
        hand_rotation.y += rotate_speed * window.delta_time
    if glfw.get_key(window.window, glfw.KEY_K) == glfw.PRESS:
        hand_rotation.y -= rotate_speed * window.delta_time
    if glfw.get_key(window.window, glfw.KEY_U) == glfw.PRESS:
        hand_rotation.z += rotate_speed * window.delta_time
    if glfw.get_key(window.window, glfw.KEY_O) == glfw.PRESS:
        hand_rotation.z -= rotate_speed * window.delta_time

    cur_camera = data.couple_list[data.curindex]
    glViewport(0, 0, int(window.window_width / 2), window.window_height)
    render_view(cur_camera.left_camera, cur_camera.left_camera_data)

    glViewport(int(window.window_width / 2), 0, int(window.window_width / 2), window.window_height)
    render_view(cur_camera.right_camera, cur_camera.right_camera_data)


def main_render():
    init()
    window.set_render_function(render)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    msg_handle = threading.Thread(target=OpenGLtkinter.tkinter_window, args=())
    msg_handle.daemon = True
    msg_handle.start()

    window.start_window_loop()


if __name__ == '__main__':
    main_render()
