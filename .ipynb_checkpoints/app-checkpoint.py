from flask import Flask
import json
import numpy as np

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello"

import glob
import base64
from io import BytesIO, StringIO
from PIL import Image
count = 0
images = glob.glob("./data/valid/*.jpg")
preds = {}

@app.route("/put_result/<float:pred>")
def put_result(pred):
    global count
    global images
    preds[images[count-1]] = pred
    print("preds", preds[images[count-1]])
    return {"data": True}

@app.route("/get_image")
def get_image():
    global count
    global images
    if count >= len(images):
        f = open("results.json", "w")
        json.dump(preds, f)
        f.close()
        print("no image - dict flushed")
        return {"data": True}

    else:
        try:
            path = images[count]
            image = Image.open(path)
            temp_image = np.array(image, dtype=np.uint8)
            vhex = np.vectorize(hex)
            temp = vhex(temp_image).ravel()
            temp = [el.strip("0x").zfill(2) for el in temp]
            count += 1
            return "@"+"".join(temp)

        except Exception as e:
            print(e)
            print("image fetch error")
            return None

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="20005", debug=True)
