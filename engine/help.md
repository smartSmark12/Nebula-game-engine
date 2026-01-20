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
The file starts with imports - first generic ones (e.g. pygame, sys, moderngl), then engine-related ones (e.g. ThreadedGameRenderer, flatpane) and lastly game-related imports (_note_: now cython imports should go after game-related ones)

## Built-in functions
Specific service functions ([alarms](#alarms), [render](#rendering), [keybinds](#keybinds--keygroups)) won't be discussed here, locate the appropriate topic for help with those
- **engine_on_init()** - starts up the engine itself, actions include preparing the game window, pygame clock and all internal handlers and services (_note_: you should **not** make any changes to this function, unless you're modifying an engine service)
- **game_on_init()** - by default empty - runs after engine_on_init() and should contain all your startup / game preparation code (global variables, service binding, sprite rescaling, etc.)
- **handle_events()** - an internal function used for game exit detection and keyHandler updates. If you need to detect a specific event that _isn't already handled_ by an internal service, then this is the place to do it efficiently
- **update()** - an internal function used to move time, update the mouse information and handle service updates. If you found this function and want to write code that should run every frame, then go to **do_logic()** instead, as this function is _engine critical_
- **do_logic()** - runs every frame and is meant to house your **game-related logic** (moving players, handling keybind presses, changing scenes, etc.)
- **run()** - a post-startup function housing loop the main update loop. (_note_: you **shouldn't** write any startup code here, **game_on_init()** is here for that reason - should only be used for specific game exit cleanup)
- **runGame()** - the engine entry point - do not write any code here
- **load_sounds()** - as Nebula doesn't currently have a unified sound management service, this is where you should load your music and sound effects (_note_: the function is **not called by default** - ideally call it in game_on_init())

## Custom classes
As written in the [file structure](#engine-file-structure), all game-related files should be placed in the [game scripts folder](/engine/game/scripts/) (read about importing [here](#imports)). Note there isn't any specific file naming convention

# Engine file structure
The engine is split into two main folders - [scripts](/engine/scripts/) and [game](/engine/game/).  
The scripts folder contains all of Nebula's code, including all [core](/engine/scripts/core/) elements, [mainEngine.py](/engine/scripts/core/mainEngine.py) and all custom libraries (e.g. [keyHandler.py](/engine/scripts/core/keyHandler.py), [mplib](/engine/scripts/mplib/)). It is heavily advised to not touch any custom library files except mainEngine.py, cython [setup.py](/engine/scripts/cython/setup.py) and (somewhat deprecated) [test.py](/engine/scripts/test.py), as it's a script name reserved for testing custom engine modifications / deep game functionality.  
The game folder is meant as a root folder for all game-related [assets](/engine/game/assets/), [scripts](/engine/game/scripts/) etc.

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

## File management
For image/animation loading see [Sprites](#sprites) or [Animations](#animations)

### Nebula files

### CSV files

### JSON files

## Scenes

## VUI

### WinVUI

## Alarms
The [alarm](/engine/scripts/alarm.py) service is meant to make frame-asynchronous function calls more accessible. Every alarm can be set to **repeat** indefinitely and also **paused / unpaused** every frame.
An alarm is an object that sets a timeout in seconds and gets assigned a function, which is called immediately when the set time runs out. Note the alarm is **started upon creation**.

Alarm-related functions in [mainEngine.py](/engine/scripts/core/mainEngine.py):
- **add_alarm(** alarmName:string, alarmTime:int | float, timeoutFunction:function, repeatAlarm:boolean **)** - adds an alarm with to the internal alarm service with a time of _alarmTime_ seconds, that is infinitely repeated when _repeatAlarm_ is set to True and calls the _timeoutFunction_ function when its set time runs out. You should always assign this function call to variable if you plan on interacting (pause, unpause, remove) with the alarm again. (_note_: the alarm is **automatically started** upon creation)
- **remove_alarm(** alarmId:int **)** - removes an alarm of _alarmId_ from the internal service (_note_: alarms are removed the next frame, but you shouldn't run into issues when removing and adding alarms of the same name in the same frame, as they're managed by IDs)
- **pause_alarm(** alarmId:str **)** and **unpause_alarm(** alarmId:str **)** - used to pause and unpause alarms (for example when switching to another scene, where the alarm shouldn't be running).

## Reactions
The [reactions](/engine/scripts/core/reactions/) framework is meant to work in [Provider](/engine/scripts/core/reactions/reactionProvider.py)-[Listener](/engine/scripts/core/reactions/reactionListener.py) (1:n) pairs where whenever the provider gets triggered, all of its listeners get triggered too (for example whenever a scene is changed, a _sceneChange_ provider fires, signalling the change to all of its listeners)

Reaction-related functions in the [ReactionService](/engine/scripts/core/reactions/reactionService.py) (self.reactionService in [mainEngine.py](/engine/scripts/core/mainEngine.py)):
- **add_provider(** providerName:str, provider:[ReactionProvider](/engine/scripts/core/reactions/reactionProvider.py) **)** - registers a new provider to the reaction service with the name (index) of _providerName_. Note the registered provider won't do anything by itself, you **have to** manually add the **trigger** to your desired action. (_note_: a few providers are built in, e.g. _frameUpdate_, _sceneChange_)
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