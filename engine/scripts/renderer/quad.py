from array import array

# fully unused
class Quad:
    def __init__(self, renderer, vertexCoords:tuple[float, float, float, float]):

        self.renderer = renderer

        self.quad_buffer = self.renderer.ctx.buffer(data=array("f", [ # cX, cY, uvX, uvY
                    -1.0,  1.0, 0.0, 0.0,
                     1.0,  1.0, 1.0, 0.0,
                    -1.0, -1.0, 0.0, 1.0,
                     1.0, -1.0, 1.0, 1.0,
                ]))