import hashlib, json, os
from datetime import datetime

CHAIN_FILE = os.path.join(os.path.dirname(__file__), "chain.json")

def carregar_chain():
    if not os.path.exists(CHAIN_FILE):
        return []
    with open(CHAIN_FILE) as f:
        conteudo = f.read().strip()
        if not conteudo:
            return []
        return json.loads(conteudo)

def salvar_chain(chain):
    with open(CHAIN_FILE, "w") as f:
        json.dump(chain, f, indent=2)

def calcular_hash(bloco):
    conteudo = f"{bloco['id']}{bloco['timestamp']}{bloco['evento']}{bloco['hash_anterior']}"
    return hashlib.sha256(conteudo.encode()).hexdigest()

def registrar_evento(evento):
    chain = carregar_chain()
    hash_anterior = chain[-1]["hash_atual"] if chain else "0" * 64
    bloco = {
        "id": len(chain) + 1,
        "timestamp": datetime.now().isoformat(),
        "evento": evento,
        "hash_anterior": hash_anterior,
        "hash_atual": ""
    }
    bloco["hash_atual"] = calcular_hash(bloco)
    chain.append(bloco)
    salvar_chain(chain)
    print(f"[Blockchain] Bloco #{bloco['id']} registrado: {evento}")

def validar_chain():
    chain = carregar_chain()
    if not chain:
        print("Blockchain vazia.")
        return True
    erros = []
    for i, bloco in enumerate(chain):
        hash_recalculado = calcular_hash(bloco)
        if hash_recalculado != bloco["hash_atual"]:
            erros.append(f"ALERTA: Bloco #{bloco['id']} adulterado!")
        if i > 0:
            if bloco["hash_anterior"] != chain[i-1]["hash_atual"]:
                erros.append(f"ALERTA: Encadeamento quebrado no bloco #{bloco['id']}!")
    if erros:
        for e in erros:
            print(e)
    else:
        print(f"Blockchain valida. {len(chain)} blocos verificados com sucesso.")
    return len(erros) == 0

def listar_eventos():
    chain = carregar_chain()
    print(f"\n=== Blockchain — {len(chain)} blocos ===")
    for bloco in chain:
        print(f"  #{bloco['id']} [{bloco['timestamp']}] {bloco['evento']}")
    print()

if __name__ == "__main__":
    registrar_evento("Sistema iniciado")
    validar_chain()
