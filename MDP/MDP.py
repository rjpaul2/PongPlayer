from random import uniform
from math import floor

class MDP:
    
    def __init__(self, 
                 ball_x=None,
                 ball_y=None,
                 velocity_x=None,
                 velocity_y=None,
                 paddle_y=None):
        '''
        Setup MDP with the initial values provided.
        '''
        self.create_state(
            ball_x=ball_x,
            ball_y=ball_y,
            velocity_x=velocity_x,
            velocity_y=velocity_y,
            paddle_y=paddle_y
        )
        
        # the agent can choose between 3 actions - stay, up or down respectively.
        self.actions = [0, 0.04, -0.04]
        # Added state for the case of a miss (reward -1)
        self.miss = False
        
        # Discrete states
        self.dis_ball_x = None
        self.dis_ball_y = None
        self.dis_velocity_x = None
        self.dis_velocity_y = None
        self.dis_paddle_y = None
        
    
    def create_state(self,
              ball_x=None,
              ball_y=None,
              velocity_x=None,
              velocity_y=None,
              paddle_y=None):
        '''
        Helper function for the initializer. Initialize member variables with provided or default values.
        '''
        self.paddle_height = 0.2
        self.ball_x = ball_x if ball_x != None else 0.5
        self.ball_y = ball_y if ball_y != None else 0.5
        self.velocity_x = velocity_x if velocity_x != None else 0.03
        self.velocity_y = velocity_y if velocity_y != None else 0.01
        # changed from self.paddle_y = 0.5
        self.paddle_y = paddle_y if paddle_y != None else 0.5
    
    def create_dis_state(self,
              dis_ball_x,
              dis_ball_y,
              dis_velocity_x,
              dis_velocity_y,
              dis_paddle_y):
        '''
        Changes discrete state.
        '''
        self.dis_ball_x = dis_ball_x 
        self.dis_ball_y = dis_ball_y 
        self.dis_velocity_x = dis_velocity_x 
        self.dis_velocity_y = dis_velocity_y 
        self.dis_paddle_y = dis_paddle_y 
    
    
    def simulate_one_time_step(self, action_selected):
        '''
        :param action_selected - Current action to execute.
        Perform the action on the current continuous state.
        '''

        # Update the paddle position
        new_paddle_y = self.paddle_y + self.actions[action_selected] 
        if new_paddle_y < 0.0:
            new_paddle_y = 0
        elif new_paddle_y > 1.0 - self.paddle_height:
            new_paddle_y = 1.0 - self.paddle_height
             
        # Update ball velocities and positions   
        new_ball_x = self.ball_x + self.velocity_x
        new_ball_y = self.ball_y + self.velocity_y
        new_velocity_x = self.velocity_x
        new_velocity_y = self.velocity_y
        
        # Ball hits top
        if new_ball_y < 0:
            new_ball_y = -1.0 * new_ball_y
            new_velocity_y = -1.0 * self.velocity_y
        # Ball hits bottom
        elif new_ball_y > 1.0:
            new_ball_y = 2.0 - new_ball_y
            new_velocity_y = -1.0 * self.velocity_y
        # Ball hits side
        elif new_ball_x < 0:
            new_ball_x = -1.0 * new_ball_x
            new_velocity_x = -1.0 * self.velocity_x
        # Ball hits paddle - ?????? how do we decide collision ?????
        elif new_ball_x >= 1.0 and new_ball_y > new_paddle_y and new_ball_y < new_paddle_y + self.paddle_height:
            new_ball_x = 2.0 - new_ball_x 
            U = uniform(-0.015, 0.015)
            V = uniform(-0.03,0.03)
            new_velocity_x = -1.0 * new_velocity_x + U
            new_velocity_y = new_velocity_y + V
            # Check if |velocity_x| < 0.03
            if new_velocity_x < 0.03 and new_velocity_x >= 0:
                new_velocity_x = 0.03
            elif new_velocity_x > -0.03 and new_velocity_x < 0:
                new_velocity_x = -0.03
        elif new_ball_x > 1.0:
            self.miss = True
            
        # Check if |velocity_x| < 1 and |velocity_y| < 1
        if new_velocity_x > 1.0:
            new_velocity_x = 1.0
        elif new_velocity_x < -1.0:
            new_velocity_x = -1.0
        if new_velocity_y > 1.0:
            new_velocity_y = 1.0
        elif new_velocity_y < -1.0:
            new_velocity_y = -1.0
        
        # Update state with the new found values
        self.create_state(new_ball_x, new_ball_y, new_velocity_x, new_velocity_y, new_paddle_y)
       
        
    
    def discretize_state(self):
        '''
        Convert the current continuous state to a discrete state.
        '''
        # Your Code Goes Here!
        # Discretize ball_x
        if self.ball_x >= 1:
            dis_ball_x = 11
        else:
            dis_ball_x = floor(12 * self.ball_x)
            
        # Discretize ball_y
        if self.ball_y >= 1:
            dis_ball_y = 11
        else:
            dis_ball_y = floor(12 * self.ball_y)
            
        # Discretize velocity_x
        dis_velocity_x = 1 if self.velocity_x >= 0 else -1
        
        # Discretize velocity_y
        if self.velocity_y < 0.015 and self.velocity_y > -0.015:
            dis_velocity_y = 0
        elif self.velocity_y > 0:
            dis_velocity_y = 1
        elif self.velocity_y < 0:
            dis_velocity_y = -1
            
        # Discretize paddle_y
        if self.paddle_y == 1 - self.paddle_height:
            dis_paddle_y = 11
        else: dis_paddle_y = floor(12 * self.paddle_y/(1 - self.paddle_height))
        '''
        # Special state - Check that this doesn't screw with the non-discrete detection
        if self.ball_x > 1:
            self.miss = True 
        '''
   
        # Update the state with new discrete data
        self.create_dis_state(dis_ball_x, dis_ball_y, dis_velocity_x, dis_velocity_y, dis_paddle_y)