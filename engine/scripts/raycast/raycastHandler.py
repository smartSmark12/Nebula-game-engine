import random

from scripts.raycast.obstacle import Obstacle
from scripts.raycast.ray import Ray
from scripts.raycast.source import Source
from scripts.raycast.wall import Wall

class Raycaster:
    def __init__(self, appInstance):
        self.app = appInstance

        # wallmap generator stuff
        self.wallmap = []
        self.wall_size = 50
        self.map_size = (20, 20)

        # other shis
        self.obstacles = []
        self.walls = [] # has to be recalculated based on obstacles
        self.sources = []

        # to force recalculate lighting
        self.force_update = False

        """ # initial wall calculation
        self.recalculate_walls() """

    def update(self):
        self.recalculate_collisions()

    def add_source(self, position:tuple, rayCount:int):
        self.sources.append(Source(position, rayCount))

    def create_walls(self):
        for y in range(self.map_size[0]):
            self.wallmap.append([])
            for x in range(self.map_size[1]):
                self.wallmap[y].append(random.randint(0, 1))

        for y in range(len(self.wallmap)):
            for x in range(len(self.wallmap[y])):
                if self.wallmap[y][x]:
                    obstacle = Obstacle((x*self.wall_size, y*self.wall_size), (self.wall_size, self.wall_size))
                    self.obstacles.append(obstacle)

    def recalculate_walls(self):
        self.walls.clear()

        for obstacle in self.obstacles:
            for wall in obstacle.walls:
                self.walls.append(wall)

        # border walls
        self.walls.append(Wall(((0, 0), (len(self.wallmap[0])*self.wall_size, 0))))
        self.walls.append(Wall(((len(self.wallmap[0])*self.wall_size, 0), (len(self.wallmap[0])*self.wall_size, len(self.wallmap)*self.wall_size))))
        self.walls.append(Wall(((len(self.wallmap[0])*self.wall_size, len(self.wallmap)*self.wall_size), (0, len(self.wallmap)*self.wall_size))))
        self.walls.append(Wall(((0, len(self.wallmap)*self.wall_size), (0, 0))))

    def recalculate_collisions(self):
        for source in self.sources:
            if source.last_pos != source.pos or self.force_update:
                source.points = source.recalculate(self.walls)

    def render(self):
        # render obstacles
        for obstacle in self.obstacles:
            for wall in obstacle.walls:
                self.app.draw("line", 2, {"start":wall.points[0], "end":wall.points[1]})

        # render rays
        for source in self.sources:
            for i in source.points:
                self.app.draw("aaline", 4, {"start":source.pos, "end":i})