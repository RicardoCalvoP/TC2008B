# server.py
from mesa.visualization.modules import PieChartModule
from model import RandomModel, ObstacleAgent, RoombaAgent, FloorAgent, ChargingStationAgent
from mesa.visualization import CanvasGrid, BarChartModule, PieChartModule
from mesa.visualization import ModularServer
from mesa.visualization import Slider


# The colors of the portrayal will depend on the floor agents's condition.
COLORS = {"Clean": "#ffffff", "Unvisited": "#808080", "Visited": "#F5F5DC", "Dirty": "#4b3621",
          "Free": "#00ffff", "Busy": "#770000"}

IMAGES = {"Clean": "rect", "Unvisited": "rect", "Visited": "rect", "Dirty": "./Resources/Poop_Emoji2.png",
          "Free": "./Resources/realistic_charging_station_free.png", "Busy": "./Resources/realistic_charging_station_busy.png",
          "Cleaning": "./Resources/Roomba.png",  "Charging": "./Resources/realistic_charging_station_busy.png"}


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
        portrayal["text"] = agent.battery, agent.floors_cleaned
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
        portrayal["w"] = 0.9
        portrayal["h"] = 0.9
        portrayal["Layer"] = 2
        portrayal["Color"] = COLORS[agent.condition]

    return portrayal


model_params = {
    "width": 20,
    "height": 20,
    "number_of_roombas": Slider("Number of Roombas", 1, 1, 5, 1),
    "number_of_dirty_floors": Slider("Number of dirty floors", 50, 1, 100, 1),
    "number_of_obstacles": Slider("number of obstacles", 30, 1, 75, 1),
}
grid = CanvasGrid(agent_portrayal, 20, 20, 750, 750)

bar_chart_steps = BarChartModule([{"Label": "Steps", "Color": "#AA0000"}],
                                 scope="agent", sorting="ascending", sort_by="Steps")

bar_chart_cleaned = BarChartModule([{"Label": "Cleaned", "Color": "#00FF00"}],
                                   scope="agent", sorting="ascending", sort_by="Cleaned")


# Configurar el gráfico de pastel
pie_chart_floors = PieChartModule(
    [
        {"Label": "Clean", "Color": COLORS["Clean"]},
        {"Label": "Dirty", "Color": COLORS["Dirty"]},
        {"Label": "Unvisited", "Color": COLORS["Unvisited"]},
        {"Label": "Visited", "Color": COLORS["Visited"]},
    ],
)


server = ModularServer(
    RandomModel, [grid, pie_chart_floors, bar_chart_cleaned, bar_chart_steps], "Random Agents", model_params)
server.port = 8521
server.launch()
