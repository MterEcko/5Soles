#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulación Mundo Completo - Portales del Quinto Sol
Sistema Maestro que integra TODOS los sistemas

FASE 1: Simulación Histórica (1500-3000)
- 16 sistemas principales + adicionales
- Conversaciones NPC-to-NPC
- Generación de cultura, rumores, leyendas
- ~270,000 NPCs con historia completa

FASE 2: Preparación para Jugadores (año 3000+)
- Exporta datos listos para servidor de tiempo real
- Crea índices optimizados
- Genera resumen estadístico completo
"""

import os
import sys
from datetime import datetime
from typing import Dict, Any

# Importar módulo de conexión unificado
from database_connector import DatabaseConnector, get_db_connection

# Importar sistemas
try:
    from sistema_conversaciones_npcs import SistemaConversacionesNPC
except ImportError:
    print("⚠️  sistema_conversaciones_npcs.py no encontrado")


class SimulacionMundoCompleto:
    """Orquestador maestro de toda la simulación"""

    def __init__(self, año_inicio: int = 1500, año_fin: int = 3000):
        self.año_inicio = año_inicio
        self.año_fin = año_fin
        self.años_totales = año_fin - año_inicio

        # Conexión de base de datos
        self.db = DatabaseConnector()
        self.conn = None
        self.cursor = None

        # Estadísticas
        self.stats = {
            'inicio_simulacion': None,
            'fin_simulacion': None,
            'duracion_total': None,
            'poblacion_inicial': 0,
            'poblacion_final': 0,
            'conversaciones_generadas': 0,
            'rumores_generados': 0,
            'conocimiento_cultural': 0,
            'guerras_totales': 0,
            'mutaciones_totales': 0,
            'hibridos_totales': 0,
            'artefactos_totales': 0,
            'organizaciones_totales': 0,
        }

    def conectar(self):
        """Establece conexión a base de datos"""
        self.conn = self.db.connect()
        # DatabaseConnector ya creó cursor con conversión de placeholders
        self.cursor = self.db.cursor
        print(f"✅ Conectado a base de datos")

    def execute(self, query, params=None):
        """
        Wrapper para ejecutar queries con conversión automática de placeholders
        SQLite usa ? | PostgreSQL usa %s
        """
        if self.db.db_type == 'postgres' and '?' in query:
            query = query.replace('?', '%s')

        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor

    def verificar_prerequisitos(self) -> bool:
        """Verifica que todos los schemas y datos base existan"""
        print("\n" + "=" * 70)
        print("VERIFICANDO PREREQUISITOS")
        print("=" * 70)

        verificaciones = []

        # 1. Verificar tablas principales
        tablas_requeridas = [
            'especies', 'civilizaciones', 'dioses', 'personas',
            'pueblos_ciudades', 'especies_civilizaciones',
            'guerras_especies', 'mutaciones_catalogo',
            'artefactos', 'organizaciones', 'monedas'
        ]

        for tabla in tablas_requeridas:
            self.execute(f"SELECT COUNT(*) FROM {tabla}")
            count = self.cursor.fetchone()[0]
            verificaciones.append((tabla, count > 0, count))

        # Mostrar resultados
        print("\n📋 Tablas verificadas:")
        for tabla, existe, count in verificaciones:
            status = "✅" if existe else "❌"
            print(f"  {status} {tabla}: {count} registros")

        # Verificar población inicial
        self.execute("SELECT COUNT(*) FROM personas WHERE año_nacimiento = ?", (self.año_inicio,))
        pob_inicial = self.cursor.fetchone()[0]
        self.stats['poblacion_inicial'] = pob_inicial

        print(f"\n👥 Población inicial (año {self.año_inicio}): {pob_inicial:,}")

        if pob_inicial == 0:
            print("⚠️  ADVERTENCIA: No hay población inicial")
            print("   Ejecutar primero: generar_poblacion.py y generar_genealogias_especies.py")
            return False

        # Todo OK
        todas_ok = all(existe for _, existe, _ in verificaciones)

        if todas_ok:
            print("\n✅ Todos los prerequisitos verificados")
        else:
            print("\n❌ Faltan prerequisitos")

        return todas_ok

    def ejecutar_fase_1_historica(self):
        """
        FASE 1: Simulación histórica completa (1500-3000)

        Ejecuta en orden:
        1. Relaciones especies-civilizaciones
        2. Genealogías humanos (ya ejecutado previamente)
        3. Genealogías especies sirvientes
        4. Longevidad por oficios
        5. Guerras inter-especies
        6. Mutaciones
        7. Matrimonios inter-especies
        8. Artefactos
        9. Organizaciones
        10. Eventos divinos
        11. Migraciones
        12. Justicia
        13. Clima
        14. Economía
        15. CONVERSACIONES NPC (NUEVO)
        """
        print("\n" + "=" * 70)
        print("FASE 1: SIMULACIÓN HISTÓRICA (1500-3000)")
        print("=" * 70)

        self.stats['inicio_simulacion'] = datetime.now()

        # ============================================================
        # 1. SISTEMAS PRINCIPALES
        # ============================================================
        print("\n" + "=" * 70)
        print("EJECUTANDO SISTEMAS PRINCIPALES")
        print("=" * 70)

        # Nota: Los sistemas ya deberían estar ejecutados por simulacion_completa_1500_3000.py
        # Aquí solo verificamos que existan datos

        self._verificar_sistema("personas", "Genealogías")
        self._verificar_sistema("guerras_especies", "Guerras")
        self._verificar_sistema("personas_mutaciones", "Mutaciones")
        self._verificar_sistema("personas_hibridas", "Híbridos")

        # ============================================================
        # 2. SISTEMAS ADICIONALES
        # ============================================================
        print("\n" + "=" * 70)
        print("EJECUTANDO SISTEMAS ADICIONALES")
        print("=" * 70)

        # Verificar si ya fueron ejecutados
        self._verificar_sistema("artefactos", "Artefactos")
        self._verificar_sistema("organizaciones", "Organizaciones")
        self._verificar_sistema("eventos_divinos_mayores", "Eventos Divinos")
        self._verificar_sistema("migraciones", "Migraciones")
        self._verificar_sistema("crimenes", "Crímenes")
        self._verificar_sistema("ciclos_climaticos", "Clima")
        self._verificar_sistema("monedas", "Economía")

        # ============================================================
        # 3. SISTEMA DE CONVERSACIONES NPC (NUEVO)
        # ============================================================
        print("\n" + "=" * 70)
        print("SISTEMA DE CONVERSACIONES NPC")
        print("=" * 70)

        # Verificar si ya existe tabla
        try:
            self.execute("SELECT COUNT(*) FROM conversaciones_historicas")
            ya_existe = True
            count_existente = self.cursor.fetchone()[0]
            print(f"✅ Sistema de conversaciones ya existe: {count_existente:,} conversaciones")

            if count_existente > 0:
                respuesta = input("\n¿Regenerar conversaciones? (s/n): ").strip().lower()
                if respuesta != 's':
                    print("⏭️  Saltando generación de conversaciones")
                    self.stats['conversaciones_generadas'] = count_existente
                    return

        except:
            ya_existe = False

        # Crear sistema de conversaciones
        print("\n🗣️  Inicializando sistema de conversaciones...")
        sistema_conv = SistemaConversacionesNPC()

        # Crear schema si no existe
        if not ya_existe:
            sistema_conv.crear_schema_conversaciones()

        # Calcular conversaciones por año (basado en población)
        self.execute("SELECT COUNT(*) FROM personas")
        poblacion_total = self.cursor.fetchone()[0]

        # ~1 conversación por cada 500 personas por año (ajustable)
        conversaciones_por_año = max(50, poblacion_total // 500)

        print(f"\n📊 Parámetros de simulación:")
        print(f"   • Población total: {poblacion_total:,}")
        print(f"   • Conversaciones por año: {conversaciones_por_año:,}")
        print(f"   • Años a simular: {self.años_totales}")
        print(f"   • Total estimado: {conversaciones_por_año * self.años_totales:,} conversaciones")
        print(f"\n⏱️  Tiempo estimado: 30-60 minutos\n")

        respuesta = input("¿Continuar con generación de conversaciones? (s/n): ").strip().lower()

        if respuesta == 's':
            # Simular conversaciones
            conv, rumores, conocimiento = sistema_conv.simular_conversaciones_periodo(
                self.año_inicio,
                self.año_fin,
                conversaciones_por_año=conversaciones_por_año
            )

            self.stats['conversaciones_generadas'] = conv
            self.stats['rumores_generados'] = rumores
            self.stats['conocimiento_cultural'] = conocimiento

            print("\n✅ Sistema de conversaciones completado")

        sistema_conv.close()

    def _verificar_sistema(self, tabla: str, nombre: str):
        """Verifica que un sistema tenga datos"""
        try:
            self.execute(f"SELECT COUNT(*) FROM {tabla}")
            count = self.cursor.fetchone()[0]

            if count > 0:
                print(f"✅ {nombre}: {count:,} registros")

                # Guardar en stats
                if 'guerras' in tabla:
                    self.stats['guerras_totales'] = count
                elif 'mutaciones' in tabla:
                    self.stats['mutaciones_totales'] = count
                elif 'hibridas' in tabla:
                    self.stats['hibridos_totales'] = count
                elif 'artefactos' in tabla:
                    self.stats['artefactos_totales'] = count
                elif 'organizaciones' in tabla:
                    self.stats['organizaciones_totales'] = count

            else:
                print(f"⚠️  {nombre}: Sin datos (ejecutar sistema correspondiente)")

        except Exception as e:
            print(f"❌ {nombre}: Error - {e}")

    def recopilar_estadisticas_finales(self):
        """Recopila estadísticas completas del mundo simulado"""
        print("\n" + "=" * 70)
        print("RECOPILANDO ESTADÍSTICAS FINALES")
        print("=" * 70)

        # Población final
        self.execute(
            "SELECT COUNT(*) FROM personas WHERE año_nacimiento <= ? AND (año_muerte IS NULL OR año_muerte > ?)",
            (self.año_fin, self.año_fin)
        )
        self.stats['poblacion_final'] = self.cursor.fetchone()[0]

        # Poblaciones por especie
        self.execute('''
            SELECT e.nombre, COUNT(p.id)
            FROM especies e
            LEFT JOIN personas p ON p.especie_id = e.id
            WHERE p.año_nacimiento <= ? AND (p.año_muerte IS NULL OR p.año_muerte > ?)
            GROUP BY e.nombre
        ''', (self.año_fin, self.año_fin))

        poblaciones_especie = dict(self.cursor.fetchall())

        # Más estadísticas
        estadisticas = {
            'Personas totales generadas': None,
            'Población viva en año 3000': self.stats['poblacion_final'],
            'Poblaciones por especie': poblaciones_especie,
            'Guerras inter-especies': None,
            'Batallas totales': None,
            'Mutaciones genéticas': None,
            'Híbridos inter-especies': None,
            'Artefactos legendarios': None,
            'Organizaciones': None,
            'Conversaciones NPC': self.stats['conversaciones_generadas'],
            'Rumores generados': self.stats['rumores_generados'],
            'Conocimiento cultural': self.stats['conocimiento_cultural'],
        }

        # Obtener datos de cada sistema
        queries = {
            'Personas totales generadas': "SELECT COUNT(*) FROM personas",
            'Guerras inter-especies': "SELECT COUNT(*) FROM guerras_especies",
            'Batallas totales': "SELECT COUNT(*) FROM batallas_guerras",
            'Mutaciones genéticas': "SELECT COUNT(*) FROM personas_mutaciones",
            'Híbridos inter-especies': "SELECT COUNT(*) FROM personas_hibridas",
            'Artefactos legendarios': "SELECT COUNT(*) FROM artefactos",
            'Organizaciones': "SELECT COUNT(*) FROM organizaciones",
        }

        for nombre, query in queries.items():
            try:
                self.execute(query)
                estadisticas[nombre] = self.cursor.fetchone()[0]
            except:
                estadisticas[nombre] = 0

        self.stats['fin_simulacion'] = datetime.now()
        self.stats['duracion_total'] = self.stats['fin_simulacion'] - self.stats['inicio_simulacion']

        # Mostrar estadísticas
        print("\n" + "=" * 70)
        print("📊 ESTADÍSTICAS DEL MUNDO SIMULADO")
        print("=" * 70)

        print(f"\n🕐 Simulación: {self.año_inicio} → {self.año_fin} ({self.años_totales} años)")
        print(f"⏱️  Duración: {self.stats['duracion_total']}")

        print(f"\n👥 POBLACIÓN:")
        print(f"   • Total generada: {estadisticas['Personas totales generadas']:,}")
        print(f"   • Viva en año {self.año_fin}: {estadisticas['Población viva en año 3000']:,}")
        print(f"\n   Por especie:")
        for especie, count in poblaciones_especie.items():
            print(f"     • {especie}: {count:,}")

        print(f"\n⚔️  CONFLICTOS:")
        print(f"   • Guerras: {estadisticas['Guerras inter-especies']:,}")
        print(f"   • Batallas: {estadisticas['Batallas totales']:,}")

        print(f"\n🧬 GENÉTICA:")
        print(f"   • Mutaciones: {estadisticas['Mutaciones genéticas']:,}")
        print(f"   • Híbridos: {estadisticas['Híbridos inter-especies']:,}")

        print(f"\n🏛️  CULTURA:")
        print(f"   • Artefactos: {estadisticas['Artefactos legendarios']:,}")
        print(f"   • Organizaciones: {estadisticas['Organizaciones']:,}")

        print(f"\n🗣️  CONVERSACIONES:")
        print(f"   • Conversaciones NPC: {estadisticas['Conversaciones NPC']:,}")
        print(f"   • Rumores: {estadisticas['Rumores generados']:,}")
        print(f"   • Conocimiento cultural: {estadisticas['Conocimiento cultural']:,}")

        # Guardar estadísticas en archivo
        self._guardar_estadisticas(estadisticas)

        return estadisticas

    def _guardar_estadisticas(self, stats: Dict[str, Any]):
        """Guarda estadísticas en archivo markdown"""
        filename = f"ESTADISTICAS_MUNDO_{self.año_fin}.md"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# Estadísticas del Mundo Simulado\n")
            f.write(f"## Portales del Quinto Sol - Año {self.año_fin}\n\n")
            f.write(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")

            f.write("## 📊 Resumen Ejecutivo\n\n")
            f.write(f"- **Período simulado:** {self.año_inicio} - {self.año_fin} ({self.años_totales} años)\n")
            f.write(f"- **Duración simulación:** {self.stats['duracion_total']}\n")
            f.write(f"- **Población final:** {stats['Población viva en año 3000']:,} NPCs\n\n")

            f.write("## 👥 Población\n\n")
            f.write(f"**Total generada:** {stats['Personas totales generadas']:,}\n\n")
            f.write(f"**Viva en año {self.año_fin}:** {stats['Población viva en año 3000']:,}\n\n")

            f.write("### Por Especie\n\n")
            f.write("| Especie | Población |\n")
            f.write("|---------|----------|\n")
            for especie, count in stats['Poblaciones por especie'].items():
                f.write(f"| {especie} | {count:,} |\n")

            f.write("\n## ⚔️ Conflictos\n\n")
            f.write(f"- **Guerras inter-especies:** {stats['Guerras inter-especies']:,}\n")
            f.write(f"- **Batallas totales:** {stats['Batallas totales']:,}\n\n")

            f.write("## 🧬 Genética\n\n")
            f.write(f"- **Mutaciones:** {stats['Mutaciones genéticas']:,} personas con mutaciones\n")
            f.write(f"- **Híbridos:** {stats['Híbridos inter-especies']:,} individuos inter-especies\n\n")

            f.write("## 🏛️ Cultura\n\n")
            f.write(f"- **Artefactos legendarios:** {stats['Artefactos legendarios']:,}\n")
            f.write(f"- **Organizaciones:** {stats['Organizaciones']:,}\n\n")

            f.write("## 🗣️ Conversaciones y Rumores\n\n")
            f.write(f"- **Conversaciones NPC-to-NPC:** {stats['Conversaciones NPC']:,}\n")
            f.write(f"- **Rumores generados:** {stats['Rumores generados']:,}\n")
            f.write(f"- **Conocimiento cultural:** {stats['Conocimiento cultural']:,}\n\n")

            f.write("---\n\n")
            f.write("## 🎮 Mundo Listo para Jugadores\n\n")
            f.write("El mundo está completamente simulado y listo para:\n\n")
            f.write("1. **Entrada de jugadores** en año 3000+\n")
            f.write("2. **Servidor de tiempo real** (1 hora real = 1 día juego)\n")
            f.write("3. **Sistema de chat NPC** con memoria histórica\n")
            f.write("4. **Economía dual** (física + cripto)\n")
            f.write("5. **NPCs con 1500 años de historia**\n\n")

        print(f"\n✅ Estadísticas guardadas en: {filename}")

    def preparar_para_produccion(self):
        """Prepara base de datos para servidor de producción"""
        print("\n" + "=" * 70)
        print("PREPARANDO PARA PRODUCCIÓN")
        print("=" * 70)

        print("\n🔧 Creando índices optimizados...")

        indices = [
            "CREATE INDEX IF NOT EXISTS idx_personas_vivos_3000 ON personas(especie_id) WHERE año_nacimiento <= 3000 AND (año_muerte IS NULL OR año_muerte > 3000)",
            "CREATE INDEX IF NOT EXISTS idx_conversaciones_año ON conversaciones_historicas(año)",
            "CREATE INDEX IF NOT EXISTS idx_rumores_activos ON rumores(activo, alcance) WHERE activo = 1",
            "CREATE INDEX IF NOT EXISTS idx_conocimiento_civ ON conocimiento_cultural(civilizacion_id, tipo)",
        ]

        for idx in indices:
            try:
                self.execute(idx)
                print("  ✅ Índice creado")
            except:
                print("  ⚠️  Índice ya existe o error")

        self.db.commit()

        print("\n✅ Base de datos lista para producción")

    def ejecutar_simulacion_completa(self):
        """Ejecuta simulación completa del mundo"""
        print("\n" + "=" * 70)
        print("SIMULACIÓN MUNDO COMPLETO")
        print("PORTALES DEL QUINTO SOL")
        print("=" * 70)

        # Conectar
        self.conectar()

        # Verificar prerequisitos
        if not self.verificar_prerequisitos():
            print("\n❌ No se puede continuar sin prerequisitos")
            print("\nEjecuta primero:")
            print("  1. python3 simulacion_completa_1500_3000.py")
            print("  2. python3 sistemas_adicionales_integrados.py")
            return

        # Ejecutar fase 1 (histórica)
        self.ejecutar_fase_1_historica()

        # Recopilar estadísticas
        self.recopilar_estadisticas_finales()

        # Preparar para producción
        self.preparar_para_produccion()

        # Cerrar conexión
        self.db.close()

        print("\n" + "=" * 70)
        print("✅ SIMULACIÓN MUNDO COMPLETO TERMINADA")
        print("=" * 70)

        print("\n🎮 Siguiente paso:")
        print("   Ejecutar servidor de tiempo real:")
        print("   python3 servidor_tiempo_juego.py")


def main():
    """Función principal"""
    print("\n⚠️  Este script ejecuta la simulación COMPLETA del mundo")
    print("⚠️  Incluye sistemas principales + adicionales + conversaciones NPC")
    print("⚠️  Tiempo estimado: 3-8 horas\n")

    respuesta = input("¿Continuar? (s/n): ").strip().lower()

    if respuesta == 's':
        simulacion = SimulacionMundoCompleto(año_inicio=1500, año_fin=3000)
        simulacion.ejecutar_simulacion_completa()
    else:
        print("❌ Cancelado")


if __name__ == '__main__':
    main()
