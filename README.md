# SecureChain Audit

Plataforma de auditoria baseada em blockchain para segurança de documentos sigilosos.

## Integrantes
- Nome 1 — Módulo de autenticação e usuários
- Nome 2 — Blockchain e validação
- Nome 3 — Backup, auditoria e monitoramento

## Tecnologias
- Python 3.13
- Debian 13
- bcrypt, hashlib, json, subprocess
- OpenSSL (AES-256)
- Git + GitHub

## Estrutura
securechain/

├── blockchain/

│   ├── blockchain.py   # lógica da blockchain

│   └── chain.json      # persistência dos blocos

├── auditoria/

│   ├── auditor.py      # coleta who, last, ss, ip a

│   └── relatorios/     # relatórios gerados

├── backup/

│   └── backup.sh       # compactação + AES-256

├── logs/               # hashes de referência

├── documentos/         # arquivos monitorados

├── usuarios/           # senhas em hash bcrypt

├── auth.py             # autenticação e cadastro

├── monitor.py          # integridade SHA-256

└── README.md

## Instalação
```bash
sudo apt install python3 python3-pip git openssl nmap -y
pip3 install bcrypt --break-system-packages
git clone https://github.com/Dudueedu/securechain.git
cd securechain
```

## Como usar

### Autenticação
```bash
python3 auth.py
```

### Monitorar arquivos
```bash
python3 monitor.py
```

### Validar blockchain
```bash
python3 -c "from blockchain.blockchain import validar_chain; validar_chain()"
```

### Gerar relatório de auditoria
```bash
python3 auditoria/auditor.py
```

### Executar backup criptografado
```bash
cd backup && bash backup.sh
```

## Segurança
- Senhas armazenadas com bcrypt + salt
- Integridade de arquivos via SHA-256
- Eventos registrados em blockchain imutável
- Backup criptografado com AES-256
- Análise de vulnerabilidades com nmap e ss

## Análise de Segurança
- Porta 80 (Apache): risco médio — HTTP sem criptografia
- Porta 631 (CUPS): risco baixo — restrito ao localhost
- /etc/shadow: permissões corretas (640) — apenas root acessa
- Avahi/mDNS: desabilitável se rede local não for necessária
