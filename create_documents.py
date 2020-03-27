"""
Example script to create elasticsearch documents.
"""
import os
import argparse
import json

import numpy as np
from PIL import Image
import tensorflow as tf
import tensorflow_hub as hub

feature_extractor_url = "https://tfhub.dev/google/imagenet/mobilenet_v1_050_160/feature_vector/4" #@param {type:"string"}
feature_extractor_layer = hub.KerasLayer(feature_extractor_url,input_shape=(224,224,3))


def create_document(doc, emb, index_name):
    return {
        '_op_type': 'index',
        '_index': index_name,
        'image': doc['image'],
        'image_vector': emb
    }


def load_dataset(path):
    docs = []
    files = os.listdir(path)
    for fl in files:
        doc = {
            'image': path + fl,
        }
        docs.append(doc)
    print('loaded dataset')
    return docs


def bulk_predict(docs, batch_size=32):
    """Predict bert embeddings."""
    for i in range(0, len(docs), batch_size):
        batch_docs = docs[i: i+batch_size]
        batch_docs = [Image.open(doc['image']) for doc in batch_docs]
        batch_docs = np.array([(np.array(doc.resize((244,244)))/255).astype(np.float32) for doc in batch_docs])

        embeddings = feature_extractor_layer(batch_docs)
        print(embeddings)
        for emb in embeddings:
            yield emb.numpy().tolist()


def main(args):
    docs = load_dataset(args.data)
    with open(args.save, 'w') as f:
        print('Getting bulk predict...')
        for doc, emb in zip(docs, bulk_predict(docs)):
            d = create_document(doc, emb, args.index_name)
            f.write(json.dumps(d) + '\n')
            f.flush()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Creating elasticsearch documents.')
    parser.add_argument('--data', default="./images/", help='data for creating documents.')
    parser.add_argument('--save', default='documents.jsonl', help='created documents.')
    parser.add_argument('--index_name', default='images', help='Elasticsearch index name.')
    args = parser.parse_args()
    print('running main...')
    main(args)
