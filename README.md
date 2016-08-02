# APOD Windows Wallpaper
This script downloads the Astronomy Picture of the Day from the Nasa site and sets it as your Windows wallpaper. It shows the title and explanation while the picture is being downloaded and once the wallpaper was set, lets you to change among 4 different image's styles (center, stretch, fit, fill) using the number keys 1 to 4. Default is fill, 4. Any other key exits the program.

For getting this to work follow the installation and configuration instructions. If something doesn't work set the logging level to INFO to see messages about what the script is doing and help you to detect the problem.

Then add the script to the Windows startup to run every time you are logged on. You can also setup the Windows screensaver to show the imagery from the downloads folder of the script.

## Features
- Sets the NASA APOD as your Windows wallpaper in HD quality.
- Shows the title and explanation of the picture.
- Different image's styles (center, stretch, fit, fill).
- Supports proxy settings.
- Provides a logger for debuging.

## Requirements
- A Windows OS
- Python 3 or higher
- PyWin32
- Requests
- Pillow

## Installation
- Download and install Python

  https://www.python.org/downloads/
  
- Download and install PyWin32

  https://sourceforge.net/projects/pywin32/
  
- Install Python packages

  ```python
  pip install requests pillow
  ```
  
## Configuration
Edit the configuration file to fit your sistem. The only field required is download_path.
- **download_path**
  
  The path where the images will be downloaded.

- **api_key** 

  DEMO_KEY should be enough but you can ask for your own API key at:
  
  https://api.nasa.gov/index.html#apply-for-an-api-key

- **proxy**

  If you are behind a proxy, for instance at work or at university.
  
  [user:password@]proxy.com:port/
  
## Run at Windows startup
Create a shortcut to the file script file at:

Start->All Programs->Startup


## Windows screensaver setup
Setup the Windows screensaver to use the imagery from the folder that you have configured as your download path.
