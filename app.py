from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector as my
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'minha_chave_secreta'  

user = os.getenv('USER')
password = os.getenv('PASSWORD')
database = os.getenv('DATABASE')
host = os.getenv('HOST')

print(f"DEBUG: host={host}, user={user}, database={database}")

def conectarBanco():
    conexao = my.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    return conexao

@app.route('/')
def index():
    titulo = 'Página inicial'
    return render_template('index.html', titulo=titulo)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        conexao = conectarBanco()
        cursor = conexao.cursor(dictionary=True)

        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()
        conexao.close()

        if usuario:
            if senha == usuario['senha']:
                # Aqui estamos garantindo que o valor de tipo é comparado corretamente
                session['usuario'] = usuario['email']
                session['nome'] = usuario['nome']
                session['tipo'] = usuario['tipo']

                if usuario['tipo'].strip().lower() == 'admin':  # Verifique por espaços e maiúsculas/minúsculas
                    return redirect(url_for('cadastrar_produto'))
                else:
                    return redirect(url_for('produtos'))
            else:
                flash('Senha incorreta.', 'error')
                return redirect(url_for('login'))
        else:
            flash('E-mail não encontrado.', 'error')
            return redirect(url_for('login'))

    return render_template('login.html', errou=False)

@app.route('/cadastrarproduto', methods=['GET', 'POST'])
def cadastrar_produto():
    if 'usuario' not in session or session.get('tipo') != 'admin':
        return redirect(url_for('login'))

    if request.method == 'POST':
        nome = request.form['nome']
        preco = request.form['preco']
        descricao = request.form['descricao']
        imagem = request.form['imagem']
        tipo = request.form['tipo']

        conexao = conectarBanco()
        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO produtos (nome, preco, descricao, imagem, tipo)
            VALUES (%s, %s, %s, %s, %s)
        """, (nome, preco, descricao, imagem, tipo))
        conexao.commit()
        conexao.close()

        return render_template('cadastrarproduto.html', sucesso=True)

    return render_template('cadastrarproduto.html', sucesso=False)

@app.route('/produtos')
def produtos():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    conexao = conectarBanco()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    conexao.close()

    return render_template('produtos.html', produtos=produtos)

@app.route('/cadastrarConta', methods=['GET', 'POST'])
def cadastrar_conta():
    conexao = conectarBanco()
    if not conexao:
        return render_template('cadastrarConta.html', erro="Erro de conexão com o banco de dados.", sucesso=False)
    
    cursor = conexao.cursor()

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        tipo = request.form['tipo']

        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        existente = cursor.fetchone()

        if existente:
            return render_template('cadastrarConta.html', erro="E-mail já cadastrado.", sucesso=False)

        cursor.execute("""
            INSERT INTO usuarios (nome, email, senha, tipo)
            VALUES (%s, %s, %s, %s)
        """, (nome, email, senha, tipo))
        conexao.commit()

        return render_template('cadastrarConta.html', sucesso=True)

    return render_template('cadastrarConta.html', sucesso=False)


@app.route('/produto/<int:id>')
def pagina_compra(id):
    conexao = conectarBanco()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("SELECT * FROM produtos WHERE id = %s", (id,))
    produto = cursor.fetchone()
    conexao.close()

    if produto is None:
        return "Produto não encontrado", 404

    return render_template('paginacompra.html', produto=produto)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
