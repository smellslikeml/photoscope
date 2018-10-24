# Simple Image Search App

## Overview
This is a simple image search flask app. Point it to a directory of images, upload an image, and find the closests image results

![app gif](https://github.com/mayorquinmachines/buddy_search_app/blob/master/image_search_app_demo.gif?raw=true)

## Dependencies
* [OpenCV](https://opencv-python-tutroals.readthedocs.io/en/latest/)
* [Flask](http://flask.pocoo.org)

## Install
Clone this repo:
```
git clone repo
```

In the `app.py` file, edit the line:
```
data_dir = "/path/to/images"
```
with your own data directory.

## Run
Run the line:
```
python app.py
```
And navigate to http://localhost:5000/ 

