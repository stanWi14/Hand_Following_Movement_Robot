# Hand_Following_Movement_Robot
This project is an updated project from HIMTI Expo Bot before, here the robot movement is going to follow our hand movement, using opencv and firmata.
We are going to use opencv for the input, so it will detect the hand coordinate and we get (X,Y) value
And we are going to use firmata to control arduino with python.
For movement & output, we use 2 servo. 1 at the bottom for horizontal movement (left and right just like our neck), and the other for vertical movemnt ( open and close for the mouth part)
We set the bottom servo according to X value, and the second servo to Y value that we get from our hand coordinate.
Feel free to try this project :D
