from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['Data']
collection = db['Data']

@app.route('/')
def index():
    data = collection.find()
    return render_template('index.html', data=data)

@app.route('/add', methods=['POST'])
def add_record():
    if request.method == 'POST':
        name = request.form['name']
        middlename = request.form['middlename']
        login = request.form['login']
        email = request.form['email']
        address = request.form['address']

        new_record = {
            'Name': name,
            'Middlename': middlename,
            'Login': login,
            'Email': email,
            'Address': address
        }
        collection.insert_one(new_record)

    return jsonify(success=True)

@app.route('/update/<record_id>', methods=['POST'])
def update_record(record_id):
    if request.method == 'POST':
        new_data = {
            'Name': request.form.get('name'),
            'Middlename': request.form.get('middlename'),
            'Login': request.form.get('login'),
            'Email': request.form.get('email'),
            'Address': request.form.get('address')
        }
        collection.update_one({'_id': ObjectId(record_id)}, {'$set': new_data})

    return jsonify(success=True)

@app.route('/delete/<record_id>', methods=['POST'])
def delete_record(record_id):
    if request.method == 'POST':
        result = collection.delete_one({'_id': ObjectId(record_id)})
        if result.deleted_count == 1:
            return jsonify(success=True)
        else:
            return jsonify(success=False, error="Rekord nie został znaleziony.")

if __name__ == '__main__':
    app.run(debug=True)
