# 🚀 Inicio Rápido con PostgreSQL
## Portales del Quinto Sol - Setup en 5 Pasos

---

## ⚡ Setup Rápido (15 minutos)

### Paso 1: Instalar PostgreSQL

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
pip install psycopg2-binary
```

#### macOS
```bash
brew install postgresql@15
brew services start postgresql@15
pip install psycopg2-binary
```

#### Windows
1. Descargar: https://www.postgresql.org/download/windows/
2. Ejecutar instalador
3. `pip install psycopg2-binary`

---

### Paso 2: Ejecutar Setup Automático ✨

```bash
python3 setup_postgresql.py
```

Este script interactivo:
- ✅ Verifica PostgreSQL instalado
- ✅ Crea archivo `.env` con tu configuración
- ✅ Crea base de datos `quinto_sol`
- ✅ Crea usuario `quinto_sol_user`
- ✅ Configura permisos
- ✅ Verifica conexión

**Output esperado:**
```
SETUP POSTGRESQL - PORTALES DEL QUINTO SOL
==========================================================

🔍 Verificando PostgreSQL...
✅ PostgreSQL instalado: PostgreSQL 15.x

CONFIGURACIÓN POSTGRESQL
==========================================================

Ingresa los datos de conexión PostgreSQL:
Host [localhost]:
Puerto [5432]:
Nombre base de datos [quinto_sol]:
Usuario [quinto_sol_user]:
Password: ****

✅ Archivo .env creado

CREANDO BASE DE DATOS Y USUARIO
==========================================================

Password de postgres: ****

✅ Usuario 'quinto_sol_user' creado
✅ Base de datos 'quinto_sol' creada
✅ Permisos configurados

VERIFICANDO CONEXIÓN
==========================================================

✅ Conexión exitosa!
   PostgreSQL 15.4 ...

✅ SETUP COMPLETADO
```

---

### Paso 3: Cargar Variables de Entorno

Cada vez que abras nueva terminal:

```bash
# Opción 1: Export manual
export $(cat .env | grep -v '^#' | xargs)

# Opción 2: Source
source <(cat .env | grep -v '^#' | sed 's/^/export /')

# Verificar
echo $DB_TYPE  # Debe mostrar: postgres
```

**TIP:** Agregar a tu `~/.bashrc` o `~/.zshrc`:

```bash
# Agregar al final de ~/.bashrc
if [ -f ~/5Soles/.env ]; then
    export $(cat ~/5Soles/.env | grep -v '^#' | xargs)
fi
```

---

### Paso 4: Verificar Conexión

```bash
python3 database_connector.py
```

**Output esperado:**
```
Configuración actual:
  DB_TYPE: postgres
  PG_HOST: localhost
  PG_PORT: 5432
  PG_DATABASE: quinto_sol
  PG_USER: quinto_sol_user

PRUEBA DE CONEXIÓN A BASE DE DATOS
======================================================================

Tipo de BD configurado: postgres
✅ Conectado a PostgreSQL: quinto_sol_user@localhost:5432/quinto_sol
PostgreSQL versión: PostgreSQL 15.4 ...

Tablas encontradas: 0

✅ Conexión exitosa
```

---

### Paso 5: Ejecutar Simulación 🎮

```bash
# Simulación completa (creará schemas automáticamente)
python3 simulacion_mundo_completo.py
```

El script:
1. ✅ Verifica PostgreSQL conectado
2. ✅ Crea todos los schemas (73 tablas)
3. ✅ Ejecuta sistemas principales
4. ✅ Ejecuta sistemas adicionales
5. ✅ Genera conversaciones NPC
6. ✅ Crea estadísticas finales
7. ✅ Optimiza para producción

**Duración estimada:** 3-8 horas
**Resultado:** 270,000 NPCs con 1500 años de historia

---

## 🔧 Setup Manual (Si prefieres control total)

### 1. Crear BD manualmente

```bash
sudo -u postgres psql

-- Dentro de psql:
CREATE DATABASE quinto_sol;
CREATE USER quinto_sol_user WITH ENCRYPTED PASSWORD 'tu_password';
GRANT ALL PRIVILEGES ON DATABASE quinto_sol TO quinto_sol_user;

-- Conectar a la BD
\c quinto_sol

-- Dar permisos en schema public (PostgreSQL 15+)
GRANT ALL ON SCHEMA public TO quinto_sol_user;
GRANT ALL ON ALL TABLES IN SCHEMA public TO quinto_sol_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO quinto_sol_user;

\q
```

### 2. Crear .env manualmente

```bash
cat > .env << 'EOF'
DB_TYPE=postgres
PG_HOST=localhost
PG_PORT=5432
PG_DATABASE=quinto_sol
PG_USER=quinto_sol_user
PG_PASSWORD=tu_password
EOF
```

### 3. Exportar variables

```bash
export $(cat .env | grep -v '^#' | xargs)
```

### 4. Verificar y ejecutar

```bash
python3 database_connector.py
python3 simulacion_mundo_completo.py
```

---

## 📊 Monitoreo PostgreSQL

### Ver Tamaño de BD

```bash
# Desde terminal
psql -U quinto_sol_user -d quinto_sol -c "SELECT pg_size_pretty(pg_database_size('quinto_sol'));"

