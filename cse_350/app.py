import os,numpy,cv2,base64,io
from flask import Flask, render_template, request
from deeplearning import hello_image
from matplotlib import pyplot as plt
from PIL import Image
import numpy as np
app=Flask(__name__)

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
UPLOAD_PATH=os.path.join(BASE_PATH,'static/upload/')
PREDICT_PATH=os.path.join(BASE_PATH,'static/roi/')

@app.route('/',methods=['POST','GET'])
def index():
    
    global numb
    if request.method == 'POST':
        upload_file=request.files['image_name']
        filename=upload_file.filename
        imageRead=upload_file.read()
        file_bytes = numpy.fromstring(imageRead, numpy.uint8)
        # convert numpy array to image
        img = cv2.imdecode(file_bytes, cv2.IMREAD_UNCHANGED)
        result=hello_image(img)
        #text=OCR(path_save,filename)
        print(result)
        numberplat=""

        for r in result[0]:
            numberplat+="  "+r[1]
        img = Image.fromarray(result[1])
        img.save(PREDICT_PATH+filename)

        return render_template('index.html',upload=True,upload_image=filename,numb=numberplat)

    return render_template('index.html',upload=False,file='webcamp.jpg')

@app.route('/upload',methods=['POST'])
def upload():
    print(request)
    upload_file=request.files['image_name']
    filename=upload_file.filename
    path_save=os.path.join(UPLOAD_PATH,filename)
    upload_file.save(path_save)
    return "Successfully uploaded"


@app.route('/uploadCamp',methods=['POST','GET'])
def uploadCamp():
    
    if request.method == 'POST':
        
        image_file=request.form.get("image_name", False) # I assume you have a way of picking unique filenames
        encoded_img = image_file.split(",")[1]
        binary = base64.b64decode(encoded_img)
        filename='webcamp.jpg'
        image = np.asarray(bytearray(binary), dtype=np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        print(image)
        result=hello_image(image)
            #text=OCR(path_save,filename)
        # print(result)
        numberplat=""

        for r in result[0]:
            numberplat+="  "+r[1]
        img = Image.fromarray(result[1])
        img.save(PREDICT_PATH+'webcamp.jpg')
        print(img)

        return render_template('index.html',upload=True,upload_image1=filename,numb=numberplat)
    return render_template('index.html',upload=False)

if __name__=="__main__":
    app.run(debug=True)