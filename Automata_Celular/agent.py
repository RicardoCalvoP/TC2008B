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
        self.condition = "Alive"  # Default starting state
        self._next_condition = None

    def get_neighbor_states(self, offsets):
        """
        Given a list of offsets, return the states of neighbors at those relative positions.

        Args:
            offsets (list of tuples): List of (dx, dy) tuples indicating the relative positions to check.

        Returns:
            list: A list of "Alive" or "Dead" states of the neighbors in the specified positions.
        """
        x, y = self.pos
        neighbor_states = []
        grid_width = 50  # Assuming grid is 50x50
        grid_height = 50

        for dx, dy in offsets:
            neighbor_x = x + dx
            neighbor_y = y + dy

            # Check if the neighbor position is within grid bounds
            if 0 <= neighbor_x < grid_width and 0 <= neighbor_y < grid_height:
                # Get the neighbor at this position
                neighbor = self.model.grid.get_cell_list_contents([(neighbor_x, neighbor_y)])
                if neighbor:
                    neighbor_states.append(neighbor[0].condition)
                else:
                    neighbor_states.append("Dead")
            else:
                # If the neighbor is out of bounds, assume it's "Dead"
                neighbor_states.append("Dead")

        return neighbor_states

    def step(self):
        # Example of using get_neighbor_states to get specific neighbors
        offsets = [(-1, +1), (0, +1), (1, +1)]  # Arriba a la izquierda, arriba, arriba a la derecha
        neighbor_states = self.get_neighbor_states(offsets)
        print("Pos: ", self.pos, "State: ",neighbor_states)
        # Define a binary string based on neighbor states ("1" for Alive, "0" for Dead)
        neighbor_pattern = "".join(["1" if state == "Alive" else "0" for state in neighbor_states])

        # Define the rule pattern
        pattern_rules = {
            "111": "Dead",
            "110": "Alive",
            "101": "Dead",
            "100": "Alive",
            "011": "Alive",
            "010": "Dead",
            "001": "Alive",
            "000": "Dead"
        }

        # Determine the next condition based on the pattern
        self._next_condition = pattern_rules.get(neighbor_pattern)

    def advance(self):
        """
        Advance the model by one step.
        """
        if self._next_condition is not None:
            self.condition = self._next_condition
