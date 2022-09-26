from datetime import datetime
import os
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
UPLOAD_FOLDER = './uploads'

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def is_file_extension_valid(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate(category, file):
    if not category:
        return False, jsonify({"response": "failed", "message": "Category should not be empty"})
    if not file:
        return False, jsonify({"response": "failed", "message": "File not found!"})
    if not file.filename and is_file_extension_valid(file.filename):
        return False, jsonify({"response": "failed", "message": "File name should be valid!"})
    return True, None
        
@cross_origin()
@app.route('/api/v1/upload', methods=['POST'])
def upload_file():
    category = request.form.get("category")
    file = request.files.get("image")
    valid, error = validate(category, file)
    if not valid:
        return error
    
    category_folder = os.path.join(app.config['UPLOAD_FOLDER'], category)
    file_name = "{category}_{datetime}.{fileExt}".format(category=category, datetime=datetime.now().strftime("%Y-%m-%d-%H-%M-%S"), fileExt="jpeg")
    os.makedirs(category_folder, exist_ok=True)
    file.save(os.path.join(category_folder, file_name))
    return jsonify({"response": "success", "message": "File uploaded successfully"})

@cross_origin()
@app.route('/', methods=['GET'])
def index():   
    return jsonify({"response": "success", "message": "Server Started"})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80, debug=True)

     
