![Art With Machine Learning](https://user-images.githubusercontent.com/98792796/207993612-64991d08-197c-42ab-8ec9-ea7017fce2a6.jpg)

# Art With Machine Learning
The Art With Machine Learning program is created by:  
-Brendan Cook  
-Blain Bahls  
-Tim Roberts  
-Brian Lamont  
-Zak Rule  

The program takes a picture from a camera feed (webcam for example) and renders the picture taken in various artistic styles from renowned artists all around the world. Not only that, but it has the capability of learning new artistic styles too! Using Tensorflow and the Nvidia CUDA/cudNN software libraries, the program can learn the style of any provided image (saved as a .ckpt file under the checkpoints folder during the learning process) as well as accelerate the  process of learning new styles using GPU Hardware Acceleration.  

Instructions:  

1.) Ensure that a webcam or similar camera device is connected and that the display is set to 1920x1080 for the GUI to display properly. 
  
2.) Run the following commands within your python environment to install the necessary libraries for the program:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-pip install pyqt5  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-pip install opencv-python  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-pip install tensorflow  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-pip install moviepy  
  
3.) Run the "main.py" file from the "GUI Layout" folder to launch the application.

4.) Have fun!

Showcase Example:  

![ShowcasePresentation](https://user-images.githubusercontent.com/98792796/208005159-7938fb94-5ce3-483d-99db-daa41c1dc900.jpg)


Thanks to the University of Toledo for allowing us to create such an awesome project to be used as a display piece within the College of Engineering!  

Credit to Logan Engstrom for providing the public fast style transfer master repository:  
https://github.com/lengstrom/fast-style-transfer

