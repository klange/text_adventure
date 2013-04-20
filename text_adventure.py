#!/usr/bin/env python
"""
	An awesome text adventure.
"""
import json
import sys

save_file = 'world.json'
if len(sys.argv) > 1:
	save_file = sys.argv[1]
with open(save_file) as f:
	global world
	world = json.loads(f.read())

current_room   = world['current_room']
current_health = world['current_health']
inventory      = world['inventory']

def go(direction):
	global current_room, inventory
	if direction in world['rooms'][current_room]['exits']:
		if world['rooms'][current_room]['exits'][direction]['locked'] and not world['rooms'][current_room]['exits'][direction]['key'] in inventory:
				print "This door is locked and you don't have the right key!"
		else:
			world['rooms'][current_room]['exits'][direction]['locked'] = 0
			current_room = world['rooms'][current_room]['exits'][direction]['target']
	else:
		print "I'm afraid you can't go that way from here."

def take(item):
	global current_room, inventory
	room = world['rooms'][current_room]
	if item in room['contents']:
		room['contents'].remove(item)
		inventory.append(item)
		print "Picked up one", item
	else:
		print "There is no", item, "here."

def drop(item):
	global current_room, inventory
	room = world['rooms'][current_room]
	if item in inventory:
		inventory.remove(item)
		room['contents'].append(item)
		print "Dropped", item
	else:
		print "You don't have a", item

while 1:
	print "You are in", world['rooms'][current_room]['description']
	if world['rooms'][current_room]['exits']:
		print "Exits are", " ".join(world['rooms'][current_room]['exits'].keys())
	else:
		print "There appears to be no way out of here."
	for item in world['rooms'][current_room]['contents']:
		print "There is a", item, "here."
	for monster in world['rooms'][current_room]['monsters'].keys():
		print "Watch out, there is a", monster, "here!"
	print ""

	command = raw_input("What do you want to do? ")
	commands = command.split(" ")

	if len(commands) < 1: # len means "length" and can be done for... lots of things.
		continue

	if commands[0] == 'go':
		if len(commands) < 2:
			print "Go where?"
		else:
			go(commands[1])
	elif commands[0] == 'inventory':
		if len(inventory) == 0:
			print "Your inventory is empty."
		else:
			print "Your inventory contains:"
			for item in inventory:
				print "-", item # - item
	elif commands[0] == 'take':
		if len(commands) < 2:
			print "Take what?"
		else:
			take( " ".join(commands[1:]) )
	elif commands[0] == 'drop':
		if len(commands) < 2:
			print "Drop what?"
		else:
			drop( " ".join(commands[1:]) )
	elif commands[0] == "save":
		if len(commands) < 2:
			print "Where should I save?"
		else:
			world['current_room']   = current_room
			world['current_health'] = current_health
			world['inventory']      = inventory
			save_name = commands[1:]
			with open(save_name, 'w') as f:
				f.write(json.dumps(world))
	else:
		print "I don't know how to do that."

	for name, monster in world['rooms'][current_room]['monsters'].items():
		print "The", name, "goes", monster['says']
		if monster['power']:
			print "... and does", monster['power'], "damage!"


