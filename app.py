import sys, os
from Cartoon.pipeline.training_pipeline import TrainPipeline
from Cartoon.exception import CartoonException
from Cartoon.logger import logging

from Cartoon.utils.main_utils import decodeImage, encodeImageIntoBase64
from flask import Flask, request, jsonify, render_template,Response
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app)

class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/train")
def trainRoute():
    try:
        obj=TrainPipeline()
        obj.run_pipeline()

    except Exception as e:
        raise CartoonException(e,sys) from e
    return "Training Successfull!!" 

@app.route("/predict", methods=['POST','GET'])
@cross_origin()
def predictRoute():
    try:

        folder_path = "yolov5/runs"
        if os.path.exists(folder_path):
            os.system("rm -rf " + folder_path)
            print("Folder deleted successfully.")
        else:
            print("Folder does not exist.")

        image = request.json['image']
        decodeImage(image, clApp.filename)
        os.system("cd yolov5/ &&  python detect.py --weights best.pt --img 416 --conf 0.5 --source ../data/inputImage.jpg")

        opencodedbase64 = encodeImageIntoBase64("yolov5/runs/detect/exp/inputImage.jpg")
        result = {"image": opencodedbase64.decode('utf-8')}
        # os.system("rm -rf yolov5/runs")

    except ValueError as val:
        print(val)
        return Response("Value not found inside  json data")
    except KeyError:
        return Response("Key value error incorrect key passed")
    except Exception as e:
        print(e)
        result = "Invalid input"

    return jsonify(result)

@app.route("/live", methods=['GET'])
@cross_origin()
def predictLive():
    try:
        folder_path = "yolov5/runs"
        if os.path.exists(folder_path):
            os.system("rm -rf " + folder_path)
            print("Folder deleted successfully.")
        else:
            print("Folder does not exist.")
        #os.system("cd yolov5/ && python detect.py --weights my_model.pt --img 416 --conf 0.5 --source 0")
        os.system("cd yolov5/ && python detect.py --weights /Users/venkat/Desktop/WIred/project/Object_detection_Real_Time_sign_language/Real-Time-Object-Detection/notebook/new_notebook_files/best.pt --img 416 --conf 0.5 --source 0")

        os.system("rm -rf yolov5/runs")
        return "Camera starting!!" 

    except ValueError as val:
        print(val)
        return Response("Value not found inside  json data") 

if __name__ == "__main__":
    clApp = ClientApp()
    app.run(host="0.0.0.0", port=8080,debug=True)


# logging.info("Welcome to Friday-night")

# try:
#     obj=TrainPipeline()
#     obj.run_pipeline()

# except Exception as e:
#     raise CartoonException(e,sys) from e