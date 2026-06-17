import bcrypt, json, os
from datetime import datetime

USUARIOS_FILE = "usuarios/usuarios.json"

def carregar_usuarios():
    if not os.path.exists(USUARIOS_FILE):
        return {}
    with open(USUARIOS_FILE) as f:
        return json.load(f)

def salvar_usuarios(dados):
    with open(USUARIOS_FILE, "w") as f:
        json.dump(dados, f, indent=2)

def cadastrar_usuario(nome, senha, perfil):
    usuarios = carregar_usuarios()
    if nome in usuarios:
        print("Usuário já existe.")
        return
    salt = bcrypt.gensalt()
    hash_senha = bcrypt.hashpw(senha.encode(), salt).decode()
    usuarios[nome] = {"hash": hash_senha, "perfil": perfil}
    salvar_usuarios(usuarios)
    from blockchain.blockchain import registrar_evento
    registrar_evento(f"Usuário criado: {nome} (perfil: {perfil})")
    print(f"Usuário '{nome}' cadastrado com sucesso.")

def login(nome, senha):
    usuarios = carregar_usuarios()
    from blockchain.blockchain import registrar_evento
    if nome not in usuarios:
        registrar_evento(f"Tentativa de acesso negada: usuário '{nome}' não existe")
        print("Usuário não encontrado.")
        return None
    hash_armazenado = usuarios[nome]["hash"].encode()
    if bcrypt.checkpw(senha.encode(), hash_armazenado):
        registrar_evento(f"Login realizado: {nome} ({datetime.now().isoformat()})")
        print(f"Login bem-sucedido! Perfil: {usuarios[nome]['perfil']}")
        return usuarios[nome]["perfil"]
    else:
        registrar_evento(f"Tentativa de acesso negada: senha incorreta para '{nome}'")
        print("Senha incorreta.")
        return None

def listar_usuarios():
    usuarios = carregar_usuarios()
    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return
    print("\n=== Usuários cadastrados ===")
    for nome, dados in usuarios.items():
        print(f"  - {nome} (perfil: {dados['perfil']})")
    print()

if __name__ == "__main__":
    cadastrar_usuario("admin", "Senha@123", "admin")
    listar_usuarios()
    login("admin", "Senha@123")
