#!/usr/bin/env python
import os
import cv2
import numpy as np
from glob import glob
from functools import partial
from flask import Flask
from flask import render_template, request

app=Flask(__name__)

data_dir = '/path/to/images'
bins = 128
num_results = 20

img_lst = glob(data_dir + '*')
print('Calculating image features')
color_hist_ = partial(color_hist, bins)
corpus_features = list(map(color_hist_, img_lst)) # bottleneck

def color_hist(bins, img_pth):
    img = cv2.imread(img_pth, 0)
    hist = cv2.calcHist([img], [0], None, [bins], [0, 256])
    return hist / (sum(hist) + 1e-10)

def dist_calc(query_img, ref_img):
    return cv2.compareHist(query_img, ref_img, cv2.HISTCMP_CHISQR)

def transform_query(img_arr):
    hist = cv2.calcHist([img_arr], [0], None, [bins], [0, 256])
    return hist / (sum(hist) + 1e-10)

@app.route('/')
def home():
    if request.method == "POST":
        data_files = request.files.getlist('file[]')
        for data_file in data_files:
            file_contents = data_file.read()
            image = Image.open(BytesIO(file_contents))
            img_array = np.array(image)[:,:,:3]
	query_hist = transform_query(img_array)
	query_dist = partial(dist_calc, query_hist)
	result_dist = list(map(query_dist, corpus_features))
	result_paths = np.argsort(result_dist)[:num_results]
	result_paths = [os.path.join(data_dir, img_lst[pth]) for pth in result_paths]
	return render_template("results.html", result_paths=result_paths)
    return render_template("index.html")

if __name__ == "__main__":
    app.run("0.0.0.0")