# Desde Python
python3 -c "
from database_connector import DatabaseConnector
db = DatabaseConnector()
db.connect()
db.execute(\"SELECT pg_size_pretty(pg_database_size('quinto_sol'))\")
print(db.fetchone()[0])
"
```

### Ver Tablas Más Grandes

```sql
-- Conectar: psql -U quinto_sol_user -d quinto_sol

SELECT
    tablename,
    pg_size_pretty(pg_total_relation_size('public.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size('public.'||tablename) DESC
LIMIT 10;
```

### Monitorear Conexiones Activas

```sql
SELECT count(*) FROM pg_stat_activity
WHERE datname = 'quinto_sol';
```

---

## 🔒 Seguridad

### Cambiar Password de Usuario

```bash
sudo -u postgres psql

ALTER USER quinto_sol_user WITH PASSWORD 'nuevo_password_seguro';
```

No olvides actualizar `.env`

### Conexión Remota (Si BD está en otro servidor)

En `.env`:
```bash
PG_HOST=192.168.1.100  # IP del servidor
PG_SSLMODE=require     # Forzar SSL
```

Editar `/etc/postgresql/15/main/postgresql.conf`:
```
listen_addresses = '*'
```

Editar `/etc/postgresql/15/main/pg_hba.conf`:
```
host    quinto_sol    quinto_sol_user    0.0.0.0/0    md5
```

Reiniciar:
```bash
sudo systemctl restart postgresql
```

---

## 🐛 Troubleshooting

### Error: "psql: command not found"

PostgreSQL no está en PATH.

**Ubuntu:**
```bash
sudo apt install postgresql-client
```

**macOS:**
```bash
export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"
```

### Error: "FATAL: Peer authentication failed"

Editar `/etc/postgresql/15/main/pg_hba.conf`:

Cambiar:
```
local   all   all   peer
```

Por:
```
local   all   all   md5
```

Reiniciar:
```bash
sudo systemctl restart postgresql
```

### Error: "could not connect to server"

PostgreSQL no está corriendo.

**Ubuntu:**
```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**macOS:**
```bash
brew services start postgresql@15
```

### Error: "permission denied for schema public"

```bash
sudo -u postgres psql -d quinto_sol

GRANT ALL ON SCHEMA public TO quinto_sol_user;
GRANT ALL ON ALL TABLES IN SCHEMA public TO quinto_sol_user;
```

---

## ✅ Checklist de Verificación

Antes de ejecutar la simulación:

- [ ] PostgreSQL instalado y corriendo
- [ ] `psycopg2-binary` instalado (`pip install psycopg2-binary`)
- [ ] Base de datos `quinto_sol` creada
- [ ] Usuario `quinto_sol_user` creado con permisos
- [ ] Archivo `.env` existe con configuración correcta
- [ ] Variables de entorno exportadas
- [ ] `python3 database_connector.py` funciona ✅
- [ ] `.env` agregado a `.gitignore`

---

## 🚀 Comandos Útiles Rápidos

```bash
# Verificar servicio PostgreSQL
sudo systemctl status postgresql

# Iniciar PostgreSQL
sudo systemctl start postgresql

# Conectar a BD
psql -U quinto_sol_user -d quinto_sol

# Ver configuración actual
python3 -c "import os; [print(f'{k}={v}') for k,v in os.environ.items() if k.startswith('PG_') or k == 'DB_TYPE']"

# Backup rápido
pg_dump -U quinto_sol_user quinto_sol > backup_$(date +%Y%m%d_%H%M%S).sql

# Restaurar backup
psql -U quinto_sol_user quinto_sol < backup.sql

# Limpiar y optimizar
psql -U quinto_sol_user -d quinto_sol -c "VACUUM ANALYZE;"
```

---

## 📚 Siguiente: Ejecutar Simulación

Una vez completado el setup:

1. **Simulación completa:**
   ```bash
   python3 simulacion_mundo_completo.py
   ```

2. **O paso a paso:**
   ```bash
   # Sistemas principales
   python3 simulacion_completa_1500_3000.py

   # Sistemas adicionales
   python3 sistemas_adicionales_integrados.py

   # Conversaciones NPC
   python3 sistema_conversaciones_npcs.py
   ```

3. **Ver estadísticas:**
   ```bash
   cat ESTADISTICAS_MUNDO_3000.md
   ```

4. **Servidor de tiempo real:**
   ```bash
   python3 servidor_tiempo_juego.py
   ```

---

## 💡 Tips de Performance

### Para Simulación

PostgreSQL es MÁS RÁPIDO que SQLite para operaciones masivas:

- Inserts en batch: 3-5x más rápido
- Queries complejas: 2-4x más rápido
- Joins grandes: 5-10x más rápido

### Configuración Óptima (postgresql.conf)

```ini
# Para servidor con 16GB RAM
shared_buffers = 4GB
effective_cache_size = 12GB
work_mem = 64MB
maintenance_work_mem = 1GB

# Para SSD
random_page_cost = 1.1
effective_io_concurrency = 200
```

Reiniciar después de cambios:
```bash
sudo systemctl restart postgresql
```

---

_Última actualización: 2025_
_Portales del Quinto Sol - MMORPG_
