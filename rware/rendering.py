import plotly.graph_objects as go


class Viewer(object):
    def __init__(self, world_size):
        self.rows, self.cols = world_size
        self.grid_size = 30
        self.icon_size = 20
        self.fig = go.FigureWidget()

    def close(self):
        pass  # No specific close operation for Plotly

    def render(self, env, return_rgb_array=False):
        self.fig = go.FigureWidget()

        # Render your environment using Plotly here
        self._draw_grid()
        self._draw_goals(env)
        self._draw_shelves(env)
        self._draw_agents(env)

        self.fig.update_layout(
            xaxis=dict(range=[0, self.cols * self.grid_size]),
            yaxis=dict(range=[0, self.rows * self.grid_size]),
        )

        self.fig.show()

    def _draw_grid(self):
        for r in range(self.rows + 1):
            self.fig.add_trace(
                go.Scatter(
                    x=[0, self.cols * self.grid_size],
                    y=[r * self.grid_size, r * self.grid_size],
                    mode="lines",
                    line=dict(color="black"),
                )
            )
        for c in range(self.cols + 1):
            self.fig.add_trace(
                go.Scatter(
                    x=[c * self.grid_size, c * self.grid_size],
                    y=[0, self.rows * self.grid_size],
                    mode="lines",
                    line=dict(color="black"),
                )
            )

    def _draw_shelves(self, env):
        for shelf in env.shelfs:
            x, y = shelf.x, shelf.y
            y = self.rows - y - 1
            shelf_color = "lightblue" if shelf in env.request_queue else "blue"
            self.fig.add_trace(
                go.Scatter(
                    x=[
                        x * self.grid_size,
                        (x + 1) * self.grid_size,
                        (x + 1) * self.grid_size,
                        x * self.grid_size,
                        x * self.grid_size,
                    ],
                    y=[
                        y * self.grid_size,
                        y * self.grid_size,
                        (y + 1) * self.grid_size,
                        (y + 1) * self.grid_size,
                        y * self.grid_size,
                    ],
                    mode="lines+text",
                    fill="toself",
                    fillcolor=shelf_color,
                    line=dict(color="black"),
                    text="",
                    hoverinfo="none",
                )
            )

    def _draw_goals(self, env):
        for goal in env.goals:
            x, y = goal
            y = self.rows - y - 1
            self.fig.add_trace(
                go.Scatter(
                    x=[
                        x * self.grid_size,
                        (x + 1) * self.grid_size,
                        (x + 1) * self.grid_size,
                        x * self.grid_size,
                        x * self.grid_size,
                    ],
                    y=[
                        y * self.grid_size,
                        y * self.grid_size,
                        (y + 1) * self.grid_size,
                        (y + 1) * self.grid_size,
                        y * self.grid_size,
                    ],
                    mode="lines",
                    line=dict(color="black"),
                    fill="toself",
                    fillcolor="gray",
                    hoverinfo="none",
                )
            )

    def _draw_agents(self, env):
        for agent in env.agents:
            col, row = agent.x, agent.y
            row = self.rows - row - 1
            radius = self.grid_size / 3
            draw_color = "red" if agent.carrying_shelf else "green"
            self.fig.add_trace(
                go.Scatter(
                    x=[col * self.grid_size],
                    y=[row * self.grid_size],
                    mode="markers",
                    marker=dict(color=draw_color, size=2 * radius),
                    hoverinfo="none",
                )
            )
