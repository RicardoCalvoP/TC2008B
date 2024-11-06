# server.py
from model import RandomModel, ObstacleAgent, RoombaAgent, FloorAgent, ChargingStationAgent
from mesa.visualization import CanvasGrid, BarChartModule
from mesa.visualization import ModularServer
from mesa.visualization import Slider


# The colors of the portrayal will depend on the floor agents's condition.
COLORS = {"Clean": "#ffffff", "Dirty": "#3d221e",
          "Free": "#00ffff", "Busy": "#770000"}

IMAGES = {"Clean": "rect", "Dirty": "./Resources/Poop_Emoji.png",
          "Free": "./Resources/realistic_charging_station_free.png", "Busy": "./Resources/realistic_charging_station_busy.png",
          "Cleaning": "./Resources/Roomba.png", "Charging": "./Resources/realistic_charging_station_busy.png"}


def agent_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    # Representación del agente Roomba
    if isinstance(agent, RoombaAgent):
        portrayal["Shape"] = IMAGES[agent.condition]
        portrayal["Filled"] = "true"
        portrayal["Color"] = "red"
        portrayal["r"] = "1"
        portrayal["Layer"] = 3
        portrayal["text"] = agent.battery
        portrayal["text_color"] = "White"



    # Representación del agente ChargingStationAgent
    elif isinstance(agent, ChargingStationAgent):
        portrayal["Shape"] = IMAGES[agent.condition]
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 1
        portrayal["Color"] = COLORS[agent.condition]

    # Representación del agente ObstacleAgent
    elif isinstance(agent, ObstacleAgent):
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["Layer"] = 1
        portrayal["Color"] = ["#000000"]

    # Representación del agente basura
    elif isinstance(agent, FloorAgent):
        portrayal["Shape"] = IMAGES[agent.condition]
        portrayal["Filled"] = "true"
        portrayal["w"] = 0.5
        portrayal["h"] = 0.5
        portrayal["Layer"] = 2
        portrayal["Color"] = COLORS[agent.condition]

    return portrayal


model_params = {
    "width": 25,
    "height": 25,
    "number_of_roombas": Slider("Number of Roombas", 1, 1, 10, 1),
    "number_of_dirty_floors": Slider("Number of dirty floors", 10, 1, 50, 1),
    "number_of_obstacles": Slider("number of obstacles", 10, 1, 50, 1),
}
grid = CanvasGrid(agent_portrayal, 25, 25, 500, 500)

bar_chart = BarChartModule([{"Label": "Steps", "Color": "#AA0000"}],
                           scope="agent", sorting="ascending", sort_by="Steps")

server = ModularServer(
    RandomModel, [grid, bar_chart], "Random Agents", model_params)
server.port = 8521
server.launch()
