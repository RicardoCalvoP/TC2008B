from mesa import Agent


class TreeCell(Agent):
    """
    A tree cell.

    Attributes:
        x, y: Grid coordinates
        condition: Can be "Alive" or "Dead"
        unique_id: (x,y) tuple.

        unique_id isn't strictly necessary here, but it's good practice to give one to each agent anyway.
    """

    def __init__(self, pos, model):
        """
        Create a new agent.

        Args:
            pos: The agent's coordinates on the grid.
            model: standard model reference for agent.
        """
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Dead"  # Default starting state
        self._next_condition = None

    def step(self):
        """
        Determine the agent's condition based on the condition of the neighbor above.
        If the neighbor above is "Dead", set the agent's condition to "Dead".
        Otherwise, set it to "Alive".
        """
        # Obtener la posición del vecino de arriba
        x, y = self.pos
        grid_height = self.model.grid.height

        if (y != grid_height-1):
            # Vecino de arriba en la posición (x-1, y+1)
            top_left_neighbor_pos = (x - 1, y + 1)
            # Vecino de arriba en la posición (x, y+1)
            top_neighbor_pos = (x, y + 1)
            # Vecino de arriba en la posición (x, y+1)
            top_right_neighbor_pos = (x + 1, y + 1)

            # Verificar si el vecino está dentro de los límites del grid
            grid_width = self.model.grid.width

            def get_neighbor_condition(pos):
                if 0 <= pos[0] < grid_width and 0 <= pos[1] < grid_height:
                    neighbor = self.model.grid.get_cell_list_contents([pos])
                    if neighbor:
                        return neighbor[0].condition
                    else:
                        return "Dead"
                else:
                    return "Dead"

            top_left_condition = get_neighbor_condition(top_left_neighbor_pos)
            top_condition = get_neighbor_condition(top_neighbor_pos)
            top_right_condition = get_neighbor_condition(
                top_right_neighbor_pos)

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
