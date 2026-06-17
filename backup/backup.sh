#!/bin/bash

DATA=$(date +"%Y%m%d_%H%M%S")
DIR_DOCS="../documentos"
BACKUP_TAR="/tmp/backup_$DATA.tar.gz"
BACKUP_ENC="backup_$DATA.tar.gz.enc"
LOG="../logs/backup.log"
SENHA="SenhaAES256Forte"

echo "[$DATA] Iniciando backup..." | tee -a "$LOG"

# Compactar
tar -czf "$BACKUP_TAR" "$DIR_DOCS"

# Criptografar com AES-256
openssl enc -aes-256-cbc -salt -pbkdf2 \
  -in "$BACKUP_TAR" \
  -out "$BACKUP_ENC" \
  -pass pass:"$SENHA"

# Remover arquivo temporário
rm "$BACKUP_TAR"

TAMANHO=$(du -sh "$BACKUP_ENC" | cut -f1)
echo "[$DATA] Backup concluido: $BACKUP_ENC ($TAMANHO)" | tee -a "$LOG"

# Registrar na blockchain
python3 -c "
import sys
sys.path.insert(0, '..')
from blockchain.blockchain import registrar_evento
registrar_evento('Backup executado: $BACKUP_ENC ($TAMANHO)')
"

echo "[$DATA] Evento registrado na blockchain." | tee -a "$LOG"
