# YoutubeDownloader
 
This program is a GUI based YouTube Downloader application. It allows you to download videos or audio from YouTube by simply pasting the URL.

## Features
1. Download as video (.mp4, .mkv) or audio (.mp3)
2. Validate YouTube URL
3. Display the download progress in GUI
4. Save the downloaded files to the location of your choice
5. Elegant theme (arc) for the application

## Dependencies
The project uses the following dependencies:

1. yt_dlp - Python library for downloading videos and audio from YouTube.
2. os - This module provides a portable way of using operating system dependent functionality.
3. ttkthemes - Provides additional themes for tkinter.
4. tkinter - Standard Python interface to the Tk GUI toolkit.
5. filedialog from tkinter - Opens a file dialog window.
6. PIL (Pillow) - Python Imaging Library adds image processing capabilities to your Python interpreter.
8. re - Provides regular expression matching operations.
8. math - Provides mathematical functions.
7. threading - This module constructs higher-level threading interfaces on top of the lower level _thread module.

## Getting Started
### Pre-requisites
Ensure you have Python 3.6+ installed on your machine. You will also need to install the following Python libraries if not already installed:

```
pip install yt-dlp
pip install ttkthemes
pip install Pillow
```
## Installing and Running the Program
1. Clone the repository to your local machine.
2. Navigate to the directory containing the program.py script.
3. Run the following command:

The application will start and you can interact with the GUI to download YouTube videos or audio.

## Usage
1. Paste a valid YouTube URL into the URL field.
2. Select the output directory by clicking the 📁 button next to the Output field.
3. Select the desired format from the Format dropdown. Options include 'Video (.mp4)', 'Video (.mkv)', 'Audio (.mp3)'.
4. Click Download to start the download. The progress will be displayed in the text area and the progress bar.

## Authors
Klaus Jürgen Folz

## License
This project is licensed under the MIT License.

## Acknowledgments
Thanks to the developers of yt-dlp for the awesome library.