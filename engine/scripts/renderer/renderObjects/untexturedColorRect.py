import numpy as np
import moderngl as mgl

from scripts.renderer.nova_config import NOVA_SOLID_RECT_BATCH_SIZE
from scripts.renderer.dataTypes import NovaType as nt
from scripts.renderer.renderObjects.renderObject import NovaRenderObject

class UntexturedColorRectRenderObject(NovaRenderObject):
    def __init__(self, app, ctx): #nt.uColorRect
        super().__init__(app, ctx, "engine/scripts/renderer/shaders/vertex/solidColor.vert", "engine/scripts/renderer/shaders/fragment/solidColor.frag", np.float32, 3, NOVA_SOLID_RECT_BATCH_SIZE)

        self.create_vao([(self.buffer, "3f", "in_vert")])

    def add_to_render(self, items:list):

        # get data from items
        points = []
        colors = []

        for item in items:

            # calculate vertex pos
            tl = self.app.gl_normalize_screen_coords((item.metadata["rect"].left, item.metadata["rect"].top))
            tr = self.app.gl_normalize_screen_coords((item.metadata["rect"].right, item.metadata["rect"].top))
            bl = self.app.gl_normalize_screen_coords((item.metadata["rect"].left, item.metadata["rect"].bottom))
            br = self.app.gl_normalize_screen_coords((item.metadata["rect"].right, item.metadata["rect"].bottom))

            points.extend([tl[0], tl[1], 0.0])
            points.extend([tr[0], tr[1], 0.0])
            points.extend([bl[0], bl[1], 0.0])
            points.extend([br[0], br[1], 0.0])

            # prepare colors for uniform
            colors.append(
                (item.metadata["color"][0] / 255, item.metadata["color"][1] / 255, item.metadata["color"][2] / 255, 1.0) # essentially a vec4 of rgb + a=1
            )

        # uniform padding
        while len(colors) < NOVA_SOLID_RECT_BATCH_SIZE:
            colors.append((1.0, 1.0, 1.0, 1.0))

        # send vertex array to vmem
        self.array = np.array(points, dtype=self.dataType)

        self.buffer.clear()
        self.buffer.write(self.array)
        
        #print(self.buffer.read())

        # set shader uniforms
        self.vao.program["cols"] = colors

