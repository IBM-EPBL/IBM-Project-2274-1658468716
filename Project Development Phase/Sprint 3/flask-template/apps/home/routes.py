# -*- encoding: utf-8 -*-
from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import load_img
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np

label=['Apple_scab', 'Apple_Black_rot', 'Cedar_apple_rust', 
         'Apple_healthy', 'Blueberry_healthy', 
         'Cherry_Powdery_mildew', 'Cherry_healthy', 
         'Corn_Cercospora_leaf_spot', 'Corn_Common_rust_', 
         'Corn_Northern_Leaf_Blight', 'Corn_healthy', 
         'Grape_Black_rot', 'Grape_Black_Measles', 
         'Grape_Leaf_blight', 'Grape_healthy', 
         'Orange_Haunglongbing', 'Peach_Bacterial_spot', 
         'Peach_healthy', 'Pepper,_bell_Bacterial_spot', 'Pepper,_bell_healthy', 
         'Potato_Early_blight', 'Potato_Late_blight', 'Potato_healthy', 
         'Raspberry_healthy', 'Soybean_healthy', 'Squash_Powdery_mildew', 
         'Strawberry_Leaf_scorch', 'Strawberry_healthy', 'Tomato_Bacterial_spot', 
         'Tomato_Early_blight', 'Tomato_Late_blight', 'Tomato_Leaf_Mold', 
         'Tomato_Septoria_leaf_spot', 'Tomato_Spider_mites Two-spotted_spider_mite', 
         'Tomato_Target_Spot', 'Tomato_Tomato_Yellow_Leaf_Curl_Virus', 
         'Tomato_Tomato_mosaic_virus', 'Tomato_healthy']

@blueprint.route('/index')
@login_required
def index():
    return render_template('home/index.html', segment='index')

@blueprint.route('/form-upload', methods=['GET', 'POST'])
@login_required
def route_form():
    return render_template('home/form-upload.html', segment='form-upload')

@blueprint.route('/api/upload', methods=['POST'])
@login_required
def upload():
    if request.method == 'POST':
        pic = request.files['image']
        pic_x = pic.filename
        pic.save(pic_x)
        
        cnn = load_model("D:\\XCodes\\IBM-Project\\Project Development Phase\\Sprint 3\\flask-template\\m1_hdf5.h5")
        dat = load_img(pic_x)
        #dl = tf.reshape(dat, [1,256,256,3])
        test_dat = img_to_array(dat)
        test_dat = test_dat/255.0
        test_dl = np.expand_dims(test_dat, axis=0)
        pred = cnn.predict(test_dl)
        y_class = pred.argmax(axis=1)
        result = label[y_class[0]]
        return render_template('home/form-upload.html', pred=result)
    return NULL


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
