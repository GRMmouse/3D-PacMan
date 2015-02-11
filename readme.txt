To play the game, simply run main.py. Make sure that math.py
and dkosbie.gif are under the same directory for the game to 
run properly.

My project is a first-peron-view 3D pac man. It uses Tkinter
 as its only graphic module. 

To achieve the 3D effects, I have written the
math.py program to support vector and matrix calculation,
using geometry to calculate the coordinates on which
the points should be projected and draw them in Tkinter.

Use A,S,D,W for movements and Q,E or the mouse for rotations.
Press P for Pause and R for Restart.
An animated tutorial is included in the game.

The rules and AIs are similar to the original pac man. The 
four ghosts have independent logic: The red one is always 
chasing pac man. The pink and blue ghosts try to cut the
pac man off in the front and the back. The orange one
randomly decides to follow pac man or move in a random
direction.

Collect all the pellets to finish the game.
