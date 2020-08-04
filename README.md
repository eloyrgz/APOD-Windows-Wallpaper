# APOD Windows Wallpaper
This script downloads the Astronomy Picture of the Day from the Nasa website and sets it as your Windows wallpaper. It also shows the title and explanation while the picture is being downloaded and once the wallpaper was set, lets you to change among 4 different image's styles (center, stretch, fit, fill) using the number keys 1 to 4. Default is fill, 4. Any other key exits the program.

Follow the installation and configuration instructions. If something doesn't work set the logging level to INFO to see the messages about what the script is doing and help you to detect the problem.

Then I recommend adding the script to the Windows startup to run every time you are logged in or at a scheduled time for instance. You can also setup the Windows screensaver to show the imagery from the downloads folder of the script.

## Features
- Sets the NASA APOD as your Windows wallpaper in HD quality.
- Shows the title and explanation of the picture.
- Different image's styles (center, stretch, fit, fill).
- Supports proxy settings.
- Provides a logger for debuging and helping you if something doesn't work.

## Requirements
- A Windows OS
- Python 3 or higher
- PyWin32
- A few python packages (requests, configparser, warnings, pillow)

## Installation with Conda (recommended)

- Well, first you will need to install [miniconda](https://docs.conda.io/en/latest/miniconda.html). 
- Then run the following commands:

  ```python
  conda create -n apod.py3.6 python=3.6
  conda activate apod.py3.6
  conda install requests configparser warnings
  conda install -c anaconda pywin32
  pip install pillow 
  ```

## Installation with PIP
- Download and install [Python](https://www.python.org/downloads/)
- Download and install [PyWin32](https://sourceforge.net/projects/pywin32/)
- Install Python packages

  ```python
  pip install requests pillow configparser warnings
  ```  
  
## Configuration
Edit the config file to fit your sistem. the only field required is download_path the rest are optional.
- **download_path**
  
  Your local path where the images will be downloaded.

- **api_key** 

  DEMO_KEY should be enough but you can always ask for your own API key [here](https://api.nasa.gov/index.html#apply-for-an-api-key).
  
  

- **proxy**

  If you were sometimes behind a proxy, for instance at work or at university and you would like to keep updating your wallpaper, you can install cntlm from [here](https://sourceforge.net/projects/cntlm/) and set it up as a gateway to your corporate proxy.
  
## Run at Windows startup
To change your wallpaper at Windows startup, create a shortcut to apod_wallpaper.py in Start->All Programs->Startup. 
If you are one of those like me who doesn't logoff very often you will also have the script to hand whenever you want to update your wallpaper.

## Windows screensaver setup
Setup the Windows screensaver to use the imagery from the folder that you have configured as your download path. 
Maybe not at the beginning but with some time you will have a nice collection of pictures of universe.
