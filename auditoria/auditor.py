import subprocess, os
from datetime import datetime

RELATORIOS = os.path.join(os.path.dirname(__file__), "relatorios")

def coletar_dados():
    data = datetime.now().strftime("%Y%m%d_%H%M%S")
    arquivo = os.path.join(RELATORIOS, f"relatorio_{data}.txt")

    comandos = {
        "Usuarios conectados (who)": "who",
        "Historico de logins (last)": "last -n 20",
        "Portas em escuta (ss)": "ss -tulpn",
        "Interfaces de rede (ip a)": "ip a",
    }

    with open(arquivo, "w") as f:
        f.write(f"=== Relatorio de Auditoria - {data} ===\n\n")
        for titulo, cmd in comandos.items():
            f.write(f"--- {titulo} ---\n")
            resultado = subprocess.run(cmd.split(), capture_output=True, text=True)
            f.write(resultado.stdout or "(sem saida)\n")
            f.write("\n")

    print(f"Relatorio salvo em: {arquivo}")

    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    from blockchain.blockchain import registrar_evento
    registrar_evento(f"Relatorio de auditoria gerado: relatorio_{data}.txt")

if __name__ == "__main__":
    coletar_dados()

