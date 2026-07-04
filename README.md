# YardMaster 🚛

Transport Management System — Django + PostgreSQL + Nginx

## Estrutura do projeto

```
yardmaster/
├── yardmaster/          # Configurações Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── transport/           # App principal
│   ├── models.py        # Modelo Load (tabela de cargas)
│   ├── views.py         # Views + API inline editing
│   ├── urls.py
│   └── admin.py
├── templates/
│   ├── registration/
│   │   └── login.html
│   └── transport/
│       └── load_list.html
├── deploy/
│   ├── deploy.sh        # Script de deploy completo
│   ├── nginx.conf       # Config Nginx
│   └── yardmaster.service  # Systemd service
├── requirements.txt
├── manage.py
└── .env.example
```

## Deploy no Ubuntu (passo a passo)

### 1. Enviar arquivos para o servidor

```bash
# No seu computador local — copie o projeto pro servidor
scp -r ./yardmaster user@seu-servidor:/tmp/yardmaster

# Ou via git
git clone <seu-repo> /tmp/yardmaster
```

### 2. Rodar o script de deploy

```bash
cd /tmp/yardmaster
sudo bash deploy/deploy.sh
```

O script faz tudo automaticamente:
- Instala Python, Postgres, Nginx
- Cria o banco de dados
- Configura o ambiente virtual
- Roda as migrations
- Configura Nginx + systemd

### 3. Editar o .env

```bash
sudo nano /var/www/yardmaster/.env
```

Preencha:
```
SECRET_KEY=gere-uma-chave-aqui   # python3 -c "import secrets; print(secrets.token_hex(32))"
DEBUG=False
ALLOWED_HOSTS=seu-ip-ou-dominio

DB_NAME=yardmaster
DB_USER=yardmaster_user
DB_PASSWORD=a-senha-que-voce-definiu
DB_HOST=localhost
DB_PORT=5432
```

### 4. Reiniciar o serviço

```bash
sudo systemctl restart yardmaster
```

---

## Gerenciar usuários

### Criar usuário admin (pode editar)

```bash
cd /var/www/yardmaster
venv/bin/python manage.py createsuperuser
```

### Criar usuário viewer (só visualiza)

Acesse `/admin/` com o superuser e crie um usuário **sem** marcar `Staff status`.

---

## Funcionalidades

| Feature | Admin | Viewer |
|---|---|---|
| Ver tabela | ✅ | ✅ |
| Filtros e busca | ✅ | ✅ |
| Export CSV | ✅ | ✅ |
| Editar células (duplo clique) | ✅ | ❌ |
| Adicionar linha | ✅ | ❌ |
| Excluir linhas | ✅ | ❌ |

---

## Comandos úteis

```bash
# Ver logs em tempo real
journalctl -u yardmaster -f

# Reiniciar após mudanças
sudo systemctl restart yardmaster

# Aplicar migrations após mudar models.py
cd /var/www/yardmaster
venv/bin/python manage.py makemigrations
venv/bin/python manage.py migrate
sudo systemctl restart yardmaster
```

---

## HTTPS (recomendado)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```
