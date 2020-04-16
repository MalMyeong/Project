
from flask import Flask, render_template, jsonify, request


app = Flask(__name__)


from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta
collection = db.upload


@app.route('/')
def home():
    return render_template('project_page1.html')

@app.route('/upload', methods=['POST'])
def upload():
    photo = request.form['photo']
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
    return jsonify({'result':'success'})



if __name__ == '__main__':
    app.run('localhost', port=5000, debug=True)