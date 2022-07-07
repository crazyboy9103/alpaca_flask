from flask import Flask
import json

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello"

import glob
import base64
from io import BytesIO, StringIO
from PIL import Image
count = 0
images = glob.glob("./data/valid/*.jpeg")
preds = {}

@app.route("/put_result/<float:pred>")
def put_result(pred):
    preds[images[count-1]] = pred

@app.route("/get_image")
def get_image():
    if count >= len(images):
        f = open("results.json", "w")
        json.dump(preds, f)
        f.close()
        print("no image - dict flushed")
        return None

    else:
        try:
            path = images[count]
            image = Image.open(path)
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue())
            count += 1
            return img_str

        except Exception as e:
            print(e)
            print("image fetch error")
            return None

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="20005", debug=True)
