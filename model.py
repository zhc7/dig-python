import keras
import numpy as np
from keras.layers import Dense, Dropout, Input, LeakyReLU
from keras.models import Model
from keras.optimizers import SGD
from keras.models import load_model
import time


class PolicyNet:
    def __init__(self, model_file=None):
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
        opt = SGD(0.01, momentum=0.9)
        self.model.compile(opt, "categorical_crossentropy", ["loss", "accuracy"])

    def train_step(self, states, labels):
        x = np.array(states)
        y = np.array(labels)
        self.model.fit(x, y, self.batch_size, self.epochs, verbose=1, validation_split=0.2)

    def predict(self, state):
        return self.model.predict(state)

    def save_model(self):
        self.model.save("models/model%s" % time.time())
