# AudioMate: Automatic Animations for Audio files

Created by: Vlad-Andrei Cursaru

## Introduction

AudioMate is a tool for creating animations based on user-provided audio files. The user may customize the animation by editing colors, backgrounds, animation smoothness, etc.

## Setup & Requirements

AudioMate requires Python3 to be installed on the machine in order to work. Python3 can be downloaded by visiting https://www.python.org/downloads/. On Windows, it can also be downloaded from the Microsoft Store.

If Python is already installed, please run the `setup.cmd` script which can be found in the `setup` directory in order to install the required python packages. After the script has finished running, AudioMate is ready to run.

In order to start, run the `AudioMate.cmd` script in the root folder. Alternatively, you can run the `audiomate.py` file directly using Python3.

## Runtime Options & Customizations

At runtime, you will be prompted with several options:

-  ***Music***: This will let you select the sound file to be processed. Any input file ***must*** be in the `input` folder. The name you provide ***must*** include the file extension. Sound files ***must*** be in `.wav` format.

- ***Background***: The background can be an image or a solid color. If an image is selected, then the file ***must*** be in the `input` folder. The name you provide ***must*** include the file extension. If you do not choose an image, you will be prompted to enter the background color. This color must be provided in RGB format. An RGB color picker can be found here: https://htmlcolorcodes.com/color-picker/. For image backgrounds, the resolution of the final video will match the resolution of the input image. For solid color backgrounds, you will be prompted for the height and width of the frames (both in pixels).

- ***Framerate***: The number of frames per second (FPS) that the output video file should have. While there is no theoretical upper limit on this value, higher framerates will benefit from audio with higher bitrates. Higher framerates provide smoother animations but take longer to generate and result in larger file sizes.

- ***Bar count***: The number of animated bars that should be displayed.

- ***Spacing***: The number of pixels of space between the animated bars. Together with the bar count, this determines how wide the bars are. The bar width is calculated in order to properly fill the horizontal resolution.

- ***Bar height***: A multiplier that is applied to the height of the animated bars. By default, with no multiplier (or a multiplier of 1), the bars do not extend to the top of the frame. Providing a higher value for this multiplier, the bars become taller.

- ***Smoothing***: Smoothing averages the value of each bar with a number of its neighbors in the time dimension. With no smoothing (a value of 0), the bars are the most responsive to the audio changes. However, this makes the bars look "jittery" and might be visually unappealing. Adding more smoothing reduces how responsive the bars are, but makes the animation more fluid.

## Output

The output will be  a `.mp4` file, which can be found in the `output` folder. During execution, temporary `.mp4` files may appear in the `output` folder. Removing these before the process finishes will cause the program to crash at some point during execution. During a successful run, the program will delete all temporary files once they are no longer needed.
