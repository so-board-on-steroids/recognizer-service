from flask import Flask, jsonify, request
import numpy as np
from flask_cors import CORS

import utils

app = Flask(__name__)

# CORS handling
CORS(app, resources={'/rowimage': {"origins": "http://localhost:8080"}})

@app.route('/rowimage', methods=['POST'])
def image_post_request():  
    img = utils.base64_to_image(request.json['img'])
    data = utils.recognize_row(img)    
    return jsonify(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)