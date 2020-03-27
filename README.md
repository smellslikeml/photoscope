# Simple Image Search App

## Overview This is a simple image search flask app featuring elasticsearch and mobilenet image embeddings for indexing. Point it to a directory of
images, upload an image, and find the closest image results!

![app gif](assets/elastic_imagesearch.gif?raw=true)

## Dependencies
* [Tensorflow==2.1.0](https://www.tensorflow.org/)
* [Tensorflow Hub](https://www.tensorflow.org/hub)
* [Elasticsearch](https://www.elastic.co/elasticsearch/?ultron=[EL]-[B]-[AMER]-US+CA-Exact&blade=adwords-s&Device=c&thor=elasticsearch&gclid=Cj0KCQjwyPbzBRDsARIsAFh15JYEyhRFpwbjk_M-v67OAevQez72jXQuIY5VbZinBakVJr5UelxEdlgaAl93EALw_wcB)
* [Pillow](https://pillow.readthedocs.io/en/stable/)
* [Flask](http://flask.pocoo.org)

## Install
Clone this repo:
```
git clone https://github.com/smellslikeml/ImageSearchApp.git
```

[Install elasticsearch](https://www.elastic.co/downloads/elasticsearch) and install the rest of the requirements:
```
pip install -r requirements.txt
```

## Index images
First create your index:
```
python create_index.py
```

And create documents to index from your images:
```
python create_documents.py
```

Finally, index the created documents:
```
python index_documents.py
```

## Run
Run the flask app:
```
python app.py
```
And navigate to http://localhost:5000/ 

You can drop any image of a scene resembling what you are searching for and the app will return the most similar indexed images.
