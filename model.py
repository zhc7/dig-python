import keras
from keras.layers import Dense, Dropout, Input



class Model:
    def __init__(self):
        self.model = self.create_model()

    def create_model(self):
        in_x = Input((14, ))
        x = Dense()