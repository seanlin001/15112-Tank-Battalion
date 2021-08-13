CMU 15-112 Summer 2021 Term Project: Tank Battalion

Description: Tank Battalion is a 2d tank shooter game that can be played endlessly.
Inspired by the 80s arcade game Battle City, the player controls a golden tank and
defends the base at the bottom from 20 enemy tanks that gradually spawn at the top. If the
base is shot or the player runs out of all 3 lives, the game is over. Difficulty
increases as enemies move faster and shoot more frequently as stages progress. The game's 
wall generation process utilizes an iterative Depth First Search algorithm
to ensure that the map does not close off any spaces with indestructable walls by
making sure that all empty spaces and destructable walls are connected with each other.

To run the game, simply open TankBattalion.exe (For Windows users). 

The other way to run the game is by running TankBattalion.py. In addition to the Python
Standard Library, please install the following
libraries: cmu_112_graphics, pygame, PIL

Shortcut command: Press L to advance to the next stage. (Demonstrates wall generation
and enemy difficulty progression)