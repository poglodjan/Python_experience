from mesa.experimental import JupyterViz, SimpleCanvas
from model import InfectiousDiseaseSpreadModel

# ======== Agent Portrayal Function ========
def agent_portrayal(agent):
    if agent.is_infected:
        return {"shape": "circle", "color": "red", "size": 0.8}
    elif agent.has_comorbidities:
        return {"shape": "circle", "color": "orange", "size": 0.6}
    else:
        return {"shape": "circle", "color": "green", "size": 0.5}

# ======== Cell Portrayal Function ========
def cell_portrayal(model, x, y):
    pos = (x, y)
    if pos in model.infected_locations:
        return "lightcoral"  # highlited fo rinfected cells
    return "white"   # else normal

# ======== Grid Component ========
grid = SimpleCanvas(agent_portrayal, cell_portrayal, 10, 10, 500, 500)

# ======== Visualization App ========
viz = JupyterViz(
    InfectiousDiseaseSpreadModel,
    model_params={
        "total_population_size": 20,
        "infected_population_size": 3,
        "comorbidity_population_size": 5,
        "moving_probability": 0.8,
    },
    name="Infectious Disease Simulation",
    canvas=grid,
)

# Add a line chart with data from the DataCollector
viz.line_chart(
    ["Direct Infection", "Location Infection"],
    title="Infections Over Time",
    colors=["red", "blue"]
)

viz.launch()
