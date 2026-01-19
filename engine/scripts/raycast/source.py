import math

from scripts.raycast.ray import Ray

class Source:
    def __init__(self, pos:tuple, numberOfRays):
        self.pos = pos
        self.last_pos = self.pos

        self.num_rays = int(numberOfRays)
        self.rays = []

        self.points = []
        
        for i in range(self.num_rays):
            self.rays.append(
                Ray(self.pos,
                                (
                                    math.cos(math.radians(i/self.num_rays*360)),
                                    math.sin(math.radians(i/self.num_rays*360))
                                )
                            )
            )

    def recalculate(self, walls:list):
        self.last_pos = self.pos
        points = []

        walls_sorted = sorted(walls, key=lambda wall: math.dist(self.pos, wall.points[0]) + math.dist(self.pos, wall.points[1]))

        """ match app.sorting_method:
            case 0:
                walls_sorted = sorted(walls, key=lambda wall: min(math.dist(self.pos, wall.pnts[0]), math.dist(self.pos, wall.pnts[1]))) # works with artifacts
            case 1:
                walls_sorted = sorted(walls, key=lambda wall: math.dist(self.pos, wall.pnts[0]) + math.dist(self.pos, wall.pnts[1])) # works with bad approximation without artifacts
            case 2:
                walls_sorted = sorted(walls, key=lambda wall: max(min(math.dist(self.pos, wall.pnts[0]), math.dist(self.pos, wall.pnts[1])), math.dist(self.pos, wall.pnts[0]) + math.dist(self.pos, wall.pnts[1]))) # still bad approx without artifacts """

        for ray in self.rays:
            ray.pos = self.pos
            intersectPoint = None

            for wall in walls_sorted:
                intersection = ray.collide(wall)

                if intersection != False:
                    intersectPoint = intersection
                    break

            if intersectPoint != None:
                points.append(intersectPoint)

        return points

    """ def render(self, walls:list, force_update):
        if self.last_pos != self.pos or force_update:
            self.points = self.recalculate(walls) """

    """ if app.render_lines:
        for i in self.points:
            app.to_render.append(RenderItem("aaline", 4, {"start":self.pos, "end":i})) """

    """ if app.render_poly:
        app.to_render.append(RenderItem("poly", 3, {"color":(240, 240, 240), "points":self.points}))

    if app.render_dotsurf:
        for i in self.points:
            pg.draw.line(app.dotsurf, white, i, i) """