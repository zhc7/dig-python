import keras
import numpy as np
from keras.layers import Dense, Dropout, Input, LeakyReLU
from keras.models import Model
from keras.optimizers import SGD
from keras.models import load_model
import time


class PolicyNet:
    def __init__(self, model_file=None):
        self.batch_size = 64
        self.epochs = 5
        self.lr = 0.01
        if model_file:
            self.model = load_model(model_file)
        else:
            self.model = self.create_model()
            self.initialize()

    def create_model(self) -> Model:
        in_x = Input((96,))
        x = Dense(256)(in_x)
        x = LeakyReLU()(x)
        x = Dense(512)(x)
        x = LeakyReLU()(x)
        x = Dense(512)(x)
        x = LeakyReLU()(x)
        x = Dense(128)(x)
        x = LeakyReLU()(x)
        x = Dense(14, activation="softmax")(x)
        model = Model(inputs=[in_x], outputs=[x])
        return model

    def initialize(self):
        opt = SGD(self.lr, momentum=0.9)
        self.model.compile(opt, "categorical_crossentropy", ["accuracy"])

    def train_step(self, states, labels):
        x = np.array(states, dtype="float32").reshape(len(states), 96)
        y = np.array(labels, dtype="float32").reshape(len(labels), 14)
        self.model.fit(x, y, self.batch_size, self.epochs, verbose=1, validation_split=0.2)

    def predict(self, state):
        return self.model.predict(np.array(state, dtype="float32").reshape((1, 96)))

    def save_model(self):
        self.model.save("models/model%s.h5" % round(time.time()))

    def copy(self):
        result = PolicyNet()
        result.model.set_weights(self.model.get_weights())
        return result
