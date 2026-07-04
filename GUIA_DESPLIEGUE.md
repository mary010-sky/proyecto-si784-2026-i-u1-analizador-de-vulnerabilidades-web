# VulnScan Pro — Guía Técnica de Despliegue Nativo en VPS Linux

## Arquitectura del Sistema

```
Internet
    │
    ▼
[Nginx :80/:443]   ← Reverse proxy, SSL, headers seguridad, rate limiting
    │
    ├─── /api/*  ──▶  [FastAPI :8000]  ← Backend Python
    │                      │
    │                      ▼
    │                 [MySQL :3306]   ← Base de datos nativa
    │
    └─── /*      ──▶  [Next.js :3000] ← Frontend React
```

## Requisitos VPS

- Ubuntu 22.04+ o Debian 12+
- 2 vCPU mínimo, 4 recomendado
- 2 GB RAM mínimo, 4 recomendado
- 20 GB disco
- MySQL ya instalado y corriendo
- Puertos 80, 443 abiertos

## Instalación Rápida (1 comando)

```bash
git clone <tu-repo> vulnscan
cd vulnscan
sudo bash deploy.sh
```

El script solicita interactivamente:
- Contraseña para usuario MySQL
- API Key de DeepSeek (opcional)
- Dominio (opcional, usa IP si se omite)

## Instalación Manual Paso a Paso

### 1. Preparar el sistema

```bash
apt-get update
apt-get install -y python3 python3-venv python3-dev \
    nodejs npm nginx mysql-server certbot python3-certbot-nginx \
    build-essential default-libmysqlclient-dev pkg-config
npm install -g pm2
```

### 2. Configurar MySQL

```bash
mysql -u root <<'EOF'
CREATE DATABASE vulnscan CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'vulnuser'@'localhost' IDENTIFIED BY 'TU_PASSWORD_SEGURO';
GRANT ALL PRIVILEGES ON vulnscan.* TO 'vulnuser'@'localhost';
FLUSH PRIVILEGES;
EOF
```

### 3. Desplegar Backend

```bash
mkdir -p /opt/vulnscan/backend
cp -r backend/* /opt/vulnscan/backend/
cd /opt/vulnscan/backend

# Entorno virtual
python3 -m venv venv
venv/bin/pip install -r requirements.txt

# Configurar .env
cp .env.example .env
nano .env  # Editar con tus valores

# Crear tablas (automático al iniciar, pero puedes forzarlo):
venv/bin/python -c "from database import init_db; init_db()"
```

### 4. Servicio systemd para Backend

```bash
cp vulnscan-backend.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable vulnscan-backend
systemctl start vulnscan-backend
systemctl status vulnscan-backend
```

### 5. Desplegar Frontend

```bash
mkdir -p /opt/vulnscan/frontend
cp -r frontend/* /opt/vulnscan/frontend/

# Configurar URL del backend
echo "NEXT_PUBLIC_API_URL=http://127.0.0.1:8000" > /opt/vulnscan/frontend/.env.local

# Compilar
cd /opt/vulnscan/frontend
npm install
npm run build

# Iniciar con PM2
pm2 start "npm start -- -p 3000" --name vulnscan-frontend --cwd /opt/vulnscan/frontend
pm2 save
pm2 startup
```

### 6. Configurar Nginx

```bash
cp nginx.conf /etc/nginx/sites-available/vulnscan
ln -sf /etc/nginx/sites-available/vulnscan /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx
```

### 7. SSL con Let's Encrypt (si tienes dominio)

```bash
certbot --nginx -d tu-dominio.com -d www.tu-dominio.com
# Certbot actualiza nginx.conf automáticamente
systemctl reload nginx
```

### 8. Configurar Firewall

```bash
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable
```

## Variables de Entorno (.env)

| Variable | Descripción | Ejemplo |
|---|---|---|
| `DATABASE_URL` | URL conexión MySQL | `mysql+pymysql://user:pass@localhost:3306/vulnscan` |
| `SECRET_KEY` | Clave JWT (32 bytes hex) | Generar: `openssl rand -hex 32` |
| `DEEPSEEK_API_KEY` | API Key de DeepSeek | `sk-xxxx...` |
| `ALLOWED_ORIGINS` | CORS orígenes permitidos | `https://tu-dominio.com` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Duración tokens JWT | `60` |

## Estructura de Base de Datos

```sql
users          -- Usuarios, roles, auth info
sessions       -- Sesiones JWT activas
scans          -- Escaneos realizados
vulnerabilities -- Hallazgos por escaneo
audit_logs     -- Log de auditoría completo
reports        -- Reportes generados
password_resets -- Tokens de recuperación
```

## Comandos de Mantenimiento

