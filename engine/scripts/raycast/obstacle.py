from scripts.raycast.wall import Wall

class Obstacle:
        def __init__(self, pos, size):
            self.pos = pos
            self.size = size
            self.walls = []

            self.create_walls()

        def create_walls(self):
            points = [
                (self.pos[0], self.pos[1]),
                (self.pos[0] + self.size[0], self.pos[1]),
                (self.pos[0] + self.size[0], self.pos[1] + self.size[1]),
                (self.pos[0], self.pos[1] + self.size[1])
            ]

            for i in range(len(points)):
                try:
                    self.walls.append(
                            Wall((points[i], points[i+1]))
                    )
                except:
                    self.walls.append(
                            Wall((points[i], points[0]))
                    )

        """ def render(self):
            for wall in self.walls:
                app.to_render.append(RenderItem("line", 2, {"start":wall.pnts[0], "end":wall.pnts[1]})) """

        """ app.to_render.append(RenderItem("rect", 2, {"rect":(self.pos[0], self.pos[1], self.pos[0] + self.size[0], self.pos[1] + self.size[1])})) """        