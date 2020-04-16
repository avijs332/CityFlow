from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers.core import Dense, Dropout
import random
import numpy as np
import pandas as pd
from operator import add
import collections
import rtc

from main import vehicles_in_step, isCruising, isSlow, eng

#vehicles_in_step = {} #dictionary with all vehicles in current step. built in the following format:
                                                            #{id: {location: {}, velocity: float}}
collisions_in_step = {} #list with all the locations of the collisions in the step
MAX_INPUT_SIZE = 500
# Reinforcement learning part of project, this agent will be the controller for the vehicle "hive mind" structure.
# Each vehicle will look like it works on its own and make it's own decisions but ultimately this algorithm will be responsible
# for all vehicle actions in the simulator. instead of each vehicle working on it's own, the alorithm will control all vehicles together
# as a type of "hive mind" to work together towards clear crossings of intersections without collisions.

CRUISING_SPEED = 16.67 #goal speed, where at cars are expected to drive if not slowing down to avoid collision


        #exit()
# def isCruising(car_id):
#     return vehicles_in_step[car_id] == CRUISING_SPEED

# def isSlow(car_id):
#     return not isCruising(car_id)
    
# def pad_with_zeros(array):
#     zeros_array = np.zeros(125)
#     for i in range(len(array)):
#         for j in range(len(array[i])):
#             zeros_array[i][j] = array[i][j]
#     return zeros_array

def pad_with_zeros(array):

    if len(array) == MAX_INPUT_SIZE:
        return array

    zeros_array = np.zeros(MAX_INPUT_SIZE)
    for i in range(len(array)-5):
            zeros_array[i] = array[i]
    return zeros_array

class DQNAgent(object):

    

    def __init__(self, params):
        self.reward = 0
        self.gamma = 0.9
        self.dataframe = pd.DataFrame()
        self.short_memory = np.array([])
        self.agent_target = 1
        self.agent_predict = 0
        self.learning_rate = params['learning_rate']
        self.epsilon = 1
        self.actual = []
        self.first_layer = params['first_layer_size']
        self.second_layer = params['second_layer_size']
        self.third_layer = params['third_layer_size']
        self.memory = collections.deque(maxlen=params['memory_size'])
        self.weights = params['weights_path']
        self.load_weights = params['load_weights']
        self.model = self.network()
    
    pred_num = 24

    def network(self):
        model = Sequential()
        model.add(Dense(units=self.first_layer, activation='relu', input_shape=(MAX_INPUT_SIZE,)))
        model.add(Dense(units=self.second_layer, activation='relu'))
        model.add(Dense(units=self.third_layer, activation='relu'))
        model.add(Dense(units=2, activation='softmax'))
        opt = Adam(self.learning_rate)
        model.compile(loss='mse', optimizer=opt)

        if self.load_weights:
            model.load_weights(self.weights)
        return model
    
    #function will return state of all vehicles in a true false array stating each cars possible moves
    #actions include slow down, speed up to set speed, cruise (drive at a static set speed).
    def get_state(self,vehicles_in_step):
        
        state = []
        for i in vehicles_in_step.keys():

            state.append(isCruising(i, vehicles_in_step))
            state.append(isSlow(i, vehicles_in_step))
        for i in range (len(state)):
            if state[i]:
                state[i]=1
            else:
                state[i]=0
        self.pred_num = len(state)
        nparray = np.asarray(state)


        return pad_with_zeros(nparray)

    #def get_state_new(self,id):
    #    state =[]
    #    state.append(isCruising(id,vehicles_in_step))
    #    state.append(isSlow(id,vehicles_in_step))
    #    for i in range (len(state)):
    #        if state[i]:
    #            state[i]=1
    #        else:
    #            state[i]=0
    #    self.pred_num = len(state)
    #    nparray = np.asarray(state)



    #reward/demerit will be set accoridngly to each action, these rewards will be given to the hive mind and not to individual cars
    # major rewards: reach dest
    # minor rewards: cruise at set speed, speed up to static speed
    # 
    # major punishment: collision
    # minor punishment: slow down (this will be very minor as we do want cars to slow down)
    def set_reward(self, speed_avg, collision):
        #print(collision, " collisions (set_reward)")
        self.reward = 0
        self.reward = self.reward - ((CRUISING_SPEED - speed_avg)*2) +5 
        self.reward += -15 * collision
        
        return self.reward


    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    # def replay_new(self, memory, batch_size):
    #     if len(memory) > batch_size:
    #         minibatch = random.sample(memory, batch_size)
    #     else:
    #         minibatch = memory
        
    #     for state, action, reward, next_state, done in minibatch:
    #         target = reward
    #         if not done:
    #             print("pred_num = ", self.pred_num)
    #             target = reward + self.gamma * np.amax(self.model.predict(np.array([next_state]))[0])
    #             #target = reward + self.gamma * np.amax(self.model.predict(next_state.reshape(1,len(state)))[0:1])
    #         target_f = self.model.predict(np.array([state]))
    #         target_f[0][np.argmax(action)] = target
    #         self.model.fit(state.reshape((1,len(state))), target_f, epochs=1, verbose=0)

    def replay_new(self, memory, batch_size):
        if len(memory) > batch_size:
            minibatch = random.sample(memory, batch_size)
        else:
            minibatch = memory
        for state, action, reward, next_state, done in minibatch:

            next_state = pad_with_zeros(next_state)
            state = pad_with_zeros(state)


            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(np.array([next_state]))[0:1])
            target_f = self.model.predict(np.array([state]))
            target_f[0][np.argmax(action)] = target
            self.model.fit(np.array([state]), target_f, epochs=1, verbose=0)

    def train_short_memory(self, state, action, reward, next_state, done):
        target = reward
        if not done:
            target = reward + self.gamma *np.amax(self.model.predict(next_state.reshape((1,MAX_INPUT_SIZE)))[0:1])
        target_f = self.model.predict(state.reshape((1, MAX_INPUT_SIZE)))
        target_f[0][np.argmax(action)] = target
        self.model.fit(state.reshape((1,MAX_INPUT_SIZE)), target_f, epochs=1, verbose=0)

   

        