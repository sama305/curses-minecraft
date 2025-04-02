# curses-minecraft v0.11

![Cover image](/images/cover_image.png)

<details>
<summary>Changelog</summary>
<br />

`release/v0.11`
* HUD properly displays button to quit and save
* bedrock can no longer be mined
* removed many unused files/imports
* if `/save_data` doesn't exist, it is created

`release/v0.10`
* added `requirements.txt`
* fixed `run.sh` to actually work
* removed tons of unneeded or accidentally added files
* fixed `save_data` loading from root
* removed worlds included with repo
* removed horrible jitter
* increased chunk render/gen distance

I apparantly forgot to document any changes I made pre-`release/v0.10`. How I got to `v0.9` is beyond me, but from this point on I'll document any changes I make.

</details>

# Note from 2025

Hi, if you've found this repo, this is my 2021 High School Senior Project for the CS AP Test. In a lot of ways, it isn't too pretty. But it also has some great programming and I think it's quite a good showcase of perlin noise. I have kept it mostly in its original form, but updated a few bugs like `run.sh` not workijng and a horrible flicker. I also added some HUD elements to make the controls more clear. Besides that, however, this is the same as it was years ago. So I hope you enjoy this experimental, buggy, but really creative project I'm still proud of to this day.

# Original description

This was my Senior Project for the Computer Science AP Test in 2021. This program showcases perlin noise being used to generate a procedural world with working structure generation, chunk generation/rendering, and the ability to modify the world.

# How to play

## Setup
Python 3 is required. Run the following commands **from root** to create/activate a virtual environment and install the only external dependency, [perlin-noise](https://pypi.org/project/perlin-noise/):
```bash
python3 -m venv .venv
.venv/bin/activate
pip3 install -r requirements.txt
```

## Starting the game
To start the program, simply execute `./run.sh`, and the start menu will open (if this file doesn't have execute permissions, just `chmod u+x run.sh` it). If this is your first time running the game, just press <kbd>Enter</kbd> and a world will be created. If you have a saved world, use <kbd>↑</kbd>/<kbd>↓</kbd> to select a world and then press <kbd>Enter</kbd> to start.

## Controls
You can move your character with <kbd>↑</kbd>, <kbd>↓</kbd>, <kbd>←</kbd>, <kbd>→</kbd>
NOTE: some surfaces are climbable/swimable (tree trunks and water for example)

You can place tiles in any direction using <kbd>w</kbd>, <kbd>e</kbd>, <kbd>d</kbd>, <kbd>c</kbd>, <kbd>x</kbd>, <kbd>z</kbd>, <kbd>a</kbd>, <kbd>q</kbd>. This layout runs clockwise starting from North.
NOTE: for background tiles, you can press <kbd>s</kbd> to place it where your character is standing.

To switch which tile you have selected, use <kbd>1</kbd> and <kbd>2</kbd> to move the selection left and right respectively.

To delete blocks, place the air (or empty) block. Hint: you can press <kbd>3</kbd> to return to the item at index 0, which is air.

To hide the HUD, press <kbd>h</kbd>.

To manually save the game (it's saved upon quitting), press <kbd>S</kbd> (capital).

Finally, to quit the game, press <kbd>Q</kbd> (also capital).

![Treehouse](/images/treehouse.png)

<details>
<summary>Old, outdated roadmap from 2021 (kept for historical reasons)</summary>

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

</details>

# Have fun!
![Ocean man](/images/ocean.png)
