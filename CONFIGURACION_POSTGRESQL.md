# Configuración PostgreSQL
## Portales del Quinto Sol - MMORPG

---

## 🐘 Por qué PostgreSQL

El sistema soporta tanto **SQLite** (desarrollo/testing) como **PostgreSQL** (producción).

### Ventajas de PostgreSQL para producción:

✅ **Concurrencia:** Miles de jugadores simultáneos
✅ **Performance:** Optimizado para queries complejas
✅ **Integridad:** ACID completo, transacciones robustas
✅ **Escalabilidad:** Manejo de millones de registros
✅ **JSON nativo:** Mejor manejo de metadata compleja
✅ **Índices avanzados:** GIN, GIST para búsquedas rápidas

---

## 📦 Instalación PostgreSQL

### Ubuntu/Debian

```bash
# Instalar PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib

# Instalar driver Python
pip install psycopg2-binary
```

### macOS (Homebrew)

```bash
brew install postgresql@15
brew services start postgresql@15

pip install psycopg2-binary
```

### Windows

1. Descargar instalador: https://www.postgresql.org/download/windows/
2. Ejecutar instalador
3. Instalar driver: `pip install psycopg2-binary`

---

## 🔧 Configuración Inicial

### 1. Crear Base de Datos

```bash
# Conectar a PostgreSQL
sudo -u postgres psql

# Dentro de psql:
CREATE DATABASE quinto_sol;
CREATE USER quinto_sol_user WITH ENCRYPTED PASSWORD 'tu_password_seguro';
GRANT ALL PRIVILEGES ON DATABASE quinto_sol TO quinto_sol_user;

# Dar permisos al schema public (PostgreSQL 15+)
\c quinto_sol
GRANT ALL ON SCHEMA public TO quinto_sol_user;
GRANT ALL ON ALL TABLES IN SCHEMA public TO quinto_sol_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO quinto_sol_user;

\q
```

### 2. Configurar Variables de Entorno

Crea archivo `.env` en el directorio del proyecto:

```bash
# .env
DB_TYPE=postgres
PG_HOST=localhost
PG_PORT=5432
PG_DATABASE=quinto_sol
PG_USER=quinto_sol_user
PG_PASSWORD=tu_password_seguro
```

O exporta directamente:

```bash
export DB_TYPE=postgres
export PG_HOST=localhost
export PG_PORT=5432
export PG_DATABASE=quinto_sol
export PG_USER=quinto_sol_user
export PG_PASSWORD=tu_password_seguro
```

### 3. Verificar Conexión

```bash
python3 database_connector.py
```

Deberías ver:

```
✅ Conectado a PostgreSQL: quinto_sol_user@localhost:5432/quinto_sol
PostgreSQL versión: PostgreSQL 15.x...
```

---

## 🔄 Migración de SQLite a PostgreSQL

### Método 1: Usar pgloader (Recomendado)

```bash
# Instalar pgloader
sudo apt install pgloader  # Ubuntu/Debian
brew install pgloader      # macOS

# Migrar
pgloader quinto_sol.db postgresql://quinto_sol_user:password@localhost/quinto_sol
```

### Método 2: Export/Import Manual

```bash
# 1. Exportar schemas de SQLite
sqlite3 quinto_sol.db .schema > schema_sqlite.sql

# 2. Convertir a PostgreSQL (ajustar manualmente):
#    - AUTOINCREMENT → SERIAL
#    - INTEGER PRIMARY KEY → SERIAL PRIMARY KEY
#    - Tipos de datos específicos

# 3. Exportar datos
sqlite3 quinto_sol.db .dump > data_sqlite.sql

# 4. Importar a PostgreSQL (después de ajustes)
psql -U quinto_sol_user -d quinto_sol -f schema_postgres.sql
psql -U quinto_sol_user -d quinto_sol -f data_postgres.sql
```

### Método 3: Script Python Personalizado

Usa el script incluido:

```bash
python3 migrar_sqlite_a_postgres.py
```

---

## ⚙️ Ajustes en Schemas para PostgreSQL

### Cambios Necesarios

```sql
-- SQLite
CREATE TABLE personas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ...
);

-- PostgreSQL
CREATE TABLE personas (
    id SERIAL PRIMARY KEY,
    ...
);
```

### BOOLEAN vs INTEGER

```sql
-- SQLite usa INTEGER (0/1)
vivo INTEGER DEFAULT 1

-- PostgreSQL tiene BOOLEAN nativo
vivo BOOLEAN DEFAULT TRUE
```

### JSON

```sql
-- SQLite: TEXT
metadata TEXT  -- JSON como string

-- PostgreSQL: JSON/JSONB
metadata JSONB  -- JSON binario, indexable
```

---

## 🚀 Ejecutar Simulación con PostgreSQL

### 1. Configurar entorno

```bash
export DB_TYPE=postgres
# ... otras variables
```

### 2. Aplicar schemas

```bash
# Los scripts detectarán automáticamente PostgreSQL
python3 simulacion_completa_1500_3000.py
```

### 3. Ejecutar sistemas adicionales

```bash
python3 sistemas_adicionales_integrados.py
```

### 4. Ejecutar simulación mundo completo

