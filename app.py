from flask import Flask, redirect, url_for, session, request, render_template
from authlib.integrations.flask_client import OAuth
from views.main import oauthRegister, User

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'

# Configurando OAuth
oauth = OAuth(app)
oauthRegister(oauth, 
              name="suap", 
              api_base_url="https://suap.ifrn.edu.br/api/", 
              request_token_url=None, 
              access_token_method="POST", 
              access_token_url="https://suap.ifrn.edu.br/o/token/", 
              authorize_url="https://suap.ifrn.edu.br/o/authorize/", 
              token="suap_token")

# Rota principal (Index)
@app.route('/')
def index():
    if 'suap_token' in session:  # Verifica se o usuário está logado
        user = User(oauth)  # Instância da classe User
        data = user.fetchUserDados()  # Busca os dados do usuário
        return render_template('user.html', data=data.json())  # Renderiza o template user.html com os dados
    else:
        return render_template('index.html')  # Renderiza a página de login (index.html) se não estiver logado

# Rota de login
@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)  # Define o redirecionamento após a autenticação
    return oauth.suap.authorize_redirect(redirect_uri)  # Redireciona para a página de autorização do SUAP

# Rota de logout
@app.route('/logout')
def logout():
    session.pop('suap_token', None)  # Remove o token da sessão
    return redirect(url_for('index'))  # Redireciona para a página inicial

# Rota de autorização (callback após login OAuth)
@app.route('/login/authorized')
def auth():
    token = oauth.suap.authorize_access_token()  # Autoriza e recebe o token de acesso
    session['suap_token'] = token  # Armazena o token na sessão
    return redirect(url_for('index'))  # Redireciona para a página inicial

# Rota para visualização de boletins
@app.route("/boletim", methods=["GET"])
def boletim():
    if 'suap_token' in session:  # Verifica se o usuário está logado
        user = User(oauth)  # Instância da classe User
        ano_letivo = request.args.get('ano_letivo')  # Obtém o ano letivo a partir dos parâmetros da URL
        if ano_letivo:
            data = user.fetchUserBoletim(ano_letivo)  # Busca o boletim para o ano letivo especificado
            return render_template("boletim.html", data=data.json())  # Renderiza o boletim com os dados
        return render_template("boletim.html")  # Exibe o formulário para selecionar o ano letivo
    else:
        return redirect(url_for('index'))  # Redireciona para a página inicial se não estiver logado

# Inicia o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
