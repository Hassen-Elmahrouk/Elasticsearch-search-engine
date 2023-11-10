from flask import Flask, request, jsonify
import os
from find import find
app = Flask(__name__)

# Define the folder where photos will be stored
UPLOAD_FOLDER = 'photos'

# Ensure the "photos" folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_photo():
    if 'photo' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['photo']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        im_path=os.path.join(app.config['UPLOAD_FOLDER'], 'photo.jpg')
        file.save(os.path.join(im_path))
        finder =find("photo.jpg")
        return jsonify({'message': 'File successfully uploaded','result':finder.search()})

if __name__ == '__main__':
    app.run(debug=True)
