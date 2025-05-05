from mesa import Agent

class PersonAgent(Agent):
    """
    Agent is simulating the person behaviour during epidemic.
    It can be rather infected (self.infected)
    It may have comorbidities (self.has_comorbidities)
    And it also can have it self moving_probability (self.moving_probability)
    """
    def __init__(self, model, unique_id, is_infected=False, has_comorbidities=False, moving_probability=1.0):
        super().__init__(model) 
        
        # Initialization of the agent parameters
        self.unique_id = unique_id
        self.is_infected = is_infected
        self.has_comorbidities = has_comorbidities
        self.moving_probability = moving_probability

    def move(self):
        """
        Move agent to a random cell with a certain probability.
        """
        if self.random.random() < self.moving_probability:
            possible_steps = self.model.grid.get_neighborhood(
                self.pos,
                moore=False,
                include_center=False
            )
            new_position = self.random.choice(possible_steps)
            self.model.grid.move_agent(self, new_position)
    
    def step(self):
        """Defines agent behavior at each step."""
        # If infected agent infects location and around
        if self.is_infected:
            self.model.infect_locations_around(self.pos)
        
        # 1. If not, trial to be infected by other agents (same loc)
        if not self.is_infected:
            agents_here = self.model.grid.get_cell_list_contents([self.pos])
            for other in agents_here:
                if other.is_infected:
                    chance = 0.5 + (0.25 if self.has_comorbidities else 0)
                    if self.random.random() < chance:
                        self.is_infected = True
                        return
            
            # 2. Trial to infect from loc
            infection_chance = 0
            if self.pos in self.model.infected_locations:
                infection_chance = 0.5
            else:
                neighbors = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
                if any(n in self.model.infected_locations for n in neighbors):
                    infection_chance = 0.5
            
            if infection_chance > 0:
                infection_chance += 0.25 if self.has_comorbidities else 0
                if self.random.random() < infection_chance:
                    print(f"[ Agent {self.unique_id} is now infected! ]")
                    self.is_infected = True
                
    def check_for_infection(self):
        pass
