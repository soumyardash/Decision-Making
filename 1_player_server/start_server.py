from utils import *
from thread import *
from math import pi
import time
import sys
import os
import argparse
import socket

start_time = time.time()
# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-v', '--visualization', dest="vis", type=int, default=0, help='visualization on/off')
parser.add_argument('-rr', '--', dest="render_rate", type=int, default=60, help='Render every nth frame')
parser.add_argument('-p', '--port', dest="port1", type=int, default=12121, help='Port for incoming connection')
parser.add_argument('-rs', '--random-seed', dest="rng", type=int, default=0, help='Random Seed')
parser.add_argument('-n', '--noise', dest="noise", type=int, default=1, help='Turn noise on/off')
parser.add_argument('-log', '--log', dest="log", type=str, default="log1", help='Name of logfile')
args = parser.parse_args()
log = args.log
render_rate = args.render_rate
vis = args.vis
port1 = args.port1
random.seed(args.rng)
host = '127.0.0.1'   # Symbolic name meaning all available interfaces
noise = args.noise
if noise == 1:
    noise1 = 0.005
    noise2 = 0.01
    noise3 = 2
else:
    noise1 = 0
    noise2 = 0
    noise3 = 0
timeout_msg = "TIMED OUT"
timeout_period = 0.5
##########################################################################

def play(state, player, action):
    pygame.init()
    clock = pygame.time.Clock()
    if vis == 1:
        screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
        pygame.display.set_caption("Carrom RL Simulation")
    space = pymunk.Space(threaded=True)
    location_self = state["location_self"]
    location_op = state["location_op"]
    HP_self = state["HP"]
    defense = state["defense"]
    barrel_heat = state["barrel_heat"]
    projectiles_left = state["projectiles_left"]
    # Setup arena
    obstacles = setup_level(space)
    # player 1
    player1_armors = []
    player1_body = pymunk.Body(500,pymunk.inf)
    player1_body.position = 300, 100
    player1_shape = pymunk.Circle(player1_body, (300*f2))
    player1_shape.elasticity = 0
    player1_shape.friction = 1.0
    player1_shape.color = THECOLORS['red']
    player1_shape.collision_type = collision_types["player"]
    armor = pymunk.Segment(player1_body,(-300*f2,-65*f2),(-300*f2,65*f2),2)
    armor.color=THECOLORS['black']
    armor.collision_type = collision_types["armor1"]
    player1_armors.append(armor)
    armor = pymunk.Segment(player1_body,(-65*f2,-300*f2),(65*f2,-300*f2),2)
    armor.color=THECOLORS['black']
    armor.collision_type = collision_types["armor1"]
    player1_armors.append(armor)
    armor = pymunk.Segment(player1_body,(300*f2,-65*f2),(300*f2,65*f2),2)
    armor.color=THECOLORS['black']
    armor.collision_type = collision_types["armor1"]
    player1_armors.append(armor)
    armor = pymunk.Segment(player1_body,(-65*f2,300*f2),(65*f2,300*f2),2)
    armor.color=THECOLORS['black']
    armor.collision_type = collision_types["armor1"]
    player1_armors.append(armor)
    anglen=armor._get_normal
    angle=0
    player1_shape7 = pymunk.Segment(player1_body,(0,0),(250*f2*cos(angle),250*f2*sin(angle)),3)
    player1_shape7.color = THECOLORS['blue']
    space.add(player1_body, player1_shape)
    #player 2
    player2_armors = []
    player2_body = pymunk.Body(500,pymunk.inf)
    player2_body.position = 500, 600
    player2_shape = pymunk.Circle(player2_body, (300*f2))
    player2_shape.elasticity = 0
    player2_shape.friction = 1.0
    player2_shape.color = THECOLORS['red']
    player2_shape.collision_type = collision_types["player2"]
    armor = pymunk.Segment(player2_body,(-300*f2,-65*f2),(-300*f2,65*f2),2)
    armor.color=THECOLORS['black']
    armor.collision_type = collision_types["armor2"]
    player2_armors.append(armor)
    armor = pymunk.Segment(player2_body,(-65*f2,-300*f2),(65*f2,-300*f2),2)
    armor.color=THECOLORS['black']
    armor.collision_type = collision_types["armor2"]
    player2_armors.append(armor)
    armor = pymunk.Segment(player2_body,(300*f2,-65*f2),(300*f2,65*f2),2)
    armor.color=THECOLORS['black']
    armor.collision_type = collision_types["armor2"]
    player2_armors.append(armor)
    armor = pymunk.Segment(player2_body,(-65*f2,300*f2),(65*f2,300*f2),2)
    armor.color=THECOLORS['black']
    armor.collision_type = collision_types["armor2"]
    player2_armors.append(armor)
    angle=0
    player2_shape7 = pymunk.Segment(player2_body,(0,0),(250*f2*cos(angle),250*f2*sin(angle)),3)
    player2_shape7.color = THECOLORS['blue']
    space.add(player2_body, player2_shape)

    # 1 - Shoot action = {action_type, yaw, speed}
    # 2 - Chase action = {action_type, position, orientation} Cover even rotating in a given position in order to be able to shoot
    # 3 - Refill action = {action_type, position, orientation} Position of the refill zone and the best orientation of the robot
    # 4 - Defense action = {action_type, position, orientation} Position of the defense zone and the best orientaton of the robot
    # 5 - Escape action = {action_type, position, orientation} Position and orientation of the robot in the best escape spot
    if action[0] == 1: #Shoot
        spawn_ball(space, player1_body.position, action[1])
    elif action[0] == 2: #Chase
        #TODO
    elif action[0] == 3: #Refill
        #TODO
    elif action[0] == 4: #Defense
        #TODO
    elif action[0] == 5: #Escape
        #TODO

    if vis == 1:
        draw_options = pymunk.pygame_util.DrawOptions(screen)
    ticks = 0
    while 1:
        if ticks % render_rate == 0:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    sys.exit(0)
        ticks += 1
        space.step(1 / TIME_STEP)
        # Remove projectiles collided with obstacle
        for projectile in projectiles:
            for obstacle in obstacles
            if dist(projectile.body.position, obstacle.body.position) < 1:
                space.remove(projectile, projectile.body)
                break
        # Remove projectiles collided with armor module
        for projectile in projectiles:
            for armor in player1_armors:
                if dist(projectile.body.position, armor.body.position) < 1:
	            if defense > 0: #Within 30s of defense zone
                    HP -= 25
                    score2 += 25
                else: 
                    HP -= 50
                    score2 += 50
                space.remove(projectile, projectile.body)

        if local_vis == 1:
            font = pygame.font.Font(None, 25)
            text = font.render("Score 1: " +
                               str(score1), 1, (220, 220, 220))
            screen.blit(text, (8000 * 0.14 / 2 - 40, 780, 0, 0))

            text = font.render("Time Elapsed: " +
                               str(round(time.time() - start_time, 2)), 1, (50, 50, 50))
            screen.blit(text, (8000 * 0.14 / 3 + 57, 25, 0, 0))

            # First tick, draw an arrow representing action
            if ticks == 1:
                action_type = action[0]
                if action_type == 1: #Shoot
                    #TODO
                elif action_type == 2: #Chase
                    #TODO
                elif action_type == 3: #Refill
                    #TODO
                elif action_type == 4: #Defense
                    #TODO
                elif action_type == 5: #Escape
                    #TODO

            pygame.display.flip()
            if ticks == 1:
                time.sleep(1)

            clock.tick()
           
        # Do post processing and return the next State
        if HP1 == 0 or HP2 == 0 or ticks > TICKS_LIMIT:
            state_new = {"location_self": [], "location_op": [], "HP": 0, "defense": 0, "barrel_heat": 0, "projectiles_left": 0}
            state_new["location_self"] = player1_body.body_position
            state_new["location_op"] = player2_body.body_position
            state_new["HP"] = HP
            state_new["defense"] = defense
            if action[0] == 1: #Shoot
                state_new["barrel_heat"] = state_new["barrel_heat"] + action[2]
                
            return state_new, score1-prevscore1, score2-prevscore2

