from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('project_page1.html')

@app.route('/upload', methods=['POST'])
def upload():
    photo = request.form.files['photo']
    db.upload.insert(photo)
    return jsonify({'result': 'success', 'msg':'업로드 완료되었습니다.'})



if __name__ == '__main__':
    app.run('localhost', port=5000, debug=True)