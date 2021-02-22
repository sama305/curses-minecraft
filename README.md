# curses-minecraft
Senior Project 2021

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
* 

## Immediate Problems/Bugs

* Shorten tile placement code (prob new function)
* Make chunk its own .py file
* Fix structures generating across chunks
* Reduce overuse of 'chunk_list'
* Make all chunk functions in the actual chunk class
