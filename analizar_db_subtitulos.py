#!/usr/bin/env python3
"""
Analizador de Base de Datos de Subtítulos
Valida esquema, metadatos y prepara para integración con Portales del Quinto Sol
"""

import sqlite3
import sys
import json
from collections import Counter
import re


def analizar_esquema(db_path):
    """Analiza el esquema completo de la base de datos"""
    print("=" * 80)
    print("ANÁLISIS DE BASE DE DATOS DE SUBTÍTULOS")
    print("=" * 80)
    print(f"\nRuta: {db_path}\n")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Obtener todas las tablas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tablas = cursor.fetchall()

    print(f"📊 TABLAS ENCONTRADAS: {len(tablas)}")
    print("-" * 80)

    esquema_completo = {}

    for (tabla_nombre,) in tablas:
        # Obtener esquema de la tabla
        cursor.execute(f"PRAGMA table_info({tabla_nombre})")
        columnas = cursor.fetchall()

        # Contar registros
        cursor.execute(f"SELECT COUNT(*) FROM {tabla_nombre}")
        num_registros = cursor.fetchone()[0]

        print(f"\n📋 Tabla: {tabla_nombre} ({num_registros:,} registros)")
        print(f"   Columnas:")

        esquema_completo[tabla_nombre] = {
            'columnas': [],
            'num_registros': num_registros
        }

        for col in columnas:
            col_id, col_nombre, col_tipo, no_null, default, pk = col
            pk_str = " [PK]" if pk else ""
            notnull_str = " NOT NULL" if no_null else ""
            print(f"      {col_nombre:30} {col_tipo:15}{pk_str}{notnull_str}")

            esquema_completo[tabla_nombre]['columnas'].append({
                'nombre': col_nombre,
                'tipo': col_tipo,
                'primary_key': bool(pk),
                'not_null': bool(no_null)
            })

    conn.close()
    return esquema_completo


def validar_metadatos(db_path):
    """Valida qué metadatos están disponibles"""
    print("\n" + "=" * 80)
    print("VALIDACIÓN DE METADATOS")
    print("=" * 80)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Intentar detectar columnas comunes
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tablas = [t[0] for t in cursor.fetchall()]

    metadatos_encontrados = {}

    for tabla in tablas:
        cursor.execute(f"PRAGMA table_info({tabla})")
        columnas = [col[1] for col in cursor.fetchall()]

        # Buscar columnas relevantes
        columnas_relevantes = []

        # IDs
        id_cols = [c for c in columnas if 'id' in c.lower()]
        if id_cols:
            columnas_relevantes.append(('IDs', id_cols))

        # Títulos
        titulo_cols = [c for c in columnas if any(x in c.lower() for x in ['title', 'titulo', 'name', 'nombre'])]
        if titulo_cols:
            columnas_relevantes.append(('Títulos', titulo_cols))

        # Tipos (película, serie, episodio)
        tipo_cols = [c for c in columnas if any(x in c.lower() for x in ['type', 'tipo', 'kind', 'category'])]
        if tipo_cols:
            columnas_relevantes.append(('Tipos', tipo_cols))

        # Temporada/Episodio
        season_cols = [c for c in columnas if any(x in c.lower() for x in ['season', 'temporada', 'episode', 'episodio', 'chapter', 'capitulo'])]
        if season_cols:
            columnas_relevantes.append(('Temporada/Episodio', season_cols))

        # Subtítulos/Diálogos
        sub_cols = [c for c in columnas if any(x in c.lower() for x in ['subtitle', 'subtitulo', 'text', 'texto', 'dialog', 'dialogo', 'content', 'contenido'])]
        if sub_cols:
            columnas_relevantes.append(('Subtítulos/Diálogos', sub_cols))

        # Idioma
        lang_cols = [c for c in columnas if any(x in c.lower() for x in ['lang', 'language', 'idioma'])]
        if lang_cols:
            columnas_relevantes.append(('Idioma', lang_cols))

        # Año
        year_cols = [c for c in columnas if any(x in c.lower() for x in ['year', 'año', 'date', 'fecha'])]
        if year_cols:
            columnas_relevantes.append(('Año', year_cols))

        if columnas_relevantes:
            metadatos_encontrados[tabla] = columnas_relevantes

    # Mostrar resultados
    for tabla, metadatos in metadatos_encontrados.items():
        cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
        num_registros = cursor.fetchone()[0]

        print(f"\n📦 {tabla} ({num_registros:,} registros)")
        for categoria, columnas in metadatos:
            print(f"   ✓ {categoria}: {', '.join(columnas)}")

    conn.close()
    return metadatos_encontrados


