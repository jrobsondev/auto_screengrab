# Auto Screengrab

## About

Auto Screengrab is a desktop application written in Python 3 leveraging the Tkinter framework. It currently only runs on Windows as support for other operating systems was not required.

I created Auto Screengrab as a tool for my wife to use to take progress pictures of her digital artwork for her university course. This was also my first Desktop app written in Python as well as my first use of classes in an application.

## How to install

Auto Screengrab does not require installation as it is a standalone executable. To use, simply run the .exe found in the dist folder.

Please note that the autoscreengrab.exe must be run in a location containing the 'icons' folder.

## How to use

Using Auto Screengrab is pretty straight forward.

1. Press the Browse button.  This will open a File Explorer window.  Using this window, select a folder that you would like to save the screenshots to.
2. Set an interval time.  This is the time between each screenshot in minutes.  A screenshot is immediately taken upon pressing start, the following screenshot will be taken after your set interval time.
3. Project name is the name which your files will be saved as. For example, if your Project name was "hello world" your file names would be: "hello world_1.png", "hello world_2.png" etc.
4. The Select Screen dropdown allows you to choose which monitor you would like to take a screenshot of (if you have multiple monitors).  You also have the option to take a screenshot of "all screens" or "all screens (separate)". These options are explained below:

   **all screens**: This takes a picture of all screens and creates a single png file with all the screens merged.

   **all screens (separate)**: This simultaneously takes screenshots of each screen and saves them into their own png file. This will create files with the following naming convention: "projectname_screen1_5". - Note the filename includes which screen the screenshot is from.

Upon starting the application, if you are in a folder that contains screenshots with a matching project name, you will be prompted to continue where you left off. This is to prevent overwriting of old files as well as a nice feature to allow you to take a break and come back to the same project.

## Copyright

Copyright 2019 Jake Robson

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
