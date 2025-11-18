#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Conversaciones NPC
Portales del Quinto Sol

Sistema completo de conversaciones NPC-to-NPC durante simulación histórica
y sistema de memoria para interacciones jugador-NPC en tiempo real.

FASE 1 (1500-3000): Generación de conversaciones con templates (rápido)
FASE 2 (3000+): Conversaciones con LLM local + memoria (jugadores)
"""

import sqlite3
import random
import json
from typing import List, Dict, Tuple, Optional
from datetime import datetime

DB_PATH = 'quinto_sol.db'

class SistemaConversacionesNPC:
    def __init__(self, db_path: str = DB_PATH):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

        # Templates para conversaciones rápidas durante simulación
        self.templates_conversacion = self._cargar_templates()

    def _cargar_templates(self) -> Dict:
        """Templates de conversaciones por categoría"""
        return {
            'saludo': [
                "{p1} saluda a {p2} en el mercado de {lugar}",
                "{p1} se encuentra con {p2} durante la ceremonia en {lugar}",
                "{p1} y {p2} conversan brevemente en {lugar}",
            ],
            'comercio': [
                "{p1} negocia con {p2} sobre {tema} en {lugar}",
                "{p1} vende {tema} a {p2} en el mercado de {lugar}",
                "{p1} intercambia {tema} con {p2} en {lugar}",
            ],
            'familia': [
                "{p1} habla con {p2} sobre asuntos familiares en {lugar}",
                "{p1} y {p2} discuten sobre el futuro de la familia en {lugar}",
                "{p1} comparte noticias familiares con {p2} en {lugar}",
            ],
            'guerra': [
                "{p1} discute estrategias de guerra con {p2} en {lugar}",
                "{p1} informa a {p2} sobre movimientos enemigos cerca de {lugar}",
                "{p1} y {p2} planean defensas para {lugar}",
            ],
            'religion': [
                "{p1} ora junto a {p2} en el templo de {lugar}",
                "{p1} discute profecías con {p2} en {lugar}",
                "{p1} y {p2} realizan ritual religioso en {lugar}",
            ],
            'chisme': [
                "{p1} comparte rumores con {p2} en {lugar}",
                "{p1} cuenta a {p2} sobre eventos recientes en {lugar}",
                "{p1} y {p2} hablan sobre otros en {lugar}",
            ],
            'conflicto': [
                "{p1} confronta a {p2} sobre {tema} en {lugar}",
                "{p1} discute acaloradamente con {p2} en {lugar}",
                "{p1} y {p2} tienen desacuerdo sobre {tema} en {lugar}",
            ],
            'alianza': [
                "{p1} propone alianza a {p2} en {lugar}",
                "{p1} y {p2} sellan acuerdo en {lugar}",
                "{p1} negocia términos con {p2} en {lugar}",
            ]
        }

    def crear_schema_conversaciones(self):
        """Crea tablas para sistema de conversaciones"""
        print("\n🗣️  Creando schema de conversaciones NPC...")

        self.cursor.executescript('''
        -- Conversaciones históricas (FASE 1: 1500-3000)
        CREATE TABLE IF NOT EXISTS conversaciones_historicas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            año INTEGER NOT NULL,
            participante_1_id INTEGER NOT NULL,
            participante_2_id INTEGER NOT NULL,
            lugar_id INTEGER,

            -- Tipo y contenido
            categoria VARCHAR(50),  -- 'saludo', 'comercio', 'guerra', etc.
            tema TEXT,
            descripcion TEXT NOT NULL,

            -- Metadata
            fue_publica BOOLEAN DEFAULT 1,
            testigos TEXT,  -- JSON: [persona_id, ...]

            -- Impacto
            genero_rumor BOOLEAN DEFAULT 0,
            rumor_id INTEGER,
            genero_evento BOOLEAN DEFAULT 0,

            FOREIGN KEY (participante_1_id) REFERENCES personas(id),
            FOREIGN KEY (participante_2_id) REFERENCES personas(id),
            FOREIGN KEY (lugar_id) REFERENCES pueblos_ciudades(id)
        );

        -- Rumores generados por conversaciones
        CREATE TABLE IF NOT EXISTS rumores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            año_origen INTEGER NOT NULL,
            conversacion_origen_id INTEGER,

            -- Contenido
            texto_original TEXT NOT NULL,
            texto_actual TEXT NOT NULL,  -- Va mutando
            categoria VARCHAR(50),
            veracidad INTEGER,  -- 0-100 (puede degradarse)

            -- Propagación
            persona_origen_id INTEGER NOT NULL,
            lugar_origen_id INTEGER NOT NULL,
            num_propagaciones INTEGER DEFAULT 0,
            alcance VARCHAR(20),  -- 'local', 'regional', 'global'

            -- Estado
            activo BOOLEAN DEFAULT 1,
            año_extincion INTEGER,

            FOREIGN KEY (conversacion_origen_id) REFERENCES conversaciones_historicas(id),
            FOREIGN KEY (persona_origen_id) REFERENCES personas(id),
            FOREIGN KEY (lugar_origen_id) REFERENCES pueblos_ciudades(id)
        );

        -- Propagación de rumores (efecto teléfono descompuesto)
        CREATE TABLE IF NOT EXISTS rumores_propagacion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rumor_id INTEGER NOT NULL,
            año_propagacion INTEGER NOT NULL,

            emisor_id INTEGER NOT NULL,
            receptor_id INTEGER NOT NULL,
            lugar_id INTEGER,

            -- Mutación
            texto_transmitido TEXT,
            distorsion INTEGER DEFAULT 0,  -- 0-100

            FOREIGN KEY (rumor_id) REFERENCES rumores(id),
            FOREIGN KEY (emisor_id) REFERENCES personas(id),
            FOREIGN KEY (receptor_id) REFERENCES personas(id),
            FOREIGN KEY (lugar_id) REFERENCES pueblos_ciudades(id)
        );

        -- Conocimiento cultural generado
        CREATE TABLE IF NOT EXISTS conocimiento_cultural (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            civilizacion_id INTEGER NOT NULL,
            año_creacion INTEGER NOT NULL,

            tipo VARCHAR(50),  -- 'leyenda', 'tradicion', 'tabú', 'ritual', 'tecnica'
            nombre VARCHAR(200) NOT NULL,
            descripcion TEXT NOT NULL,

            -- Origen
            persona_creador_id INTEGER,
            lugar_origen_id INTEGER,
            evento_origen_id INTEGER,

            -- Transmisión
            oral BOOLEAN DEFAULT 1,
            escrito BOOLEAN DEFAULT 0,
            num_conocedores INTEGER DEFAULT 1,

            -- Importancia
            sagrado BOOLEAN DEFAULT 0,
            secreto BOOLEAN DEFAULT 0,
            nivel_importancia INTEGER DEFAULT 1,  -- 1-10

            FOREIGN KEY (civilizacion_id) REFERENCES civilizaciones(id),
            FOREIGN KEY (persona_creador_id) REFERENCES personas(id),
            FOREIGN KEY (lugar_origen_id) REFERENCES pueblos_ciudades(id)
        );

        -- Memoria de NPC para jugadores (FASE 2: año 3000+)
        CREATE TABLE IF NOT EXISTS npc_memoria_jugadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            npc_id INTEGER NOT NULL,
            jugador_id VARCHAR(100) NOT NULL,  -- UUID del jugador

            año_primer_encuentro INTEGER NOT NULL,
            año_ultimo_encuentro INTEGER NOT NULL,
            num_encuentros INTEGER DEFAULT 1,

            -- Relación
            afinidad INTEGER DEFAULT 50,  -- 0-100
            confianza INTEGER DEFAULT 50,  -- 0-100
            tipo_relacion VARCHAR(50),  -- 'desconocido', 'conocido', 'amigo', 'enemigo'

            -- Memoria episódica (eventos importantes)
            eventos_recordados TEXT,  -- JSON: [{año, tipo, descripcion}, ...]

            FOREIGN KEY (npc_id) REFERENCES personas(id),
            UNIQUE(npc_id, jugador_id)
        );

        -- Conversaciones con jugadores
        CREATE TABLE IF NOT EXISTS conversaciones_jugadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            npc_id INTEGER NOT NULL,
            jugador_id VARCHAR(100) NOT NULL,
            año INTEGER NOT NULL,

            -- Conversación
            mensaje_jugador TEXT NOT NULL,
            respuesta_npc TEXT NOT NULL,

            -- Contexto
            lugar_id INTEGER,
            otros_presentes TEXT,  -- JSON: [jugador_id/npc_id, ...]

            -- Metadata
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            emocion_npc VARCHAR(50),  -- 'feliz', 'enojado', 'neutral', etc.

            FOREIGN KEY (npc_id) REFERENCES personas(id),
            FOREIGN KEY (lugar_id) REFERENCES pueblos_ciudades(id)
        );

        -- Índices
        CREATE INDEX IF NOT EXISTS idx_conv_hist_año ON conversaciones_historicas(año);
        CREATE INDEX IF NOT EXISTS idx_conv_hist_p1 ON conversaciones_historicas(participante_1_id);
        CREATE INDEX IF NOT EXISTS idx_conv_hist_p2 ON conversaciones_historicas(participante_2_id);
        CREATE INDEX IF NOT EXISTS idx_rumores_año ON rumores(año_origen);
        CREATE INDEX IF NOT EXISTS idx_rumores_activos ON rumores(activo) WHERE activo = 1;
        CREATE INDEX IF NOT EXISTS idx_conocimiento_civ ON conocimiento_cultural(civilizacion_id);
        CREATE INDEX IF NOT EXISTS idx_npc_memoria_jugador ON npc_memoria_jugadores(jugador_id);
        CREATE INDEX IF NOT EXISTS idx_conv_jugadores_npc ON conversaciones_jugadores(npc_id);
        ''')

        self.conn.commit()
        print("✅ Schema de conversaciones creado")

    def generar_conversaciones_año(self, año: int, num_conversaciones: int = 50):
        """
        Genera conversaciones NPC-to-NPC para un año específico (FASE 1)
        Usa templates para velocidad durante simulación histórica
        """

        # Obtener personas vivas en ese año
        self.cursor.execute('''
            SELECT id, nombre, oficio FROM personas
            WHERE año_nacimiento <= ?
            AND (año_muerte IS NULL OR año_muerte >= ?)
            ORDER BY RANDOM()
            LIMIT ?
        ''', (año, año, num_conversaciones * 2))

        personas_disponibles = self.cursor.fetchall()

        if len(personas_disponibles) < 2:
            return 0

        # Obtener lugares
        self.cursor.execute('SELECT id, nombre FROM pueblos_ciudades ORDER BY RANDOM() LIMIT 10')
        lugares = self.cursor.fetchall()

        if not lugares:
            return 0

        conversaciones_generadas = 0

        for _ in range(min(num_conversaciones, len(personas_disponibles) // 2)):
            # Seleccionar dos personas diferentes
            p1, p2 = random.sample(personas_disponibles, 2)
            lugar = random.choice(lugares)

            # Seleccionar categoría basada en contexto
            categoria = self._seleccionar_categoria(año, p1, p2)

            # Generar conversación desde template
            template = random.choice(self.templates_conversacion[categoria])
            tema = self._generar_tema(categoria, p1, p2)

            descripcion = template.format(
                p1=p1[1],  # nombre
                p2=p2[1],
                lugar=lugar[1],
                tema=tema
            )

            # Probabilidad de generar rumor
            genero_rumor = random.random() < 0.1  # 10%

            # Insertar conversación
            self.cursor.execute('''
                INSERT INTO conversaciones_historicas (
                    año, participante_1_id, participante_2_id, lugar_id,
                    categoria, tema, descripcion, fue_publica, genero_rumor
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (año, p1[0], p2[0], lugar[0], categoria, tema, descripcion, True, genero_rumor))

            conv_id = self.cursor.lastrowid

            # Si generó rumor, crear rumor
            if genero_rumor:
                self._crear_rumor(conv_id, año, p1[0], lugar[0], categoria, tema)

            conversaciones_generadas += 1

        self.conn.commit()
        return conversaciones_generadas

    def _seleccionar_categoria(self, año: int, p1: Tuple, p2: Tuple) -> str:
        """Selecciona categoría de conversación basada en contexto"""

        # Verificar si hay guerra activa en este año
        self.cursor.execute('SELECT COUNT(*) FROM guerras_especies WHERE año_inicio <= ? AND año_fin >= ?', (año, año))
        hay_guerra = self.cursor.fetchone()[0] > 0

        if hay_guerra and random.random() < 0.3:  # 30% si hay guerra
            return 'guerra'

        # Si ambos tienen oficios relacionados
        if p1[2] and p2[2]:  # oficio
            if any(word in p1[2].lower() for word in ['sacerdote', 'curandero', 'chamán']):
                if random.random() < 0.4:
                    return 'religion'
            if any(word in p1[2].lower() for word in ['comerciante', 'artesano', 'herrero']):
                if random.random() < 0.4:
                    return 'comercio'

        # Por defecto, aleatorio ponderado
        return random.choices(
            ['saludo', 'comercio', 'familia', 'religion', 'chisme', 'conflicto', 'alianza'],
            weights=[30, 20, 15, 10, 15, 5, 5],
            k=1
        )[0]

    def _generar_tema(self, categoria: str, p1: Tuple, p2: Tuple) -> str:
        """Genera tema de conversación según categoría"""

        temas = {
            'comercio': ['jade', 'obsidiana', 'cacao', 'plumas', 'cerámica', 'herramientas'],
            'guerra': ['defensa', 'ataque enemigo', 'alianzas', 'estrategia', 'armamento'],
            'familia': ['matrimonio', 'hijos', 'herencia', 'tradiciones', 'educación'],
            'religion': ['sacrificios', 'profecías', 'dioses', 'rituales', 'templos'],
            'chisme': ['escándalo', 'secretos', 'romances', 'conflictos', 'noticias'],
            'conflicto': ['deudas', 'territorio', 'honor', 'traición', 'justicia'],
            'alianza': ['comercio', 'matrimonio', 'defensa mutua', 'tratados', 'recursos']
        }

        if categoria in temas:
            return random.choice(temas[categoria])

        return 'varios temas'

    def _crear_rumor(self, conv_id: int, año: int, persona_id: int, lugar_id: int, categoria: str, tema: str):
        """Crea un rumor basado en una conversación"""

        textos_rumor = [
            f"Se dice que algo importante ocurrió relacionado con {tema}",
            f"Corre el rumor sobre {tema} en la ciudad",
            f"Han escuchado sobre {tema}? Dicen que...",
            f"Las noticias sobre {tema} se extienden rápidamente",
            f"Se comenta en el mercado sobre {tema}",
        ]

        texto = random.choice(textos_rumor)
        veracidad = random.randint(50, 100)  # Los rumores nuevos suelen tener algo de verdad

        self.cursor.execute('''
            INSERT INTO rumores (
                año_origen, conversacion_origen_id, texto_original, texto_actual,
                categoria, veracidad, persona_origen_id, lugar_origen_id, alcance
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (año, conv_id, texto, texto, categoria, veracidad, persona_id, lugar_id, 'local'))

    def propagar_rumores_año(self, año: int):
        """Propaga rumores activos durante un año (efecto teléfono descompuesto)"""

        # Obtener rumores activos
        self.cursor.execute('''
            SELECT id, texto_actual, veracidad, lugar_origen_id, num_propagaciones
            FROM rumores
            WHERE activo = 1 AND año_origen <= ?
            ORDER BY RANDOM()
            LIMIT 20
        ''', (año,))

        rumores = self.cursor.fetchall()

        for rumor_id, texto, veracidad, lugar_id, num_prop in rumores:
            # Número de propagaciones este año (1-5)
            propagaciones = random.randint(1, 5)

            for _ in range(propagaciones):
                # Seleccionar emisor y receptor
                self.cursor.execute('''
                    SELECT id FROM personas
                    WHERE año_nacimiento <= ? AND (año_muerte IS NULL OR año_muerte >= ?)
                    ORDER BY RANDOM() LIMIT 2
                ''', (año, año))

                personas = self.cursor.fetchall()
                if len(personas) < 2:
                    continue

                emisor_id, receptor_id = personas[0][0], personas[1][0]

                # Calcular distorsión (aumenta con cada propagación)
                distorsion = min(100, num_prop * 5 + random.randint(0, 20))

                # Insertar propagación
                self.cursor.execute('''
                    INSERT INTO rumores_propagacion (
                        rumor_id, año_propagacion, emisor_id, receptor_id,
                        lugar_id, texto_transmitido, distorsion
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (rumor_id, año, emisor_id, receptor_id, lugar_id, texto, distorsion))

            # Actualizar contador de propagaciones
            nuevo_num_prop = num_prop + propagaciones

            # Rumor se extingue si ha sido muy propagado o muy distorsionado
            if nuevo_num_prop > 50 or veracidad < 10:
                self.cursor.execute('''
                    UPDATE rumores
                    SET activo = 0, año_extincion = ?, num_propagaciones = ?
                    WHERE id = ?
                ''', (año, nuevo_num_prop, rumor_id))
            else:
                self.cursor.execute('''
                    UPDATE rumores
                    SET num_propagaciones = ?, veracidad = MAX(0, veracidad - ?)
                    WHERE id = ?
                ''', (nuevo_num_prop, random.randint(1, 5), rumor_id))

        self.conn.commit()

    def generar_conocimiento_cultural_año(self, año: int):
        """Genera conocimiento cultural basado en eventos del año"""

        # Probabilidad de crear nueva leyenda/tradición (5% por año)
        if random.random() > 0.05:
            return 0

        self.cursor.execute('SELECT id, nombre FROM civilizaciones')
        civilizaciones = self.cursor.fetchall()

        if not civilizaciones:
            return 0

        civ = random.choice(civilizaciones)
        civ_id, civ_nombre = civ

        # Tipos de conocimiento
        tipos = ['leyenda', 'tradicion', 'tabú', 'ritual', 'tecnica']
        tipo = random.choice(tipos)

        # Generar nombre y descripción
        nombres = {
            'leyenda': f'La Leyenda del {random.choice(["Guerrero", "Chamán", "Héroe", "Espíritu"])} de {civ_nombre}',
            'tradicion': f'Tradición de {random.choice(["Cosecha", "Guerra", "Matrimonio", "Muerte"])} de {civ_nombre}',
            'tabú': f'Prohibición sobre {random.choice(["fuego sagrado", "animales", "lugares", "nombres"])}',
            'ritual': f'Ritual de {random.choice(["Invocación", "Protección", "Purificación", "Bendición"])}',
            'tecnica': f'Técnica de {random.choice(["metalurgia", "agricultura", "navegación", "combate"])}'
        }

        nombre = nombres[tipo]
        descripcion = f"Conocimiento cultural generado en el año {año} en {civ_nombre}"

        # Seleccionar creador
        self.cursor.execute('''
            SELECT id FROM personas
            WHERE año_nacimiento <= ? AND (año_muerte IS NULL OR año_muerte >= ?)
            ORDER BY RANDOM() LIMIT 1
        ''', (año, año))

        creador = self.cursor.fetchone()
        creador_id = creador[0] if creador else None

        # Insertar
        self.cursor.execute('''
            INSERT INTO conocimiento_cultural (
                civilizacion_id, año_creacion, tipo, nombre, descripcion,
                persona_creador_id, nivel_importancia, sagrado, secreto
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (civ_id, año, tipo, nombre, descripcion, creador_id,
              random.randint(1, 10),
              tipo in ['ritual', 'tabú'],
              random.random() < 0.2))

        self.conn.commit()
        return 1

    def simular_conversaciones_periodo(self, año_inicio: int, año_fin: int,
                                      conversaciones_por_año: int = 50):
        """
        Simula conversaciones para todo un período
        OPTIMIZADO: No genera una por una, usa batches
        """
        print(f"\n🗣️  Simulando conversaciones NPC {año_inicio}-{año_fin}...")
        print(f"   Generando ~{conversaciones_por_año} conversaciones por año")

        inicio = datetime.now()
        total_conversaciones = 0
        total_rumores = 0
        total_conocimiento = 0

        # Simular por décadas para mejor performance
        for decada_inicio in range(año_inicio, año_fin, 10):
            decada_fin = min(decada_inicio + 9, año_fin)

            for año in range(decada_inicio, decada_fin + 1):
                # Conversaciones
                conv = self.generar_conversaciones_año(año, conversaciones_por_año)
                total_conversaciones += conv

                # Propagar rumores
                self.propagar_rumores_año(año)

                # Generar conocimiento cultural
                conoc = self.generar_conocimiento_cultural_año(año)
                total_conocimiento += conoc

                if año % 100 == 0:
                    print(f"   Año {año}: {conv} conversaciones generadas")

            # Commit por década
            self.conn.commit()

        # Contar rumores generados
        self.cursor.execute('SELECT COUNT(*) FROM rumores WHERE año_origen >= ? AND año_origen <= ?',
                           (año_inicio, año_fin))
        total_rumores = self.cursor.fetchone()[0]

        fin = datetime.now()
        duracion = fin - inicio

        print(f"\n✅ Conversaciones simuladas:")
        print(f"   • {total_conversaciones:,} conversaciones NPC-to-NPC")
        print(f"   • {total_rumores:,} rumores generados")
        print(f"   • {total_conocimiento:,} piezas de conocimiento cultural")
        print(f"   • Duración: {duracion}")

        return total_conversaciones, total_rumores, total_conocimiento

    def obtener_estadisticas(self):
        """Obtiene estadísticas del sistema de conversaciones"""
        stats = {}

        # Conversaciones totales
        self.cursor.execute('SELECT COUNT(*) FROM conversaciones_historicas')
        stats['conversaciones_totales'] = self.cursor.fetchone()[0]

        # Por categoría
        self.cursor.execute('''
            SELECT categoria, COUNT(*)
            FROM conversaciones_historicas
            GROUP BY categoria
        ''')
        stats['por_categoria'] = dict(self.cursor.fetchall())

        # Rumores
        self.cursor.execute('SELECT COUNT(*) FROM rumores')
        stats['rumores_totales'] = self.cursor.fetchone()[0]

        self.cursor.execute('SELECT COUNT(*) FROM rumores WHERE activo = 1')
        stats['rumores_activos'] = self.cursor.fetchone()[0]

        # Conocimiento cultural
        self.cursor.execute('SELECT COUNT(*) FROM conocimiento_cultural')
        stats['conocimiento_total'] = self.cursor.fetchone()[0]

        self.cursor.execute('''
            SELECT tipo, COUNT(*)
            FROM conocimiento_cultural
            GROUP BY tipo
        ''')
        stats['conocimiento_por_tipo'] = dict(self.cursor.fetchall())

        return stats

    def close(self):
        """Cierra conexión"""
        self.conn.close()


def main():
    """Función principal de prueba"""
    print("=" * 70)
    print("SISTEMA DE CONVERSACIONES NPC")
    print("Portales del Quinto Sol")
    print("=" * 70)

    sistema = SistemaConversacionesNPC()

    # Crear schema
    sistema.crear_schema_conversaciones()

    # Simular período corto de prueba
    print("\n⚠️  Modo de prueba: simulando 10 años (1500-1510)")
    sistema.simular_conversaciones_periodo(1500, 1510, conversaciones_por_año=20)

    # Mostrar estadísticas
    print("\n📊 ESTADÍSTICAS:")
    stats = sistema.obtener_estadisticas()

    print(f"\nConversaciones: {stats['conversaciones_totales']:,}")
    print("\nPor categoría:")
    for cat, count in stats.get('por_categoria', {}).items():
        print(f"  • {cat}: {count}")

    print(f"\nRumores totales: {stats['rumores_totales']:,}")
    print(f"Rumores activos: {stats['rumores_activos']:,}")

    print(f"\nConocimiento cultural: {stats['conocimiento_total']:,}")
    if stats.get('conocimiento_por_tipo'):
        print("Por tipo:")
        for tipo, count in stats['conocimiento_por_tipo'].items():
            print(f"  • {tipo}: {count}")

    sistema.close()
    print("\n✅ Prueba completada")


if __name__ == '__main__':
    main()
