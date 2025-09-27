from flask import Flask, render_template, request, redirect, url_for

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

        if email == 'admin@example.com' and senha == '1234':
            return redirect(url_for('index'))
        else:
            return render_template('login.html', errou=True)

    return render_template('login.html', errou=False)

if __name__ == '__main__':
    app.run(debug=True)
