from Simulator.simulator import Simulator
from MDP.MDP import MDP

if __name__ == "__main__":
    '''
    Runner code to start the training and game play.
    '''
    #Testing some stuff
    '''
    # mdp= MDP(0.5, 0.5, 0.03, 0.01, 0.4)
    mdp= MDP(1.0, 0.05, 0.03, 0.01, 0)
    for i in range(0,1): 
        mdp.simulate_one_time_step(1)
    mdp.discretize_state()
    print("CONTINUOUS: \nball_x: " + str(mdp.ball_x) + "\nball_y: " + str(mdp.ball_y) + "\nvelocity_x: " + str(mdp.velocity_x) + "\nvelocity_y: " +  str(mdp.velocity_y) + "\npaddle_y " + str(mdp.paddle_y) + "\nmiss: " + str(mdp.miss))
    print("\nDISCRETE: \nball_x: " + str(mdp.dis_ball_x) + "\nball_y: " + str(mdp.dis_ball_y) + "\nvelocity_x: " + str(mdp.dis_velocity_x) + "\nvelocity_y: " +  str(mdp.dis_velocity_y) + "\npaddle_y " + str(mdp.dis_paddle_y) + "\nmiss: " + str(mdp.miss))
    '''
    '''
    alpha_value = 0.4
    gamma_value = 0.95
    epsilon_value = 0.04
    num_games = 1000
    '''
    alpha_value = 0.4
    gamma_value = 0.95
    epsilon_value = 0.04
    num_games = 1000
    Simulator(num_games, alpha_value, gamma_value, epsilon_value)
   