def analizar_ids_imdb(db_path, tabla_principal):
    """Analiza los IDs para correlación con IMDB/TMDB"""
    print("\n" + "=" * 80)
    print("ANÁLISIS DE IDs PARA CORRELACIÓN IMDB/TMDB")
    print("=" * 80)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Obtener columnas de la tabla principal
    cursor.execute(f"PRAGMA table_info({tabla_principal})")
    columnas = [col[1] for col in cursor.fetchall()]

    print(f"\n🔍 Analizando tabla: {tabla_principal}")
    print(f"   Columnas disponibles: {', '.join(columnas)}")

    # Buscar columna de ID
    id_cols = [c for c in columnas if 'id' in c.lower()]

    if not id_cols:
        print("\n⚠️  No se encontraron columnas de ID")
        conn.close()
        return None

    print(f"\n📋 Columnas de ID encontradas: {', '.join(id_cols)}")

    # Analizar cada columna de ID
    for id_col in id_cols[:3]:  # Analizar primeras 3 columnas de ID
        print(f"\n🔎 Analizando columna: {id_col}")

        # Obtener muestras
        cursor.execute(f"SELECT DISTINCT {id_col} FROM {tabla_principal} WHERE {id_col} IS NOT NULL LIMIT 10")
        muestras = cursor.fetchall()

        if muestras:
            print(f"   Muestras (primeras 10):")
            for (muestra,) in muestras:
                # Intentar detectar formato
                if isinstance(muestra, int):
                    # Formato numérico - posible ID de IMDB
                    imdb_id = f"tt{str(muestra).zfill(7)}"
                    print(f"      {muestra:15} → {imdb_id} (IMDB format)")
                elif isinstance(muestra, str):
                    # Ya es string
                    if muestra.startswith('tt'):
                        print(f"      {muestra:15} → {muestra} (Ya formato IMDB)")
                    else:
                        # Intentar agregar 'tt'
                        try:
                            num = int(muestra)
                            imdb_id = f"tt{str(num).zfill(7)}"
                            print(f"      {muestra:15} → {imdb_id} (IMDB format)")
                        except:
                            print(f"      {muestra:15} → Formato desconocido")

        # Contar IDs únicos
        cursor.execute(f"SELECT COUNT(DISTINCT {id_col}) FROM {tabla_principal} WHERE {id_col} IS NOT NULL")
        num_unicos = cursor.fetchone()[0]
        print(f"   Total IDs únicos: {num_unicos:,}")

    conn.close()
    return id_cols


def analizar_contenido_dialogos(db_path, tabla_principal, columna_texto, limite=100):
    """Analiza el contenido de los diálogos"""
    print("\n" + "=" * 80)
    print("ANÁLISIS DE CONTENIDO DE DIÁLOGOS")
    print("=" * 80)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Obtener muestras de diálogos
    cursor.execute(f"""
        SELECT {columna_texto}
        FROM {tabla_principal}
        WHERE {columna_texto} IS NOT NULL
        AND LENGTH({columna_texto}) > 10
        LIMIT {limite}
    """)

    dialogos = [d[0] for d in cursor.fetchall()]

    if not dialogos:
        print("⚠️  No se encontraron diálogos")
        conn.close()
        return

    print(f"\n📊 Analizados {len(dialogos)} diálogos de muestra")

    # Estadísticas básicas
    longitudes = [len(d) for d in dialogos]
    print(f"\n📏 Longitud de diálogos:")
    print(f"   Promedio: {sum(longitudes)/len(longitudes):.0f} caracteres")
    print(f"   Mínimo: {min(longitudes)} caracteres")
    print(f"   Máximo: {max(longitudes)} caracteres")

    # Detectar idioma (español)
    palabras_español = ['el', 'la', 'de', 'que', 'y', 'a', 'en', 'es', 'por', 'un', 'para', 'con', 'no', 'una', 'su']
    palabras_ingles = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it', 'for', 'not', 'on', 'with']

    texto_completo = ' '.join(dialogos).lower()
    count_español = sum(texto_completo.count(f' {p} ') for p in palabras_español)
    count_ingles = sum(texto_completo.count(f' {p} ') for p in palabras_ingles)

    if count_español > count_ingles:
        print(f"\n🇪🇸 Idioma detectado: ESPAÑOL (confianza: {count_español/(count_español+count_ingles)*100:.0f}%)")
    else:
        print(f"\n🇬🇧 Idioma detectado: INGLÉS (confianza: {count_ingles/(count_español+count_ingles)*100:.0f}%)")

    # Mostrar muestras
    print(f"\n📝 Muestras de diálogos (primeros 5):")
    for i, dialogo in enumerate(dialogos[:5], 1):
        # Limpiar y truncar
        dialogo_limpio = dialogo.strip()[:100]
        print(f"   {i}. {dialogo_limpio}...")

    # Detectar patrones útiles
    print(f"\n🔍 Patrones detectados:")

    # Preguntas
    preguntas = [d for d in dialogos if '?' in d]
    print(f"   Preguntas (¿?): {len(preguntas)} ({len(preguntas)/len(dialogos)*100:.1f}%)")

    # Exclamaciones
    exclamaciones = [d for d in dialogos if '!' in d]
    print(f"   Exclamaciones (!): {len(exclamaciones)} ({len(exclamaciones)/len(dialogos)*100:.1f}%)")

    # Diálogos largos (narrativos)
    largos = [d for d in dialogos if len(d) > 150]
    print(f"   Diálogos largos (>150 chars): {len(largos)} ({len(largos)/len(dialogos)*100:.1f}%)")

    # Palabras clave de emoción
    emociones = {
        'alegría': ['feliz', 'alegre', 'contento', 'bien', 'genial', 'excelente', 'maravilloso'],
        'tristeza': ['triste', 'llorar', 'pena', 'dolor', 'mal', 'terrible', 'horrible'],
        'ira': ['enojado', 'furioso', 'odio', 'maldito', 'mierda', 'carajo'],
        'miedo': ['miedo', 'terror', 'asustado', 'peligro', 'cuidado', 'socorro'],
    }

    print(f"\n😊 Detección de emociones (muestra):")
    for emocion, palabras in emociones.items():
        count = sum(any(palabra in d.lower() for palabra in palabras) for d in dialogos)
        if count > 0:
            print(f"   {emocion.capitalize()}: {count} diálogos ({count/len(dialogos)*100:.1f}%)")

    # Total de diálogos en la tabla
    cursor.execute(f"SELECT COUNT(*) FROM {tabla_principal} WHERE {columna_texto} IS NOT NULL")
    total_dialogos = cursor.fetchone()[0]
    print(f"\n💬 Total de diálogos en base de datos: {total_dialogos:,}")

    conn.close()