# Generate logs
def logger(log, msg):
    f = open("logs/"+log, "a")
    f.write(msg)
    f.close()


# The server receives an action from the agent
def request_action(conn1):
    try:
        data = conn1.recv(1024)
    except:
        data = timeout_msg
    finally:
        return data

# The server sends it's state to the agent


def send_state(state, conn1):
    try:
        conn1.send(state)
    except socket.error:
        print "Aborting, player did not respond within timeout"
        #logger(log, "Aborting, player did not respond within timeout\n")
        sys.exit()
    return True


if __name__ == '__main__':

    # Bind to socket, and wait for the agent to connect
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s1.bind((host, port1))
    except socket.error as msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

    s1.listen(1)
    conn1, addr1 = s1.accept()
    conn1.settimeout(timeout_period)

    winner = 0
    reward = 0
    score1 = 0

    state = INITIAL_STATE
    next_state = state

    it = 0

    while it < 5000:  # Number of chances given to the player
        it += 1
        # print "Sending ", next_state
        send_state(str(next_state) + str(reward), conn1)
        s = request_action(conn1)
        if not s:  # response empty
            print "No response from player 1, aborting"
            #logger(log, "No response from player 1, aborting\n")
            sys.exit()
        elif s == timeout_msg:
            print "Player 1 timeout, aborting"
            #logger(log, "Player 1 timeout, aborting\n")
            sys.exit()
        else:
            action = tuplise(s.replace(" ", "").split(','))

        '''next_state, queen_flag, reward = play(
            next_state, 1, validate(action, next_state))'''
        # call play function here    

        
    if it >= 5000:
        #logger(log, "Player took more than 500 turns, aborting\n")
        print "Player took more than 500 turns, aborting"
        sys.exit()

    tmp = "Cleared Board in " + str(it) + " turns. Realtime taken: "+str(time.time(
    ) - start_time)+" s @ "+str(round((it*1.0)/(time.time() - start_time), 2)) + " turns/s" +" with random seed " + str(args.rng) + "\n"
    #logger(log, tmp)
    don(s1, conn1)
