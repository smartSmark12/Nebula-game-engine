def collide(wall_points:tuple, ray_pos:tuple, ray_dir:tuple):
    wpnt1 = wall_points[0]
    wpnt2 = wall_points[1]

    rpnt3 = ray_pos
    rpnt4 = (ray_pos[0] + ray_dir[0], ray_pos[1] + ray_dir[1])

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