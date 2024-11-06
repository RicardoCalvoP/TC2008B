from mesa import Agent


class RoombaAgent(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID
        direction: Randomly chosen direction chosen from one of eight directions
    """

    def __init__(self, unique_id, model):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        # Condition Cleaning | Charging
        self.condition = "Cleaning"
        self.direction = 4
        self.steps_taken = 0

    def move(self):
        # Obtener las posiciones vecinas
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,     # Incluir las diagonales
            include_center=False  # Excluir la posición actual
        )

        # Diccionario para almacenar las posiciones y tipos de agentes descubiertos
        neighbor_info = {}

        # Explorar vecinos y clasificar agentes en las posiciones vecinas
        for pos in possible_steps:
            agents = self.model.grid.get_cell_list_contents(pos)
            for agent in agents:
                agent_type = type(agent)
                # Guarda la posición y tipo de agente si es FloorAgent o cualquier otro agente relevante
                if agent_type not in neighbor_info:
                    neighbor_info[agent_type] = []
                neighbor_info[agent_type].append(pos)

        # Ejemplo de movimiento: moverse a una posición con FloorAgent si está disponible
        if FloorAgent in neighbor_info:
            next_move = self.random.choice(neighbor_info[FloorAgent])
        else:
            # Si no hay FloorAgent en los vecinos, elegir una dirección aleatoria
            next_move = self.random.choice(possible_steps)

        # Realizar el movimiento con probabilidad del 10%
        self.model.grid.move_agent(self, next_move)
        self.steps_taken += 1


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
        self.condition = "Clean"
        self._next_condition = None

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
