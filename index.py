# Store this code in 'app.py' file

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import hashlib


from Smart_Blockchain import *


app = Flask(__name__, template_folder='template')
blockchain = Smart_Blockchain()


app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_sekolah'

mysql = MySQL(app)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        password_enc = hashlib.md5(password.encode(
            'utf-8')).hexdigest()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM tb_user WHERE username LIKE %s AND password LIKE % s', (username, password_enc, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = account['username']
            session['password'] = account['password']
            msg = account['id_user']
            return redirect(url_for('index', msg=msg))
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)


@app.route('/index', methods=['GET', 'POST'])
def index():
    # Check that the required fields are in the POST'ed data
    # sender = request.form['sender']
    # recipient = request.form['recipient']
    # amount = request.form['amount']
    # Create a new Transaction
    # index = blockchain.new_transaction(
    #     sender, recipient, amount)

    # response = {'message': f'Transaction will be added to Block {index}'}

    # last_block = blockchain.last_block

    # # Forge the new Block by adding it to the chain
    # previous_hash = blockchain.hash(last_block)
    # block = blockchain.new_block(previous_hash)

    # response = {
    #     'message': "New Block Forged",
    #     'index': block['index'],
    #     'transactions': block['transactions'],
    #     'previous_hash': block['previous_hash'],
    # }

    if request.method == 'POST' and 'sender' in request.form and 'recipient' in request.form and 'amount' in request.form:
        sender = request.form['sender']
        recipient = request.form['recipient']
        amount = request.form['amount']
        index = blockchain.new_transaction(sender, amount,  recipient)
        last_block = blockchain.last_block
        previous_hash = blockchain.hash(last_block)
        block = blockchain.new_block(previous_hash)

    # Forge the new Block by adding it to the chain
        # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # query = "INSERT INTO blockchainn(sender, recipient, amount) VALUES(%s,%s,%s)"
        # values = (sender, recipient, amount,)
        # cursor.execute(query, values)
        # mysql.connection.commit()
        # msg = 'You have successfully registered !'
        # response = {
        #     'message': "New Block Forged",
        #     'index': block['index'],
        #     'transactions': block['transactions'],
        #     'previous_hash': block['previous_hash'],
        # }

        # return jsonify(response), 201
        return redirect(url_for('transaksi'))

    return render_template('index.html')


@app.route('/transaksi', methods=['GET'])
def transaksi():
    # response = {
    #     'chain': blockchain.chain,
    #     'length': len(blockchain.chain),
    # }
    if request.method == 'GET':

        chain = blockchain.chain
        panjang = len(blockchain.chain)
        now = panjang-1

        index = chain[now]["index"]
        transactions = chain[now]["transactions"]
        transactions2 = transactions[0]
        hashh = chain[now]["previous_hash"]
        sender = transactions2["sender"]
        recipient = transactions2["recipient"]
        amount = transactions2["amount_send"]
        semua = {
            'message': 'transaksi berhasil',
            'index': index,
            'hash': hashh,
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'panjangnya': panjang

        }

    return render_template('transaksi.html', index=index, hashh=hashh, sender=sender, recipient=recipient, amount=amount)


@app.route('/chain', methods=['GET'])
def chain():
    # response = {
    #     'chain': blockchain.chain,
    #     'length': len(blockchain.chain),
    # }
    if request.method == 'GET':
        a = 1
        b_list = []
        b = 0
        chain = blockchain.chain
        panjang = len(blockchain.chain)
        list_semua = []
        pengirim = []
        penerima = []
        hashnya = []
        indexnya = []
        duit = []
        heading = ["index", "previous hash",
                   "pengirim", "penerima", "Jumlah transaksi"]
        semuanya = []
        while a < panjang:
            index = chain[a]["index"]
            transactions = chain[a]["transactions"]
            transactions2 = transactions[0]
            hashh = chain[a]["previous_hash"]

            sender = transactions2["sender"]
            recipient = transactions2["recipient"]
            amount = transactions2["amount_send"]
            indexnya.append(index)
            hashnya.append(hashh)
            pengirim.append(sender)
            penerima.append(recipient)
            duit.append(amount)
            b_list.append(b)
            b += 1

            semua = {
                'index': index,
                'hash': hashh,
                'sender': sender,
                'recipient': recipient,
                'amount': amount,
                'panjangnya': panjang

            }
            list_semua.append(semua)
            a += 1

    return render_template('chain.html', b_list=b_list, indexnya=indexnya, hashnya=hashnya, pengirim=pengirim, penerima=penerima, duit=duit, heading=heading)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'nama_user' in request.form and 'role' in request.form:
        username = request.form['username']
        password_enc = hashlib.md5(request.form['password'].encode(
            'utf-8')).hexdigest()

        nama_user = request.form['nama_user']
        role = request.form['role']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM tb_user WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'

        elif not username or not password_enc or not nama_user:
            msg = 'Please fill out the form !'
        else:
            query = "INSERT INTO tb_user(username, password, nama_user, role) VALUES(%s,%s,%s,%s)"
            values = (username, password_enc, nama_user, role,)
            cursor.execute(query, values)
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            return redirect(url_for('login'))
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)


if __name__ == "__main__":
    app.run(debug=True)
