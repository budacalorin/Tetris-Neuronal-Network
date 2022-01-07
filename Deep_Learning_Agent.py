import keras.models
from keras.models import Sequential
from keras.layers import Dense
from collections import deque
import numpy as np
import random
import os


class DeepLearningAgent:

    def __init__(self,
                 size_input_domain,
                 model_file_path,
                 replay_buffer_size=10000,
                 discount=0.95,
                 epsilon=1,
                 episodes_per_training=32,
                 epsilon_min=0,
                 epsilon_stop_training=400,
                 size_hidden_layers=[32, 32],
                 activations=['relu', 'relu', 'linear'],
                 loss='mse',
                 optimizer='adam',
                 replay_buffer_start_size=None):
        self.path = model_file_path
        self.size_input_domain = size_input_domain
        self.memory = deque(maxlen=replay_buffer_size)
        self.discount = discount
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = (self.epsilon - self.epsilon_min) / (epsilon_stop_training / episodes_per_training)
        self.size_hidden_layers = size_hidden_layers
        self.activations = activations
        self.loss = loss
        self.optimizer = optimizer
        if not replay_buffer_start_size:
            replay_buffer_start_size = replay_buffer_size / 2
        self.replay_start_size = replay_buffer_start_size
        self.model = self.build_model()

    def build_model(self):
        """
        Creates a learning model using Tensorflow 2.0 + Keras
        Input Layer: [4 x 32]
        Hidden Layer: [32 x 32]
        Output Layer: [32 x 1]
        :return: learning-model
        """
        if os.path.isfile(self.path):
            learning_model = keras.models.load_model(self.path)
        else:
            learning_model = Sequential()
            learning_model.add(Dense(self.size_hidden_layers[0], input_dim=self.size_input_domain, activation=self.activations[0]))

            for i in range(1, len(self.size_hidden_layers)):
                learning_model.add(Dense(self.size_hidden_layers[i], activation=self.activations[i]))

            learning_model.add(Dense(1, activation=self.activations[-1]))

            learning_model.compile(loss=self.loss, optimizer=self.optimizer)

        return learning_model

    def add_to_memory(self, current_state, next_state, reward, done):
        """
        :param current_state: current state of the game
        :param next_state: the predicted state for the current game
        :param reward: the reward gained for the taken action
        :param done: if the game is finished or not
        :return:
        """
        current_state = self.extract_input_from_state(current_state)
        next_state = self.extract_input_from_state(next_state)
        self.memory.append((current_state, next_state, reward, done))

    def random_value(self):
        return random.random()

    def predict_value(self, state):
        """

        :param state: the state of the current game
        :return: the predicted score of the state
        """
        return self.model.predict(state)[0]

    def act(self, state):
        """
        Epsilon-greedy policy for better exploration of the search space; the epsilon factor
        decreases over time, so in latter training there will be less random actions taken
        :param state: the state of the game
        :return: the predicted score for the taken action
        """
        state = np.reshape(state, [1, self.size_input_domain])
        if random.random() <= self.epsilon:
            return self.random_value()
        else:
            return self.predict_value(state)

    def extract_input_from_states(self, states):
        return list(map(lambda state: self.extract_input_from_state(state), states))

    def extract_input_from_state(self, state):
        return [state.fullLines, state.holes, state.bumpiness, state.totalHeight]

    def best_state(self, states):
        """
        Evaluates the states and returns the index of the best state from the batch using epsilon-greedy policy
        :param states: the batch with states of the game
        :return: the index of the best action the game can take
        """
        states = self.extract_input_from_states(states)

        max_value = None
        best_state_index = None

        if random.random() <= self.epsilon:
            return random.randint(0, len(states) - 1)
        else:
            for state_index in range(len(states)):
                state = states[state_index]
                value = self.predict_value(np.reshape(state, [1, self.size_input_domain]))
                if not max_value or value > max_value:
                    max_value = value
                    best_state_index = state_index
        return best_state_index

    def train(self, batch_size=32, epochs=1):
        """
        Training the model; if we have in memory enough states - for the replay buffer and for the
        mini-batch size, we select a mini-batch at random, take the states from it, predict the scores using the model,
        calculate the new scores using the discount rate if the game is done or maintain the same score, otherwise.
        At last, we fit the model with the new values
        :param batch_size: the size of the mini-batch
        :param epochs: the number of epochs used for fitting the model with the new values
        """
        n = len(self.memory)

        if n >= self.replay_start_size and n >= batch_size:

            batch = random.sample(self.memory, batch_size)
            next_states = np.array([x[1] for x in batch])
            next_qs = [x[0] for x in self.model.predict(next_states)]

            x = []
            y = []

            for i, (state, _, reward, done) in enumerate(batch):
                if not done:
                    new_q = reward + self.discount * next_qs[i]
                else:
                    new_q = reward

                x.append(state)
                y.append(new_q)

            self.model.fit(np.array(x), np.array(y), batch_size=batch_size, epochs=epochs, verbose=0)

            if self.epsilon > self.epsilon_min:
                self.epsilon -= self.epsilon_decay
