from flask import Flask, render_template, request, redirect, url_for
import mysql.connector as my
import os
from dotenv import load_dotenv

load_dotenv()

user = os.getenv('USER')
password = os.getenv('PASSWORD')
database = os.getenv('DATABASE')
host = os.getenv('HOST')

def conectarBanco():
    conexao = my.connect(
        user=user,
        password=password,
        database=database,
        host=host
    )
    return conexao

conectarBanco()

app = Flask(__name__)

@app.route('/')
def index():
    titulo = 'Página inicial'
    return render_template('index.html', titulo=titulo)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        if email == 'admin@loja.com' and senha == '1234':
            return redirect(url_for('index'))
        else:
            return render_template('login.html', errou=True)

    return render_template('login.html', errou=False)

if __name__ == '__main__':
    app.run(debug=True)