```bash
python3 simulacion_mundo_completo.py
```

### 5. Servidor de tiempo real

```bash
python3 servidor_tiempo_juego.py
```

---

## 🔍 Monitoreo y Optimización

### Ver Tamaño de Base de Datos

```sql
SELECT
    pg_size_pretty(pg_database_size('quinto_sol')) as size;
```

### Ver Tablas Más Grandes

```sql
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
LIMIT 10;
```

### Analizar Performance

```sql
-- Vacuum (limpieza)
VACUUM ANALYZE;

-- Ver queries lentas
SELECT
    query,
    calls,
    total_time,
    mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;
```

### Crear Índices Adicionales

```sql
-- Índice GIN para búsquedas en JSONB
CREATE INDEX idx_personas_metadata_gin ON personas USING GIN (metadata);

-- Índice parcial para personas vivas
CREATE INDEX idx_personas_vivos ON personas(especie_id)
WHERE año_muerte IS NULL;

-- Índice compuesto
CREATE INDEX idx_personas_año_especie ON personas(año_nacimiento, especie_id);
```

---

## 🔐 Seguridad

### Conexión Segura (SSL)

```bash
# En .env
PG_SSLMODE=require
```

```python
# En código
conn = psycopg2.connect(
    ...,
    sslmode='require'
)
```

### Roles y Permisos

```sql
-- Usuario solo lectura (para analytics)
CREATE USER quinto_sol_readonly WITH ENCRYPTED PASSWORD 'password';
GRANT CONNECT ON DATABASE quinto_sol TO quinto_sol_readonly;
GRANT USAGE ON SCHEMA public TO quinto_sol_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO quinto_sol_readonly;

-- Usuario para servidor de juego (sin DROP)
CREATE USER quinto_sol_game WITH ENCRYPTED PASSWORD 'password';
GRANT CONNECT ON DATABASE quinto_sol TO quinto_sol_game;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO quinto_sol_game;
```

---

## 🔄 Backup y Recuperación

### Backup Completo

```bash
# Dump completo
pg_dump -U quinto_sol_user quinto_sol > backup_quinto_sol_$(date +%Y%m%d).sql

# Dump comprimido
pg_dump -U quinto_sol_user quinto_sol | gzip > backup_$(date +%Y%m%d).sql.gz
```

### Backup Solo Datos

```bash
pg_dump -U quinto_sol_user --data-only quinto_sol > data_backup.sql
```

### Backup Solo Schema

```bash
pg_dump -U quinto_sol_user --schema-only quinto_sol > schema_backup.sql
```

### Restaurar

```bash
# Desde dump SQL
psql -U quinto_sol_user quinto_sol < backup.sql

# Desde dump comprimido
gunzip -c backup.sql.gz | psql -U quinto_sol_user quinto_sol
```

---

## 📊 Configuración de Producción

### postgresql.conf

```ini
# Memoria
shared_buffers = 4GB              # 25% de RAM disponible
effective_cache_size = 12GB       # 75% de RAM
work_mem = 64MB
maintenance_work_mem = 512MB

# Connections
max_connections = 200

# Checkpoints
checkpoint_completion_target = 0.9
wal_buffers = 16MB

# Query Planning
random_page_cost = 1.1  # Para SSD
effective_io_concurrency = 200
```

### Tuning Automático

```bash
# Usar PGTune: https://pgtune.leopard.in.ua/
# Genera configuración óptima según hardware
```

---

## ❓ Troubleshooting

### Error: "role does not exist"

```bash
# Crear usuario
sudo -u postgres createuser -s quinto_sol_user
```

### Error: "permission denied for schema public"

```sql
-- En PostgreSQL 15+
\c quinto_sol
GRANT ALL ON SCHEMA public TO quinto_sol_user;
```

### Error: "too many connections"

```sql
-- Aumentar max_connections en postgresql.conf
max_connections = 300

-- Reiniciar PostgreSQL
sudo systemctl restart postgresql
```

### Error: "database is being accessed by other users"

```sql
-- Terminar conexiones activas
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = 'quinto_sol' AND pid <> pg_backend_pid();
```

---

## 🔗 Recursos Adicionales

- **Documentación oficial:** https://www.postgresql.org/docs/
- **PostgreSQL Tutorial:** https://www.postgresqltutorial.com/
- **psycopg2 docs:** https://www.psycopg.org/docs/
- **PGTune:** https://pgtune.leopard.in.ua/
- **pgAdmin:** https://www.pgadmin.org/ (GUI para administración)

---

## ✅ Checklist de Producción

- [ ] PostgreSQL 15+ instalado
- [ ] Base de datos `quinto_sol` creada
- [ ] Usuario con permisos configurado
- [ ] Variables de entorno configuradas
- [ ] Conexión verificada con `database_connector.py`
- [ ] Schemas migrados/aplicados
- [ ] Datos migrados (si aplica)
- [ ] Índices creados
- [ ] Backup automático configurado
- [ ] Monitoring habilitado
- [ ] postgresql.conf optimizado
- [ ] SSL configurado (si aplica)
- [ ] Firewall configurado

---

_Última actualización: 2025_
_Portales del Quinto Sol - MMORPG_
