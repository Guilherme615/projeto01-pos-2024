import os
from authlib.integrations.flask_client import OAuth
from flask import session
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env, caso ele exista
if os.path.isfile(".env"):
    load_dotenv()

# Função para registrar o cliente OAuth no SUAP
def oauthRegister(oauth, **kwargs):
    return oauth.register(
        name=kwargs["name"],
        client_id=os.getenv("CLIENT_ID"),  # Carrega o CLIENT_ID do .env
        client_secret=os.getenv("CLIENT_SECRET"),  # Carrega o CLIENT_SECRET do .env
        api_base_url=kwargs["api_base_url"],
        request_token_url=kwargs["request_token_url"],
        access_token_method=kwargs["access_token_method"],
        access_token_url=kwargs["access_token_url"],
        authorize_url=kwargs["authorize_url"],
        fetch_token=lambda: session.get(kwargs["token"])  # Busca o token armazenado na sessão
    )

# Classe User para interagir com a API do SUAP
class User:
    def __init__(self, oauth):
        self.oauth = oauth

    # Método para buscar os dados do usuário
    def fetchUserDados(self):
        return self.oauth.suap.get('v2/minhas-informacoes/meus-dados')

    # Método para buscar o boletim do usuário para um ano letivo específico
    def fetchUserBoletim(self, ano_letivo):
        return self.oauth.suap.get(f'/api/v2/minhas-informacoes/boletim/{ano_letivo}/1/')
