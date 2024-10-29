import mesa
from mesa import Model, DataCollector
from mesa.space import SingleGrid
from mesa.time import SimultaneousActivation
from random import choice

from agent import TreeCell

class CellularAutomaton(Model):
  def __init__(self, height=50, width=50, density=0.65):
    self.schedule = SimultaneousActivation(self)
    self.grid = SingleGrid(height, width, torus=False)

    self.datacollector = DataCollector(
            {
                "Alive": lambda m: self.count_type(m, "Alive"),
                "Dead": lambda m: self.count_type(m, "Dead"),
            }
        )

    for contents, (x, y) in self.grid.coord_iter():
            if self.random.random() < density:
                # Create a tree
                new_tree = TreeCell((x, y), self)

                # Set all trees in the first line alive or dead in random order .
                if y == 0:
                  new_tree.condition = choice(["Alive", "Dead"])



                self.grid.place_agent(new_tree, (x, y))
                self.schedule.add(new_tree)

    self.running = True
    self.datacollector.collect(self)

    def step(self):
        """
        Have the scheduler advance each cell by one step
        """
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

        # Halt if no more fire
        if self.count_type(self, "On Fire") == 0:
            self.running = False


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