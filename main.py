import rtc
import numpy as np
import argparse
import seaborn as sns
import matplotlib.pyplot as plt
import DQAgent
from random import randint
from keras.utils import to_categorical

from utilities import findCollisions, plot_seaborn


MAX_INPUT_SIZE = 500
vehicles_in_step = {} #dictionary with all vehicles in current step. built in the following format:
                                                            #{id: {location: {}, velocity: float}}
collisions_in_step = [] #list with all the locations of the collisions in the step
CRUISING_SPEED = 16.67 #goal speed, where at cars are expected to drive if not slowing down to avoid collision

eng = rtc.Engine("examples/config.json", thread_num=1)

old_states = []

def isCruising(car_id, vehicles):
    return vehicles[car_id]["velocity"] == CRUISING_SPEED

def isSlow(car_id, vehicles):
    return not isCruising(car_id, vehicles)

def refreshDicts(eng):
    refreshVehicleList(eng)
    refreshCollisionList(eng)

def refreshVehicleList(eng):
    vehicles_in_step.clear()
    vehicles = eng.get_vehicles() # get vehicle list
    speeds = eng.get_vehicle_speed() # get speed list ({car_id: speed})
    locations = eng.get_vehicle_location() # get locations ({car_id: ((x1, y1), (x2, y2))})

    # add items to dictionary
    for k in vehicles:
        vehicles_in_step[k] = {}
        vehicles_in_step[k]["velocity"] = speeds[k]
        vehicles_in_step[k]["location"] = locations[k]

def get_vehicle_speed_average():
    speeds = eng.get_vehicle_speed()
    return sum(speeds.values())/len(speeds)


def refreshCollisionList(eng):
    
    collisions_in_step[:] = findCollisions(eng)
    print(len(collisions_in_step), " collisions (refreshCollisionList)")

#################################
#   Define parameters manually  #
#################################
def define_parameters():
    params = dict()
    params['epsilon_decay_linear'] = 1/75
    params['learning_rate'] = 0.0005
    params['first_layer_size'] = 150   # neurons in the first layer
    params['second_layer_size'] = 150   # neurons in the second layer
    params['third_layer_size'] = 150    # neurons in the third layer
    params['episodes'] = 5            
    params['memory_size'] = 2500
    params['batch_size'] = 500
    params['weights_path'] = 'weights/weights.hdf5'
    params['load_weights'] = False
    params['train'] = True
    return params



def _rerun(params):
    agent = DQAgent.DQNAgent(params)
    weights_filepath = params['weights_path']
    if params['load_weights']:
        agent.model.load_weights(weights_filepath)
        print("weights loaded")
    for i in range(params['episodes']):
        run_sim(params, agent, i)

def run_sim(params, agent, count_runs):
    score_plot = []
    counter_plot = []

    for i in range(200):
        
        #do stuff
        eng.next_step()
        print("Step ", i)
        
        refreshDicts(eng)

        

        if i%2 == 0:
            
            final_moves = []
            init_sim(params,agent,params['batch_size'])
            if not params['train']:
                agent.epsilon = 1
            else:
                agent.epsilon = 1 -(count_runs * params['epsilon_decay_linear'])
                #for i in vehicles_in_step.keys():
                state_old = agent.get_state(vehicles_in_step)
                old_states.append(state_old) #add to list of old states

                if randint(0,1) < agent.epsilon:
                    final_move = to_categorical(randint(0,1) ,num_classes=2)
                else:
                    
                    #prediction = agent.model.predict(state_old.reshape(1,MAX_INPUT_SIZE))
                    for state in old_states:
                        prediction_new = agent.model.predict_on_batch(state.reshape(1,MAX_INPUT_SIZE))
                        new_move = to_categorical(np.argmax(prediction_new[0]))
                        move = new_move.tolist()
                        if(len(new_move) == 1):
                            move.append(0.0)
                        print("predict list: ", move)
                        final_moves.append(move)

                    #print("New Prdict")
                    #print(prediction_new)
                        #print("predict")
                        #print(prediction)
                    #final_move = to_categorical(np.argmax(prediction[0]), num_classes=len(vehicles_in_step))
                    #final_moves.append(final_move.tolist()[0])
                    #final_moves.append(final_move.tolist()[1])
                    #print("final move")
                    #print(final_moves)
            if len(final_moves):
                final_move = final_moves[-1]
            do_move(final_moves, agent)
            state_new = agent.get_state(vehicles_in_step)

            reward = agent.set_reward(get_vehicle_speed_average(), len(collisions_in_step))
            print("Current reward: ", reward)
            if params['train']:
                agent.train_short_memory(state_old, final_move, reward, state_new, False)
                agent.remember(state_old, final_move, reward, state_new, False)
            
            if params['train']:
                agent.replay_new(agent.memory, params['batch_size'])
                agent.model.save_weights(params['weights_path'])

            score_plot.append(reward)
            counter_plot.append(i)

            collisions_in_step.clear()
    
    print("Counter plot: ", counter_plot)
    print("Score plot: ", score_plot )
    plot_seaborn(counter_plot, score_plot)            

            

     
        


def init_sim(params, agent, batch_size):
    state_init1 = agent.get_state(vehicles_in_step)#add params
    action = []
    for i in range(len(vehicles_in_step)):
        x = randint(0,1)
        if x==1:
            action.append(1)
            action.append(0)
        else:
            action.append(0)
            action.append(1)

    do_move(action, agent)
    state_init2 = agent.get_state(vehicles_in_step)#add params
    reward1 = agent.set_reward(get_vehicle_speed_average(), len(collisions_in_step))
    agent.remember(state_init1, action, reward1, state_init2, False)
    agent.replay_new(agent.memory, batch_size)

def do_move(action, agent):
    act =[]
    for i, j in zip(range(0,len(action)//2,2), vehicles_in_step.keys()):
        
        act.append(action[i])
        act.append(action[i+1])
        print("action (do_move)")
        print(act)

        if np.array_equal(act,[1,0]):
            #speed up to set speed
            eng.set_vehicle_speed(j, CRUISING_SPEED)
            print("speed up")
            
        elif np.array_equal(act,[0,1]):
            #slow down to 60% of set speed
            eng.set_vehicle_speed(j, CRUISING_SPEED*0.6)
            print("slow down")
        act.clear()
    

    
        

            

if __name__ == '__main__':
    _rerun(define_parameters())
    print("Completed 5 runs containing 200 steps. 1000 steps total")
    exit()
