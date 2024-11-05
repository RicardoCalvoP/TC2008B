# model.py
from mesa import Model, agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa import DataCollector
from agent import RandomAgent, ObstacleAgent, DirtAgent


class RandomModel(Model):
    # ... (el código de inicialización existente permanece)

    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = RandomActivation(self)
        self.running = True

        # Inicializar el recolector de datos
        self.datacollector = DataCollector(agent_reporters={
                                           "Steps": lambda a: a.steps_taken if isinstance(a, RandomAgent) else 0})

        # Generador de posiciones aleatorias
        def pos_gen(w, h): return (
            self.random.randrange(w), self.random.randrange(h))

        # Crear agentes ObstacleAgent en posiciones aleatorias
        for i in range(self.num_agents):
            obs = ObstacleAgent(i + 2000, self)
            pos = pos_gen(self.grid.width, self.grid.height)

            while not self.grid.is_cell_empty(pos):
                pos = pos_gen(self.grid.width, self.grid.height)

            self.grid.place_agent(obs, pos)

        # Crear agentes DirtAgemt en posiciones aleatorias
        for i in range(self.num_agents):
            obs = DirtAgent(i + 2000, self)
            pos = pos_gen(self.grid.width, self.grid.height)

            while not self.grid.is_cell_empty(pos):
                pos = pos_gen(self.grid.width, self.grid.height)

            self.grid.place_agent(obs, pos)

        # Crear agentes RandomAgent y colocarlos en celdas aleatorias
        for i in range(self.num_agents):
            a = RandomAgent(i + 1000, self)
            self.schedule.add(a)

            pos = pos_gen(self.grid.width, self.grid.height)
            while not self.grid.is_cell_empty(pos):
                pos = pos_gen(self.grid.width, self.grid.height)

            self.grid.place_agent(a, pos)

        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
