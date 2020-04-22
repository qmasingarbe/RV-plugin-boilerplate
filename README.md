# RV plugin boilerplate
This repo aims to provide a quick explanation and a template for TDs wanting to create a RV plugin.

![Result image](./result.jpg)
This is the result of the start code, a Qt widget populated by paths when new sources are added (also basic menu + basic settings)

### Setup
  - copy the content of the `code` directory of this repo to somewhere in your source code repository   
  - create a **rvpkg** using this command `zip my_package-0.0.rvpkg PACKAGE my_code.py`.
  The .rvpkg file is the proper way to install a plugin in RV, it should contain everything needed for the plugin.
  - install the rvpkg by starting RV, going in RV > Preferences... > Packages > Add packages...
  RV will show you were the package is going to be installed, keep note of this path
  - check Installed and Load checkboxes on our plugin in the package list.
  - to edit our plugin we can go to the installation directory, in the Python folder we should find our file.
  This avoid doing a new package and removing and installing our plugin using RV UI.
  You have to restart RV to see any change to the .py file, I didn't find a way to reload the plugin.

### Code
The code folder contains 2 files :
  - PACKAGE : this file is mandatory and should be named like this, it contains a description of our plugin
  - my_code.py : fell free to rename it, this is the actual python code, see the comments inside.

Any `print` statement in your python code will be written in the Rv console (Window > Console) or in the terminal which launched RV process.

### Ressources
- python quickstart : https://support.shotgunsoftware.com/hc/en-us/articles/219042308-RV-Python-quickstart
- main documentation on plugins : https://support.shotgunsoftware.com/hc/en-us/articles/360024280254-Reference-Manual

### Disclaimer
Code is provided as is, with no guaranty/support  
It was tested on RV 7.1.1 on win10 and RV 7.3.1 on linux