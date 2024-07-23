from turtle import Screen, Turtle
from collections import deque
import time 

class FileHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        with open(self.file_path, 'r') as file:
            return file.read()

class drawMap:
    def __init__(self, maze):
        self.maze = maze
        self.screen = Screen()
        self.screen.title("Maze")
        self.screen.setup(width=1000, height=800)  # Adjusted for larger squares
        self.turtle = Turtle()
        self.turtle.speed("fastest")
        self.turtle.hideturtle()
        self.turtle.penup()
        self.start_position = None  # Initialize start position attribute
        self.setup_map()

    def setup_map(self):
        self.find_start_position()  # Find and set start position
        self.draw()

        # Initialize drone movement after drawing the maze
        self.drone = drone_movement(self.screen, self.maze, self.start_position, self)
        self.drone.setup_drone_movement()

    def find_start_position(self):
        for y in range(len(self.maze)):
            for x in range(len(self.maze[y])):
                if self.maze[y][x] == 's':
                    self.start_position = (x, y)
                    return
        print("Start position 's' not found in the maze!")    

    def draw(self):
        self.screen.tracer(0)
        square_size = 40  # Increase square size to enlarge the map
        
        for y in range(len(self.maze)):
            for x in range(len(self.maze[y])):
                char = self.maze[y][x]
                screen_x = -len(self.maze[y]) * square_size / 2 + x * square_size
                screen_y = len(self.maze) * square_size / 2 - y * square_size

                if char == 'X':
                    self.draw_square(screen_x, screen_y, "gray", square_size)
                elif char == '.':
                    self.draw_square(screen_x, screen_y, "white", square_size)
                elif char == 's':
                    self.draw_square(screen_x, screen_y, "green", square_size)
                elif char == 'e':
                    self.draw_square(screen_x, screen_y, "blue", square_size)
                else:
                    print(f"Unintended symbol '{char}' found in the maze data!")

        self.screen.update()

    def draw_square(self, x, y, color, size):
        self.turtle.goto(x, y)
        self.turtle.color(color)
        self.turtle.pencolor("black")
        self.turtle.pendown()
        self.turtle.begin_fill()
        for _ in range(4):
            self.turtle.forward(size)
            self.turtle.right(90)
        self.turtle.end_fill()
        self.turtle.penup()

    def highlight_shortest_path(self, path):
        square_size = 40

        for x, y in path:
            screen_x = -len(self.maze[y]) * square_size / 2 + x * square_size + square_size / 2
            screen_y = len(self.maze) * square_size / 2 - y * square_size - square_size / 2

            # Calculate the center of the square
            center_x = screen_x + square_size / 2 - 20
            center_y = screen_y - square_size / 2 + 20

            # Draw a yellow circle on each square
            self.draw_circle(center_x, center_y, "yellow", square_size / 4)

        self.screen.update()

    def draw_circle(self, x, y, color, radius):
        self.turtle.goto(x, y - radius)
        self.turtle.color(color)
        self.turtle.pendown()
        self.turtle.begin_fill()
        self.turtle.circle(radius)
        self.turtle.end_fill()
        self.turtle.penup()

