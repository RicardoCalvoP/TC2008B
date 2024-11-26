"""
Ricardo Alfredo Calvo Perez y  Andrés Eduardo Gomes Brandt
18/11/2024

In this file we will find the base model of our simulation
"""

from mesa import Model, agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agents import Car, Obstacle, Traffic_Light, Road, Destination
import numpy as np
import random
import json


class City(Model):
    """
    Creates a model with the agents
    [More description]
    """

    def __init__(self, width, height):
        super().__init__(seed=42)  # Ask what seed=42 means
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = RandomActivation(self)
        self.running = True

        self.width = width
        self.height = height
        self.traffic_lights = []
        self.destinations = []
        self.carSpawns = [(0, 0), (width - 1, 0),
                          (0, height-1), (width-1, height-1)]
        self.streets = []
        self.num_cars = 0
        self.num_steps = 0
        try:

            # Load the map dictionary. The dictionary maps the characters in the map file to the corresponding agent.
            dataDictionary = json.load(open("city_files/mapDictionary.json"))

            # Load the map file. The map file is a text file where each character represents an agent.
            with open('city_files/2022_base.txt') as baseFile:
                lines = baseFile.readlines()

                # Goes through each character in the map file and creates the corresponding agent.
                for r, row in enumerate(lines):
                    for c, col in enumerate(row):
                        # Roads
                        if col in ["v", "^", ">", "<"]:
                            agent = Road(
                                f"r{r*self.width+c}", dataDictionary[col], self)
                            pos = (c, self.height - r - 1)
                            self.grid.place_agent(
                                agent, pos)
                            self.streets.append((pos, agent.direction))
                        # Traffic Ligths

                        elif col in ["S", "s"]:
                            agent = Traffic_Light(
                                f"tl{r*self.width+c}", False if col == "S" else True, int(dataDictionary[col]), self)
                            pos = (c, self.height - r - 1)
                            self.grid.place_agent(
                                agent, pos)
                            self.schedule.add(agent)
                            self.traffic_lights.append(agent)
                        # Buildings
                        elif col == "#":
                            agent = Obstacle(f"ob{r*self.width+c}", self)
                            pos = (c, self.height - r - 1)
                            self.grid.place_agent(
                                agent, pos)
                        # Destinations
                        elif col == "D":
                            agent = Destination(f"d{r*self.width+c}", self)
                            pos = (c, self.height - r - 1)
                            self.grid.place_agent(
                                agent, pos)
                            self.destinations.append(pos)
            for i in range(4):
                destination = random.choice(self.destinations)
                pos = self.carSpawns[i]
                agent = Car(f"ca{self.num_cars+1000+i}", pos,
                            destination, self.streets, self)
                self.grid.place_agent(
                    agent, pos)
                self.schedule.add(agent)
                self.num_cars += 1

        except FileNotFoundError:
            print(f"Error: No se encontró el archivo. en model")
        except Exception as e:
            print(f"Error inesperado: {e}")

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        self.num_steps += 1

        if self.num_steps % 10 == 0:
            for i in range(4):
                destination = random.choice(self.destinations)
                pos = self.carSpawns[i]
                agent = Car(f"ca{self.num_cars+1000+i}", pos,
                            destination, self.streets, self)
                self.grid.place_agent(
                    agent, pos)
                self.schedule.add(agent)
                self.num_cars += 1
