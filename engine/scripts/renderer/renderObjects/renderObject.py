import numpy as np
import moderngl as mgl

class NovaRenderObject:
    def __init__(self, app, ctx:mgl.Context, vertexShaderPath:str, fragmentShaderPath:str, dataType:np.dtype, bufferVertexSize:int, bufferAmount:int):
        self.app = app
        self.ctx = ctx

        self.dataType = dataType
        self.bufferVertexSize = bufferVertexSize
        self.bufferAmount = bufferAmount

        self.create_buffers(dataType=dataType, bufferVertexSize=bufferVertexSize, bufferAmount=bufferAmount)

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

    def create_buffers(self, dataType:np.dtype, bufferVertexSize:int, bufferAmount:int):
        self.array = None
        self.buffer = self.ctx.buffer(reserve=np.dtype(dataType).itemsize * bufferAmount * bufferVertexSize)

        print(f"\ncreated VMEM buffer:")
        print(f"reserved VMEM: {np.dtype(dataType).itemsize * bufferAmount * bufferVertexSize} B")
        print(f"buffer type: {np.dtype(dataType)}")
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

        print(f"created VAO: {self.vao}")

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
        #print("rendered!")
        self.vao.render(mode=mgl.TRIANGLE_STRIP, vertices=4)