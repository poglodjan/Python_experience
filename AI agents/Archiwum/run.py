"""
run.py - basic simulation that can be used for testing the model
"""
from model import InfectiousDiseaseSpreadModel
from agents import PersonAgent

# Model Initialization
model = InfectiousDiseaseSpreadModel(
    total_population_size=20,
    infected_population_size=3,
    comorbidity_population_size=5,
    moving_probability=0.8
)

# Testing the simulation for 10steps
step_count = 0
while model.running and step_count < 10:
    model.step()
    step_count += 1

    if step_count==1:
        print("Model intialization:\n")
    infected_count = sum(1 for a in model._my_agents.values() if a.is_infected)
    print(f"Step {step_count}: {infected_count} infected agents\n")

print("Simulation finished.")

# Method to print the grid after all steps
print("\nFinal grid state:")
for y in reversed(range(model.grid.height)):  
    row = ""
    for x in range(model.grid.width):
        cell_agents = model.grid.get_cell_list_contents([(x, y)])
        if not cell_agents:
            row += ". "  
        else:
            infected = any(agent.is_infected for agent in cell_agents)
            row += "X " if infected else "O "  # X = infected, O = healthy
    print(row)
