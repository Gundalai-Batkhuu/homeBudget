from src.model.model import Model



class View:
    myModel: Model

    def __init__(self, model: Model):
        self.myModel = model

    def update(self):
        self.make_window()

    def make_window(self):
        pass

