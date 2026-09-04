import numpy as np
import moderngl as mgl

from scripts.renderer.nova_config import NOVA_DEFAULT_BATCH_SIZE
from scripts.renderer.dataTypes import NovaType as nt
from scripts.renderer.renderObjects.renderObject import NovaRenderObject

class ColorTriangleRenderObject(NovaRenderObject):
    def __init__(self, app, ctx):
        super().__init__(app, ctx, "engine/scripts/renderer/shaders/vertex/solidTriangle.vert", "engine/scripts/renderer/shaders/fragment/solidTriangle.frag", np.float32, 3, 6, NOVA_DEFAULT_BATCH_SIZE)

        self.create_vao([(self.buffer, "3f", "in_vert")])

    def render(self, items):
        i = 0
        while len(items) > NOVA_DEFAULT_BATCH_SIZE * i:
            self.add_to_render(items[NOVA_DEFAULT_BATCH_SIZE * i: NOVA_DEFAULT_BATCH_SIZE * i + NOVA_DEFAULT_BATCH_SIZE])
            self._render()

            i += 1

    def add_to_render(self, items:list):

        # get data from items
        points = []

        colors = []

        for item in items:

            # calculate vertex pos
            t_points = item.metadata["points"]
            color = item.metadata["color"]

            p1 = self.app.gl_normalize_screen_coords(t_points[0])
            p2 = self.app.gl_normalize_screen_coords(t_points[1])
            p3 = self.app.gl_normalize_screen_coords(t_points[2])

            # quad building
            
            # tri 1
            points.extend([p1[0], p1[1], 0.0])
            points.extend([p2[0], p2[1], 0.0])
            points.extend([p3[0], p3[1], 0.0])

            # prepare colors for uniform
            colors.append(
                (color[0] / 255, color[1] / 255, color[2] / 255, 1.0) # essentially a vec4 of rgb + a=1
            )

        # uniform padding
        while len(colors) < NOVA_DEFAULT_BATCH_SIZE:
            colors.append((1.0, 1.0, 1.0, 1.0))

        # send vertex array to vmem
        self.array = np.array(points, dtype=self.dataType)

        self.buffer.clear()
        self.buffer.write(self.array)

        # set shader uniforms
        self.vao.program["cols"] = colors

