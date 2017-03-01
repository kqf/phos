Styling tools
=============

This folder contains all tools and scripts that produce interim results: such as bad maps and their differences, nice looking plots, projections etc.


## Usage
All input `*.root` files are supposed to be in the directory `input`.To configure the plots use `*.json` files in the `config` directory.Look at the makefile for more details.

```bash

# Configure the style/ select histograms
vim config/some-style.py

# Update makefile varable "inpconf = config/some-style"
#

# Save the images
make
```