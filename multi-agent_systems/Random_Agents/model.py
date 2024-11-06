# model.py
from mesa import Model, agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa import DataCollector
from agent import RoombaAgent, ObstacleAgent, FloorAgent, ChargingStationAgent


class RandomModel(Model):
    # ... (el código de inicialización existente permanece)

    def __init__(self, width, height, number_of_roombas, number_of_dirty_floors, number_of_obstacles):
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = RandomActivation(self)
        self.running = True

        # Inicializar el recolector de datos
        self.datacollector = DataCollector(
            agent_reporters={
                "Steps": lambda a: a.steps_taken if isinstance(a, RoombaAgent) else 0,
                "Clean": lambda f: f.condition if isinstance(f, FloorAgent) else 0,
                "Dirty": lambda f: f.condition if isinstance(f, FloorAgent) else 0,
            })
        # Crear agentes ObstacleAgent en posiciones aleatorias
        border = [(x, y) for y in range(height) for x in range(
            width) if y in [0, height-1] or x in [0, width - 1]]

        # Genera posiciones sin incluir el borde
        area = [(x, y) for y in range(1, height - 1)
                for x in range(1, width - 1)]

        # Add obstacles to the grid
        for pos in border:
            obs = ObstacleAgent(pos, self)
            self.grid.place_agent(obs, pos)

        # ----------------------------------------------------------
        # Function to generate random positions
        # ----------------------------------------------------------
        def pos_gen(w, h): return (
            self.random.randrange(w), self.random.randrange(h))

        # ----------------------------------------------------------
        # Create Roombas and charging stations in randoms positions
        # ----------------------------------------------------------
        for i in range(number_of_roombas):
            roomba = RoombaAgent(i, self)
            chargingStation = ChargingStationAgent(i+number_of_roombas, self)
            self.schedule.add(roomba)

            pos = pos_gen(self.grid.width, self.grid.height)
            while not self.grid.is_cell_empty(pos):
                pos = pos_gen(self.grid.width, self.grid.height)

            self.grid.place_agent(roomba, pos)
            self.grid.place_agent(chargingStation, pos)

        # ----------------------------------------------------------
        # Create Dirty Floors
        # ----------------------------------------------------------
        for i in range(number_of_dirty_floors):
            floor = FloorAgent(i + 1000, self)
            floor.condition = "Dirty"
            pos = pos_gen(self.grid.width, self.grid.height)

            while not self.grid.is_cell_empty(pos):
                pos = pos_gen(self.grid.width, self.grid.height)

            self.grid.place_agent(floor, pos)

        # ----------------------------------------------------------
        # Create Obstacles
        # ----------------------------------------------------------
        for i in range(number_of_obstacles):
            obs = ObstacleAgent(i + 2000, self)
            pos = pos_gen(self.grid.width, self.grid.height)

            while not self.grid.is_cell_empty(pos):
                pos = pos_gen(self.grid.width, self.grid.height)

            self.grid.place_agent(obs, pos)

        # ----------------------------------------------------------
        # Create rest of the floors
        # ----------------------------------------------------------

        for new_pos in area:
            floor = FloorAgent(new_pos, self)
            if self.grid.is_cell_empty(new_pos):
                self.grid.place_agent(floor, new_pos)

        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
