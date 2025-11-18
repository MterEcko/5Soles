#!/usr/bin/env python3
"""
Sistema de consultas para la base de datos genealógica
"""

import sqlite3
from typing import List, Tuple

class ConsultorGenealogico:
    def __init__(self, db_path='quinto_sol.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def estadisticas_generales(self):
        """Muestra estadísticas generales de la base de datos"""
        print("\n" + "="*70)
        print("ESTADÍSTICAS GENERALES")
        print("="*70 + "\n")

        # Total de personas
        self.cursor.execute("SELECT COUNT(*) FROM personas")
        total_personas = self.cursor.fetchone()[0]
        print(f"Total de personas: {total_personas:,}")

        # Personas por especie
        self.cursor.execute('''
            SELECT e.nombre, COUNT(p.id) as total
            FROM especies e
            LEFT JOIN personas p ON e.id = p.especie_id
            GROUP BY e.id, e.nombre
            ORDER BY total DESC
        ''')
        print("\nPersonas por especie:")
        for especie, total in self.cursor.fetchall():
            print(f"  • {especie}: {total:,}")

        # Personas por civilización
        self.cursor.execute('''
            SELECT c.nombre, COUNT(p.id) as total
            FROM civilizaciones c
            LEFT JOIN personas p ON c.id = p.civilizacion_id
            GROUP BY c.id, c.nombre
            ORDER BY total DESC
        ''')
        print("\nPersonas por civilización:")
        for civ, total in self.cursor.fetchall():
            print(f"  • {civ}: {total:,}")

        # Matrimonios
        self.cursor.execute("SELECT COUNT(*) FROM matrimonios")
        total_matrimonios = self.cursor.fetchone()[0]
        print(f"\nTotal de matrimonios: {total_matrimonios:,}")

        # Promedio de hijos
        self.cursor.execute("SELECT AVG(hijos_totales) FROM matrimonios WHERE hijos_totales > 0")
        promedio_hijos = self.cursor.fetchone()[0]
        if promedio_hijos:
            print(f"Promedio de hijos por matrimonio: {promedio_hijos:.2f}")

        # Personas por clase social
        self.cursor.execute('''
            SELECT clase_social, COUNT(*) as total
            FROM personas
            GROUP BY clase_social
            ORDER BY total DESC
        ''')
        print("\nPersonas por clase social:")
        for clase, total in self.cursor.fetchall():
            print(f"  • {clase}: {total:,}")

    def buscar_persona(self, nombre: str):
        """Busca una persona por nombre"""
        print(f"\n{'='*70}")
        print(f"BÚSQUEDA: '{nombre}'")
        print(f"{'='*70}\n")

        self.cursor.execute('''
            SELECT
                p.id,
                p.nombre_completo,
                p.genero,
                p.año_nacimiento,
                p.año_muerte,
                p.clase_social,
                c.nombre as civilizacion,
                e.nombre as especie
            FROM personas p
            LEFT JOIN civilizaciones c ON p.civilizacion_id = c.id
            LEFT JOIN especies e ON p.especie_id = e.id
            WHERE p.nombre LIKE ? OR p.apellido LIKE ? OR p.nombre_completo LIKE ?
            ORDER BY p.año_nacimiento
            LIMIT 20
        ''', (f'%{nombre}%', f'%{nombre}%', f'%{nombre}%'))

        resultados = self.cursor.fetchall()

        if not resultados:
            print("No se encontraron resultados.")
            return

        print(f"Se encontraron {len(resultados)} persona(s):\n")

        for persona in resultados:
            pid, nombre_comp, genero, nac, muerte, clase, civ, especie = persona
            edad = muerte - nac if muerte else "viva"
            print(f"ID: {pid}")
            print(f"  Nombre: {nombre_comp}")
            print(f"  Género: {genero}")
            print(f"  Años de vida: {nac} - {muerte} (vivió {edad} años)" if muerte else f"  Nacimiento: {nac}")
            print(f"  Clase: {clase}")
            print(f"  Civilización: {civ}")
            print(f"  Especie: {especie}")
            print()

    def ver_arbol_genealogico(self, persona_id: int, niveles: int = 3):
        """Muestra el árbol genealógico de una persona"""
        print(f"\n{'='*70}")
        print(f"ÁRBOL GENEALÓGICO - Persona ID: {persona_id}")
        print(f"{'='*70}\n")

        # Información de la persona
        self.cursor.execute('''
            SELECT nombre_completo, año_nacimiento, año_muerte, clase_social
            FROM personas WHERE id = ?
        ''', (persona_id,))

        persona = self.cursor.fetchone()
        if not persona:
            print("Persona no encontrada.")
            return

        nombre, nac, muerte, clase = persona
        print(f"📍 {nombre} ({nac}-{muerte or 'presente'})")
        print(f"   Clase: {clase}\n")

        # Padres
        self.cursor.execute('''
            SELECT
                p_padre.id, p_padre.nombre_completo, p_padre.año_nacimiento,
                p_madre.id, p_madre.nombre_completo, p_madre.año_nacimiento
            FROM personas p
            LEFT JOIN personas p_padre ON p.padre_id = p_padre.id
            LEFT JOIN personas p_madre ON p.madre_id = p_madre.id
            WHERE p.id = ?
        ''', (persona_id,))

        padres = self.cursor.fetchone()
        if padres and (padres[0] or padres[3]):
            print("👪 Padres:")
            if padres[0]:
                print(f"   👨 Padre: {padres[1]} (ID: {padres[0]}, nacido {padres[2]})")
            if padres[3]:
                print(f"   👩 Madre: {padres[4]} (ID: {padres[3]}, nacida {padres[5]})")
            print()

        # Cónyuge e hijos
        self.cursor.execute('''
            SELECT
                CASE
                    WHEN m.persona1_id = ? THEN m.persona2_id
                    ELSE m.persona1_id
                END as conyuge_id,
                p.nombre_completo,
                m.año_union,
                m.hijos_totales
            FROM matrimonios m
            JOIN personas p ON p.id = CASE
                WHEN m.persona1_id = ? THEN m.persona2_id
                ELSE m.persona1_id
            END
            WHERE m.persona1_id = ? OR m.persona2_id = ?
        ''', (persona_id, persona_id, persona_id, persona_id))

        matrimonio = self.cursor.fetchone()
        if matrimonio:
            conyuge_id, conyuge_nombre, año_union, hijos_total = matrimonio
            print(f"💑 Matrimonio:")
            print(f"   Cónyuge: {conyuge_nombre} (ID: {conyuge_id})")
            print(f"   Año de unión: {año_union}")
            print(f"   Hijos: {hijos_total}\n")

            # Listar hijos
            self.cursor.execute('''
                SELECT id, nombre_completo, genero, año_nacimiento, año_muerte, clase_social
                FROM personas
                WHERE (padre_id = ? AND madre_id = ?)
                   OR (padre_id = ? AND madre_id = ?)
                ORDER BY año_nacimiento
            ''', (persona_id, conyuge_id, conyuge_id, persona_id))

            hijos = self.cursor.fetchall()
            if hijos:
                print(f"👶 Hijos ({len(hijos)}):")
                for hijo in hijos:
                    h_id, h_nombre, h_gen, h_nac, h_muerte, h_clase = hijo
                    icono = "👦" if h_gen == "masculino" else "👧"
                    vida = f"{h_nac}-{h_muerte or 'presente'}"
                    print(f"   {icono} {h_nombre} (ID: {h_id}, {vida}, {h_clase})")
                print()

        # Hermanos
        if padres and (padres[0] or padres[3]):
            self.cursor.execute('''
                SELECT id, nombre_completo, genero, año_nacimiento
                FROM personas
                WHERE (padre_id = ? OR madre_id = ?)
                  AND id != ?
                ORDER BY año_nacimiento
            ''', (padres[0], padres[3], persona_id))

            hermanos = self.cursor.fetchall()
            if hermanos:
                print(f"👫 Hermanos ({len(hermanos)}):")
                for hermano in hermanos:
                    h_id, h_nombre, h_gen, h_nac = hermano
                    icono = "👨" if h_gen == "masculino" else "👩"
                    print(f"   {icono} {h_nombre} (ID: {h_id}, nacido {h_nac})")
                print()

    def ver_oficios_persona(self, persona_id: int):
        """Muestra los oficios de una persona"""
        print(f"\n{'='*70}")
        print(f"OFICIOS - Persona ID: {persona_id}")
        print(f"{'='*70}\n")

        self.cursor.execute('''
            SELECT p.nombre_completo
            FROM personas p WHERE id = ?
        ''', (persona_id,))

        nombre = self.cursor.fetchone()
        if not nombre:
            print("Persona no encontrada.")
            return

        print(f"📍 {nombre[0]}\n")

        self.cursor.execute('''
            SELECT
                o.nombre,
                o.categoria,
                po.nivel_maestria,
                po.es_principal,
                po.año_inicio
            FROM persona_oficios po
            JOIN oficios o ON po.oficio_id = o.id
            WHERE po.persona_id = ?
            ORDER BY po.es_principal DESC, po.nivel_maestria DESC
        ''', (persona_id,))

        oficios = self.cursor.fetchall()
        if not oficios:
            print("Esta persona no tiene oficios registrados.")
            return

        print(f"Oficios ({len(oficios)}):")
        for oficio in oficios:
            nombre_of, categoria, maestria, principal, año_inicio = oficio
            principal_str = "⭐ Principal" if principal else "  Secundario"
            print(f"  {principal_str}: {nombre_of}")
            print(f"    Categoría: {categoria}")
            print(f"    Maestría: {maestria}/10")
            if año_inicio:
                print(f"    Desde: {año_inicio}")
            print()

    def ver_habilidades_persona(self, persona_id: int):
        """Muestra las habilidades de una persona"""
        print(f"\n{'='*70}")
        print(f"HABILIDADES - Persona ID: {persona_id}")
        print(f"{'='*70}\n")

        self.cursor.execute('''
            SELECT p.nombre_completo
            FROM personas p WHERE id = ?
        ''', (persona_id,))

        nombre = self.cursor.fetchone()
        if not nombre:
            print("Persona no encontrada.")
            return

        print(f"📍 {nombre[0]}\n")

        self.cursor.execute('''
            SELECT
                h.nombre,
                h.categoria,
                h.nivel_poder,
                ph.nivel_dominio,
                ph.año_adquisicion,
                d.nombre as dios_asociado
            FROM persona_habilidades ph
            JOIN habilidades h ON ph.habilidad_id = h.id
            LEFT JOIN dioses d ON h.dios_asociado_id = d.id
            WHERE ph.persona_id = ?
            ORDER BY ph.nivel_dominio DESC, h.nivel_poder DESC
        ''', (persona_id,))

        habilidades = self.cursor.fetchall()
        if not habilidades:
            print("Esta persona no tiene habilidades registradas.")
            return

        print(f"Habilidades ({len(habilidades)}):")
        for habilidad in habilidades:
            nombre_hab, categoria, poder, dominio, año_adq, dios = habilidad
            print(f"  🌟 {nombre_hab}")
            print(f"    Categoría: {categoria}")
            print(f"    Poder: {poder}/10")
            print(f"    Dominio: {dominio}/10")
            if dios:
                print(f"    Dios asociado: {dios}")
            if año_adq:
                print(f"    Adquirida en: {año_adq}")
            print()

    def linajes_importantes(self, min_descendientes: int = 20):
        """Muestra los linajes más importantes (familias grandes)"""
        print(f"\n{'='*70}")
        print(f"LINAJES IMPORTANTES (mínimo {min_descendientes} descendientes)")
        print(f"{'='*70}\n")

        # Buscar personas con muchos descendientes
        self.cursor.execute('''
            WITH RECURSIVE descendientes(id, ancestro_id, nivel) AS (
                -- Caso base: personas originales
                SELECT id, id, 0
                FROM personas
                WHERE padre_id IS NULL AND madre_id IS NULL

                UNION ALL

                -- Caso recursivo: hijos
                SELECT p.id, d.ancestro_id, d.nivel + 1
                FROM personas p
                JOIN descendientes d ON p.padre_id = d.id OR p.madre_id = d.id
                WHERE d.nivel < 10  -- Limitar profundidad
            )
            SELECT
                p.id,
                p.nombre_completo,
                p.año_nacimiento,
                p.clase_social,
                COUNT(DISTINCT d.id) - 1 as total_descendientes
            FROM personas p
            JOIN descendientes d ON p.id = d.ancestro_id
            GROUP BY p.id, p.nombre_completo, p.año_nacimiento, p.clase_social
            HAVING total_descendientes >= ?
            ORDER BY total_descendientes DESC
            LIMIT 20
        ''', (min_descendientes,))

        linajes = self.cursor.fetchall()

        if not linajes:
            print(f"No se encontraron linajes con {min_descendientes} o más descendientes.")
            return

        print(f"Se encontraron {len(linajes)} linajes:\n")

        for i, linaje in enumerate(linajes, 1):
            pid, nombre, año_nac, clase, desc = linaje
            print(f"{i}. {nombre} (ID: {pid})")
            print(f"   Nacimiento: {año_nac}")
            print(f"   Clase: {clase}")
            print(f"   Descendientes: {desc}")
            print()

    def eventos_historicos(self):
        """Muestra eventos históricos"""
        print(f"\n{'='*70}")
        print(f"LÍNEA DE TIEMPO - EVENTOS HISTÓRICOS")
        print(f"{'='*70}\n")

        self.cursor.execute('''
            SELECT
                e.nombre,
                e.descripcion,
                e.tipo,
                e.año,
                er.nombre as era,
                pc.nombre as lugar
            FROM eventos e
            LEFT JOIN eras er ON e.era_id = er.id
            LEFT JOIN pueblos_ciudades pc ON e.lugar_id = pc.id
            ORDER BY e.año
        ''')

        eventos = self.cursor.fetchall()

        if not eventos:
            print("No hay eventos históricos registrados.")
            return

        era_actual = None
        for evento in eventos:
            nombre, desc, tipo, año, era, lugar = evento

            if era != era_actual:
                print(f"\n{'─'*70}")
                print(f"⏳ {era or 'Era Desconocida'}")
                print(f"{'─'*70}\n")
                era_actual = era

            icono = {
                'batalla': '⚔️',
                'fundacion': '🏛️',
                'catastrofe': '💥',
                'portal': '🌀',
                'divino': '✨',
                'tratado': '📜',
                'unificacion': '🤝',
            }.get(tipo, '📍')

            print(f"{icono} {año}: {nombre}")
            print(f"   {desc}")
            if lugar:
                print(f"   Lugar: {lugar}")
            print()

    def cerrar(self):
        """Cierra la conexión"""
        self.conn.close()


def menu_principal():
    """Menú interactivo"""
    consultor = ConsultorGenealogico()

    while True:
        print("\n" + "="*70)
        print("PORTALES DEL QUINTO SOL - Sistema de Consultas")
        print("="*70)
        print("\n1. Estadísticas generales")
        print("2. Buscar persona por nombre")
        print("3. Ver árbol genealógico (por ID)")
        print("4. Ver oficios de una persona (por ID)")
        print("5. Ver habilidades de una persona (por ID)")
        print("6. Linajes importantes")
        print("7. Eventos históricos")
        print("8. Salir")

        opcion = input("\nSelecciona una opción: ")

        try:
            if opcion == '1':
                consultor.estadisticas_generales()
            elif opcion == '2':
                nombre = input("Nombre a buscar: ")
                consultor.buscar_persona(nombre)
            elif opcion == '3':
                persona_id = int(input("ID de la persona: "))
                consultor.ver_arbol_genealogico(persona_id)
            elif opcion == '4':
                persona_id = int(input("ID de la persona: "))
                consultor.ver_oficios_persona(persona_id)
            elif opcion == '5':
                persona_id = int(input("ID de la persona: "))
                consultor.ver_habilidades_persona(persona_id)
            elif opcion == '6':
                min_desc = int(input("Mínimo de descendientes (default 20): ") or "20")
                consultor.linajes_importantes(min_desc)
            elif opcion == '7':
                consultor.eventos_historicos()
            elif opcion == '8':
                print("\n¡Hasta pronto!")
                break
            else:
                print("\nOpción inválida.")

            input("\nPresiona Enter para continuar...")

        except ValueError as e:
            print(f"\nError: {e}")
            input("\nPresiona Enter para continuar...")
        except Exception as e:
            print(f"\nError inesperado: {e}")
            input("\nPresiona Enter para continuar...")

    consultor.cerrar()


if __name__ == '__main__':
    menu_principal()
