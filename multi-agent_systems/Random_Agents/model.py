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
                "Cleaned": lambda a: a.floors_cleaned if isinstance(a, RoombaAgent) else 0,
            },
            model_reporters={
                "Clean": lambda m: m.count_type(m, "Clean"),
                "Dirty": lambda m: m.count_type(m, "Dirty"),
                "Unvisited": lambda m: m.count_type(m, "Unvisited"),
                "Visited": lambda m: m.count_type(m, "Visited"),
            },
        )
        # Crear agentes ObstacleAgent en posiciones aleatorias
        border = [(x, y) for y in range(height) for x in range(
            width) if y in [0, height-1] or x in [0, width - 1]]

        # Genera posiciones sin incluir el borde
        area = [(x, y) for y in range(1, height - 1)
                for x in range(1, width - 1)]

        # Add obstacles to the grid
        for pos in border:
            id_obstacle = 5000
            obs = ObstacleAgent(id_obstacle, self)
            self.grid.place_agent(obs, pos)
            id_obstacle += 1
        # ----------------------------------------------------------
        # Function to generate random positions
        # ----------------------------------------------------------
        def pos_gen(w, h): return (
            self.random.randrange(w), self.random.randrange(h))

        # ----------------------------------------------------------
        # Create Roombas and charging stations in randoms positions
        # ----------------------------------------------------------
        for i in range(number_of_roombas):

            # Position if number of roombas is 1
            pos = (1, 1)

            # Generate positions if there is more than 1 roomba
            if (number_of_roombas != 1):
                pos = pos_gen(self.grid.width, self.grid.height)
                while not self.grid.is_cell_empty(pos):
                    pos = pos_gen(self.grid.width, self.grid.height)

            roomba = RoombaAgent(i, self, pos)
            chargingStation = ChargingStationAgent(i+number_of_roombas, self)
            self.schedule.add(roomba)
            self.grid.place_agent(roomba, pos)
            self.grid.place_agent(chargingStation, pos)

        # ----------------------------------------------------------
        # Create Dirty Floors
        # ----------------------------------------------------------
        for i in range(number_of_dirty_floors):
            floor = FloorAgent(i + 1000, self)
            floor.condition = "Dirty"
            floor.num_dirty_floors = 1
            pos = pos_gen(self.grid.width, self.grid.height)

            while not self.grid.is_cell_empty(pos):
                pos = pos_gen(self.grid.width, self.grid.height)

            self.grid.place_agent(floor, pos)
        #   self.schedule.add(floor)

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
            floor_id = 3000
            floor = FloorAgent(floor_id, self)
            if self.grid.is_cell_empty(new_pos):
                self.grid.place_agent(floor, new_pos)
                # self.schedule.add(floor)

            floor_id += 1
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        # Contar pisos sucios directamente del grid
        dirty_floors = 0

        for contents, (x, y) in self.grid.coord_iter():
            for agent in contents:
                if isinstance(agent, FloorAgent) and agent.condition == "Dirty":
                    dirty_floors +=1

        # Detener la simulación si no hay pisos sucios o si se llega al paso 600
        if self.schedule.steps >= 600-1 or dirty_floors == 0:
            print("Simulación detenida: Todos los pisos están limpios o se alcanzó el límite de pasos.")
            self.running = False

    @staticmethod
    def count_type(model, floor_condition):
        # Helper method to count number of floors depending in a given condition in a given model.

        count = 0
        for contents, (x, y) in model.grid.coord_iter():
            for agent in contents:
                if isinstance(agent, FloorAgent) and agent.condition == floor_condition:
                    count +=1
        return count