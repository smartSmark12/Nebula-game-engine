# Nova Renderer (Nebula render service) Config

# renderer information
NOVA_TARGET_VERSION = "0.0.5r"
NOVA_VERSION = "0.0.1"

# render batching config # HAS TO BE CHANGED IN THE RELEVANT SHADER TOO
# for more info, refer to engine/help.md #engine-configuration

# used whenever no specific batching size is set
NOVA_DEFAULT_BATCH_SIZE = 32

NOVA_SOLID_RECT_BATCH_SIZE = 64
NOVA_SOLID_CIRCLE_BATCH_SIZE = 64
NOVA_TEXTURED_RECT_BATCH_SIZE = 32