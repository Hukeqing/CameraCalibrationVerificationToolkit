from OpenGL.GL import *
from OpenGL.GLUT import *
import glfw
import time
from GEngine.camera3D import CAMERA_MOVEMENT


class GWindow:
    def __init__(self, window_name, window_width, window_height, camera, keep_mouse_stay=False):
        self.window_name = window_name
        self.window_width = window_width
        self.window_height = window_height
        # self.io_process = io_process
        self.camera = camera
        # self.io_process.set_window_size(window_width, window_height)
        self.delta_time = 0.0
        self.last_frame = 0.0
        self.fps_count = 0
        self._fps = 0
        self.NUM_SAMPLES = 10
        self.frameTimes = []
        self.currentFrame = 0
        self.prevTicks = 0
        self._frameTime = None
        self.keep_mouse_stay = keep_mouse_stay

        self.last_x = self.window_width / 2.0
        self.last_y = self.window_height / 2.0
        self.first_mouse = True

        self.__init_window_context()
        self.__bind_io_process()

    def reshape(self, window, w, h):
        glViewport(0, 0, w, h)
        # self.window_height = h
        # self.window_width = w
        # self.io_process.set_window_size(w, h)

    def __init_window_context(self):
        if not glfw.init():
            return
        self.window = glfw.create_window(self.window_width, self.window_height, self.window_name, None, None)
        if not self.window:
            glfw.terminate()
            return
        glfw.make_context_current(self.window)
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)
        print(glGetString(GL_VERSION))

    def __bind_io_process(self):

        # glfw.set_cursor_pos_callback(self.window, self.mouse_callback)
        glfw.set_scroll_callback(self.window, self.scroll_callback)
        # glfw.set_framebuffer_size_callback(self.window, self.reshape)

        # glutDisplayFunc(self.draw_function)
        # glutIdleFunc(self.draw_function)
        # glutReshapeFunc(self.reshape)
        # glutKeyboardFunc(self.io_process.keys_down)
        # glutKeyboardUpFunc(self.io_process.keys_up)
        # glutPassiveMotionFunc(self.io_process.mouse_move)
        # glutMotionFunc(self.io_process.mouse_move)
        # if self.keep_mouse_stay:
        #     glutEntryFunc(self.io_process.mouse_state)

    def process_input(self, window, delta_time):
        if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(window, True)
        if (glfw.get_key(window, glfw.KEY_W) == glfw.PRESS):
            self.camera.process_keyboard(CAMERA_MOVEMENT.FORWARD, delta_time)
        if (glfw.get_key(window, glfw.KEY_S) == glfw.PRESS):
            self.camera.process_keyboard(CAMERA_MOVEMENT.BACKWARD, delta_time)
        if (glfw.get_key(window, glfw.KEY_A) == glfw.PRESS):
            self.camera.process_keyboard(CAMERA_MOVEMENT.LEFT, delta_time)
        if (glfw.get_key(window, glfw.KEY_D) == glfw.PRESS):
            self.camera.process_keyboard(CAMERA_MOVEMENT.RIGHT, delta_time)

    def mouse_callback(self, window, xpos, ypos):
        if self.first_mouse:
            self.last_x = xpos
            self.last_y = ypos
            self.first_mouse = False

        xoffset = xpos - self.last_x
        yoffset = self.last_y - ypos
        self.last_x = xpos
        self.last_y = ypos
        self.camera.process_mouse_movement(xoffset, yoffset)

    def scroll_callback(self, window, xoffset, yoffset):
        self.camera.process_mouse_scroll(yoffset)

    def set_render_function(self, render):
        self.render = render

    def draw_function(self):
        current_frame = glfw.get_time()
        self.process_input(self.window, self.delta_time)

        self.render()

        self.last_frame = glfw.get_time()
        self.delta_time = (self.last_frame - current_frame)
        # self.io_process.process_keys_by_frame(self.delta_time / 1000)
        if self.delta_time * 1000 < 16:
            time.sleep((16 - self.delta_time * 1000) / 1000)
            pass
        self.calculate_fps()
        if self.fps_count == 100:
            self.fps_count = 0
            print('fps: %.2f' % self._fps)
        self.fps_count += 1

    def calculate_fps(self):
        current_ticks = glfw.get_time()
        NUM_SAMPLES = self.NUM_SAMPLES
        self._frameTime = current_ticks - self.prevTicks
        self.currentFrame += 1
        if self.currentFrame <= NUM_SAMPLES:
            self.frameTimes.append(self._frameTime)
        else:
            self.frameTimes[(self.currentFrame) % NUM_SAMPLES] = self._frameTime
        if self.currentFrame < NUM_SAMPLES:
            count_ = self.currentFrame
        else:
            count_ = NUM_SAMPLES

        frame_time_average = 0
        for i in range(count_):
            frame_time_average += self.frameTimes[i]

        self.prevTicks = current_ticks

        frame_time_average /= count_
        if frame_time_average > 0:
            self._fps = 1 / frame_time_average

        else:
            self._fps = 0.00

    def start_window_loop(self):
        while not glfw.window_should_close(self.window):
            self.draw_function()
            glfw.swap_buffers(self.window)
            glfw.poll_events()
        glfw.terminate()
