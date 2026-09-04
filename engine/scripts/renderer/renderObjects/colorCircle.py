import numpy as np
import moderngl as mgl

from scripts.core.settings import HEIGHT

from scripts.renderer.nova_config import NOVA_SOLID_CIRCLE_BATCH_SIZE
from scripts.renderer.dataTypes import NovaType as nt
from scripts.renderer.renderObjects.renderObject import NovaRenderObject

class ColorCircleRenderObject(NovaRenderObject):
    def __init__(self, app, ctx):
        super().__init__(app, ctx, "engine/scripts/renderer/shaders/vertex/solidCircle.vert", "engine/scripts/renderer/shaders/fragment/solidCircle.frag", np.float32, 3, 6, NOVA_SOLID_CIRCLE_BATCH_SIZE)

        self.create_vao([(self.buffer, "3f", "in_vert")])

    def render(self, items):
        i = 0
        while len(items) > NOVA_SOLID_CIRCLE_BATCH_SIZE * i:
            self.add_to_render(items[NOVA_SOLID_CIRCLE_BATCH_SIZE * i: NOVA_SOLID_CIRCLE_BATCH_SIZE * i + NOVA_SOLID_CIRCLE_BATCH_SIZE])
            self._render()

            i += 1

    def add_to_render(self, items:list):

        # get data from items
        points = []

        colors = []
        centers = []
        radii = []
        widths = []

        for item in items:

            # calculate vertex pos
            center = item.metadata["center"]
            radius = item.metadata["radius"]
            width = item.metadata["width"]
            color = item.metadata["color"]

            tl = self.app.gl_normalize_screen_coords((center[0] - radius, center[1] - radius))
            tr = self.app.gl_normalize_screen_coords((center[0] + radius, center[1] - radius))
            bl = self.app.gl_normalize_screen_coords((center[0] - radius, center[1] + radius))
            br = self.app.gl_normalize_screen_coords((center[0] + radius, center[1] + radius))

            # quad building
            
            # tri 1
            points.extend([tl[0], tl[1], 0.0])
            points.extend([tr[0], tr[1], 0.0])
            points.extend([bl[0], bl[1], 0.0])

            # tri 2
            points.extend([tr[0], tr[1], 0.0])
            points.extend([br[0], br[1], 0.0])
            points.extend([bl[0], bl[1], 0.0])

            # prepare colors for uniform
            colors.append(
                (color[0] / 255, color[1] / 255, color[2] / 255, 1.0) # essentially a vec4 of rgb + a=1
            )

            # prepare centers for uniform
            centers.append(
                (center[0], HEIGHT - center[1])
            )

            # prepare radius for uniform
            radii.append(
                radius # radius, center, width not converted to screen space, as gl_FragCoord is pixel based for some fucking reason
            )

            # prepare width for uniform
            widths.append(
                width
            )

        # uniform padding
        while len(colors) < NOVA_SOLID_CIRCLE_BATCH_SIZE:
            colors.append((1.0, 1.0, 1.0, 1.0))

        while len(centers) < NOVA_SOLID_CIRCLE_BATCH_SIZE:
            centers.append((0.0, 0.0))

        while len(radii) < NOVA_SOLID_CIRCLE_BATCH_SIZE:
            radii.append(0.0)

        while len(widths) < NOVA_SOLID_CIRCLE_BATCH_SIZE:
            widths.append(0.0)

        # send vertex array to vmem
        self.array = np.array(points, dtype=self.dataType)

        self.buffer.clear()
        self.buffer.write(self.array)

        # set shader uniforms
        self.vao.program["cols"] = colors
        self.vao.program["centers"] = centers
        self.vao.program["radii"] = radii
        self.vao.program["widths"] = widths

