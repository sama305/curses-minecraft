# curses-minecraft v0.9

![Cover image](/images/cover_image.png)
Senior Project 2021

# Description:

This program showcases perlin noise being used to generate a procedural world with working structure generation, chunk generation/rendering, and the ability to modify the world.

# How to play

## Setup:
If you are using a windows device, you must `pip install windows-curses`. Please note that on windows you may need to configure your environment variables, adjust the run.bat, or even install python before (if not already installed).

## Creating a world:
Upon starting the program, you will be greeted by a menu. You can either load a previous world here or create one from scratch.
NOTE: to delete/rename any files you will need to go into the 'save_data' folder. You must also change the .json atribute at the bottom of the file for the name change to take effect.

## Controls:
You can move your character with arrow keys `↑, ↓, ←, →`
NOTE: some surfaces are climbable/swimable (tree trunks and water for example)

You can add tiles in any direction using `w, e, d, c, x, z, a, q`. This layout is clockwise starting from North.
NOTE: for tiles you can walk through, you can press `s` to place it where your character is standing

To switch which tile you have selected, use `1` and `2` (`1` for backwards, `2` for forwards). You can press `3` to return to air.

The way to delete blocks is to place an air block (ID:0)

To hide the hude, press `h`

To manually save the game (it's saved upon quitting), press `S` (capital)

Finally, to quit the game, press `Q` (also capital)

# Project Layout

## What's already in

* Procedural generation, all the way from the surface to the depths below
* Chunk and region generation, with set sizes for both
* Character movement
* The ability to change the terrain
* Saving/Loading as well as a main menu
* Height dependent generation (snow, water level, etc.)
* Functionally different blocks
* Selecting tiles
* Dynamic structures (seaweed)

## What's planned

* Add more structures
* Possibly add NPC's
* ^ would require making updates not dependent on input
* Deleting, renaming worlds and quitting the game in the main menu

## Immediate Problems/Bugs

* Negative chunks don't generate right
* Boilerplate
* Structures generating incorrectly when crossing chunk borders
* Crashing when reaching world height or world depth
* Chunk generating can sometimes cause poor performance
* Inconvenient block picking
* Crashing when resizing window sometimes
* Some layers are a bit boring
