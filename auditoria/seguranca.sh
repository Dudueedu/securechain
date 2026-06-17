#!/bin/bash
echo "=== Auditoria de Segurança ==="
echo "--- Portas abertas ---"
nmap -sV localhost
echo "--- Serviços em escuta ---"
ss -tulpn
echo "--- Permissões críticas ---"
ls -la /etc/passwd /etc/shadow
echo "--- Usuários com shell ativo ---"
cat /etc/passwd | grep -v nologin | grep -v false
echo "=== Concluído ==="
