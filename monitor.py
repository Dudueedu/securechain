import hashlib, json, os, time
from blockchain.blockchain import registrar_evento

HASH_FILE = "logs/hashes_referencia.json"
DIRETORIO = "documentos"

def calcular_hash_arquivo(caminho):
    sha = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(4096), b""):
            sha.update(bloco)
    return sha.hexdigest()

def inicializar_hashes():
    hashes = {}
    for arq in os.listdir(DIRETORIO):
        caminho = os.path.join(DIRETORIO, arq)
        if os.path.isfile(caminho):
            hashes[arq] = calcular_hash_arquivo(caminho)
    with open(HASH_FILE, "w") as f:
        json.dump(hashes, f, indent=2)
    print(f"{len(hashes)} arquivo(s) monitorado(s).")

def verificar_integridade():
    if not os.path.exists(HASH_FILE):
        print("Inicialize os hashes primeiro.")
        return
    with open(HASH_FILE) as f:
        hashes_ref = json.load(f)

    arquivos_atuais = set(os.listdir(DIRETORIO))
    arquivos_ref = set(hashes_ref.keys())

    for arq in arquivos_atuais - arquivos_ref:
        registrar_evento(f"ALERTA: Arquivo incluido: {arq}")
        print(f"Arquivo novo detectado: {arq}")

    for arq in arquivos_ref - arquivos_atuais:
        registrar_evento(f"ALERTA: Arquivo excluido: {arq}")
        print(f"Arquivo excluido detectado: {arq}")

    for arq in arquivos_atuais & arquivos_ref:
        caminho = os.path.join(DIRETORIO, arq)
        hash_atual = calcular_hash_arquivo(caminho)
        if hash_atual != hashes_ref[arq]:
            registrar_evento(f"ALERTA: Arquivo alterado: {arq}")
            print(f"Arquivo alterado detectado: {arq}")

    print("Verificacao concluida.")

if __name__ == "__main__":
    inicializar_hashes()
    # Criar arquivo de teste
    with open("documentos/teste.txt", "w") as f:
        f.write("documento original")
    inicializar_hashes()
    print("--- Verificando sem alteracoes ---")
    verificar_integridade()
    # Simular alteracao
    with open("documentos/teste.txt", "w") as f:
        f.write("documento ALTERADO")
    print("--- Verificando apos alteracao ---")
    verificar_integridade()
    print("\n--- Monitoramento continuo (Ctrl+C para parar) ---")
    try:
        while True:
            verificar_integridade()
            time.sleep(30)
    except KeyboardInterrupt:
        print("Monitoramento encerrado.")
