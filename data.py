class bg_model:
    def __init__(self, path):
        self.path = path
        self.flag = False
        self.Model = None


bg_model_left = bg_model('source/leftCamera.png')
bg_model_right = bg_model('source/rightCamera.png')


def change_render(new_path, left=True):
    if left:
        global bg_model_left
        if bg_model_left.path != new_path:
            bg_model_left.path = new_path
            bg_model_left.flag = True
    else:
        global bg_model_right
        if bg_model_right.path != new_path:
            bg_model_right.path = new_path
            bg_model_right.flag = True
