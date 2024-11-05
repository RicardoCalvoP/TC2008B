# server.py
from model import RandomModel, ObstacleAgent, RandomAgent, DirtAgent
from mesa.visualization import CanvasGrid, BarChartModule
from mesa.visualization import ModularServer


def agent_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    # Representación del agente Roomba
    if isinstance(agent, RandomAgent):
        portrayal["Shape"] = "circle"
        portrayal["Filled"] = "true"
        portrayal["Color"] = "red"
        portrayal["r"] = "0.5"
        portrayal["Layer"] = 3
        portrayal["text"] = f"Steps: {agent.steps_taken}"
        portrayal["text_color"] = "Black"

    # Representación del agente ObstacleAgent
    elif isinstance(agent, ObstacleAgent):
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["Layer"] = 1
        portrayal["Color"] = ["#000000"]

    # Representación del agente basura
    elif isinstance(agent, DirtAgent):
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["w"] = 0.75
        portrayal["h"] = 0.75
        portrayal["Layer"] = 2
        portrayal["Color"] = ["#3d251e"]

    return portrayal


model_params = {"N": 5, "width": 10, "height": 10}
grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

bar_chart = BarChartModule([{"Label": "Steps", "Color": "#AA0000"}],
                           scope="agent", sorting="ascending", sort_by="Steps")

server = ModularServer(
    RandomModel, [grid, bar_chart], "Random Agents", model_params)
server.port = 8521
server.launch()
