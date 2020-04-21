# Photoscope: Find your memories faster! 

## Overview 
Have a ton of images on your computer struggling to find what you're looking for? 

This is a simple reverse image search app to help you find your pictures faster.
Index a directory of images, upload an image to the local app, and receive your most similar images.
![app gif](assets/elastic_imagesearch.gif?raw=true)

## How it works
This flask search app features elasticsearch for fast results and uses image feature vectors extracted with a TFHub hosted headless mobilenet model to find related images with greater context.

Matching images based on similarity of image embeddings offers higher recall of semantically relevant results, helping you find what your looking for faster!

## Dependencies
* Python 3
* [Tensorflow==2.1.0](https://www.tensorflow.org/)
* [Tensorflow Hub](https://www.tensorflow.org/hub)
* [Elasticsearch](https://www.elastic.co/elasticsearch/?ultron=[EL]-[B]-[AMER]-US+CA-Exact&blade=adwords-s&Device=c&thor=elasticsearch&gclid=Cj0KCQjwyPbzBRDsARIsAFh15JYEyhRFpwbjk_M-v67OAevQez72jXQuIY5VbZinBakVJr5UelxEdlgaAl93EALw_wcB)
* [Pillow](https://pillow.readthedocs.io/en/stable/)
* [Flask](http://flask.pocoo.org)
* Requests

## Install
Pip install the package:
```
pip install photoscope
```

Or clone this repo and install:
```
git clone https://github.com/smellslikeml/photoscope.git
cd photoscope/
pip install -e .
```

[Install elasticsearch](https://www.elastic.co/downloads/elasticsearch) and start the elasticsearch service:
```
sudo service elasticsearch start
```
## Configure photoscope
First, make sure to configure photoscope with the full path to your images directory:
```
$ photoscope configure --data_dir="/path/to/images/"
```
Add the ```--index_name``` flag to change the default index name ```--index_name="MyIndexName"```.

## Index images
After configuring, run:
```
$ photoscope index
```
This will bulk index all files in the image directory named. 


## Run the app
Run the flask app with:
```
$ photoscope app start
```
And navigate to http://localhost:5000/ 

You can drop any image of a scene resembling what you are searching for and the app will return the most similar indexed images.

Stop the elasticsearch service after you are done to free up memory.
```
sudo service elasticsearch stop
```

## References

* [Blog post](https://smellslikeml.com/bertsearch.html)
* [Elasticsearch text embeddings](https://www.elastic.co/blog/text-similarity-search-with-vectors-in-elasticsearch)
* [Bertsearch](https://github.com/Hironsan/bertsearch)
* [Extracting image feature vectors](https://www.tensorflow.org/hub/common_signatures/images#feature-vector)
