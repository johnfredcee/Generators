#!/usr/bin/env python

import pyglet
from pyglet.gl import *
from city import City

config = Config(sample_buffers=1, samples=4,
                depth_size=16, double_buffer=True,)
window = pyglet.window.Window(resizable=True, config=config)

        
  
def update(dt):
        #print dt
        return

pyglet.clock.schedule(update)   
   
def setup():
    # One-time GL setup
    glClearColor(1, 1, 1, 1)
    glColor3f(1, 0, 0)
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_CULL_FACE)

    # Uncomment this line for a wireframe view
    #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    # Simple light setup.  On Windows GL_LIGHT0 is enabled by default,
    # but this is not the case on Linux or Mac, so remember to always
    # include it.
    glDisable(GL_LIGHTING)
    #glEnable(GL_LIGHT0)
    #glEnable(GL_LIGHT1)



@window.event
def on_resize(width, height):
    # Override the default on_resize handler to create a 3D projection
    # print width, height
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glViewport(0, 0, width, height)
    return pyglet.event.EVENT_HANDLED

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)
    glClearColor(1,1,1,1)
    glColor3f(1.0,0.0,0.0)
    city.draw()
   
city = City(8,8)
city.generate_end_points(0.65)
city.build_lines()
city.horizontal_sweep()
city.vertical_sweep()
city.count_connections()
city.build_bounding_box()
city.build_display_list()


#print centre_points
pyglet.app.run()
