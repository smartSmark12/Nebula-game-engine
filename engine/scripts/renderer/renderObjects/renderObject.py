import numpy as np
import moderngl as mgl

class NovaRenderObject:
    def __init__(self, app, ctx:mgl.Context, vertexShaderPath:str, fragmentShaderPath:str, dataType:np.dtype, bufferVertexSize:int, bufferVertsPerItem:int, bufferAmount:int):
        self.app = app
        self.ctx = ctx

        self.dataType = dataType
        self.bufferVertexSize = bufferVertexSize
        self.bufferVertsPerItem = bufferVertsPerItem
        self.bufferAmount = bufferAmount

        self.create_buffers(dataType=dataType, bufferVertexSize=bufferVertexSize, bufferVertsPerItem=bufferVertsPerItem, bufferAmount=bufferAmount)

        self._vs = vertexShaderPath
        self._fs = fragmentShaderPath

        # VAOS NOT AUTOMATICALLY CREATED
        # use create_vao() in init

    def create_vao(self, buffers:list[tuple]):
        self._create_vao(
            self.load_shader(self._vs),
            self.load_shader(self._fs),
            buffers
        )

    def create_buffers(self, dataType:np.dtype, bufferVertexSize:int, bufferVertsPerItem:int, bufferAmount:int):
        reserve_bytes = np.dtype(dataType).itemsize * bufferAmount * bufferVertsPerItem * bufferVertexSize
        reserve_type = np.dtype(dataType)

        self.array = None
        self.buffer = self.ctx.buffer(reserve=reserve_bytes)

        print(f"\ncreated VMEM buffer:")
        print(f"reserved VMEM: {reserve_bytes} B ({reserve_bytes / 1024} kB)")
        print(f"buffer type: {reserve_type}")
        print(f"vertexDataSize: {bufferVertexSize}")

    def _create_vao(self, vertexShader:str, fragmentShader:str, buffers:list) -> mgl.VertexArray:
    
        program = self.ctx.program(
                vertex_shader=vertexShader,
                fragment_shader=fragmentShader
            )
        
        render_object = self.ctx.vertex_array(
                program,
                buffers
            )

        # buffers in a format of [vertexData, format, allocation]

        #[(
        #    vertexData, # "buffer" ig
        #    '2f 2f',    # buffer data format
        #    'vert',     # buffer data names
        #    'texcoord'
        #)]

        self.vao = render_object

        print("\ncreated VAO")

    def load_shader(self, shaderPath:str) -> str:
        shader = None

        with open(shaderPath, 'r') as f:
            shader = f.read()

        return shader

    def add_to_render(self):
        pass # use to add vertex data, uniforms etc

    def pre_render(self):
        pass # use to setup uniforms etc

    def render(self):
        self.pre_render()

        buffer_vertices = self.array.size // self.bufferVertexSize

        self.vao.render(mode=mgl.TRIANGLES, vertices=buffer_vertices)