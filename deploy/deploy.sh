#!/bin/bash
# YardMaster — Deploy Script for Ubuntu + Nginx
# Run as root or with sudo

set -e
APP_DIR="/var/www/yardmaster"
REPO_DIR="$(pwd)"   # run from the project root

echo "=== 1. Install system dependencies ==="
apt update
apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx

echo "=== 2. Create Postgres database and user ==="
sudo -u postgres psql <<EOF
DO \$\$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'yardmaster_user') THEN
    CREATE USER yardmaster_user WITH PASSWORD 'CHANGE_THIS_PASSWORD';
  END IF;
END
\$\$;
CREATE DATABASE yardmaster OWNER yardmaster_user;
EOF

echo "=== 3. Copy project files ==="
mkdir -p $APP_DIR
cp -r $REPO_DIR/* $APP_DIR/
mkdir -p /var/www/yardmaster/staticfiles

echo "=== 4. Create virtual environment ==="
python3 -m venv $APP_DIR/venv
$APP_DIR/venv/bin/pip install --upgrade pip
$APP_DIR/venv/bin/pip install -r $APP_DIR/requirements.txt

echo "=== 5. Set up .env ==="
if [ ! -f $APP_DIR/.env ]; then
  cp $APP_DIR/.env.example $APP_DIR/.env
  echo ""
  echo "⚠️  Edit $APP_DIR/.env with your real values before continuing!"
  echo "   Especially: SECRET_KEY, DB_PASSWORD, ALLOWED_HOSTS"
  exit 1
fi

echo "=== 6. Django setup ==="
cd $APP_DIR
venv/bin/python manage.py migrate
venv/bin/python manage.py collectstatic --noinput

echo "=== 7. Create superuser ==="
echo "Create your admin user:"
venv/bin/python manage.py createsuperuser

echo "=== 8. Set permissions ==="
chown -R www-data:www-data $APP_DIR

echo "=== 9. Nginx config ==="
cp $APP_DIR/deploy/nginx.conf /etc/nginx/sites-available/yardmaster
ln -sf /etc/nginx/sites-available/yardmaster /etc/nginx/sites-enabled/yardmaster
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx

echo "=== 10. Systemd service ==="
cp $APP_DIR/deploy/yardmaster.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable yardmaster
systemctl start yardmaster

echo ""
echo "✅ YardMaster is running!"
echo "   Check status: systemctl status yardmaster"
echo "   View logs:    journalctl -u yardmaster -f"
echo ""
echo "📝 To add more users:"
echo "   cd $APP_DIR && venv/bin/python manage.py createsuperuser"
echo "   Or use /admin/ in the browser"
