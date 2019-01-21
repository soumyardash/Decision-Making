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

parser.add_argument('-v', '--visualization', dest="vis", type=int,
                    default=0,
                    help='visualization on/off')

parser.add_argument('-rr', '--', dest="render_rate", type=int,
                    default=60,
                    help='Render every nth frame')

parser.add_argument('-p', '--port', dest="port1", type=int,
                    default=12121,
                    help='Port for incoming connection')

parser.add_argument('-rs', '--random-seed', dest="rng", type=int,
                    default=0,
                    help='Random Seed')

parser.add_argument('-n', '--noise', dest="noise", type=int,
                    default=1,
                    help='Turn noise on/off')

parser.add_argument('-log', '--log', dest="log", type=str,
                    default="log1",
                    help='Name of logfile')

args = parser.parse_args()

log = args.log
render_rate = args.render_rate
vis = args.vis
port1 = args.port1
random.seed(args.rng)

host = '127.0.0.1'   # Symbolic name meaning all available interfaces


timeout_msg = "TIMED OUT"
timeout_period = 0.5

##########################################################################




def play(state, player, action):
    pygame.init()
    screen = pygame.display.set_mode((width,height)) 
    pygame.display.set_caption("ERA RL Simulation")
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.SysFont("Arial", 16)
    ### Physics stuff
    space = pymunk.Space(threaded=True)
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    setup_level(space)
    ticks = 0
    

    # Player description
    
    # player 1
    player1_body = pymunk.Body(500,pymunk.inf)
    player1_body.position = 300, 100
    player1_shape = pymunk.Circle(player1_body, (300*f2))
    player1_shape.elasticity = 0
    player1_shape.friction = 1.0
    player1_shape.color = THECOLORS['red']
    player1_shape.collision_type = collision_types["player"]
    
    player1_shape3 = pymunk.Segment(player1_body,(-300*f2,-65*f2),(-300*f2,65*f2),2)
    player1_shape3.color=THECOLORS['black']
    player1_shape3.collision_type = collision_types["armor1"]

    player1_shape4 = pymunk.Segment(player1_body,(-65*f2,-300*f2),(65*f2,-300*f2),2)
    player1_shape4.color=THECOLORS['black']
    player1_shape4.collision_type = collision_types["armor1"]

    player1_shape5 = pymunk.Segment(player1_body,(300*f2,-65*f2),(300*f2,65*f2),2)
    player1_shape5.color=THECOLORS['black']
    player1_shape5.collision_type = collision_types["armor1"]

    player1_shape6 = pymunk.Segment(player1_body,(-65*f2,300*f2),(65*f2,300*f2),2)
    player1_shape6.color=THECOLORS['black']
    player1_shape6.collision_type = collision_types["armor1"]
    anglen=player1_shape6._get_normal
    

    angle=0
    player1_shape7 = pymunk.Segment(player1_body,(0,0),(250*f2*cos(angle),250*f2*sin(angle)),3)
    player1_shape7.color = THECOLORS['blue']
    


    #player 2
    player2_body = pymunk.Body(500,pymunk.inf)
    player2_body.position = 500, 600
    
    player2_shape = pymunk.Circle(player2_body, (300*f2))
    player2_shape.elasticity = 0
    player2_shape.friction = 1.0
    player2_shape.color = THECOLORS['red']

    player2_shape.collision_type = collision_types["player2"]
    



    player2_shape3 = pymunk.Segment(player2_body,(-300*f2,-65*f2),(-300*f2,65*f2),2)
    player2_shape3.color=THECOLORS['black']
    player2_shape3.collision_type = collision_types["armor2"]

    player2_shape4 = pymunk.Segment(player2_body,(-65*f2,-300*f2),(65*f2,-300*f2),2)
    player2_shape4.color=THECOLORS['black']
    player2_shape4.collision_type = collision_types["armor2"]

    player2_shape5 = pymunk.Segment(player2_body,(300*f2,-65*f2),(300*f2,65*f2),2)
    player2_shape5.color=THECOLORS['black']
    player2_shape5.collision_type = collision_types["armor2"]

    player2_shape6 = pymunk.Segment(player2_body,(-65*f2,300*f2),(65*f2,300*f2),2)
    player2_shape6.color=THECOLORS['black']
    player2_shape6.collision_type = collision_types["armor2"]
    
    

    angle=0
    player2_shape7 = pymunk.Segment(player2_body,(0,0),(250*f2*cos(angle),250*f2*sin(angle)),3)
    player2_shape7.color = THECOLORS['blue']




    def remove_first(arbiter, space, data):
        ball_shape = arbiter.shapes[0]
        space.remove(ball_shape, ball_shape.body)
        return True
    h = space.add_collision_handler(
        collision_types["ball"], 
        collision_types["brick"])
    h.begin = remove_first

    def hit_armor(arbiter, space, data):
        global hp2
        ball_shape = arbiter.shapes[0]
        armor_shape = arbiter.shapes[1]
        space.remove(ball_shape, ball_shape.body)
        hp2=hp2-10
        print("hooray")
        #print(arbiter.shapes)
        #print( space.shape_query(armor_shape))
        return True
    def hitend_armor(arbiter, space, data):
        player2_body.velocity=(0,0)
        player2_body.angular_velocity = 0
    h = space.add_collision_handler(
        collision_types["ball"], 
        collision_types["armor2"])
    h.begin = hit_armor
    h.separate = hitend_armor
    def hit_player(arbiter, space, data):
        ball_shape = arbiter.shapes[0]
        space.remove(ball_shape, ball_shape.body)
        return True
    def hitend_armor(arbiter, space, data):
        player2_body.velocity=(0,0)
        player2_body.angular_velocity = 0
    h = space.add_collision_handler(
        collision_types["ball"], 
        collision_types["player2"])
    h.begin = hit_player
    h.separate = hitend_armor

    def player_collision(arbiter, space, data):
        player1_body.velocity=(0,0)
        player1_body.angular_velocity = 0
        player2_body.velocity=(0,0)
        player2_body.angular_velocity = 0
        print("hit it")
    h1 = space.add_collision_handler(
        collision_types["player"], 
        collision_types["player2"])
    h2 = space.add_collision_handler(
        collision_types["player"], 
        collision_types["armor2"])
    h3 = space.add_collision_handler(
        collision_types["player2"], 
        collision_types["armor2"])
    h4 = space.add_collision_handler(
        collision_types["armor1"], 
        collision_types["armor2"])
    h1.begin = player_collision
    h1.separate = player_collision
    h2.begin = player_collision
    h2.separate = player_collision
    h3.begin = player_collision
    h3.separate = player_collision
    h4.begin = player_collision
    h4.separate = player_collision

    def wall1_collision(arbiter, space, data):
        player_body.velocity=(0,0)
        player_body.angular_velocity = 0
        print("hit the wall")
    def wall2_collision(arbiter, space, data):
        player2_body.velocity=(0,0)
        player2_body.angular_velocity = 0
        print("hit the wall")
    h1 = space.add_collision_handler(
        collision_types["player"], 
        collision_types["brick"])
    h2 = space.add_collision_handler(
        collision_types["player2"], 
        collision_types["brick"])
    h3 = space.add_collision_handler(
        collision_types["brick"], 
        collision_types["armor2"])
    h4 = space.add_collision_handler(
        collision_types["armor1"], 
        collision_types["brick"])
    h1.separate = wall1_collision
    h2.separate = wall2_collision
    h3.separate = wall2_collision
    h4.separate = wall1_collision












    while 1:

        if ticks % render_rate == 0:
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    sys.exit(0)
        

        ticks += 1

        
        
        space.debug_draw(draw_options)

        space.step(1 / TIME_STEP)

        # Remove pocketed striker

        
        # Remove pocketed coins

        

        
        

        

        pygame.display.flip()
        if ticks == 1:
            time.sleep(1)

        clock.tick()

        # Do post processing and return the next State
        if is_ended(space) or ticks > TICKS_LIMIT:
            '''state_new = {"Black_Locations": [],
                         "White_Locations": [], "Red_Location": [], "Score": 0}

            for coin in space._get_shapes():
                if coin.color == BLACK_COIN_COLOR:
                    state_new["Black_Locations"].append(coin.body.position)
                if coin.color == WHITE_COIN_COLOR:
                    state_new["White_Locations"].append(coin.body.position)
                if coin.color == RED_COIN_COLOR:
                    state_new["Red_Location"].append(coin.body.position)
            if foul == True:
                print "Foul.. striker pocketed"
                for coin in pocketed:
                    if coin[0].color == BLACK_COIN_COLOR:
                        state_new["Black_Locations"].append(ret_pos(state_new))
                        score -= 1
                    if coin[0].color == WHITE_COIN_COLOR:
                        state_new["White_Locations"].append(ret_pos(state_new))
                        score -= 1
                    if coin[0].color == RED_COIN_COLOR:
                        state_new["Red_Location"].append(ret_pos(state_new))

            if (queen_pocketed == True and foul == False):
                if len(state_new["Black_Locations"]) + len(state_new["White_Locations"]) == 18:
                    print "The queen cannot be the first to be pocketed: player ", player
                    state_new["Red_Location"].append(ret_pos(state_new))
                else:
                    if score - prevscore > 0:
                        score += 3
                        print "Queen pocketed and covered in one shot"
                    else:
                        queen_flag = True

            if len(state_new["Black_Locations"]) == 0 and len(state_new["White_Locations"]) == 0:
                if len(state_new["Red_Location"]) > 0:
                    state_new["Black_Locations"].append(ret_pos(state_new))
                    score -= 1
                    print "Failed to clear queen, getting another turn"

            state_new["Score"] = score
            print "Coins Remaining: ", len(state_new["Black_Locations"]), "B ", len(state_new["White_Locations"]), "W ", len(state_new["Red_Location"]), "R"'''
            return state_new, queen_flag, score-prevscore



# Generate logs


'''def logger(log, msg):
    f = open("logs/"+log, "a")
    f.write(msg)
    f.close()'''


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
