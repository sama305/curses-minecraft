# curses-minecraft
Senior Project 2021

# Description:

This program showcases perlin noise being used to generate a procedural world with working structure generation, chunk generation/rendering, and the ability to modify the world.

# How to play

## Setup:
To use this application, you must `pip install perlin-noise` and if you are using a windows device, you must `pip install windows-curses`. Please note that on windows you may need to configure your environment variables, adjust the run.bat, or even install python before (if not already installed). If all else fails simply `py main.py` in the command line.

## Controls:

You can move left and right using the arrow keys, and perform actions using the WASD keys. To do actions diagonally, you can use QEZX. By default, you will be in dig mode, but you can press 2 to switch to build mode.

# Project Layout

## What's already in

* Procedural generation
* 16x256 chunks able to be generated, saved, loaded, and rendered
* The ability to destroy tiles
* Walking across tiles
* Simple falling
* Simple structures (still buggy)

## What's planned

* Add block placing/picking (try to use window/pad)
* Add more structures
* Add cave generation
* Add special case blocks (ladders as an example)
* ^ will require changing collision code to make collision a "tag"

## Immediate Problems/Bugs

* Shorten tile placement code (prob new function)
* Make chunk its own .py file
* Fix structures generating across chunks
* Reduce overuse of 'chunk_list'
* Make all chunk functions in the actual chunk class
