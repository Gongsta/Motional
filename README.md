# HackTheValley-7
For this project, whenever we want to capture a new hand pose, this is the process: (NOT NEEDED, relative distance is enough)
1. Capture a sequence of 50 landmarks (5 seconds, the capture happens around 10FPS) with the label true of the pose 
	- There should be a countdown for this from a GUI perspective (NOT NEEDED)
2. Train a Neural Network to learn these landmarks in the background, and
display a loading bar
3. 

Layout:
- Right side for our own gui, left side for playing the game.


Pitch:
- The mouth playing is also a way to gamify practice. Certain people with disabilities need to practice exercising certain muscles such as their mouths. So this is a really good way to get people to practice.

Icons used are from [Material Design by Google](https://fonts.google.com/icons).

TODO:
- Add jumping with pose
- Add crouching, because that didn't work super well

Ideas:
- Store Configuration for gesture -> control mapping
	- Display gesture -> control mapping in case people forget what configuration they had
- Add finger gesture recognition, so detecting sequences of motion (this is HARD, but super interesting!)
- Add up to 4 person multiplayer, by splitting the camera feed into 4 quadrants

### Getting Started
These instructions are Macbook specific.

```bash
pip3 install virtualenv # install virtualenv if you haven't already

virtualenv env # Start a virtual environment
source env/bin/activate # Activate a virtual environment
pip install -r requirements.txt

```

You might also need to install additional packages, such as Tkinter.
```bash
brew install python-tk

```
