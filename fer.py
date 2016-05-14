#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  fichier fer.py
#  projet :  Wood workbench for FreeCAD
#  Copyright 2016 Mourad <contact@grognon.net>
#
""" 
	Fer is the french word for kinfe of spindle moulder
	Syntax: 
		knife = Fer(label, height, (x0, y0), [(x, y) | (a, x, y)], ...)
		label is a string, "F096" for example
		height : integer, the height of knife
		(x0, y0) : start point
		(x, y) : do a line from current point to (x, y)
		(a, x, y) make an arc frome the current point to (x, y)
			a is an angle ie the direction to start the arc
		...
	Usage:
		In FreeCAD 
			Menu : Macro > Macross ...
			Then browse to file fer.py
"""
from math import *
from FreeCAD import Base
import Part, PartGui
# Create a new document
doc = App.newDocument("F096")
# used in arcTo
def fv(x, y, z): return FreeCAD.Vector(x, y, z)

class Fer:
	# init 
	def __init__(self, label, h, *args):
		self.n = 0 # count of edges
		self.edges = [] # edges of the shape
		arg = args[0] # start point
		self.x, self.y = arg[0], arg[1] # current point of the drawing
		for arg in args[1:]:
			if len(arg) == 2: # line
				self.lineTo(*arg) 
			else: # arc
				self.arcTo(*arg)
		w = Part.Wire(self.edges) 
		face = Part.Face(w) 
		fer = face.extrude(fv(0, 0, h))
		fobj = doc.addObject("Part::Feature", label)
		fobj.Shape = fer

	# append self.edges
	def addEdge(self, e):
		self.n += 1
		name = "e" + str(self.n)
		self.edges.append(e)
	# make line		
	def lineTo(self, x, y):
		""" Draw a line from the current point to (x, y)
		update the current point """
		x0, y0  = self.x, self.y
		self.x, self.y = x, y
		e = Part.makeLine((x0, y0, 0), (x, y, 0))
		self.addEdge(e)
	# make arc
	def arcTo(self, alpha, x, y):
		""" a is the start angle of the arc from the current point
		(x, y) is the end point
		draw an arc from the current point to (x, y)
		update the current point
		"""
		a = radians(alpha)
		x0, y0 = self.x, self.y # start point
		self.x, self.y = x, y # update current start point
		p = x*x + y*y - x0*x0 - y0*y0
		q = x0*cos(a) + y0*sin(a)
		d = (x - x0)*sin(a) - (y - y0)*cos(a)
		X = (.5*sin(a)*p - (y-y0)*q) / d # center of arc
		Y = ((x-x0)*q -.5*cos(a)*p) / d
		r = hypot(X - x, Y - y)
		g = (y - y0)*cos(a) - (x - x0)*sin(a)
		a = degrees(copysign(acos((x0 - X)/r), y0 - Y))
		b = degrees(copysign(acos((x - X)/r), y - Y))
		if g > 0:
			e = Part.makeCircle(r, fv(X, Y, 0), fv(0, 0, 1), a, b)
		else: 
			e = Part.makeCircle(r, fv(X, Y, 0), fv(0, 0, 1), b, a)
		self.addEdge(e)
#----------------------------------------------------------end class Fer		
#exampleprogram 
if __name__ == '__main__':

	f = Fer("fer", 6, # name, height
		(20, 0), # start point
		(-8.5, 0), # line to (-8.5, 0)
		(-8.5, 3),
		(180, -15, 9.5), # arc to (-15, 9.5), start dir 180°
		(0, 9.5),
		(0, 14.5),
		(-6.5, 14.5),
		(-6.5, 22),
		(0, 0, 28.5), 
		(-15, 28.5),
		(-15, 33.5),
		(-8.5, 33.5),
		(-8.5, 40),
		(20, 40),
		(-70, 20, 0)
	)

	Gui.SendMsgToActiveView("ViewFit")
	Gui.activeDocument().activeView().setCameraType("Perspective")

