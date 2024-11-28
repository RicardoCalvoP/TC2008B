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

import heapq

import heapq
from mesa import Agent

import heapq
from mesa import Agent

class Car(Agent):
    def __init__(self, unique_id, position, destination, streets, model):
        """
        Initialize the Car agent with position, destination, and streets.
        """
        super().__init__(unique_id, model)
        self.identification = unique_id
        self.lastPosition = position
        self.position = position
        self.destination = destination
        self.streets = streets  # List of (position, direction)
        self.path = []  # Calculated path to the destination

    def findDirections(self, last_position, current_pos, next_pos):
        """
        Validate the movement between positions respecting direction constraints.
        """
        _, last_direction = last_position
        _, direction = current_pos
        _, next_direction = next_pos

        if next_direction == "s":
            next_direction = last_direction

        if direction == "Left" and next_direction == "Right":
            return False
        if direction == "Right" and next_direction == "Left":
            return False
        if direction == "Down" and next_direction == "Up":
            return False
        if direction == "Up" and next_direction == "Down":
            return False
        return True

    def find_path(self):
        """
        Implementa A* para encontrar el camino más corto mientras respeta las reglas de movimiento.
        """
        def heuristic(a, b):
            # Distancia Manhattan
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        open_set = []
        heapq.heappush(open_set, (0, self.position, None))  # (f_score, position, direction)
        came_from = {}  # Diccionario para rastrear el camino
        g_score = {self.position: 0}  # Costo del camino más corto hacia un nodo
        f_score = {self.position: heuristic(self.position, self.destination)}  # Estimación del costo total

        visited = set()

        while open_set:
            _, current, current_dir = heapq.heappop(open_set)

            if current in visited:
                continue
            visited.add(current)

            # Si llegamos al destino, reconstruimos el camino
            if current == self.destination:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                self.path = path
                print(f"Path found: {self.path}")
                return

            # Vecinos válidos basados en las calles
            neighbors = [
                (pos, dir) for (pos, dir) in self.streets
                if self.findDirections((self.lastPosition, None), (current, current_dir), (pos, dir)) and pos not in visited
            ]

            for neighbor, neighbor_dir in neighbors:
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    # Actualizamos `came_from` y los puntajes
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, self.destination)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor, neighbor_dir))

        # Si no se encuentra camino
        self.path = []
        print(f"No path found from {self.position} to {self.destination}.")

    def step(self):
        """
        Execute a single step for the Car agent.
        """
        if not self.path:
            self.find_path()  # Calculate the path if it doesn't exist

        if self.path:
            # Move to the next step in the path
            next_pos = self.path.pop(0)
            self.lastPosition = self.position
            self.position = next_pos
            self.model.grid.move_agent(self, next_pos)

            # Debug: Print the full path and current step
            print(f"Car {self.identification} moved to {next_pos}. Current path: {self.path}")


class Traffic_Light(Agent):

    """
    Traffic lights agents will change conditions within time
    from green to red and from red to green
    """

    def __init__(self, unique_id,  condition, timeToChange, direction, model):
        super().__init__(unique_id, model)
        self.direction = direction
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
