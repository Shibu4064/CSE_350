import os,numpy,cv2
from flask import Flask, render_template, request
from deeplearning import hello_image
from matplotlib import pyplot as plt
from PIL import Image
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

    return render_template('index.html',upload=False)

@app.route('/upload',methods=['POST'])
def upload():
    print(request)
    upload_file=request.files['image_name']
    filename=upload_file.filename
    path_save=os.path.join(UPLOAD_PATH,filename)
    upload_file.save(path_save)
    return "Successfully uploaded"

if __name__=="__main__":
    app.run(debug=True)