import os
import json
import argparse
import numpy as np
from photoscope.labels import labels

from PIL import Image
import tensorflow_hub as hub
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


class Index(object):
    def __init__(self, index_name, index_file, data, client):
        self.index_name = index_name
        self.index_file = index_file
        self.data = data

        self.client = client

    def loadDataset(self, path):
        with open(path) as f:
            return [json.loads(line) for line in f]

    def createIndex(self):
        self.client.indices.delete(index=self.index_name, ignore=[404])
        with open(self.index_file) as index_file:
            source = index_file.read().strip()
            self.client.indices.create(index=self.index_name, body=source)

    def bulkIndex(self):
        docs = self.loadDataset(self.data)
        bulk(self.client, docs)

    def index(self, doc):
        self.client.index(index=self.index_name, body=doc)


class Document(object):
    def __init__(self, image_dir, data, index_name):
        self.image_dir = image_dir
        self.data = data
        self.index_name = index_name

        self.feature_extractor_url = "https://tfhub.dev/google/imagenet/mobilenet_v1_050_160/feature_vector/4" 
        self.classifier_url = "https://tfhub.dev/google/imagenet/mobilenet_v1_050_160/classification/4" 
        self.sentence_encoder_url = "https://tfhub.dev/google/universal-sentence-encoder/4"

        self.feature_extractor_layer = hub.KerasLayer(self.feature_extractor_url, input_shape=(224,224,3))
        self.classifier = hub.KerasLayer(self.classifier_url, input_shape=(224,224,3))
        self.sentence_encoder = hub.load(self.sentence_encoder_url)


    def createDocument(self, doc, emb, tag, tag_vector, index_name):
        return {
            '_op_type': 'index',
            '_index': index_name,
            'filepath': doc['image'],
            'image_vector': emb,
            'tag': tag,
            'tag_vector': tag_vector,
        }


    def loadDataset(self, path):
        docs = []
        files = os.listdir(path)
        for fl in files:
            doc = {
                'image': path + fl,
            }
            docs.append(doc)
        return docs
    

    def bulkPredict(self, docs, batch_size=32):
        """Extract mobilenet embeddings."""
        for i in range(0, len(docs), batch_size):
            batch_docs = docs[i: i+batch_size]
            batch_docs = [Image.open(doc['image']) for doc in batch_docs]
            batch_docs = np.array([(np.array(doc.resize((224,224)))/255).astype(np.float32) for doc in batch_docs])

            embeddings = self.feature_extractor_layer(batch_docs)
            tags = self.classifier(batch_docs)

            tag_sentences = [x.argsort()[-5:][::-1] for x in tags.numpy()] 
            tag_sentences = [', '.join([labels[i] for i in sublist]) for sublist in tag_sentences]

            tag_embeddings = self.sentence_encoder(tag_sentences)

            for emb, tag, tag_emb in zip(embeddings, tag_sentences, tag_embeddings):
                yield emb.numpy().tolist(), tag, tag_emb.numpy().tolist()


    def run(self):
        docs = self.loadDataset(self.image_dir)
        with open(self.data, 'w') as f:
            for doc, preds in zip(docs, self.bulkPredict(docs)):
                d = self.createDocument(doc, preds[0], preds[1], preds[2], self.index_name)
                f.write(json.dumps(d) + '\n')
                f.flush()
