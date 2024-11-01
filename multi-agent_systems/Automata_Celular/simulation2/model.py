import mesa
from mesa import Model, DataCollector
from mesa.space import SingleGrid
from mesa.time import SimultaneousActivation
from random import choice

from agent import TreeCell


class CellularAutomaton(Model):
    def __init__(self, height=50, width=50, density=0.65):
        self.schedule = SimultaneousActivation(self)
        # Acitvamos Torus para que no haya limitaciones en el grid
        self.grid = SingleGrid(width, height, torus=True)

        self.datacollector = DataCollector(
            {
                "Alive": lambda m: self.count_type(m, "Alive"),
                "Dead": lambda m: self.count_type(m, "Dead")
            }
        )

        for contents, (x, y) in self.grid.coord_iter():
            # Crear un agente en cada celda
            new_tree = TreeCell((x, y), self)

            # Asignar estado basado en la densidad
            if self.random.random() < density:
                new_tree.condition = choice(["Alive", "Dead"])
            # Asignar estado aleatorio a los agentes en la primera fila
            else:
                new_tree.condition = "Alive"
            # Colocar el agente en el grid y añadirlo al scheduler
            self.grid.place_agent(new_tree, (x, y))
            self.schedule.add(new_tree)

    def step(self):
        """
        Have the scheduler advance each cell by one step
        """
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

    # staticmethod is a Python decorator that makes a method callable without an instance.
    @staticmethod
    def count_type(model, tree_condition):
        """
        Helper method to count trees in a given condition in a given model.
        """
        count = 0
        for tree in model.schedule.agents:
            if tree.condition == tree_condition:
                count += 1
        return count
