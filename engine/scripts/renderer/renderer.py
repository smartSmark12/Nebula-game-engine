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

class NovaRenderer:
    def __init__(self, app, thread_lock:Lock):
        self.app = app

        self.lock = thread_lock
        self.window = app.window
        self.layers = self.app.render_layers

        self.to_render = []

        self.current_log = []

        # prepare modernGL prerequisities
        self.ctx = mgl.create_context()

        #self.ctx.screen

        self.shaders = {}
        self.vaos = {}

        # cpu-gpu memory init
        self.create_render_objects()

        # start the secondary render thread ## should be last to prevent random behavior
        #_thread.start_new_thread(self.render_thread)


    # BUFFERS
    def create_render_objects(self):
        # likely need a single-item texture rendering buffer, cause i don't know shis about 2D GPU rendering
        # but i can still have multiple untextured items rendered at once, cause GPU VMEM packing

        self.render_objects = {}

        self.render_objects["rect"] = UntexturedColorRectRenderObject(self.app, self.ctx)


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

    def render(self, to_render):
        local_to_render = sorted(to_render.copy(), key=lambda item: item.item_type)

        self.ctx.clear(0.0, 0.22, 0.3, 1.0)

        for layer in range(self.layers): # goes through every layer; set number of layers at the top in "engine default variables - layers_current"
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
            pg.display.flip()
    
    def render_get_log(self):
        with self.lock:
            send_log = self.current_log.copy()
            self.current_log.clear()
        return send_log