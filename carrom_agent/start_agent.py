from thread import *
import time
import socket
import sys
import argparse
import random
import ast

# Parse arguments
parser = argparse.ArgumentParser()
'''parser.add_argument('-np', '--num-players', dest="num_players", type=int,
                    default=1,
                    help='1 Player or 2 Player')'''
parser.add_argument('-p', '--port', dest="port", type=int, default=12121, help='port')
parser.add_argument('-rs', '--random-seed', dest="rng", type=int, default=0, help='Random Seed')
parser.add_argument('-c', '--color', dest="color", type=str, default="Black", help='Legal color to pocket')
args = parser.parse_args()

host = '127.0.0.1'
port = args.port
num_players = args.num_players
random.seed(args.rng)  # Important
color = args.color

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect((host, port))

# Given a message from the server, parses it and returns state and action
def parse_state_message(msg):
    s = msg.split(";REWARD")
    s[0] = s[0].replace("Vec2d", "")
    try:
        reward = float(s[1])
    except:
        reward = 0
    state = ast.literal_eval(s[0])
    return state, reward

def agent_1player(state):
    flag = 1
    # print state
    try:
        state, reward = parse_state_message(state)  # Get the state and reward
    except:
        pass

    # Choose an action based on observation
    a = PG.choose_action(state)
    
    try:
        s.send(a)
    except Exception as e:
        print "Error in sending:",  a, " : ", e
        print "Closing connection"
        flag = 0
        
    # Store transition for training
    PG.store_transition(state, a, reward)

    return flag

if __name__ == "__main__":

    # Load checkpoint
    load_version = 8
    save_version = load_version + 1
    load_path = "output/weights/LunarLander/{}/LunarLander-v2.ckpt".format(load_version)
    save_path = "output/weights/LunarLander/{}/LunarLander-v2.ckpt".format(save_version)

    global PG = PolicyGradient(
        n_x = ,#add shape of state space
        n_y = ,#add shape of action space
        learning_rate=0.02,
        reward_decay=0.99,
        load_path=load_path,
        save_path=save_path
    )


    for episode in range(EPISODES):

        
        episode_reward = 0

        tic = time.clock()

        while True:
            state=s.recv(1024)# receive state from server
            if agent_1player(state)==0:
                break
            toc = time.clock()
            elapsed_sec = toc - tic
            if elapsed_sec > 180:
                done = True

            episode_rewards_sum = sum(PG.episode_rewards)
            if episode_rewards_sum < -250:
                done = True

            if done:
                episode_rewards_sum = sum(PG.episode_rewards)
                rewards.append(episode_rewards_sum)
                max_reward_so_far = np.amax(rewards)

                print("==========================================")
                print("Episode: ", episode)
                print("Seconds: ", elapsed_sec)
                print("Reward: ", episode_rewards_sum)
                print("Max reward so far: ", max_reward_so_far)

                # Train neural network
                discounted_episode_rewards_norm = PG.learn()

                


                break

        s.close()

            
