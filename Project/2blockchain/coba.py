from flask import Flask, request, jsonify, make_response, url_for, redirect, render_template, flash
import pymysql
import hashlib
import datetime
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, JWTManager

app = Flask(__name__, template_folder='template')


mydb = pymysql.connect(
    host="localhost",
    user="root",
    passwd="",
    database="db_sekolah"  # database yang digunakan
)

messages = []


@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        username = username.lower()
        password_enc = hashlib.md5(password.encode(
            'utf-8')).hexdigest()

        # Cek kredensial didalam database
        query = " SELECT id_user, password FROM tb_user WHERE username = %s "
        values = (username, )

        mycursor = mydb.cursor()
        mycursor.execute(query, values)
        data_user = mycursor.fetchall()

        if len(data_user) == 0:  # jika user gak ada
            return make_response(jsonify(deskripsi="Username tidak ditemukan"), 401)

        data_user = data_user[0]

        db_password = data_user[1]

        if password_enc != db_password:
            return make_response(jsonify(deskripsi="Password salah"), 401)

        return redirect(url_for('beranda'))

    return render_template('index.html')


@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        username = request.form['username']
        role = request.form['role']
        password = hashlib.md5(request.form['password'].encode(
            'utf-8')).hexdigest()

        nis = request.form['nis']
        nama = request.form['nama']
        umur = request.form['umur']
        alamat = request.form['alamat']

        messages.append({'nis': nis,
                         'nama': nama,
                         'umur': umur,
                         'alamat': alamat
                         })
        # Username dan Password
        query = "INSERT INTO tb_user(username, password, nama_user, role) VALUES(%s,%s,%s,%s)"
        values = (username, password, nama, role,)

        query2 = "INSERT INTO tb_siswa(nis, nama, umur, alamat) VALUES(%s,%s,%s,%s)"
        values2 = (nis, nama, umur, alamat,)

        mycursor = mydb.cursor()
        mycursor.execute(query, values)
        mycursor.execute(query2, values2)
        mydb.commit()

        return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/beranda')
def beranda():
    return render_template('beranda.html')


if __name__ == "__main__":
    app.run(debug=True)
