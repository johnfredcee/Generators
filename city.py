#!/usr/bin/env python

import pyglet
from pyglet.gl import *
from geom import vec3
import math
import random
from sets import Set
from geom import *
from connection import Connection

class City(object):
    def __init__(self, gridx, gridy):
        self.gridx = gridx
        self.gridy = gridy
        self.end_points = []
        self.point_connection_count = []
        self.connections = Set()
        return
           
    def generate_end_points(self, peturbation):
        """ Generate the end points of each line in the network"""
        self.end_points = []
        max_dist = math.sqrt(self.gridx * self.gridx + self.gridy * self.gridy)
        for x in range(-self.gridx,self.gridx):
            for y in range(-self.gridy, self.gridy):
                distance = math.sqrt(x * x + y * y) / max_dist
                if (random.gauss(0.0,1.0) > distance):
                    x_peturbation = random.random() * peturbation
                    y_peturbation = random.random() * peturbation
                    self.end_points.append(vec3((x + x_peturbation) / self.gridx, (y + y_peturbation) / self.gridy, 1.0))
        return
   


    def build_lines(self):
        """ Build a set of connections of close points """
        points_todo = range(0, len(self.end_points))
        points_done = []
        done = [ False ] * len(self.end_points)
        ic = points_todo[ len(points_todo) / 2 ] # start in the middle
        while points_todo:
            c = self.end_points[ic]
            # find closest point
            i = 0
            ix = -1
            min_distance = 10000.0
            # print "Point ", ic
            for cn in self.end_points:
                delta = c - cn
                if ((delta.x == 0) and (delta.y == 0) and (delta.z == 0)):
                    i = i + 1
                    continue
                if (done[i]):
                    i = i + 1
                    continue
                dist = delta.length()
                #print "dist ", dist
                #print "mindist ", min_distance
                if (dist < min_distance):
                    min_distance = dist
                    ix = i
                    #print "!!", ix
                i = i + 1    
            #print ic, ix            
            if (ix != -1):
                self.connections.add(Connection(ic,ix))
            done[ic] = True
            points_done.append(ic)
            points_todo.remove(ic)
            #done[ix] = True
            ic = ix
            if (ic == -1) and (points_todo):
                ic = points_todo[0]            
        return

    def horizontal_sweep(self):
        """ Build a set of connnections of horizontally close points """
        self.hclosest = []
        ic = 0
        for c in self.end_points:
            # find closest point to the right
            i = 0
            ix = -1
            min_distance = 10000.0
            for cn in self.end_points:
                delta = c - cn
                if ((delta.x == 0) and (delta.y == 0) and (delta.z == 0)):
                    i = i + 1
                    continue
                if (cn.x < c.x):
                    i = i + 1
                    continue
                dist = (cn - c).length()
                if (dist < min_distance):
                    min_distance = dist
                    ix = i
                i = i + 1
            #print ic, ix            
            if (ix != -1):
                self.connections.add(Connection(ic, ix))
            ic = ic + 1
        return

    def vertical_sweep(self):
        """ Build a set of connections of vertically close points """
        self.vclosest = []
        ic = 0
        for c in self.end_points:
            # find closest point to the right
            i = 0
            ix = -1
            min_distance = 10000.0
            for cn in self.end_points:
                delta = c - cn
                if ((delta.x == 0) and (delta.y == 0) and (delta.z == 0)):
                    i = i + 1
                    continue
                if (cn.y < c.y):
                    i = i + 1
                    continue
                dist = (cn - c).length()
                if (dist < min_distance):
                    min_distance = dist
                    ix = i
                i = i + 1
            #print ic, ix            
            if (ix != -1):
                self.connections.add(Connection(ic,ix))
            ic = ic + 1
        return

                            
  
    def connection_count(self, ix):
        result = 0
        for c in self.connections:
            if ix in c:
                result = result + 1
        return result

    def count_connections(self):
        i = 0
        for i in range(0, len(self.end_points)):
            self.point_connection_count.append(self.connection_count(i))
            
    def build_display_list(self):
        """ Build a displayable list of OpenGL Primitives """
        glPointSize(4)
        glEnable(GL_POINT_SMOOTH)
        self.vertices = []
        for v in self.end_points:
            self.vertices.append( v.x )
            self.vertices.append( v.y )
        self.lines = []
        for c in  self.connections:
            self.lines.append( self.end_points[c[0]].x )
            self.lines.append( self.end_points[c[0]].y )
            self.lines.append( self.end_points[c[1]].x )
            self.lines.append( self.end_points[c[1]].y )

        self.box = []
        self.box.append( self.topleft.x )
        self.box.append( self.topleft.y  )
        self.box.append( self.topleft.x )
        self.box.append( self.bottomright.y  )
        self.box.append( self.bottomright.x )
        self.box.append( self.bottomright.y )
        self.box.append( self.bottomright.x )
        self.box.append( self.topleft.y )
        

    def build_bounding_box(self):
        self.topleft = vec3(0.0,0.0,0.0)
        self.bottomright = vec3(0.0,0.0,0.0)
        for c in self.end_points:
            if (c.x < self.topleft.x):
                self.topleft.x = c.x
            if (c.y < self.topleft.y):
                self.topleft.y  = c.y
            if (c.x > self.bottomright.x):
                self.bottomright.x = c.x
            if (c.y > self.bottomright.y):
                self.bottomright.y  = c.y
                
            
    def draw(self):
        """ Actually draw the results """
        glColor3f(0.0,0.0,1.0)
        pyglet.graphics.draw( len(self.vertices) / 2, pyglet.gl.GL_POINTS, ('v2f', self.vertices ))
        glColor3f(0.0,1.0,0.0)
        pyglet.graphics.draw( len(self.lines) / 2, pyglet.gl.GL_LINES, ('v2f', self.lines ))
        glColor3f(0.0,0.0,0.0)
        pyglet.graphics.draw( len(self.box) / 2, pyglet.gl.GL_LINE_LOOP, ('v2f', self.box ))
