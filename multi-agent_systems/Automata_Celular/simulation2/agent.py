from mesa import Agent


class TreeCell(Agent):
    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Dead"
        self._next_condition = None

    def step(self):
        """
        Determine the agent's condition based on the condition of the top-left, top,
        and top-right neighbors using torus=True (wrap-around grid).
        """
        x, y = self.pos
        grid_width = self.model.grid.width
        grid_height = self.model.grid.height

        """ Calcular las posiciones de los vecinos usando aritmética modular
            para poder conocer las casillas de los lados espejos y que de esta
            manera el Torus funcione como se espera
        """
        top_left_neighbor_pos = ((x - 1) % grid_width, (y + 1) % grid_height)
        top_neighbor_pos = (x % grid_width, (y + 1) % grid_height)
        top_right_neighbor_pos = ((x + 1) % grid_width, (y + 1) % grid_height)

        # Obtener el contenido de las celdas de los vecinos
        top_left = self.model.grid.get_cell_list_contents(
            [top_left_neighbor_pos])
        top = self.model.grid.get_cell_list_contents([top_neighbor_pos])
        top_right = self.model.grid.get_cell_list_contents(
            [top_right_neighbor_pos])

        # Obtener el estado de cada vecino, asumiendo que siempre hay un agente
        top_left_condition = top_left[0].condition if top_left else "Dead"
        top_condition = top[0].condition if top else "Dead"
        top_right_condition = top_right[0].condition if top_right else "Dead"

        # Aplicar las reglas según las condiciones de los tres vecinos
        if top_left_condition == "Alive" and top_condition == "Alive" and top_right_condition == "Alive":
            self._next_condition = "Dead"  # 111 -> 0
        elif top_left_condition == "Alive" and top_condition == "Alive" and top_right_condition == "Dead":
            self._next_condition = "Alive"  # 110 -> 1
        elif top_left_condition == "Alive" and top_condition == "Dead" and top_right_condition == "Alive":
            self._next_condition = "Dead"  # 101 -> 0
        elif top_left_condition == "Alive" and top_condition == "Dead" and top_right_condition == "Dead":
            self._next_condition = "Alive"  # 100 -> 1
        elif top_left_condition == "Dead" and top_condition == "Alive" and top_right_condition == "Alive":
            self._next_condition = "Alive"  # 011 -> 1
        elif top_left_condition == "Dead" and top_condition == "Alive" and top_right_condition == "Dead":
            self._next_condition = "Dead"  # 010 -> 0
        elif top_left_condition == "Dead" and top_condition == "Dead" and top_right_condition == "Alive":
            self._next_condition = "Alive"  # 001 -> 1
        elif top_left_condition == "Dead" and top_condition == "Dead" and top_right_condition == "Dead":
            self._next_condition = "Dead"  # 000 -> 0

    def advance(self):
        """
        Advance the model by one step.
        """
        if self._next_condition is not None:
            self.condition = self._next_condition
