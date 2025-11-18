# SISTEMAS COMPLETADOS - Portales del Quinto Sol

## Resumen

Se han implementado todos los sistemas principales para la simulación histórica del mundo (1500-3000):

1. ✅ Sistema de Relaciones Especies-Civilizaciones-Dioses
2. ✅ Sistema de Flora (1000 especies)
3. ✅ Sistema de Fauna (300 especies)
4. ✅ Genealogías de Especies Sirvientes (300 años longevidad)
5. ✅ Sistema de Longevidad por Oficio (hasta 200 años para humanos)
6. ✅ Sistema de Guerras Inter-Especies

---

## 1. Relaciones Especies-Civilizaciones-Dioses

**Archivos:**
- `schema_relaciones_especies_civilizaciones.sql` - Schema de 4 tablas
- `poblar_relaciones_especies_civilizaciones.py` - Poblador de datos iniciales

**Tablas creadas:**
- `especies_civilizaciones` - Relaciones entre especies, civilizaciones y dioses patronos
- `diplomacia_especies` - Estado diplomático entre especies
- `tratados_especies` - Tratados y alianzas
- `embajadores` - Sistema de embajadores inter-especies

**Relaciones iniciales (año 1500):**
- **Tlacatl de Luz** → Toltecas del Viento + Quetzalcóatl (95% devoción)
- **Sombra-Coyotes** → Purépecha del Fuego + Tezcatlipoca (90% devoción)
- **Bio-Constructores** → Zapotecas del Eco + Centéotl (92% devoción)
- **Acuátiles** → Mayas Celeste + Tláloc (93% devoción)
- **Guerreros Solares** → Mexica de Obsidiana + Huitzilopochtli (98% devoción)

**Datos poblados:**
- 15 relaciones especies-civilizaciones
- 30 relaciones diplomáticas (bidireccionales)
- 3 tratados activos iniciales

**Uso:**
```bash
python3 poblar_relaciones_especies_civilizaciones.py
```

---

## 2. Sistema de Flora (1000 Especies)

**Archivos:**
- `schema_flora.sql` - Schema completo con 7 tablas
- `flora_1000_especies.py` - Generador de 777 especies de plantas

**Tablas creadas:**
- `especies_flora` - Catálogo de especies
- `flora_zonas` - Distribución por zonas (spawn system)
- `plantas_individuales` - Plantas únicas/legendarias
- `recetas_herbolaria` - Recetas y combinaciones
- `cultivos` - Sistema de agricultura
- `inventario_flora` - Inventarios de NPCs/jugadores
- `mercado_flora` - Transacciones comerciales

**Clasificaciones:**
- **Alimento** (191 especies): Frutas, verduras, granos, hongos comestibles
- **Curativo** (207 especies): Plantas medicinales
- **Veneno** (99 especies): Plantas tóxicas y venenosas
- **Alucinógeno** (51 especies): Peyote, Teonanácatl, etc.
- **Adorno** (149 especies): Flores ornamentales
- **Recursos** (80 especies): Maderas, fibras, tintes, resinas

**Características:**
- Nombres en Náhuatl
- Rareza (0.01-1.0)
- Biomas preferidos
- Valor de mercado
- Sistema de cultivo
- Épocas de disponibilidad

**Uso:**
```bash
python3 flora_1000_especies.py
```

---

## 3. Sistema de Fauna (300 Especies)

**Archivos:**
- `schema_especies_fauna.sql` - Schema con 5 tablas
- `fauna_300_especies.py` - Generador de 315 especies animales

**Tablas creadas:**
- `especies_fauna` - Catálogo de especies animales
- `fauna_zonas` - Sistema de spawn por zona
- `fauna_domesticada` - Animales domesticados/mascotas
- `fauna_caza` - Registro de caza y recolección
- `fauna_comercio` - Comercio de animales

**Categorías:**
- **Mamíferos** (120 especies): Xoloitzcuintle, jaguares, venados, etc.
- **Aves** (95 especies): Quetzales, águilas, guacamayas
- **Reptiles** (45 especies): Serpientes, iguanas, cocodrilos
- **Anfibios** (15 especies): Ajolotes, ranas venenosas
- **Acuáticos** (25 especies): Peces, delfines, mantarrayas
- **Mitológicos** (15 especies): Nahual, Ahuizotl, Cipactli

**Características:**
- Sistema de spawn sin genealogía
- Rareza por zona
- Agresividad y peligrosidad
- Valor comercial
- Recursos obtenibles (carne, piel, plumas)

**Uso:**
```bash
python3 fauna_300_especies.py
```

---

