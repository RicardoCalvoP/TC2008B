from mesa import Agent
import math


class RoombaAgent(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID
        direction: Randomly chosen direction chosen from one of eight directions
    """

    def __init__(self, unique_id, model, charging_station):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        # Condition Cleaning | Charging
        self.agent_type = "Roomba"  # Identificador del tipo de agente
        self.steps_taken = 0
        self.floors_cleaned = 0
        self.condition = "Cleaning"
        self.direction = 4
        self.battery = 100
        self.charging_station = charging_station
        self.visited_cells = set([self.charging_station])
        self.path_to_station = []  # Lista para registrar el camino de regreso

    def step(self):
        """
        hierarchy

        - Return home if battery low
        - Clean
        - Move
        """

        if self.pos == self.charging_station and self.steps_taken > 0:
            # Recargar batería hasta el máximo
            self.condition = "Charging"
            print("El Roomba está cargando...", self.battery, "%")
            self.battery = min(self.battery + 5, 100)
            if (self.battery == 100):
                self.condition = "Cleaning"
                self.clean()
        else:
            min_dist = self.get_distance(self.pos, self.charging_station)
            if (self.battery <= min_dist+2):
                self.return_to_station()
            elif (self.condition == "Cleaning"):
                self.clean()

    def get_distance(self, pos_1, pos_2):
        x1, y1 = pos_1
        x2, y2 = pos_2

        return abs(x1 - x2) + abs(y1 - y2)

    def update_path_to_station(self):
        """
        Recalcula el camino más eficiente desde la posición actual hasta la estación de carga,
        considerando únicamente las celdas marcadas como "Clean" y la estación de carga.
        """
        from collections import deque

        queue = deque([[self.pos]])
        visited = set()
        visited.add(self.pos)

        while queue:
            path = queue.popleft()
            current_pos = path[-1]

            # Si llegamos a la estación, guardar el camino
            if current_pos == self.charging_station:
                self.path_to_station = path  # Actualizar el camino
                return

            # Explorar vecinos accesibles que estén en "Clean" o sean la estación de carga
            neighbors = self.model.grid.get_neighborhood(
                current_pos, moore=True, include_center=False
            )

            for neighbor in neighbors:
                if neighbor not in visited:
                    agents_in_cell = self.model.grid.get_cell_list_contents(
                        neighbor)

                    # Verificar si el vecino es una celda "Clean" o la estación de carga
                    if any(isinstance(agent, FloorAgent) and agent.condition == "Clean" for agent in agents_in_cell) or \
                            any(isinstance(agent, ChargingStationAgent) for agent in agents_in_cell):
                        visited.add(neighbor)
                        queue.append(path + [neighbor])

    def return_to_station(self):

        # Sigue el camino en path_to_station para regresar a la estación de carga.

        # Tomar el siguiente paso en el camino
        next_move = self.path_to_station.pop(0)
        self.model.grid.move_agent(self, next_move)
        self.steps_taken += 1
        self.battery -= 1

        # Verificar si llegamos a la estación
        if next_move == self.charging_station:
            print("Roomba ha llegado a la estación de carga.")

    def clean(self):
        # Registrar la celda actual como visitada y marcarla como "Clean"
        self.visited_cells.add(self.pos)

        # Obtener las posiciones vecinas
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,  # Incluir diagonales
            include_center=False  # Excluir la posición actual
        )

        # Filtrar vecinos para clasificar las celdas en prioridades
        accessible_steps = []
        dirty_steps = []
        visited_steps = []
        to_visit_steps = []

        for pos in possible_steps:
            # Obtener agentes en la celda
            agents_in_cell = self.model.grid.get_cell_list_contents(pos)

            # Ignorar celdas con obstáculos
            if any(isinstance(agent, ObstacleAgent) for agent in agents_in_cell):
                continue

            for agent in agents_in_cell:
                if isinstance(agent, FloorAgent):
                    # Si la celda está sucia
                    if agent.condition == "Dirty":
                        dirty_steps.append(pos)
                    # Si ya hemos estado directamente en la celda
                    elif agent.condition == "Clean":
                        visited_steps.append(pos)
                    # Si conocemos la celda pero no hemos estado en ella
                    elif agent.condition == "Visited":
                        to_visit_steps.append(pos)
                    else:
                        # Si no tiene un estado previo, marcar como "Visited"
                        agent.condition = "Visited"
                        to_visit_steps.append(pos)

                    # Agregar a la lista general de accesibles
                    accessible_steps.append(pos)

        # Priorización de movimiento: Dirty > To Visit > Visited
        if dirty_steps:
            next_move = self.random.choice(dirty_steps)
        elif to_visit_steps:
            next_move = self.random.choice(to_visit_steps)
        elif visited_steps:
            next_move = self.random.choice(visited_steps)
        else:
            # Este caso no debería suceder porque siempre hay posibles pasos accesibles
            print("No hay movimientos disponibles.")
            return

        # Obtener agentes en la celda seleccionada
        current_cell = self.model.grid.get_cell_list_contents(next_move)

        # Cambiar condición de las celdas seleccionadas
        for agent in current_cell:
            if isinstance(agent, FloorAgent):
                # Restar batería si la celda estaba sucia
                if agent.condition == "Dirty":
                    self.battery -= 1
                    self.floors_cleaned += 1
                # Marcar como "Clean" si llegamos directamente a ella
                agent.condition = "Clean"

        # Realizar el movimiento
        self.model.grid.move_agent(self, next_move)
        self.update_path_to_station()
        self.steps_taken += 1
        self.battery -= 1


class ObstacleAgent(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass


class FloorAgent(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        # Condition Clean | Dirty
        self.agent_type = "Floor"  # Identificador del tipo de agente
        self.condition = "Unvisited"

    def step(self):
        pass


class ChargingStationAgent(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        # Condition Free | Busy
        self.condition = "Free"
        self._next_condition = None

    def step(self):
        pass