def generar_reporte_json(esquema, metadatos, output_file='analisis_subtitulos.json'):
    """Genera reporte JSON con el análisis"""
    reporte = {
        'esquema': esquema,
        'metadatos': metadatos,
        'timestamp': '2025-11-18'
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(reporte, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Reporte guardado en: {output_file}")


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 analizar_db_subtitulos.py <ruta_db_sqlite>")
        print("\nEjemplo:")
        print("  python3 analizar_db_subtitulos.py /ruta/a/subtitulos.db")
        sys.exit(1)

    db_path = sys.argv[1]

    try:
        # 1. Analizar esquema
        esquema = analizar_esquema(db_path)

        # 2. Validar metadatos
        metadatos = validar_metadatos(db_path)

        # 3. Solicitar tabla principal al usuario
        print("\n" + "=" * 80)
        print("CONFIGURACIÓN")
        print("=" * 80)

        tablas = list(esquema.keys())
        print("\nTablas disponibles:")
        for i, tabla in enumerate(tablas, 1):
            print(f"  {i}. {tabla} ({esquema[tabla]['num_registros']:,} registros)")

        # Intentar autodetectar tabla principal
        # Buscar tabla con más registros que tenga columna de texto
        tabla_sugerida = None
        max_registros = 0

        for tabla, info in esquema.items():
            columnas = [c['nombre'] for c in info['columnas']]
            tiene_texto = any(any(x in c.lower() for x in ['text', 'texto', 'subtitle', 'subtitulo', 'content', 'dialog']) for c in columnas)

            if tiene_texto and info['num_registros'] > max_registros:
                max_registros = info['num_registros']
                tabla_sugerida = tabla

        if tabla_sugerida:
            print(f"\n💡 Tabla principal sugerida: {tabla_sugerida} ({max_registros:,} registros)")

            # 4. Analizar IDs
            id_cols = analizar_ids_imdb(db_path, tabla_sugerida)

            # 5. Analizar contenido de diálogos
            # Buscar columna de texto
            columnas_texto = [c['nombre'] for c in esquema[tabla_sugerida]['columnas']
                            if any(x in c['nombre'].lower() for x in ['text', 'texto', 'subtitle', 'subtitulo', 'content', 'dialog'])]

            if columnas_texto:
                print(f"\n💡 Columna de texto sugerida: {columnas_texto[0]}")
                analizar_contenido_dialogos(db_path, tabla_sugerida, columnas_texto[0])

        # 6. Generar reporte
        generar_reporte_json(esquema, metadatos)

        print("\n" + "=" * 80)
        print("✅ ANÁLISIS COMPLETADO")
        print("=" * 80)
        print("\n📋 Próximos pasos:")
        print("  1. Revisar analisis_subtitulos.json para validar estructura")
        print("  2. Ejecutar script de correlación con IMDB/TMDB")
        print("  3. Extraer y clasificar diálogos por emoción y personalidad")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
