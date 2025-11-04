NGF_VERSION = "0.0.4"
GAME_NAME = "Placeholder_name"

WIDTH = 1920
HEIGHT = 1080

RESOLUTION = (WIDTH, HEIGHT)
IN_FULLSCREEN = False

# rendering options
FPS_LOGIC_LIMIT = 0#35#85
FPS_RENDER_LIMIT = 0#35
SYNC_UPS_FPS = 1                    # should client synchronize UPS and FPS? (leads to better UPS-FPS ratio) - EXPERIMENTAL!!
RENDER_LAYERS = 10                  # set how many layers your game uses; start from 0, empty layers usually don't impact performance much
MULTITHREADED_RENDERING = True      # use a newer multithreaded rendering method - EXPERIMENTAL

OGL_ENABLED = 0 # opengl implementation for shader support (currently resource heavy)
DEFAULT_SHADER_PATH = "./engine/shaders/default" # adds '.vert' & '.frag' automatically

DEFAULT_SPRITE_PATH = "./engine/scripts/sprites_to_load.py"
DEFAULT_SPRITE_JSON_PATH = "./engine/scripts/json/sprites_to_load.json"
DEFAULT_ANIMATION_PATH = "./engine/scripts/animations_to_create.py"

# server settings
SERVER_CONNECTIONS = 4          # max connections the server will expect at start
SERVER_DATA_SIZE = 1024*16      # max bytesize the client will send and accept
SERVER_UPS = 60
SERVER_DELTA = (1000/SERVER_UPS)/1000   # minimum time delay between sending packets
SERVER_TIMEOUT = 5              # max time of no response from server before kicking player

# server debug settings
SERVER_LOCAL_SERVER = 1         # whether to connect to a local server or to an external one
SERVER_IP = None                # external server IP