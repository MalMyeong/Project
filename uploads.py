
from flask import Flask, render_template, jsonify, request, redirect, url_for
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta
collection = db.uploads


@app.route('/')
def home():
    return render_template('project_page1.html')

@app.route('/analyze')
def analyze_page():
    return render_template('project_page2.html')

@app.route('/analyze', methods=['POST'])
def search_data():
    main_value = request.form['main_value']
    equipment = request.form['equipment']
    sub_value = request.form['sub_value']
    find_main = db.uploads.find({'main_value':main_value})
    find_equip = find_main({'equipment':equipment})
    list(find_equip({'sub_value':sub_value}))
    return jsonify({'result':'success'})



@app.route('/uploads', methods=['POST'])
def upload_data():
    file = request.files['file']
    photo = file.filename
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
    db.uploads.insert_one(doc)
    return jsonify({"result":"success"})

@app.route('/uploads', methods=['GET'])
def read_data():
    read = list(db.uploads.find({},{'_id':0}))
    return jsonify({'result':'success', 'read':read})

@app.route('/uploads/delete', methods=['POST'])
def delete_data():
    # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
    title = request.form['title']
    # 2. mystar 목록에서 delete_one으로 name이 name_receive와 일치하는 star를 제거합니다.
    db.uploads.remove({'title':title})
    # 3. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run('localhost', port=5000, debug=True)