## 4. Genealogías Especies Sirvientes (300 años)

**Archivo:**
- `generar_genealogias_especies.py` - Generador completo

**Especies implementadas:**

### 4.1 Tlacatl de Luz
- **Longevidad:** 250-320 años
- **Fertilidad:** Hasta 180 años
- **Hijos:** 3-6 por pareja
- **Esterilidad:** 10%
- **Mortalidad infantil:** 5%
- **Características:** Sabios, diplomáticos, plumas y escamas
- **Inteligencia:** 150 (1500) → 100 (3000)

### 4.2 Sombra-Coyotes
- **Longevidad:** 200-280 años
- **Fertilidad:** Hasta 160 años
- **Hijos:** 2-5 por pareja
- **Esterilidad:** 15%
- **Mortalidad infantil:** 8%
- **Características:** Nocturnos, sigilo, orejas de coyote

### 4.3 Bio-Constructores
- **Longevidad:** 280-350 años (los más longevos)
- **Fertilidad:** Hasta 200 años
- **Hijos:** 4-7 por pareja
- **Esterilidad:** 8%
- **Mortalidad infantil:** 4%
- **Características:** Piel vegetal, regeneración natural

### 4.4 Acuátiles
- **Longevidad:** 230-300 años
- **Fertilidad:** Hasta 170 años
- **Hijos:** 3-6 por pareja
- **Esterilidad:** 12%
- **Mortalidad infantil:** 6%
- **Características:** Anfibios, branquias funcionales, manos palmeadas

### 4.5 Guerreros Solares
- **Longevidad:** 180-250 años
- **Fertilidad:** Hasta 150 años
- **Hijos:** 4-8 por pareja
- **Esterilidad:** 9%
- **Mortalidad infantil:** 10%
- **Características:** Piel dorada brillante, sangre dorada

**Características comunes:**
- Intervalos de nacimiento: 3-7 años
- Resistencia base: 85-95 (superior a humanos)
- Inteligencia degrada linealmente con el tiempo
- Distribuciones sociales específicas por especie
- ~5 generaciones en 1500 años

**Poblaciones iniciales (año 1500):**
- Tlacatl de Luz: 150
- Sombra-Coyotes: 100
- Bio-Constructores: 180
- Acuátiles: 140
- Guerreros Solares: 200

**Uso:**
```bash
python3 generar_genealogias_especies.py
```

---

## 5. Sistema de Longevidad por Oficio (200 años)

**Archivo:**
- `sistema_longevidad_oficios.py` - Sistema completo

**Longevidad por categoría de oficios:**

### 5.1 Muy Alta (140-200 años)
- Sacerdote, Sacerdotisa: 140-200
- Filósofo: 135-195
- Astrónomo: 130-190
- Matemático: 135-195

### 5.2 Alta (120-180 años)
- Bio-Ingeniero: 125-185
- Tecnomístico: 130-185
- Geomante: 125-180
- Arquitecto: 115-165
- Escriba: 120-170
- Curandero: 115-165

### 5.3 Media (90-145 años)
- Artesanos: 95-160
- Comerciante: 105-150
- Agricultores: 90-140
- Cocinero: 95-140

### 5.4 Baja (70-130 años)
- Guerrero: 65-115
- Guardián: 75-125
- Pescador: 85-135
- Cazador: 80-130
- Minero: 75-120

### 5.5 Muy Baja (50-100 años)
- Asesino: 50-95
- Contrabandista: 55-100
- Espía: 55-100

**Modificadores de hábitos:**
- **Excelente** (1.25x): Alimentación balanceada, meditación, ejercicio
- **Bueno** (1.15x): Buenos hábitos
- **Promedio** (1.0x): Vida normal
- **Malo** (0.85x): Malos hábitos
- **Pésimo** (0.65x): Alcoholismo, drogas

**Modificadores clase social:**
- Sacerdote/Noble: +15-20%
- Artesano: +5%
- Campesino: -5%
- Guerrero: -10%
- Esclavo: -30%

**Características:**
- Cap máximo: 200 años
- Cap mínimo: 50 años
- Distribución realista
- Sistema de actualización masiva
- Reportes estadísticos

**Uso:**
```bash
python3 sistema_longevidad_oficios.py
```

---

## 6. Sistema de Guerras Inter-Especies

**Archivos:**
- `schema_guerras_especies.sql` - Schema con 6 tablas
- `sistema_guerras_especies.py` - Sistema completo

