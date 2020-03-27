import os
import time
import numpy as np
from glob import glob
from PIL import Image
from io import BytesIO
from flask import Flask
from flask import render_template, request, send_from_directory, jsonify
from elasticsearch import Elasticsearch

import tensorflow as tf
import tensorflow_hub as hub 

feature_extractor_url = "https://tfhub.dev/google/imagenet/mobilenet_v1_050_160/feature_vector/4" #@param {type:"string"}
feature_extractor_layer = hub.KerasLayer(feature_extractor_url,input_shape=(224,224,3))

client = Elasticsearch()

SEARCH_SIZE = 6
INDEX_NAME = 'images'
app = Flask(__name__)

data_dir = 'images/'

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        data_files = request.files.getlist('file[]')
        for data_file in data_files:
            file_contents = data_file.read()
            image = Image.open(BytesIO(file_contents))
            image = (np.array(image.resize((224,224)))/255).astype(np.float32)
            img_array = np.expand_dims(image, axis=0)
            embedding = feature_extractor_layer(img_array)
            query_vector = embedding.numpy().tolist()[0]
        

        script_query = {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, doc['image_vector']) + 1.0",
                    "params": {"query_vector": query_vector}
                }
            }
        }

        response = client.search(
            index=INDEX_NAME,
            body={
                "size": SEARCH_SIZE,
                "query": script_query,
                "_source": {"includes": ["image"]}
            }
        )
        result_paths = [x['_source']['image'] for x in response['hits']['hits']]
        result_paths = [pth.split('/')[-1] for pth in result_paths]
        print(result_paths)
        return render_template("results.html", result_paths=result_paths)
    return render_template("index.html")


@app.route('/image/<path:filename>')
def get_image(filename):
    return send_from_directory(data_dir, filename)

if __name__ == "__main__":
    app.run("0.0.0.0", port=5000)