class drone_movement:
    def __init__(self, screen, maze, start_position, drawer):
        self.screen = screen
        self.maze = maze
        self.start_position = start_position
        self.drawer = drawer
        self.drone = Turtle()
        self.drone.shape('triangle')  # Set the shape of the drone
        self.drone.color('red')
        self.drone.penup()
        self.step_size = 40  # Corresponding step size for larger squares

    def setup_drone_movement(self):
        x, y = self.start_position
        screen_x = -len(self.maze[y]) * 40 / 2 + x * 40 + 20  # Adjusted for larger squares
        screen_y = len(self.maze) * 40 / 2 - y * 40 - 20  # Adjusted for larger squares
        self.drone.goto(screen_x, screen_y)
        self.drone.showturtle()  # Ensure the drone is visible

        # Update the screen to immediately show the drone
        self.screen.update()

        self.setup_key_bindings()

    def setup_key_bindings(self):
        wn = self.screen
        drone = self.drone
        drawer = self.drawer

        def move():
            current_x, current_y = drone.position()
            new_x, new_y = current_x, current_y

            if drone.heading() == 0:
                new_x += self.step_size
            elif drone.heading() == 90:
                new_y += self.step_size
            elif drone.heading() == 180:
                new_x -= self.step_size
            elif drone.heading() == 270:
                new_y -= self.step_size

            # Check if the new position is within the maze boundaries
            if not self.is_within_bounds(new_x, new_y):
                return

            # Calculate maze grid position based on new coordinates
            grid_x = int((new_x + len(self.maze[0]) * 40 / 2) // 40)
            grid_y = int((len(self.maze) * 40 / 2 - new_y) // 40)

            # Check if the new position is a wall (grey square)
            if self.maze[grid_y][grid_x] == 'X':
                return

            # Move the drone
            drone.goto(new_x, new_y)
            wn.update()

        def move_up():
            drone.setheading(90)
            move()

        def move_left():
            drone.setheading(180)
            move()

        def move_right():
            drone.setheading(0)
            move()

        def move_down():
            drone.setheading(270)
            move()

        def show_path():
            current_x, current_y = drone.position()
            grid_x = int((current_x + len(self.maze[0]) * 40 / 2) // 40)
            grid_y = int((len(self.maze) * 40 / 2 - current_y) // 40)

            path_finder = PathFinder(self.maze)
            path = path_finder.find_shortest_path_from(grid_x, grid_y)
            if path:
                print(f"Shortest Path: {path}")
                drawer.highlight_shortest_path(path)
            else:
                print("No path found!")

        def move_along_path():
            current_x, current_y = drone.position()
            grid_x = int((current_x + len(self.maze[0]) * 40 / 2) // 40)
            grid_y = int((len(self.maze) * 40 / 2 - current_y) // 40)

            path_finder = PathFinder(self.maze)
            path = path_finder.find_shortest_path_from(grid_x, grid_y)
            if path:
                self.move_drone_along_path(path)
            else:
                print("No path found!")        

        def quit_game():
            self.screen.bye()  # Close the Turtle graphics window

        def on_key_press(key):
            key_actions = {
                'Up': move_up,
                'Left': move_left,
                'Right': move_right,
                'Down': move_down,
                'f': show_path,
                'q': quit_game,
                'g': move_along_path  
            }
            action = key_actions.get(key)
            if action:
                action()

        for key in ['Up', 'Left', 'Right', 'Down', 'f', 'q', 'g']:
            wn.onkey(lambda k=key: on_key_press(k), key)
        wn.listen()   

    def move_drone_along_path(self, path):
        for i in range(len(path) - 1):
            x, y = path[i]
            next_x, next_y = path[i + 1]

            # Calculate direction to the next point
            if next_x > x:
                direction = 0  # East
            elif next_x < x:
                direction = 180  # West
            elif next_y > y:
                direction = 90  # North
            elif next_y < y:
                direction = 270  # South
            else:
                continue  # Should not happen if path is valid

            # Move the drone to the next point
            screen_x = -len(self.maze[y]) * 40 / 2 + next_x * 40 + 20
            screen_y = len(self.maze) * 40 / 2 - next_y * 40 - 20

            # Remove yellow circle highlight from the current square
            if i > 0:
                prev_x, prev_y = path[i - 1]
                center_x = -len(self.maze[prev_y]) * 40 / 2 + prev_x * 40 + 20
                center_y = len(self.maze) * 40 / 2 - prev_y * 40 - 20
                self.drawer.draw_circle(center_x, center_y, "white", 40 / 4)

            # Rotate the drone to face the direction
            self.drone.setheading(direction)

            # Move the drone to the next point
            self.drone.goto(screen_x, screen_y)
            self.screen.update()
            time.sleep(0.3)

        # Remove yellow circle highlight from the last square in the path
        last_x, last_y = path[-1]
        center_x = -len(self.maze[last_y]) * 40 / 2 + last_x * 40 + 20
        center_y = len(self.maze) * 40 / 2 - last_y * 40 - 20
        self.drawer.draw_circle(center_x, center_y, "white", 40 / 4)

    def is_within_bounds(self, x, y):
        maze_width = len(self.maze[0]) * 40 / 2
        maze_height = len(self.maze) * 40 / 2
        return -maze_width < x < maze_width and -maze_height < y < maze_height

class PathFinder:
    def __init__(self, maze):
        self.maze = maze

    def find_shortest_path_from(self, start_x, start_y):
        queue = deque([(start_x, start_y, [])])
        visited = set()
        visited.add((start_x, start_y))

        while queue:
            cx, cy, path = queue.popleft()
            cx = int(cx)
            cy = int(cy)
            if self.maze[cy][cx] == 'e':
                return path + [(cx, cy)]

            for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                nx, ny = cx + dx, cy + dy

                if 0 <= nx < len(self.maze[0]) and 0 <= ny < len(self.maze) and (nx, ny) not in visited and self.maze[ny][nx] != 'X':
                    visited.add((nx, ny))
                    queue.append((nx, ny, path + [(cx, cy)]))

        return None  # No path found 

if __name__ == "__main__":
    maze_file = "map01.txt"

    file_handler = FileHandler(maze_file)
    maze = file_handler.read().strip().split('\n')

    drawer = drawMap(maze)

    # Exit on click
    screen = drawer.screen
    screen.exitonclick()
