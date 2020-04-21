import os
import time
import json
import base64
import requests
import numpy as np
from glob import glob
from PIL import Image
from io import BytesIO
from flask import Flask
from flask import render_template, request, send_from_directory, jsonify, redirect, url_for, session
from elasticsearch import Elasticsearch
import photoscope.config as cfg
from photoscope.labels import labels
from photoscope.utils import Index, Document
from werkzeug.utils import secure_filename


app = Flask(__name__)

client = Elasticsearch()

temp_dir= 'tmp/'

indexer = Index(cfg.index_name, cfg.index_file, cfg.doc_json, client)
doc = Document(cfg.data_dir, cfg.doc_json, cfg.index_name)

image_encoder = doc.feature_extractor_layer
classifier = doc.classifier
sentence_encoder = doc.sentence_encoder

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        data_file = request.files.getlist('file[]')[0]
        url = request.form.get('url')
        tags = request.form.get('tag')
        if data_file:
            file_contents = data_file.read()
        elif url:
            response = requests.get(url)
            file_contents = response.content

        if data_file or url:
            image = Image.open(BytesIO(file_contents))
            image = (np.array(image.resize((224,224)))/255).astype(np.float32)
            img_array = np.expand_dims(image, axis=0)

            embedding = image_encoder(img_array)
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
        elif tags:
            sentence_embedding = sentence_encoder([tags])
            query_vector = sentence_embedding.numpy().tolist()[0]
            script_query = {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, doc['tag_vector']) + 1.0",
                        "params": {"query_vector": query_vector}
                    }
                }
            }


        response = client.search(
            index=cfg.index_name,
            body={
                "size": cfg.search_size,
                "query": script_query,
                "_source": {"includes": ["filepath", "tags"]}
            }
        )
        result_paths = [x['_source']['filepath'] for x in response['hits']['hits']]
        result_paths = [pth.split('/')[-1] for pth in result_paths]
        return render_template("results.html", result_paths=result_paths)
    return render_template("index.html")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == "POST":
        data_files = request.files.getlist('file[]')
        images_list = []
        tags_list = []
        for pic in data_files:
            file_contents = pic.read()

            # Generate tags for image
            img = Image.open(BytesIO(file_contents))
            img.save(temp_dir + pic.filename)
            image = (np.array(img.resize((224,224)))/255).astype(np.float32)
            img_array = np.expand_dims(image, axis=0)

            embedding = classifier(img_array)
            tags = embedding.numpy()[0].argsort()[-5:][::-1] 
            tags = ','.join([labels[i] for i in tags])

            images_list.append(pic.filename)
            tags_list.append(tags)
        session["images_list"] = images_list
        session["tags_list"] = tags_list
        return redirect(url_for("confirm"))
    return render_template("upload.html")


@app.route('/confirm', methods=['GET', 'POST'])
def confirm():
    images_list = session.get("images_list")
    tags_list = session.get("tags_list")
    if request.method == "POST":
        for i in range(len(images_list)):
            tags = request.form.get('tokenfield{}'.format(i)) #getting all confirmed tags
            sent_embedding = sentence_encoder([tags])

            img = Image.open(temp_dir + images_list[i])
            img = (np.array(img.resize((224,224)))/255).astype(np.float32)
            img_array = np.expand_dims(img, axis=0)
            img_embedding = image_encoder(img_array)

            image_vector = img_embedding.numpy().tolist()[0]
            tag_vector = sent_embedding.numpy().tolist()[0]

            new_doc = {'filepath': str(os.path.join(cfg.data_dir, images_list[i])),
                    'image_vector': image_vector,
                    'tag': str(tags),
                    'tag_vector': tag_vector}

            os.rename(os.path.join(temp_dir, images_list[i]), os.path.join(cfg.data_dir, images_list[i]))

            indexer.index(json.dumps(new_doc))
            return redirect(url_for("home"))
    return render_template("confirm.html", images_list=images_list, tags_list=tags_list)

@app.route('/t/<path:filename>')
def get_temp(filename):
    return send_from_directory(temp_dir, filename)

@app.route('/image/<path:filename>')
def get_image(filename):
    return send_from_directory(cfg.data_dir, filename)

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.run("0.0.0.0", port=5000)
