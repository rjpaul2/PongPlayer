from MDP.MDP import MDP
import random
from math import floor, inf

class Simulator:
    
    def __init__(self, num_games=0, alpha_value=0, gamma_value=0, epsilon_value=0):
        '''
        Setup the Simulator with the provided values.
        :param num_games - number of games to be trained on.
        :param alpha_value - 1/alpha_value is the decay constant.
        :param gamma_value - Discount Factor.
        :param epsilon_value - Probability value for the epsilon-greedy approach.
        '''
        self.num_games = num_games       
        self.epsilon_value = epsilon_value       
        self.alpha_value = alpha_value       
        self.gamma_val = gamma_value
        
        self.total_rebounds = 0
        self.mdp= MDP(0.5, 0.5, 0.03, 0.01, 0.4)
        #self.Q = [[[[[[0] * 3] * 12] * 3] * 2] * 12] * 12
        self.Q = [[[[[[0 for i in range(3)] for j in range(12)] for k in range(3)] for l in range(2)] for m in range(12)] for n in range(12)]
        #self.R = [[[[[0] * 12] * 3] * 2] * 12] * 12
        self.R = [[[[[0 for i in range(12)] for j in range(3)] for k in range(2)] for l in range(12)] for m in range(12)]
        
        self.train_agent()
    
    def f_function(self):
        '''
        Choose action based on an epsilon greedy approach
        :return action selected
        '''
        action_selected = None
        
        self.mdp.discretize_state()
        r = random.random()
        if(r > self.epsilon_value):
            curr_max = 0
            for a in range(0,3):
                if self.Q[self.mdp.dis_ball_x][self.mdp.dis_ball_y][self.mdp.dis_velocity_x][self.mdp.dis_velocity_y][self.mdp.dis_paddle_y][a] >= curr_max:
                    curr_max = self.Q[self.mdp.dis_ball_x][self.mdp.dis_ball_y][self.mdp.dis_velocity_x][self.mdp.dis_velocity_y][self.mdp.dis_paddle_y][a]
                    action_selected = a
            # If they're all zeros, chose one at random
            if curr_max == 0:
                action_selected = floor(random.random() * 3)
        else:
            action_selected = floor(random.random() * 3) 
            
        # Create a temporary MDP for help with the Q learning formula, in order to look forward into the future
        temp_mdp = MDP(self.mdp.ball_x, self.mdp.ball_y, self.mdp.velocity_x, self.mdp.velocity_y, self.mdp.paddle_y)
        temp_mdp.simulate_one_time_step(action_selected)
        temp_mdp.discretize_state()
        max_a_prime = max(self.Q[temp_mdp.dis_ball_x][temp_mdp.dis_ball_y][temp_mdp.dis_velocity_x][temp_mdp.dis_velocity_y][temp_mdp.dis_paddle_y][0],
                          self.Q[temp_mdp.dis_ball_x][temp_mdp.dis_ball_y][temp_mdp.dis_velocity_x][temp_mdp.dis_velocity_y][temp_mdp.dis_paddle_y][1],
                          self.Q[temp_mdp.dis_ball_x][temp_mdp.dis_ball_y][temp_mdp.dis_velocity_x][temp_mdp.dis_velocity_y][temp_mdp.dis_paddle_y][2])
                    

        # Update Q via the learning function
        self.Q[self.mdp.dis_ball_x][self.mdp.dis_ball_y][self.mdp.dis_velocity_x][self.mdp.dis_velocity_y][self.mdp.dis_paddle_y][action_selected] = \
        (1 - self.alpha_value) * self.Q[self.mdp.dis_ball_x][self.mdp.dis_ball_y][self.mdp.dis_velocity_x][self.mdp.dis_velocity_y][self.mdp.dis_paddle_y][action_selected] \
         + self.alpha_value * (self.R[self.mdp.dis_ball_x][self.mdp.dis_ball_y][self.mdp.dis_velocity_x][self.mdp.dis_velocity_y][self.mdp.dis_paddle_y] + self.gamma_val * max_a_prime)
                 
        return action_selected

    def train_agent(self):
        '''
        Train the agent over a certain number of games.
        '''
        for i in range(0, self.num_games):
            self.mdp= MDP(0.5, 0.5, 0.03, 0.01, 0.4)
            self.play_game()
        
        '''Testing
        print("\nAvg Rebounds: " + str(self.total_rebounds / self.num_games))

        print("\nTotal Rebounds:" + str(self.total_rebounds))
        
        self.total_rebounds = 0
        for i in range(0,6):
            self.play_game()
        
        print("\nRebounds after training: " + str(self.total_rebounds / 5))
      
        #print(str(self.R))
        #print(str("\n" + str(self.Q)))
        '''
    
    def play_game(self):
        '''
        Simulate an actual game till the agent loses.
        '''
        while self.mdp.miss != True:
            # Ball hits paddle, update reward
            reward = 0
            self.mdp.simulate_one_time_step(self.f_function())
            if self.mdp.dis_paddle_y == self.mdp.dis_ball_y and self.mdp.dis_ball_x == 11:
                reward = 1
                self.total_rebounds = self.total_rebounds + 1
            elif self.mdp.dis_paddle_y != self.mdp.dis_ball_y and self.mdp.dis_ball_x == 11:
                reward = -1
  
            # print("CONTINUOUS: \nball_x: " + str(self.mdp.ball_x) + "\nball_y: " + str(self.mdp.ball_y) + "\nvelocity_x: " + str(self.mdp.velocity_x) + "\nvelocity_y: " +  str(self.mdp.velocity_y) + "\npaddle_y " + str(self.mdp.paddle_y) + "\nmiss: " + str(self.mdp.miss))
            # print("\nDISCRETE: \nball_x: " + str(self.mdp.dis_ball_x) + "\nball_y: " + str(self.mdp.dis_ball_y) + "\nvelocity_x: " + str(self.mdp.dis_velocity_x) + "\nvelocity_y: " +  str(self.mdp.dis_velocity_y) + "\npaddle_y " + str(self.mdp.dis_paddle_y) + "\nmiss: " + str(self.mdp.miss))

            self.R[self.mdp.dis_ball_x][self.mdp.dis_ball_y][self.mdp.dis_velocity_x][self.mdp.dis_velocity_y][self.mdp.dis_paddle_y] = reward
        
                
                
        
