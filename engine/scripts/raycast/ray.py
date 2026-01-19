from scripts.raycast.raycaster import collide

class Ray:
    def __init__(self, pos:tuple, dir:tuple):
        self.pos = pos
        self.dir = dir

    def collide(self, wall):
        return collide(wall.points, self.pos, self.dir)

        wpnt1 = wall.pnts[0]
        wpnt2 = wall.pnts[1]

        rpnt3 = self.pos
        rpnt4 = (self.pos[0] + self.dir[0], self.pos[1] + self.dir[1])

        num = (wpnt1[0] - rpnt3[0]) * (rpnt3[1] - rpnt4[1]) - (wpnt1[1] - rpnt3[1]) * (rpnt3[0] - rpnt4[0])
        den = (wpnt1[0] - wpnt2[0]) * (rpnt3[1] - rpnt4[1]) - (wpnt1[1] - wpnt2[1]) * (rpnt3[0] - rpnt4[0])

        if den == 0:
            return False

        t = num / den
        u = ((wpnt2[0] - wpnt1[0]) * (wpnt1[1] - rpnt3[1]) - (wpnt2[1] - wpnt1[1]) * (wpnt1[0] - rpnt3[0])) / den

        if (t > 0 and t < 1 and u > 0):
            px = (wpnt1[0] + t * (wpnt2[0] - wpnt1[0]))
            py = (wpnt1[1] + t * (wpnt2[1] - wpnt1[1]))
            return (px, py)
        else:
            return False