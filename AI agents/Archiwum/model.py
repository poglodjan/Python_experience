import logging
import random
from mesa import Model
from mesa.space import MultiGrid
from agents import PersonAgent
from mesa.datacollection import DataCollector

logger = logging.getLogger(__name__)

class InfectiousDiseaseSpreadModel(Model):
    """ 
    Model simulating spreading of the virus X simulation
    """
    def __init__(self, total_population_size, infected_population_size, comorbidity_population_size, moving_probability):
        super().__init__()
        self.num_agents = total_population_size
        self.grid = MultiGrid(width=10, height=10, torus=False)
        self._my_agents = {}  # my agents dictionary
        self.running = True # for the stop conditions

        # Initializing dictiories for the infection mechanism
        self.infection_layer = {}
        self.infected_locations = {}  

        # configuring the index of agents
        all_ids = list(range(total_population_size))
        infected_ids = random.sample(all_ids, infected_population_size)
        remaining_ids = [i for i in all_ids if i not in infected_ids]
        comorbidity_ids = random.sample(remaining_ids, comorbidity_population_size)

        # infection iterators for visualization and data collector
        self.direct_infections = 0
        self.location_infections = 0
        self.datacollector = DataCollector(
            model_reporters={
                "Direct Infection": lambda m: m.direct_infections,
                "Location Infection": lambda m: m.location_infections
            }
        )
        
        # creating agents based on the parameters
        for i in range(total_population_size):
            is_infected = i in infected_ids
            has_comorbidities = i in comorbidity_ids

            agent = PersonAgent(
                model=self,
                unique_id=i,
                is_infected=is_infected,
                has_comorbidities=has_comorbidities,
                moving_probability=moving_probability
            )
            self._my_agents[i] = agent  # adding created agent to the dictionary
            
            # agent position set to the random position in grid
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))

            # Setting all infection layers to False
            for x in range(self.grid.width): 
                for y in range(self.grid.height):
                    self.infection_layer[(x, y)] = False
        
        self.datacollector.collect(self)

    def infect_locations_around(self, pos):
        """
        Infects current location and neighborhood for 2 steps
        """
        self.infected_locations[pos] = 2 #2steps

        neighbors = self.grid.get_neighborhood(pos, moore=False, include_center=False)
        for n_pos in neighbors:
            self.infected_locations[n_pos] = 2

    def _stop_condition(step) -> None:
        '''
        Decorator: Checks if all agents are infected.
        '''
        def perform_step(self):
            # Checking if all agents (in the _my_agents directory) are infected
            infected = [agent for agent in self._my_agents.values() if agent.is_infected]
            if len(infected) == len(self._my_agents):  # If all infected then stop running
                self.running = False
                logger.info("All agents are infected. Stopping the simulation.")
            else:
                step(self)
        
        return perform_step

    @_stop_condition
    def step(self):
        """
        Advance the simulation by one step. Each agent may move or be infected.
        """
        to_remove_infected_steps = []
        for loc in self.infected_locations:
            self.infected_locations[loc] -= 1
            if self.infected_locations[loc] <= 0:
                to_remove_infected_steps.append(loc)
        
        for loc in to_remove_infected_steps:
            del self.infected_locations[loc]

        for agent in self._my_agents.values(): 
            agent.move()
            agent.step()

        self.datacollector.collect(self)
        
        # Infection layer actualization
        for (x,y) in self.infection_layer:
            agents = self.grid.get_cell_list_contents([(x,y)])
            self.infection_layer[(x,y)] = any(agent.is_infected for agent in agents)
