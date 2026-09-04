# Nebula Render Service Nova v0.0.1
# configs provided by nova_config.py

from array import array
import pygame as pg
import moderngl as mgl
import numpy as np

from scripts.renderer.nova_config import *
from scripts.core.settings import *
from scripts.renderItem import RenderItem
from scripts.renderer.dataTypes import NovaType as nt

import _thread
from threading import Lock

from scripts.renderer.renderObjects.untexturedColorRect import UntexturedColorRectRenderObject
from scripts.renderer.renderObjects.colorCircle import ColorCircleRenderObject
from scripts.renderer.renderObjects.smoothColorCircle import SmoothColorCircleRenderObject
from scripts.renderer.renderObjects.colorTriangle import ColorTriangleRenderObject

class NovaRenderer:
    def __init__(self, app, thread_lock:Lock):

        # initialization debug info
        print(f"\n{__name__}: NRS Nova v{NOVA_VERSION} for Nebula v{NGF_VERSION}")

        self.app = app

        self.lock = thread_lock
        self.window = app.window
        self.layers = self.app.render_layers

        self.to_render = []

        self.current_log = []

        # prepare modernGL prerequisities
        self.ctx = mgl.create_context()
        self.ctx.disable(mgl.CULL_FACE) # not needed for 2D either way
        self.ctx.enable(mgl.BLEND) # enables alpha

        # version debug info
        print(f"using ModernGL via OpenGL (version {self.ctx.info['GL_VERSION']})")

        # cpu-gpu memory init
        self.create_render_objects()

        # start the secondary render thread ## should be last to prevent random behavior
        #_thread.start_new_thread(self.render_thread)


    # RENDER OBJECTS
    def create_render_objects(self):
        # likely need a single-item texture rendering buffer, cause i don't know shis about 2D GPU rendering
        # but i can still have multiple untextured items rendered at once, cause GPU VMEM packing

        self.render_objects = {}

        self.register_render_object("rect", UntexturedColorRectRenderObject)
        self.register_render_object("circle", ColorCircleRenderObject)
        self.register_render_object("smooth_circle", SmoothColorCircleRenderObject)
        self.register_render_object("triangle", ColorTriangleRenderObject)

    def register_render_object(self, objectType:str, renderObjectClass):

        if self.render_objects.get(objectType) == None:
            try:
                self.render_objects[objectType] = renderObjectClass(self.app, self.ctx)

            except Exception as e:
                print(f"{__name__}: render object couldn't be registered ({e})")

        else:
            print(f"{__name__}: render object for '{objectType}' couldn't be registered; another render object had already been registered for this render item type")


    ## SHADERS
    def get_ctx(self):
        return self.ctx

    def surf_to_tex(self, surf):
        tex = self.ctx.texture(surf.get_size(), 4)
        tex.filter = (mgl.NEAREST, mgl.NEAREST)
        tex.swizzle = "BGRA"
        
        tex.write(surf.get_view("1"))

        return tex


    ## RENDERING
    def render_thread(self):
        self.clock = pg.time.Clock()
        self.dt = 0

        while self.app.is_running:
            if SYNC_UPS_FPS:
                self.dt = self.clock.tick(self.app.clock.get_fps()) / 1000
            else:
                self.dt = self.clock.tick(FPS_RENDER_LIMIT) / 1000

            with self.lock:
                self.app.to_render_full.append(RenderItem("text", self.app.LAYER_UI_TOP, {"no_bg":True, "color":(255, 0, 0), "rect":pg.Rect(10, 50, 0, 0), "text":"REN: "+str(round(self.clock.get_fps()))}))
        
            #with self.lock:
                if self.app.to_render_full != None and self.app.to_render_full != []:
                    self.to_render = self.app.to_render_full.copy()

            self.render(self.to_render)

    def split_render_data(self, to_render:list) -> dict[dict]:

        layer_data = {}

        # formatted as
        # layer_data = {
        #   0: {
        #       "rect": [<item>, <item>, <item>, ...],
        #       "sprite": [<item>, ...],
        #       ...
        #   },
        #   ...
        # }

        # split by render data
        for layer in range(self.app.render_layers):
            layer_data[layer] = {}

        for item in to_render:
            if layer_data[item.layer].get(item.item_type) == None:
                layer_data[item.layer][item.item_type] = []

            layer_data[item.layer][item.item_type].append(item)

        return layer_data



        # 84


    def render(self, to_render):

        # split render data
        layer_data = self.split_render_data(to_render)

        # clear fbo
        self.ctx.clear(0.0, 0.0, 0.0, 1.0)

        for layer, layer_items in layer_data.items():
            for item_type, items in layer_items.items():
                try:
                    match item_type:
                        case "sprite":
                            continue

                        case "rect":
                            self.render_objects["rect"].render(items)

                        case "line":
                            continue

                        case "aaline":
                            continue

                        case "circle":
                            self.render_objects["circle"].render(items)

                        case "smooth_circle":
                            self.render_objects["smooth_circle"].render(items)

                        case "text":
                            continue

                        case "triangle":
                            self.render_objects["triangle"].render(items)

                        case "poly":
                            continue

                        case _:
                            if item_type in self.render_objects.keys():
                                try:
                                    self.render_objects[item_type].render(items)
                                except Exception as e:
                                    self.current_log.append(
                                        f"{__name__}: couldn't render item of type {item_type}; check item parameters ({e})"
                                    )
                            else:
                                self.current_log.append(
                                    f"{__name__}: item type {item_type} is not recognized by NRS; check item parameters"
                                )

                except Exception as e:
                    self.current_log.append(
                        f"{__name__}: failed to render item of type {item_type}; check metadata parameters ({e})"
                    )

        with self.lock:
            pg.display.flip()

        """ for layer in range(self.layers): # goes through every layer; set number of layers at the top in "engine default variables - layers_current"
            for item in local_to_render: # sprite, rect, line, aaline, circle, text
                if item.layer == layer: # checks if current item is at the set layer, else skips it
                    #try:
                        match item.item_type:
                            case "sprite":
                                continue
                                self.window_drawing.blit(item.metadata["sprite"], item.metadata["rect"])
                            case "rect":
                                self.render_objects["rect"].add_to_render([item])
                                self.render_objects["rect"].render()

                                continue
                            case "line":
                                continue
                                pg.draw.line(self.window_drawing, item.metadata["color"], item.metadata["start"], item.metadata["end"], item.metadata["width"])
                            case "aaline":
                                continue
                                pg.draw.aaline(self.window_drawing, item.metadata["color"], item.metadata["start"], item.metadata["end"])
                            case "circle":
                                continue
                                pg.draw.circle(self.window_drawing, item.metadata["color"], item.metadata["center"], item.metadata["radius"], item.metadata["width"])
                            case "text":
                                continue
                                if "no_bg" in item.metadata: self.window_drawing.blit(item.metadata["font"].render(item.metadata["text"], item.metadata["antialias"], item.metadata["color"]), item.metadata["rect"])
                                else: self.window_drawing.blit(item.metadata["font"].render(item.metadata["text"], item.metadata["antialias"], item.metadata["color"], item.metadata["bgcolor"]), item.metadata["rect"])
                            case "poly":
                                continue
                                pg.draw.polygon(self.window_drawing, item.metadata["color"], item.metadata["points"], item.metadata["width"])
                    #except:
                    #    self.current_log.append(f"{__name__}: Item '{item.item_type}' in layer {item.layer} couldn't be rendered; check metadata parameters")

        with self.lock:
            pg.display.flip() """
    
    def render_get_log(self):
        with self.lock:
            send_log = self.current_log.copy()
            self.current_log.clear()
        return send_log