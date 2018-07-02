import os
import numpy as np
from keras_contrib.utils import save_load_utils
import LoadData
import Models
import Training

# global variables for threading
EMBEDDING_SIZE = 300
SENTENCE_LENGTH = 16
FREQUENCY_OF_WORDS_NEEDED = 8

SENTENCE_START_SYMBOL = '*S*'
SENTECEN_END_SYMBOL = '*E*'
UNKNOWN_SYMBOL = 'ukn'


class Agent:
    def __init__(self, name, train_dataset, val_dataset, w2v_model_number):
        np.random.seed(7)

        self.name = name

        self.loaded_data = LoadData.LoadData(w2v_model_number, SENTENCE_LENGTH, FREQUENCY_OF_WORDS_NEEDED, EMBEDDING_SIZE, train_dataset, val_dataset)

        # get size of state and action, and inputs
        self.state_space = [SENTENCE_LENGTH, EMBEDDING_SIZE]
        self.action_size = self.loaded_data.action_size
        self.image_vector_size = self.loaded_data.image_vector_size

        # create model for actor network
        self.actor = Models.build_actor_model(self.state_space, self.action_size, self.image_vector_size)


    def train_model(self, minibatch = 128, epochs = 20):
        agent = Training.Training(self.actor, self.loaded_data)
        agent.train()
        save_load_utils.save_all_weights(self.actor, './save_model/actor_' + self.name + '.model')


    def load_actor(self, path):
        if (os.path.isfile(path)):
            save_load_utils.load_all_weights(self.actor, path)
            print('Weights from old actor model found and loaded')


if __name__ == "__main__":
    name = "Img2SeqTest01"
    train_dataset = 'train'
    val_dataset = 'val'
    w2vModel = 0

    agent = Agent(name, train_dataset, val_dataset, w2vModel)

    # global_agent.load_actor(r'./save_model/actor_only_pretrain_A3C_Test.model')
    # global_agent.load_actor('./save_model/A3C_Test_actor.model')

    agent.train_model()