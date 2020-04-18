
from flask import Flask, render_template, jsonify, request
from werkzeug.utils import secure_filename
app = Flask(__name__)


from pymongo import MongoClient
from gridfs import GridFS
from bson import objectid
client = MongoClient('localhost', 27017)
db = client.dbsparta
fs = GridFS(db)
collection = db.upload


@app.route('/')
def home():
    return render_template('project_page1.html')

@app.route('/upload', methods=['POST'])
def upload_data():
    file = request.files['file']
    photo = fs.put(file, filename=file.filename, encoding='utf-8')
    title = request.form['title']
    main_value = request.form['main_value']
    equip = request.form['equip']
    sub_value = request.form['sub_value']
    data = request.form['data']
    doc = {
        'photo': photo,
        'title': title,
        'main_value': main_value,
        'equipment': equip,
        'sub_value': sub_value,
        'data': data
    }
    db.upload.insert_one(doc)
    return render_template('project_page1.html')

@app.route('/upload', methods=['GET'])
def read_data():
    read = list(db.upload.find({},{'_id':0}))
    return jsonify({'result':'success', 'read':read})

if __name__ == '__main__':
    app.run('localhost', port=5000, debug=True)