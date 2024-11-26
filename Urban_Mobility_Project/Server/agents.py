"""
Ricardo Alfredo Calvo Perez - A01028889
Andrés Eduardo Gomes Brandt - A01781321
18/11/2024

In this file we are going to find our agents used in our simulation
Used Agents:
  * Cars
  * Traffic light
  * Road
  * Building
"""

from mesa import Agent
import math

import heapq
from collections import deque


class Car(Agent):
    """
    Car Agent moves depending on the state on the road
    following the correct path to get to the destination.

    Attributes:
        - unique_id: Unique identifier for the agent.
        - position: Current position of the car.
        - destination: Target position.
        - streets: List of tuples representing the street connections.
        - model: Reference to the simulation model.
    """

    def __init__(self, unique_id, position, destination, streets, model):
        super().__init__(unique_id, model)
        self.steps_taken = 0
        self.destination = destination
        self.path = []
        self.pos = position
        self.destination = destination
        self.streets = streets

    def Move(self):
        """
        Moves the car along the precomputed path.
        """
        if self.steps_taken + 1 < len(self.path):  # Validate there are more steps
            next_pos = self.path[self.steps_taken + 1]
            agents_in_cell = self.model.grid.get_cell_list_contents(next_pos)
            if all(not isinstance(agent, Car) for agent in agents_in_cell):  # Check if the cell is free
                self.model.grid.move_agent(self, next_pos)
                self.steps_taken += 1

    def get_neighbors_from_list(self, streets, current_node):
        """
        Finds all neighbors of a node in the streets list.
        Args:
            streets (list): List of street connections.
            current_node (tuple): Current position (x, y).
        Returns:
            list: List of tuples (neighbor_node, weight).
        """
        directions = {
            "Down": (0, -1),
            "Up": (0, 1),
            "Left": (-1, 0),
            "Right": (1, 0),
        }

        neighbors = []
        for node, direction in streets:
            if node == current_node:
                dx, dy = directions[direction]
                neighbor = (node[0] + dx, node[1] + dy)
                neighbors.append((neighbor, 1))  # Weight is 1 by default
        return neighbors

    def get_path(self, streets, start, destination):
        """
        BFS para encontrar el camino más corto desde 'start' hasta 'destination'.
        Args:
            streets (list): Lista de conexiones de calles.
            start (tuple): Nodo inicial (posición x, y).
            destination (tuple): Nodo destino (posición x, y).
        Returns:
            list: Camino más corto desde 'start' hasta 'destination'.
        """
        queue = deque([[start]])  # Cada elemento de la cola es un camino
        visited = set()  # Nodos visitados
        visited.add(start)

        while queue:
            path = queue.popleft()
            current_pos = path[-1]

            # Si alcanzamos el destino, devolvemos el camino
            if current_pos == destination:
                return path

            # Obtener vecinos del nodo actual
            neighbors = self.get_neighbors_from_list(streets, current_pos)
            for neighbor, _ in neighbors:  # Ignoramos el peso en BFS
                if neighbor not in visited:
                    visited.add(neighbor)
                    # Agregamos el nuevo camino
                    queue.append(path + [neighbor])

        # Si no hay un camino disponible
        print("No path found")
        return []

    def step(self):
        """
        Perform a single step in the simulation.
        """

        print("position: ", self.pos, "destination:", self.destination)
        if self.pos == self.destination:
            # Remove agent upon reaching destination
            self.model.grid.remove_agent(self)

        if not self.path and self.pos != self.destination:
            self.path = self.get_path(self.streets, self.pos, self.destination)

        print(self.path)
        if self.pos != self.destination:
            self.Move()


class Traffic_Light(Agent):

    """
    Traffic lights agents will change conditions within time
    from green to red and from red to green
    """

    def __init__(self, unique_id,  condition, timeToChange, model):
        super().__init__(unique_id, model)

        self.condition = condition
        self.timeToChange = timeToChange

    def step(self,):
        """
        To change the state (green or red) of the traffic light in case you consider the time to change of each traffic light.
        """
        if self.model.schedule.steps % self.timeToChange == 0:
            self.condition = not self.condition


class Road(Agent):
    """
    Road agent. Determines where the cars can move, and in which direction.
    """

    def __init__(self, unique_id, direction, model):
        """
        Creates a new road.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            direction: Direction where the cars can move
        """
        super().__init__(unique_id, model)
        self.direction = direction

    def step(self):
        pass


class Obstacle(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass


class Destination(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass
