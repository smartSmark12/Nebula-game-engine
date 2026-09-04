<!-- hello from Val :3 -->

*Documentation Nebula engine target version:* **v0.0.5r**

## NOTICE
This is an **not** a full documentation yet, so expect mistakes and **missing** or frequently **changing** paragraphs

# Table of contents
- [Table of contents](#table-of-contents)
- [Engine code structure](#engine-code-structure)
  - [Imports](#imports)
  - [Built-in functions](#built-in-functions)
  - [Engine configuration](#engine-configuration)
  - [Custom classes](#custom-classes)
- [Engine file structure](#engine-file-structure)
- [Engine features \& services](#engine-features--services)
  - [Rendering](#rendering)
    - [Drawing](#drawing)
    - [RenderItem metadata](#renderitem-metadata)
    - [RenderItem types](#renderitem-types)
      - [sprite](#sprite)
      - [rect](#rect)
      - [line](#line)
      - [aaline](#aaline)
      - [circle](#circle)
      - [smooth\_circle](#smooth_circle)
      - [text](#text)
      - [triangle](#triangle)
      - [poly](#poly)
    - [Renderer types](#renderer-types)
  - [Sprites](#sprites)
    - [Loading sprites](#loading-sprites)
    - [Using sprites](#using-sprites)
  - [Animations](#animations)
    - [Loading animations](#loading-animations)
    - [Using animations](#using-animations)
  - [Keybinds \& Keygroups](#keybinds--keygroups)
  - [File management](#file-management)
    - [Nebula files](#nebula-files)
    - [CSV files](#csv-files)
    - [JSON files](#json-files)
  - [Scenes](#scenes)
  - [VUI](#vui)
    - [WinVUI](#winvui)
  - [Alarms](#alarms)
  - [Reactions](#reactions)
  - [Multiplayer](#multiplayer)
    - [Networking](#networking)
    - [Server-side](#server-side)
    - [Client-side](#client-side)
  - [TileScripts](#tilescripts)
  - [Shaders](#shaders)
  - [Misc](#misc)
    - [Cython](#cython)
    - [Runtime log handler](#runtime-log-handler)
    - [Raycaster](#raycaster)

# Engine code structure
The only place containing active code is (and should be) [mainEngine.py](/engine/scripts/core/mainEngine.py). This is where all game-related code should be called from / handled in.

## Imports
The file starts with imports - first generic ones (e.g. pygame, sys, moderngl), then engine-related ones (e.g. ThreadedGameRenderer, flatpane) and finally game-related imports (_note_: now cython imports should go after game-related ones)

## Built-in functions
Specific service functions ([alarms](#alarms), [render](#rendering), [keybinds](#keybinds--keygroups)) won't be discussed here; locate the appropriate topic for help with those
- **engine_on_init()** - starts up the engine itself, actions include preparing the game window, pygame clock and all internal handlers and services (_note_: you should **not** make any changes to this function, unless you're modifying an engine service)
- **game_on_init()** - by default empty - runs after engine_on_init() and should contain all your game startup / preparation code (global variables, service binding, sprite rescaling, etc.)
- **handle_events()** - an internal function used for game exit detection and keyHandler updates. If you need to detect a specific event that _isn't already handled_ by an internal service, then this is the place to do it efficiently
- **update()** - an internal function used to move time, update the mouse information and handle service updates. If you found this function and want to write code that should run every frame, then go to **do_logic()** instead, as this function is _engine-critical_
- **do_logic()** - runs every frame and is meant to house your **game-related logic** (moving players, handling keybind presses, changing scenes, etc.)
- **run()** - a post-startup function housing the main update loop. (_note_: you **shouldn't** write any startup code here, **game_on_init()** is here for that reason - should only be used for specific game exit cleanup)
- **runGame()** - the engine entry point - do not write any code here
- **load_sounds()** - as Nebula doesn't currently have a unified sound management service, this is where you should load your music and sound effects (_note_: the function is **not called by default** - ideally call it in game_on_init())

## Engine configuration
There are currently two main config files; [one](/engine/scripts/core/settings.py) for the Nebula engine itself and [one](/engine/scripts/renderer/nova_config.py) for the Nebula Render Service Nova.  
The [engine settings file](/engine/scripts/core/settings.py) contains multiple sections:
- **engine information** -
  - *NGF_VERSION* - internal engine version used for debugging or version compatibility checking, meaning you **should not change it**
  - *GAME_NAME* - name which will be used within the window header and/or which you can use in your game
- **display settings** - currently used as the default game resolution whenever you don't use an internal resolution / fullscreen override
- **rendering options**
  - *FPS_LOGIC_LIMIT* - maximum/target logic (CPU) FPS when multithreading is used or general maximum/target FPS otherwise.
  - *FPS_RENDER_LIMIT* - maximum/target GPU FPS when multithreading is used, otherwise it's ignored and the *FPS_LOGIC_LIMIT* is used instead
  - *SYNC_UPS_FPS* - whether the engine should limit rendered (GPU) FPS to the current logic (CPU) FPS (*note*: *current* meaning the frame-by-frame live FPS, not the *FPS_LOGIC_LIMIT*, e.g. if the game is running at 39 CPU FPS, the rendered (GPU) FPS will be also limited to 39)
  - *RENDER_LAYERS* - total number of layers which will be used for rendering. There is only a negligible performance decrease when using a large number of render layers
  - *MULTITHREADED_RENDERING* - whether to run the render worker on a separate thread. There is no real benefit to using multithreaded rendering, as the current python version is still locked using the [GIL](https://en.wikipedia.org/wiki/Global_interpreter_lock) and because the [default renderer](#renderer-types) is the only one currently capable of running multithreaded
  - *RENDERER_TYPE* - which renderer to use; 0 - default, 1 - screenspace shader, 2 - NRS Nova
  - *DEFAULT_SPRITE_PATH* - *legacy*; default file path from which the older sprite loader will load sprite information
  - *DEFAULT_SPRITE_JSON_PATH* - default file path from which the sprite loader will load sprite information
  - *DEFAULT_ANIMATION_PATH* - default file path from which the animation loader will load animation information
- **scene settings**
  - *DEFAULT_SCENE_NAME* - name of the default processed scene. Can be changed here, but a better way is to change it programmatically using engine commands
- **server settings**  
    (*note*: the current server architecture is extremely impractical and mostly exists as a proof of concept. More information available [here](#multiplayer))
  - *SERVER_CONNECTIONS* - maximum number of connections the server will be listening for
  - *SERVER_DATA_SIZE* - maximum bytesize the server and client will be able to send/receive. Any packets larger than that will be truncated and most likely corrupted
  - *SERVER_UPS* - target logic (CPU) FPS for the server to run at
  - *SERVER_DELTA* - minimum time delay between packets sent by the server in seconds
  - *SERVER_TIMEOUT* - maximum time of no response from a client in seconds, after which the client is disconnected from the server
- **server debug settings**
  - *SERVER_LOCAL_SERVER* - will connect to a *localhost* server address instead of an external one when True
  - *SERVER_IP* - IP address of an external server to which the client will attempt to connect unless overridden

The [NRS Nova config file](/engine/scripts/renderer/nova_config.py) options:
- **renderer information**
  - *NOVA_TARGET_VERSION* - Nebula version the current NRS Nova version is built for / tested to work with. **Should not be changed**
  - *NOVA_VERSION* - internal NRS Nova version. **Should not be changed**
- **render batching config**  
    **Disclaimer:** when changing any of these values, make sure to also change the relevant buffer/uniform sizes in the relevant shaders, otherwise the shaders will fail to compile/won't work in general 
  - *NOVA_SOLID_RECT_BATCH_SIZE* - batch size for untextured (colored) rectangles
  - *NOVA_SOLID_CIRCLE_BATCH_SIZE* - batch size for circles (both normal and smooth_circles)
  - *NOVA_TEXTURED_RECT_BATCH_SIZE* - batch size for textured rectangles

## Custom classes
As written in the [file structure](#engine-file-structure), all game-related files should be placed in the [game scripts folder](/engine/game/scripts/) (read about importing [here](#imports)). Note there isn't any specific file naming convention

# Engine file structure
The engine is split into two main folders - [scripts](/engine/scripts/) and [game](/engine/game/).  
The _scripts_ folder contains all of Nebula's code, including all [core](/engine/scripts/core/) elements, [mainEngine.py](/engine/scripts/core/mainEngine.py) and all custom libraries (e.g. [keyHandler.py](/engine/scripts/core/keyHandler.py), [mplib](/engine/scripts/mplib/)). You are heavily advised not to touch any custom library files except mainEngine.py, cython [setup.py](/engine/scripts/cython/setup.py) and (somewhat deprecated) [test.py](/engine/scripts/test.py), as it's a script name reserved for testing custom engine modifications / deep game functionality.  
The _game_ folder is meant as a root folder for all game-related [scripts](/engine/game/scripts/), [assets](/engine/game/assets/) etc.

# Engine features & services

## Rendering
For shader support see [Shaders](#shaders)

Nebula uses a custom [rendering adapter](/engine/scripts/core/render.py) built on [RenderItems](/engine/scripts/renderItem.py), which you don't directly interact with (you can, but that's only recommended for compatibility or customization).  
As of right now, the rendering adapter is firmly fixed to certain object types and certain rendering steps (allowing for a single-threaded/multi-threaded mode and some base screenspace [shader](#shaders) support), but that is all planned to be improved in later versions with a custom [OpenGL/ModernGL](https://moderngl.readthedocs.io/) renderer with unlocked customization.

### Drawing
To draw to the screen, use the *self.draw()* method of [mainEngine.py](/engine/scripts/core/mainEngine.py) with the specific [RenderItem type](#renderitem-types), the desired layer to draw onto (you can setup the total layer count in [settings.py](/engine/scripts/core/settings.py)) and the appropriate [metadata](#renderitem-metadata) as follows:  
- **draw(** itemType:str, layer:int, metadata:dict **)** - note that this method doesn't immediately draw onto the screen, instead the item information is stored to be later asynchronously (when using multi-threaded rendering) drawn onto the screen.

### RenderItem metadata
The current fixed renderer uses specific arguments for every [type of RenderItem](#renderitem-types) called RI *metadata*. They range from object color to polygon point information and consist of key:value pairs (dicts) and are specified [below](#renderitem-types).

### RenderItem types
The renderer(s) currently support(s) a few basic render types:
- sprite
- rect
- line
- aaline
- circle
- smooth_circle (*NRS Nova only*)
- text
- triangle (*NRS Nova only*)
- poly
  
#### sprite
Used to render bitmap textures  
Metadata:
- "sprite" - sprite/texture in the pg.Surface type. Sprites loaded using [sprites_to_load.json](/engine/scripts/json/sprites_to_load.json) are stored in **self.sprites** in [mainEngine.py](/engine/scripts/core/mainEngine.py)
- "rect" - [pg.Rect](https://www.pygame.org/docs/ref/rect.html)-like shape to where the sprite will be rendered on screen (use to_scale and its variants for resolution independent positioning)
#### rect
Used to render rectangular shapes. The *width* and *radius* parameters can be used to render the shape only as a continuous edge and/or set the corner radius respectively  
Metadata:
- "rect" - [pg.Rect](https://www.pygame.org/docs/ref/rect.html)-like shape which the drawn rectangle will follow
- "color" - <red, green, blue> formatted tuple of color for the rectangle to be drawn with (*note*: some predefined colors are available in [colors.py](/engine/scripts/colors.py))
- "width" - edge width in pixels:int. If the edge width isn't provided or is 0, the shape will be filled
- "radius" - corner radius in pixels:int
#### line
Used to draw lines of set width specified by starting and ending points  
Metadata:
- "color" - <red, green, blue> formatted tuple of color for the line to be drawn with (*note*: some predefined colors are available in [colors.py](/engine/scripts/colors.py))
- "start" - <pixel, pixel> starting coordinate
- "end" - <pixel, pixel> ending coordinate
- "width" - width of the line in pixels:int
#### aaline
Used to draw single-pixel wide antialiased lines specified by starting and ending points  
Metadata:
- "color" - <red, green, blue> formatted tuple of color for the antialiased line to be drawn with (*note*: some predefined colors are available in [colors.py](/engine/scripts/colors.py))
- "start" - <pixel, pixel> starting coordinate
- "end" - <pixel, pixel> starting coordinate
- *note*: the antialiased line doesn't accept any width parameter, because it is exactly 1 pixel wide
#### circle
Used to draw filled or circumference-only circles  
Metadata:
- "color" - <red, green, blue> formatted tuple of color for the circle to be drawn with (*note*: some predefined colors are available in [colors.py](/engine/scripts/colors.py))
- "center" - <pixel, pixel> center coordinate
- "radius" - circle radius in pixels:int
- "width" - edge width in pixels:int. If the edge width isn't provided or is 0, the shape will be filled
#### smooth_circle
*(Only available when using NRS Nova)*  
Used to draw antialiased filled or circumference-only circles  
Metadata:
- "color" - <red, green, blue> formatted tuple of color for the circle to be drawn with (*note*: some predefined colors are available in [colors.py](/engine/scripts/colors.py))
- "center" - <pixel, pixel> center coordinate
- "radius" - circle radius in pixels:int
- "width" - edge width in pixels:int. If the edge width isn't provided or is 0, the shape will be filled
#### text
Used to draw texts using specified fonts. When no font is specified, an Arial font of size 30p will be used to render the text  
Metadata:
- "font" - [pg.font.Font](https://www.pygame.org/docs/ref/font.html#pygame.font.Font)-like
- "text" - plain text to be rendered : str
- "antialias" - <True | False> whether to antialas the text : bool
- "color" - <red, green, blue> formatted tuple of color for the text to be drawn with. When no color is specified, the text background will be drawn black (*note*: some predefined colors are available in [colors.py](/engine/scripts/colors.py))
- "bgcolor" - <red, green, blue> formatted tuple of color for the text background to be drawn with. A transparent background is used instead if the *no_bg* parameter is set to *True*
- "no_bg" - <True | False> when set to *True*, the text is rendered on a transparent background, else the background is black when no *bg_color* is specified
- "rect" - [pg.Rect](https://www.pygame.org/docs/ref/rect.html)-like shape which the text will be drawn onto (*note*: only the *x*, *y* coordinate is important, the *width* and *height* can be left as 0, 0 and the text will still be drawn)
#### triangle
*(Only available when using NRS Nova)*  
Used to draw triangles (*marginally cheaper than rendering triangles with poly*)  
Metadata:
- "points" - list of <pixel, pixel> coordinates that will make up the triangle
- "color" - <red, green, blue> formatted tuple of color for the polygon to be drawn with (*note*: some predefined colors are available in [colors.py](/engine/scripts/colors.py))
#### poly
Used to draw polygons  
Metadata:
- "color" - <red, green, blue> formatted tuple of color for the polygon to be drawn with (*note*: some predefined colors are available in [colors.py](/engine/scripts/colors.py))
- "points" - list of <pixel, pixel> coordinates, the space among which will be drawn. The last point will get connected back to the first one automatically
- "width" - edge width in pixels:int. If the edge width isn't provided or is 0, the shape will be filled

### Renderer types
Nebula currently supports three mostly compatible/interchangeable renderers (*note*: you can select which renderer to use in the [settings](/engine/scripts/core/settings.py) file. More information available [here](#engine-configuration)).
- The **default** (*legacy*) and the most compatible renderer uses the RenderItem->pygame pipeline
- The **second** (*experimental/legacy*) renderer is useful when you need to have a single shader cover the entire screen (e.g. bloom postprocessing). Unless you absolutely need to **don't use this renderer**, as it runs at a significantly reduced FPS than the default renderer and may experience some incompatibility with mobile/older devices. Under the hood it uses the default renderer to draw all RenderItems to an offscreen framebuffer, which is then used as a shader texture input
- The **third** (*experimental/in development*) renderer is the [*Nebula Render Service Nova*](/engine/scripts/renderer/renderer.py), which is a custom [OpenGL/ModernGL](https://moderngl.readthedocs.io/) based system with significantly increased performance and more features in comparison to the default pipeline. It also supports custom RenderObjects with full vertex/fragment shader customization.

## Sprites
### Loading sprites
### Using sprites

## Animations
### Loading animations
### Using animations

## Keybinds & Keygroups
Nebula doesn't use typical single-key keybinds, instead opting for _keygroups_. A keygroup is a group of one or more keys that all act as one _keybind_, which can be accessed through the [keybind service](/engine/scripts/core/keyHandler.py). Keygroups and their [keycodes🔗](https://www.pygame.org/docs/ref/key.html) have to be registered at game startup (or during runtime).

Keybind management functions accessible through the kebind service (self.keyhandler in [mainEngine.py](/engine/scripts/core/mainEngine.py) - *only for special purposes*):
- **get_keybind_pressed(** keybind:str **)** - returns a boolean depending on if the specified *registered* keygroup *keybind* is currently pressed / held (*note*: for detecting single-frame keygroup presses use *get_keybind_just_pressed()*)
- **get_keybind_just_pressed(** keybind:str **)** - returns True for one frame whenever a specified *registered* keygroup *keybind* is pressed.
- 

## File management
For image/animation loading see [Sprites](#sprites) or [Animations](#animations)

### Nebula files

### CSV files

### JSON files
Nebula provides an easy way of reading and writing json files using the [json loader](/engine/scripts/json_loader.py)  

Json functions available in [mainEngine.py](/engine/scripts/core/mainEngine.py):
- **write_to_file(** filepath:str, data:dict **)** - creates a file at _filepath_ if it doesn't exist already and writes the entire json-formatted _data_ dictionary into it. Note that this function **will overwrite** any existing data present in the _filepath_ file without a warning.
- **load_from_file(** filepath:str **)** - returns a dictionary with the json data read from _filepath_.
- **create_new_file(** filepath:str **)** - creates a new empty file at _filepath_; returns True when successful and False if a file already exists at _filepath_.

## Scenes
Nebula's [scene handler](/engine/scripts/core/scenes/scene_handler.py) provides a simple way to split your game into multiple [scenes](/engine/scripts/core/scenes/scene.py). Every scene has a built in _update_ and _render_ functions, which are called every frame by the engine at appropriate times when the scene is active, but custom functions and objects can be bound to scenes as well.  

Scene management functions available for [scene handler](/engine/scripts/core/scenes/scene_handler.py) (self.scene_handler in [mainEngine.py](/engine/scripts/core/mainEngine.py)):

- **addScene(** sceneToAdd:Scene **)** - registers the scene _sceneToAdd_ in the scene management service. Now it can be accessed by other functions of the scene manager. (_note_: scenes _can_ exist by themselves, but you're advised not to do so)
- **setActiveScene(** sceneName:str | None **)** - makes a _registered_ scene with the name _sceneName_ active, meaning its _update_ and _render_ functions will get called every frame. Setting the active scene to _None_ will make all scenes inactive, meaning only engine functions (e.g.  _update_ and _do_logic_) will be executed. Note activating a different scene **will not pause any Alarms** or change any non-scene-related behavior by default.
- **getActiveScene()** - returns the currently active Scene object. Useful for changing scene variables.
- **getActiveSceneName()** - returns the name of the currently active scene.
- **getScene(** sceneName:str **)** - returns a _registered_ scene of the name _sceneName_. Useful for changing scene variables.

## VUI

### WinVUI

## Alarms
The [alarm](/engine/scripts/alarm.py) service is meant to make frame-asynchronous function calls more accessible. Every alarm can be set to **repeat** indefinitely and also **paused / unpaused** every frame.
An alarm is an object that sets a timeout in seconds and gets assigned a function, which is called immediately when the set time runs out. Note that the alarm is **started upon creation**.

Alarm-related functions in [mainEngine.py](/engine/scripts/core/mainEngine.py):
- **add_alarm(** alarmName:string, alarmTime:int | float, timeoutFunction:function, repeatAlarm:boolean **)** - adds an alarm to the internal alarm service with a time of _alarmTime_ seconds, that is infinitely repeated when _repeatAlarm_ is set to True and calls the _timeoutFunction_ function when its set time runs out. You should always assign this function call to a variable if you plan on interacting (pause, unpause, remove) with the alarm again. (_note_: the alarm is **automatically started** upon creation)
- **remove_alarm(** alarmId:int **)** - removes an alarm of _alarmId_ from the internal service (_note_: alarms are removed the next frame, but you shouldn't run into issues when removing and adding alarms of the same name in the same frame, as they're managed by IDs)
- **pause_alarm(** alarmId:str **)** and **unpause_alarm(** alarmId:str **)** - used to pause and unpause alarms (for example when switching to another scene, where the alarm shouldn't be running).

## Reactions
The [reactions](/engine/scripts/core/reactions/) framework is meant to work in [Provider](/engine/scripts/core/reactions/reactionProvider.py)-[Listener](/engine/scripts/core/reactions/reactionListener.py) (1:n) pairs where whenever the provider gets triggered, all of its listeners get triggered too (for example whenever a scene is changed, a _sceneChange_ provider fires, signalling the change to all of its listeners)

Reaction-related functions in the [ReactionService](/engine/scripts/core/reactions/reactionService.py) (self.reactionService in [mainEngine.py](/engine/scripts/core/mainEngine.py)):
- **add_provider(** providerName:str, provider:[ReactionProvider](/engine/scripts/core/reactions/reactionProvider.py) **)** - registers a new provider to the reaction service with the name (index) of _providerName_. Note that the registered provider won't do anything by itself; you **have to** manually add the **trigger** to your desired action. (_note_: a few providers are built in, e.g. _frameUpdate_, _sceneChange_)
- **remove_provider(** providerName:str **)** - removes a _registered_ provider of name _providerName_ and all of its listeners from the reaction service and returns the provider in case you need to re-bind the listeners.
- **trigger_provider(** providerName:str **)** - triggers all listeners bound to a _registered_ provider of name _providerName_. This is a much better way than manually calling _self.providerService.get_provider(Provider).trigger()_
- **get_provider(** providerName:str **)** - returns a _registered_ provider of name _providerName_. Useful for binding listeners.

## Multiplayer

### Networking

### Server-side

### Client-side

## TileScripts

## Shaders

## Misc

### Cython

### Runtime log handler

### Raycaster