**Tablas creadas:**
- `guerras_especies` - Guerras principales
- `batallas_guerras` - Batallas individuales
- `escaramuzas_especies` - Conflictos menores
- `alianzas_militares` - Alianzas entre especies
- `impacto_guerra_poblaciones` - Impacto demográfico
- `crimenes_guerra` - Atrocidades de guerra

**Probabilidades:**
- Guerra: 0.3% anual (~4.5 guerras en 1500 años)
- Escaramuza: 1.5% anual (más común)

**Causas de guerra:**
- **Territorial** (35%): Disputa por territorios
- **Recursos** (25%): Agua, minerales, flora
- **Religiosa** (15%): Profanación, guerra santa
- **Venganza** (12%): Agravios previos
- **Expansión** (8%): Imperialismo
- **Defensa** (5%): Defensa preventiva

**Intensidades:**
- **Escaramuza:** 5-50 bajas, 1-30 días
- **Batalla:** 50-300 bajas, 1-6 meses
- **Guerra:** 200-1500 bajas, 0.5-3 años
- **Guerra Total:** 1000-8000 bajas, 3-10 años

**Características:**
- Intervención divina (20% probabilidad)
- Impacto en diplomacia (-20 a -30)
- Generación de batallas individuales
- Comandantes y héroes
- Impacto poblacional detallado
- Sistema de vencedores

**Uso:**
```bash
python3 sistema_guerras_especies.py
```

---

## 7. Simulación Completa

**Archivo:**
- `simulacion_completa_1500_3000.py` - Orquestador maestro

**Orden de ejecución:**
1. Backup de base de datos
2. Verificación de prerequisitos
3. Limpieza opcional de datos previos
4. **Paso 1:** Relaciones especies-civilizaciones-dioses
5. **Paso 2:** Genealogías especies sirvientes
6. **Paso 3:** Genealogías humanos (manual)
7. **Paso 4:** Longevidad por oficios
8. **Paso 5:** Guerras inter-especies
9. Resumen final y estadísticas

**Características:**
- Backup automático
- Logging completo
- Manejo de errores
- Resumen estadístico
- Estimación de tiempo

**Uso:**
```bash
python3 simulacion_completa_1500_3000.py
```

**⚠️ ADVERTENCIA:** La simulación completa puede tardar varias horas.

---

## Estadísticas Esperadas

**Poblaciones finales estimadas (año 3000):**
- Humanos I: ~150,000 - 250,000
- Tlacatl de Luz: ~1,500 - 2,500
- Sombra-Coyotes: ~800 - 1,500
- Bio-Constructores: ~2,000 - 3,500
- Acuátiles: ~1,500 - 2,500
- Guerreros Solares: ~2,500 - 4,000

**Conflictos esperados (1500-3000):**
- Guerras: 4-6
- Escaramuzas: 20-30
- Batallas totales: 50-150

**Relaciones:**
- 15 relaciones especies-civilizaciones
- 30 relaciones diplomáticas
- 3-5 tratados activos

---

## Archivos de Utilidad

**Scripts de verificación:**
- `check_oficios.py` - Listar todos los oficios
- `check_relaciones.py` - Verificar relaciones
- `check_civilizaciones.py` - Listar civilizaciones
- `check_all_civilizaciones.py` - Información completa de civilizaciones
- `drop_relaciones_tables.py` - Limpiar tablas de relaciones

---

## Base de Datos

**Tablas nuevas creadas:**
- `especies_civilizaciones`
- `diplomacia_especies`
- `tratados_especies`
- `embajadores`
- `especies_flora`
- `flora_zonas`
- `plantas_individuales`
- `recetas_herbolaria`
- `cultivos`
- `inventario_flora`
- `mercado_flora`
- `especies_fauna`
- `fauna_zonas`
- `fauna_domesticada`
- `fauna_caza`
- `fauna_comercio`
- `guerras_especies`
- `batallas_guerras`
- `escaramuzas_especies`
- `alianzas_militares`
- `impacto_guerra_poblaciones`
- `crimenes_guerra`

---

## Próximos Pasos

1. Ejecutar `simulacion_completa_1500_3000.py`
2. Verificar resultados con reportes
3. Ajustar parámetros si es necesario
4. Integrar con sistema de juego principal

---

## Notas Técnicas

**Requerimientos:**
- Python 3.7+
- SQLite3
- Espacio en disco: ~5-10 GB para BD completa
- RAM: ~4 GB mínimo
- Tiempo estimado: 2-6 horas

**Optimizaciones:**
- Índices en todas las tablas principales
- Commits por lotes
- Queries optimizadas

---

## Autor

Sistema desarrollado para "Portales del Quinto Sol" - MMORPG
Simulación histórica: 1500-3000 (1500 años)
