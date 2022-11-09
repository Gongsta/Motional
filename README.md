# Motional: HackTheValley-7
Motional is a hackathon-winning project that was developed on at [HackTheValley](https://devpost.com/software/motional) for the "Best Gaming Related Hack". Using state-of-the-art machine learning models, Motional can detect over 500 features on the human body (468 facial features, 21 hand features, and 33 body features) and use these features as control inputs to any video game using PyAutoGUI. Our Devpost page can be found [here](https://devpost.com/software/motional).

Click the image below to see a live demo of the product. 
[![IMAGE ALT TEXT](http://img.youtube.com/vi/9Zgh0sf959I/0.jpg)](https://www.youtube.com/watch?v=9Zgh0sf959I "Motional")

Motional operates in 3 modes: using hand gestures, face gestures, or full-body gestures. We ship certain games out-of-the-box such as Flappy Bird and Snake, with predefined gesture-to-key mappings, so you can play the game directly with the click of a button. For many of these games, jumping in real-life (body gesture) /opening the mouth (face gesture) will be mapped to pressing the "space-bar"/"up" button.

However, the true power of Motional comes with customization. Every simple possible pose can be trained and clustered to provide a custom command. Motional will also play a role in creating a more inclusive gaming space for people with accessibility needs, who might not physically be able to operate a keyboard dexterously.

Icons used are from [Material Design by Google](https://fonts.google.com/icons).

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
