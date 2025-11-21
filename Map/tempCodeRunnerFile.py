    def generate_maze(self, grid_width, grid_height):
        """
        Generate a maze layout using recursive backtracking
        Args:
            grid_width (int): Width of the maze grid
            grid_height (int): Height of the maze grid
        Returns:
            list: 2D list representing the maze layout
                0: path
                1: wall
        """

        visited = [[False]*grid_width for _ in range(grid_height)]
        maze = [[1]*grid_width for _ in range(grid_height)]  # 1 = wall, 0 = path

        def carve(x, y):
            """
            Carve paths in the maze using recursive backtracking
            Args:
                x (int): Current x position
                y (int): Current y position
            """

            visited[y][x] = True
            maze[y][x] = 0

            directions = [(1,0), (-1,0), (0,1), (0,-1)]
            random.shuffle(directions)

            for dx, dy in directions:
                nx, ny = x + dx*2, y + dy*2
                if 0 <= nx < grid_width and 0 <= ny < grid_height and not visited[ny][nx]:
                    maze[y + dy][x + dx] = 0
                    carve(nx, ny)

        carve(1, 1)

        return maze