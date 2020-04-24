import numpy
from flask import Flask, render_template, jsonify, request, redirect, url_for
from bs4 import BeautifulSoup
import requests
from bson.objectid import ObjectId
app = Flask(__name__)


import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from io import BytesIO
import base64

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta
collection = db.uploads


@app.route('/')
def home():
    return render_template('project_page1.html')
# 분석 페이지 연결
@app.route('/analyze')
def analyze_page():
    return render_template('project_page2.html')

#분석 페이지 옵션에 맞는 데이터 찾기
@app.route('/analyze', methods=['POST'])
def search_data():
    main_value = request.form['main_value']
    equipment = request.form['equipment']
    sub_value = request.form['sub_value']
    result = db.uploads.find({'$and':[{'main_value':main_value,'equipment':equipment,'sub_value':sub_value}]})
    total_data = list()
    total_title = list()
    for i in result:
        data = float(i['data'])
        title = i['title']
        total_data.append(data)
        total_title.append(title)
    total_data = total_data
    total_title = total_title
    select = request.form['select_option']
    if select == '1':
        img = BytesIO()
        x = total_title
        y = total_data
        plt.plot(x,y , color='#B89977')
        plt.savefig(img, format='png')
        plt.close()
        img.seek(0)
        result = base64.b64encode(img.getvalue()).decode('utf8')
    elif select == '2':
        result = numpy.mean(total_data)
    elif select == '3':
        result = numpy.std(total_data)
    elif select == '4':
        maximum = max(total_data)
        minimum = min(total_data)
        result = '최대값 : ' + str(maximum) + '\n' +  '  최소값 : ' + str(minimum)

    return render_template('project_page2.html',result=result)

# 데이터 업로드 페이지
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

#업로드된 데이터 보여주는 페이지
@app.route('/uploads', methods=['GET'])
def read_data():
    read = list(db.uploads.find())
    for doc in read:
        doc['_id'] = str(doc['_id'])
    return jsonify({'result':'success', 'read': read})

#데이터 삭제 페이지
@app.route('/uploads/delete', methods=['POST'])
def delete_data():
    # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
    title = request.form['title']
    # 2. mystar 목록에서 delete_one으로 name이 name_receive와 일치하는 star를 제거합니다.
    db.uploads.delete_one({'title':title})
    # 3. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success'})
# 입력 데이터 수정 페이지
@app.route('/uploads/edit', methods=['GET'])
def edit():
    data_id = request.args.get('data_id')
    return render_template('page_edit.html', data_id=data_id)
#수정한 데이터 입력 & home으로 돌아가기

@app.route('/uploads/edit', methods=['POST'])
def edit_page():
    #file = request.files['file']
    #photo = file.filename
    #title = request.form['title']
    #main_value = request.form['main_value']
    #equip = request.form['equip']
    #sub_value = request.form['sub_value']
    #data = request.form['data']
    data_id = ObjectId(request.form['data_id'])
    print(data_id)
    #db.uploads.update({'_id':data_id},{'$set':{'photo':photo}})
    #db.uploads.update({'_id':data_id}{'$set': {'title':title}})
    #db.uploads.update({'_id':data_id}{'$set': {'main_value':main_value}})
    #db.uploads.update({'_id':data_id}{'$set': {'equipment':equip}})
    #db.uploads.update({'_id':data_id}{'$set': {'sub_value':sub_value}})
    #db.uploads.update({'_id':data_id}{'$set': {'data':data}})
    return jsonify({'result':'success'})



if __name__ == '__main__':
    app.run('localhost', port=5000, debug=True)