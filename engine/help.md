## NOTICE
This is an **not** a full documentation yet, so expect mistakes and **missing** or frequently **changing** paragraphs

# Table of contents
- [Table of contents](#table-of-contents)
- [Engine code structure](#engine-code-structure)
  - [Imports](#imports)
  - [Built-in functions](#built-in-functions)
  - [Custom classes](#custom-classes)
- [Engine file structure](#engine-file-structure)
- [Engine features \& services](#engine-features--services)
  - [Rendering](#rendering)
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

## Custom classes
As written in the [file structure](#engine-file-structure), all game-related files should be placed in the [game scripts folder](/engine/game/scripts/) (read about importing [here](#imports)). Note there isn't any specific file naming convention

# Engine file structure
The engine is split into two main folders - [scripts](/engine/scripts/) and [game](/engine/game/).  
The _scripts_ folder contains all of Nebula's code, including all [core](/engine/scripts/core/) elements, [mainEngine.py](/engine/scripts/core/mainEngine.py) and all custom libraries (e.g. [keyHandler.py](/engine/scripts/core/keyHandler.py), [mplib](/engine/scripts/mplib/)). You are heavily advised not to touch any custom library files except mainEngine.py, cython [setup.py](/engine/scripts/cython/setup.py) and (somewhat deprecated) [test.py](/engine/scripts/test.py), as it's a script name reserved for testing custom engine modifications / deep game functionality.  
The _game_ folder is meant as a root folder for all game-related [scripts](/engine/game/scripts/), [assets](/engine/game/assets/) etc.

# Engine features & services

## Rendering
For shader support see [Shaders](#shaders)

## Sprites
### Loading sprites
### Using sprites

## Animations
### Loading animations
### Using animations

## Keybinds & Keygroups
Nebula doesn't use typical single-key keybinds, instead opting for _keygroups_. A keygroup is a group of one or more keys that all act as one _keybind_, which can be accessed through the [keybind service](/engine/scripts/core/keyHandler.py). Keygroups and their [keycodes🔗](https://www.pygame.org/docs/ref/key.html) have to be registered at game startup (or during runtime)

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