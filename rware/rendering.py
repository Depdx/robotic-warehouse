import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Ellipse
from IPython.display import display, clear_output


class Viewer(object):
    def __init__(self, world_size):
        self.rows, self.cols = world_size
        self.grid_size = 30
        self.icon_size = 20
        self.fig, self.ax = None, None

    def close(self):
        plt.close()

    def render(self, env, return_rgb_array=False):
        self.fig, self.ax = plt.subplots()

        # Render your environment using Matplotlib here
        self._draw_grid()
        self._draw_goals(env)
        self._draw_shelves(env)
        self._draw_agents(env)

        plt.xlim(0, self.cols * self.grid_size)
        plt.ylim(0, self.rows * self.grid_size)
        plt.gca().set_aspect("equal", adjustable="box")

        plt.draw()
        plt.pause(0.001)

    def _draw_grid(self):
        for r in range(self.rows + 1):
            plt.plot(
                [0, self.cols * self.grid_size],
                [r * self.grid_size, r * self.grid_size],
                color="black",
            )
        for c in range(self.cols + 1):
            plt.plot(
                [c * self.grid_size, c * self.grid_size],
                [0, self.rows * self.grid_size],
                color="black",
            )

    def _draw_shelves(self, env):
        for shelf in env.shelfs:
            x, y = shelf.x, shelf.y
            y = self.rows - y - 1
            shelf_color = "lightblue" if shelf in env.request_queue else "blue"
            rectangle = Rectangle(
                (x * self.grid_size, y * self.grid_size),
                self.grid_size,
                self.grid_size,
                linewidth=1,
                edgecolor="black",
                facecolor=shelf_color,
            )
            self.ax.add_patch(rectangle)

    def _draw_goals(self, env):
        for goal in env.goals:
            x, y = goal
            y = self.rows - y - 1
            rectangle = Rectangle(
                (x * self.grid_size, y * self.grid_size),
                self.grid_size,
                self.grid_size,
                linewidth=1,
                edgecolor="black",
                facecolor="gray",
            )
            self.ax.add_patch(rectangle)

    def _draw_agents(self, env):
        for agent in env.agents:
            col, row = agent.x, agent.y
            row = self.rows - row - 1
            radius = self.grid_size / 3
            draw_color = "red" if agent.carrying_shelf else "green"
            ellipse = Ellipse(
                (
                    col * self.grid_size + self.grid_size / 2,
                    row * self.grid_size + self.grid_size / 2,
                ),
                width=2 * radius,
                height=2 * radius,
                edgecolor="black",
                facecolor=draw_color,
            )
            self.ax.add_patch(ellipse)
