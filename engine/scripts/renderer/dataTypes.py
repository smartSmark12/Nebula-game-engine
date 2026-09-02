import numpy as np

class NovaType:

    # untextured rect
    # 3f
    # vec4 uniform (rgba)
    uColorRect = np.dtype([
        ('x', np.float32),
        ('y', np.float32),
        ('z', np.float32)
    ])

    # textured rect
    # 3f 2f
    # sampler2D uniform
    texturedRect = np.dtype([
        ('x', np.float32),
        ('y', np.float32),
        ('z', np.float32),
        ('uvx', np.float32),
        ('uvy', np.float32)
    ])