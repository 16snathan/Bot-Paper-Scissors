Bot Paper Scissors
Shiva Nathan
15-112 Andersen
4 May 2017

A combination Python and C program that enables a computer to use its camera to play rock-paper-scissors against a human being. Using OpenCV, the computer is able to recognize what move a human makes and then control a prosthetic hand to play against them. On Easy mode, it randomly chooses a hand. On Impossible, it determines what hand its opponent will make using the camera and plays the winning hand. Occasionally it might get cheeky!

Incorporates code written by Zane Lee for finger detection.
https://github.com/lzane/Fingers-Detection-using-OpenCV-and-Python/blob/master/new.py
Original code by Zane Lee in fingertest3.py


Python 2.7.13
OpenCV 2.4.8

Does not need any further installation; the OpenCV dependency files are included in the folder.

If you have your own Arduino-controlled prosthetic hand, upload the script "arduino_python_comms.ino" to the hand. Then enter the command-line, navigate to the TPFinal folder, and run ‘python BPS.py’.

If you don’t have your very own prosthetic hand, simply enter the command-line, navigate to the TPFinal folder, and run ‘python BPS-handless.py’.

Bot Paper Scissors is an OpenCV-based project that plays rock-paper-scissors against the player using a robotic hand as the computer’s avatar.

There are two programs involved - a C program and a Python program. 

The Python program controls the game and user interface. It allows the player to select the difficulty and help screen, detects the player’s move, chooses the move of the bionic hand, determines the winner, shows the round number, winner of each round, and scores of both players.

The C program controls the Arduino. It receives a single character, “r”,”p”,”s”, or “g” from the Python program via serial and controls the servos in the prosthetic hand depending on the character received.
