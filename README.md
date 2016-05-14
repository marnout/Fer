# Fer
Modeling a Knife for spindle moulder using FreeCAD

This is the first step for a wood workbench for FreeCAD
fer.py define a class Fer (knife for spindle moulder in french)

## Syntax: 
	knife = Fer(label, height, (x0, y0), [(x, y) | (a, x, y)], ...)
	label is a string, "F096" for example
	height : integer, the height of knife
	(x0, y0) : start point
	(x, y) : do a line from current point to (x, y)
	(a, x, y) make an arc frome the current point to (x, y)
		a is an angle ie the direction to start the arc
	...

## Usage:
	In FreeCAD 
		Menu : Macro > Macross ...
		Then browse to file fer.py

This class can also usefull to create a shape using lines and arcs and then extrude this face

Please take a look at www.grognon.net (in french only)

https://github.com/marnout/Fer
