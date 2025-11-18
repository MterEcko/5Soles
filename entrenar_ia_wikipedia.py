#!/usr/bin/env python3
"""
Script para extraer conocimientos de Wikipedia y entrenar IA multilingüe
Wikipedia es una excelente fuente de datos con licencia Creative Commons
"""

import requests
from typing import List, Dict
import sqlite3
import json

class ExtractorWikipedia:
    """
    Extrae artículos de Wikipedia en múltiples idiomas para entrenamiento de IA
    """

    def __init__(self, db_path='quinto_sol.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.session = requests.Session()

        # Mapeo de códigos de idioma a prefijos de Wikipedia
        self.wiki_langs = {
            'es': 'es.wikipedia.org',
            'en': 'en.wikipedia.org',
            'fr': 'fr.wikipedia.org',
            'ru': 'ru.wikipedia.org',
            'zh': 'zh.wikipedia.org',
            'ja': 'ja.wikipedia.org',
            'nah': 'nah.wikipedia.org',  # Náhuatl tiene Wikipedia!
        }

    def extraer_articulo(self, titulo: str, lang: str = 'es') -> Dict:
        """
        Extrae el contenido de un artículo de Wikipedia

        Args:
            titulo: Título del artículo (ej: 'Quetzalcóatl')
            lang: Código de idioma

        Returns:
            Dict con título, extracto, contenido completo, categorías, etc.
        """

        if lang not in self.wiki_langs:
            print(f"⚠️  Idioma '{lang}' no soportado")
            return None

        wiki_domain = self.wiki_langs[lang]
        url = f"https://{wiki_domain}/w/api.php"

        params = {
            'action': 'query',
            'format': 'json',
            'titles': titulo,
            'prop': 'extracts|categories|langlinks|pageimages',
            'explaintext': True,
            'exsectionformat': 'plain',
            'lllimit': 'max',
        }

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            pages = data.get('query', {}).get('pages', {})
            if not pages:
                return None

            # Obtener la primera (y única) página
            page = list(pages.values())[0]

            if 'missing' in page:
                print(f"⚠️  Artículo '{titulo}' no encontrado en Wikipedia ({lang})")
                return None

            return {
                'titulo': page.get('title'),
                'extracto': page.get('extract', '')[:500],  # Primeros 500 caracteres
                'contenido': page.get('extract', ''),
                'categorias': [c.get('title') for c in page.get('categories', [])],
                'idioma': lang,
                'url': f"https://{wiki_domain}/wiki/{titulo.replace(' ', '_')}",
            }

        except Exception as e:
            print(f"❌ Error al extraer '{titulo}': {e}")
            return None

    def extraer_articulos_mitologia_mesoamericana(self) -> List[Dict]:
        """
        Extrae artículos sobre mitología mesoamericana en múltiples idiomas
        """

        temas = [
            # Dioses principales
            'Quetzalcóatl', 'Tezcatlipoca', 'Tláloc', 'Huitzilopochtli',
            'Ixchel', 'Mictlantecuhtli', 'Xipe Tótec', 'Xochiquetzal',
            'Chaac', 'Centéotl', 'Mayahuel',

            # Culturas
            'Mexica', 'Cultura maya', 'Cultura zapoteca', 'Cultura mixteca',
            'Cultura purépecha', 'Tolteca', 'Cultura olmeca',

            # Lenguas
            'Idioma náhuatl', 'Lenguas mayas', 'Lenguas zapotecas',
            'Idioma purépecha', 'Lenguas mixtecas',

            # Historia
            'Conquista de México', 'Tenochtitlan', 'Aztlán',
            'Quinto Sol', 'Calendario azteca',

            # Mitología
            'Popol Vuh', 'Leyenda de los Soles', 'Códice Borgia',
        ]

        articulos = []
        idiomas = ['es', 'en']  # Español e inglés por ahora

        print(f"\nExtrayendo {len(temas)} temas en {len(idiomas)} idiomas...")
        print("="*70 + "\n")

        for tema in temas:
            for lang in idiomas:
                print(f"📖 Extrayendo: {tema} ({lang})...")
                articulo = self.extraer_articulo(tema, lang)
                if articulo:
                    articulos.append(articulo)
                    print(f"   ✓ Extraído: {len(articulo['contenido'])} caracteres")
                else:
                    print(f"   ⚠️  No se pudo extraer")

        return articulos

    def guardar_conocimiento(self, articulos: List[Dict]):
        """
        Guarda el conocimiento extraído en una tabla de entrenamiento
        """

        # Crear tabla de conocimientos si no existe
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS conocimientos_ia (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fuente VARCHAR(50),
                tema VARCHAR(200),
                idioma VARCHAR(10),
                titulo TEXT,
                extracto TEXT,
                contenido TEXT,
                metadata TEXT,
                fecha_extraccion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        for articulo in articulos:
            self.cursor.execute('''
                INSERT INTO conocimientos_ia
                (fuente, tema, idioma, titulo, extracto, contenido, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                'Wikipedia',
                articulo.get('titulo'),
                articulo.get('idioma'),
                articulo.get('titulo'),
                articulo.get('extracto'),
                articulo.get('contenido'),
                json.dumps({
                    'url': articulo.get('url'),
                    'categorias': articulo.get('categorias', [])
                })
            ))

        self.conn.commit()
        print(f"\n✓ {len(articulos)} artículos guardados en conocimientos_ia")

    def generar_dataset_entrenamiento(self, output_file='dataset_entrenamiento.jsonl'):
        """
        Genera un archivo JSONL para entrenamiento de modelos de lenguaje
        Formato compatible con OpenAI fine-tuning, GPT, etc.
        """

        self.cursor.execute('''
            SELECT titulo, idioma, extracto, contenido
            FROM conocimientos_ia
            WHERE contenido IS NOT NULL AND contenido != ''
        ''')

        articulos = self.cursor.fetchall()

        with open(output_file, 'w', encoding='utf-8') as f:
            for titulo, idioma, extracto, contenido in articulos:
                # Formato de conversación para fine-tuning
                ejemplo = {
                    "messages": [
                        {
                            "role": "system",
                            "content": "Eres un experto en mitología y cultura mesoamericana."
                        },
                        {
                            "role": "user",
                            "content": f"Cuéntame sobre {titulo}"
                        },
                        {
                            "role": "assistant",
                            "content": contenido[:2000]  # Limitar longitud
                        }
                    ],
                    "metadata": {
                        "tema": titulo,
                        "idioma": idioma,
                        "fuente": "Wikipedia"
                    }
                }

                f.write(json.dumps(ejemplo, ensure_ascii=False) + '\n')

        print(f"\n✓ Dataset generado: {output_file}")
        print(f"  Contiene {len(articulos)} ejemplos de entrenamiento")

    def cerrar(self):
        """Cierra la conexión"""
        self.conn.close()


def main():
    """
    Ejemplo de uso completo
    """

    print("="*70)
    print("EXTRACTOR DE CONOCIMIENTOS - Wikipedia para IA")
    print("="*70)

    extractor = ExtractorWikipedia()

    try:
        # 1. Extraer artículos de Wikipedia
        print("\n📚 Paso 1: Extrayendo artículos de Wikipedia...")
        articulos = extractor.extraer_articulos_mitologia_mesoamericana()

        # 2. Guardar en base de datos
        print("\n💾 Paso 2: Guardando en base de datos...")
        extractor.guardar_conocimiento(articulos)

        # 3. Generar dataset de entrenamiento
        print("\n🤖 Paso 3: Generando dataset de entrenamiento...")
        extractor.generar_dataset_entrenamiento()

        print("\n" + "="*70)
        print("✓ Proceso completado exitosamente")
        print("="*70)

        print("\n📝 Próximos pasos:")
        print("  1. Revisar dataset_entrenamiento.jsonl")
        print("  2. Usar el dataset para fine-tuning de modelos")
        print("  3. Agregar más fuentes de conocimiento (libros, artículos)")
        print("  4. Expandir a más idiomas indígenas")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        extractor.cerrar()


if __name__ == '__main__':
    main()


# NOTAS SOBRE ENTRENAMIENTO DE IA:
#
# 1. FUENTES DE DATOS:
#    - Wikipedia (CC-BY-SA) ✓
#    - Wikcionario (diccionarios de lenguas indígenas)
#    - Proyecto Gutenberg (libros históricos)
#    - Corpus lingüísticos académicos
#    - Documentos coloniales digitalizados
#
# 2. TIPOS DE MODELOS A ENTRENAR:
#    - Traducción automática (Náhuatl ↔ Español)
#    - Generación de texto (narrativas históricas)
#    - Chatbot multilingüe (NPC conversacionales)
#    - Reconocimiento de entidades (personas, lugares, dioses)
#
# 3. HERRAMIENTAS RECOMENDADAS:
#    - Hugging Face Transformers (modelos pre-entrenados)
#    - OpenAI API (fine-tuning de GPT)
#    - spaCy (NLP en español)
#    - FastText (embeddings multilingües)
#
# 4. CONSIDERACIONES ÉTICAS:
#    - Respetar las lenguas indígenas
#    - Consultar con hablantes nativos
#    - No perpetuar estereotipos
#    - Dar crédito a las fuentes