```bash
# Estado de servicios
systemctl status vulnscan-backend
pm2 status

# Logs en tiempo real
journalctl -u vulnscan-backend -f
pm2 logs vulnscan-frontend
tail -f /var/log/nginx/vulnscan_access.log

# Reiniciar
systemctl restart vulnscan-backend
pm2 restart vulnscan-frontend

# Actualizar código
cd /opt/vulnscan
git pull
systemctl restart vulnscan-backend
cd frontend && npm run build
pm2 restart vulnscan-frontend

# Backup MySQL
mysqldump -u vulnuser -p vulnscan > backup_$(date +%Y%m%d).sql

# Ver puertos activos
ss -tlnp | grep -E ":(80|443|8000|3000|3306)"
```

## API Endpoints Principales

```
POST /api/auth/register     Registro de usuario
POST /api/auth/login        Login (OAuth2 form)
GET  /api/auth/me           Perfil del usuario actual
PUT  /api/auth/change-password  Cambiar contraseña

POST /api/scans/            Iniciar nuevo escaneo
GET  /api/scans/            Listar escaneos
GET  /api/scans/{id}        Detalle de escaneo con vulnerabilidades
DELETE /api/scans/{id}      Eliminar escaneo

GET  /api/reports/{id}/json  Reporte en JSON
GET  /api/reports/{id}/html  Reporte HTML descargable
GET  /api/reports/{id}/pdf   Reporte PDF descargable

GET  /api/admin/dashboard   Estadísticas del sistema (admin)
GET  /api/admin/users       Gestión de usuarios (admin)
GET  /api/admin/logs        Logs de auditoría (admin)

GET  /api/modules           Lista de módulos disponibles
GET  /health                Health check
GET  /api/docs              Swagger UI interactivo
```

## Módulos de Escaneo

| ID | Detecta |
|---|---|
| `Headers` | Headers HTTP inseguros, cookies, CORS |
| `SSL` | Certificados SSL/TLS, versiones inseguras |
| `XSS` | Cross-Site Scripting reflejado |
| `SQLi` | SQL Injection (error-based y blind) |
| `CSRF` | Formularios POST sin token CSRF |
| `OpenRedirect` | Redirecciones abiertas |
| `LFI` | Local File Inclusion / Path Traversal |
| `CommandInjection` | Inyección de comandos OS |
| `SSRF` | Server-Side Request Forgery |
| `SensitiveFiles` | Archivos sensibles expuestos (.env, .git, etc.) |
| `HttpMethods` | Métodos HTTP peligrosos (PUT, DELETE, TRACE) |
| `ErrorDisclosure` | Mensajes de error detallados |
| `Crawling` | Descubrimiento de URLs y endpoints |

## Sistema de Roles

| Rol | Permisos |
|---|---|
| `admin` | Acceso total: usuarios, logs, todos los escaneos |
| `analyst` | Escaneos propios y de todos, sin gestión de usuarios |
| `user` | Solo sus propios escaneos |

**Nota:** El primer usuario registrado es automáticamente `admin`.

## Seguridad

- Contraseñas hasheadas con bcrypt (cost factor 12)
- JWT con expiración configurable
- Rate limiting en login (5 intentos/min) y API general
- Bloqueo automático tras 5 intentos fallidos (15 minutos)
- Headers de seguridad en Nginx y FastAPI
- CORS restringido a orígenes configurados
- Logs de auditoría de todas las acciones
- MySQL con usuario dedicado de mínimos privilegios
- Archivos .env con chmod 600
- systemd con NoNewPrivileges y PrivateTmp

## Solución de Problemas Comunes

**Backend no inicia:**
```bash
journalctl -u vulnscan-backend -n 50
# Comprobar MySQL: mysql -u vulnuser -p vulnscan -e "SELECT 1"
# Comprobar .env: cat /opt/vulnscan/backend/.env
```

**Error de conexión MySQL:**
```bash
mysql -u root -e "SHOW GRANTS FOR 'vulnuser'@'localhost';"
# Verificar DATABASE_URL en .env
```

**Frontend no carga:**
```bash
pm2 logs vulnscan-frontend --lines 50
# Verificar NEXT_PUBLIC_API_URL en .env.local
```

**Nginx 502 Bad Gateway:**
```bash
# Verificar que backend esté corriendo
curl http://127.0.0.1:8000/health
# Verificar logs nginx
tail -f /var/log/nginx/vulnscan_error.log
```

**DeepSeek AI no funciona:**
- Verificar `DEEPSEEK_API_KEY` en `.env`
- El sistema funciona sin IA (usa análisis local como fallback)
- Verificar conectividad: `curl https://api.deepseek.com/v1/models -H "Authorization: Bearer TU_KEY"`
