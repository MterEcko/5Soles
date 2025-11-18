#!/usr/bin/env python3
"""
Modelo de IA Conversacional para NPCs
Sistema de diálogos con memoria, personalidad y contexto histórico
"""

import sqlite3
import random
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class NPCConversacional:
    """
    NPC con IA conversacional que:
    - Tiene personalidad única
    - Recuerda interacciones pasadas
    - Hereda memorias de sus padres
    - Responde según necesidades y contexto
    """

    def __init__(self, npc_id: int, conn: sqlite3.Connection):
        self.npc_id = npc_id
        self.conn = conn
        self.cursor = conn.cursor()

        # Cargar información del NPC
        self.cargar_informacion()
        self.cargar_personalidad()
        self.cargar_memorias()

    def cargar_informacion(self):
        """Carga información básica del NPC"""
        self.cursor.execute('''
            SELECT
                p.nombre_completo,
                p.genero,
                p.año_nacimiento,
                p.año_muerte,
                p.clase_social,
                c.nombre as civilizacion,
                d.nombre as dios_patron,
                p.padre_id,
                p.madre_id,
                p.lugar_residencia_id
            FROM personas p
            LEFT JOIN civilizaciones c ON p.civilizacion_id = c.id
            LEFT JOIN dioses d ON p.dios_patron_id = d.id
            WHERE p.id = ?
        ''', (self.npc_id,))

        row = self.cursor.fetchone()
        if not row:
            raise ValueError(f"NPC {self.npc_id} no encontrado")

        (self.nombre, self.genero, self.año_nac, self.año_muerte,
         self.clase_social, self.civilizacion, self.dios_patron,
         self.padre_id, self.madre_id, self.lugar_id) = row

        # Cargar oficios
        self.cursor.execute('''
            SELECT o.nombre, po.nivel_maestria, po.es_principal
            FROM persona_oficios po
            JOIN oficios o ON po.oficio_id = o.id
            WHERE po.persona_id = ?
            ORDER BY po.es_principal DESC, po.nivel_maestria DESC
        ''', (self.npc_id,))
        self.oficios = self.cursor.fetchall()
        self.oficio_principal = self.oficios[0][0] if self.oficios else "campesino"

    def cargar_personalidad(self):
        """Carga rasgos de personalidad"""
        self.cursor.execute('''
            SELECT rp.nombre, rp.categoria, pp.intensidad
            FROM persona_personalidad pp
            JOIN rasgos_personalidad rp ON pp.rasgo_id = rp.id
            WHERE pp.persona_id = ?
            ORDER BY pp.intensidad DESC
        ''', (self.npc_id,))

        self.rasgos = {}
        for nombre, categoria, intensidad in self.cursor.fetchall():
            self.rasgos[nombre] = {
                'categoria': categoria,
                'intensidad': intensidad
            }

    def cargar_memorias(self, jugador_id: Optional[int] = None):
        """Carga memorias relevantes"""
        if jugador_id:
            # Memorias específicas del jugador
            self.cursor.execute('''
                SELECT tipo_memoria, descripcion, importancia, año, emocion
                FROM memoria_npc
                WHERE npc_id = ? AND (jugador_id = ? OR jugador_id IS NULL)
                ORDER BY importancia DESC, año DESC
                LIMIT 20
            ''', (self.npc_id, jugador_id))
        else:
            # Memorias generales
            self.cursor.execute('''
                SELECT tipo_memoria, descripcion, importancia, año, emocion
                FROM memoria_npc
                WHERE npc_id = ?
                ORDER BY importancia DESC, año DESC
                LIMIT 20
            ''', (self.npc_id,))

        self.memorias = self.cursor.fetchall()

    def cargar_memorias_heredadas(self) -> List[Dict]:
        """Carga memorias de los padres (para diálogos de sucesión)"""
        memorias_padres = []

        for padre_id in [self.padre_id, self.madre_id]:
            if padre_id:
                self.cursor.execute('''
                    SELECT
                        p.nombre_completo,
                        m.descripcion,
                        m.año,
                        m.importancia,
                        m.jugador_id
                    FROM memoria_npc m
                    JOIN personas p ON m.npc_id = p.id
                    WHERE m.npc_id = ? AND m.importancia >= 7
                    ORDER BY m.importancia DESC
                    LIMIT 5
                ''', (padre_id,))

                for nombre_padre, desc, año, imp, jug_id in self.cursor.fetchall():
                    memorias_padres.append({
                        'nombre_padre': nombre_padre,
                        'descripcion': desc,
                        'año': año,
                        'importancia': imp,
                        'jugador_id': jug_id
                    })

        return memorias_padres

    def obtener_necesidad_critica(self) -> Optional[str]:
        """Obtiene la necesidad más crítica del NPC"""
        self.cursor.execute('''
            SELECT n.nombre, pn.nivel_actual, pn.nivel_minimo
            FROM persona_necesidades pn
            JOIN necesidades n ON pn.necesidad_id = n.id
            WHERE pn.persona_id = ? AND pn.nivel_actual < pn.nivel_minimo
            ORDER BY (pn.nivel_actual - pn.nivel_minimo)
            LIMIT 1
        ''', (self.npc_id,))

        row = self.cursor.fetchone()
        return row[0] if row else None

    def tiene_rasgo(self, rasgo: str, min_intensidad: int = 5) -> bool:
        """Verifica si el NPC tiene un rasgo con cierta intensidad"""
        if rasgo in self.rasgos:
            return self.rasgos[rasgo]['intensidad'] >= min_intensidad
        return False

    def generar_saludo(self, jugador_id: Optional[int] = None, año_actual: int = 1500) -> str:
        """Genera un saludo contextual"""

        # Verificar si hay memorias previas con el jugador
        if jugador_id:
            self.cursor.execute('''
                SELECT COUNT(*) FROM memoria_npc
                WHERE npc_id = ? AND jugador_id = ? AND tipo_memoria = 'interaccion'
            ''', (self.npc_id, jugador_id))
            num_interacciones = self.cursor.fetchone()[0]
        else:
            num_interacciones = 0

        # Saludo según personalidad y contexto
        saludos = []

        # Primera interacción
        if num_interacciones == 0:
            if self.tiene_rasgo('Amigable'):
                saludos.append(f"¡Saludos, viajero! Soy {self.nombre}, {self.oficio_principal} de {self.civilizacion}.")
            elif self.tiene_rasgo('Hostil'):
                saludos.append(f"¿Qué quieres? No tengo tiempo para extraños.")
            elif self.tiene_rasgo('Tímido'):
                saludos.append(f"Ah... hola. Me llamo {self.nombre}. ¿Necesitas algo?")
            else:
                saludos.append(f"Bienvenido. Soy {self.nombre}, {self.oficio_principal}.")

        # Interacción previa
        else:
            if self.tiene_rasgo('Amigable'):
                saludos.append(f"¡{self.nombre} te saluda! Es bueno verte de nuevo, amigo.")
            elif self.tiene_rasgo('Carismático'):
                saludos.append(f"¡Ah, mi cliente favorito! ¿Qué te trae por aquí hoy?")
            else:
                saludos.append(f"Has vuelto. ¿En qué puedo ayudarte?")

        # Verificar si es sucesor de alguien que conoció al jugador
        memorias_heredadas = self.cargar_memorias_heredadas()
        memoria_relevante = [m for m in memorias_heredadas if m.get('jugador_id') == jugador_id]

        if memoria_relevante and num_interacciones == 0:
            memoria = memoria_relevante[0]
            saludos.append(
                f"\nEspera... {memoria['nombre_padre']} me habló de ti. "
                f"Decía que {memoria['descripcion'].lower()}"
            )

        # Añadir contexto de necesidades
        necesidad = self.obtener_necesidad_critica()
        if necesidad:
            if necesidad == 'Materiales de Trabajo':
                saludos.append(f"\n(Parece preocupado) Necesito más materiales para trabajar...")
            elif necesidad == 'Comida':
                saludos.append(f"\n(Se ve hambriento)")
            elif necesidad == 'Clientes':
                saludos.append(f"\n¡Perfecta oportunidad! Necesito clientes urgentemente.")

        return ''.join(saludos)

    def generar_dialogo_comercio(self, item_solicitado: str, cantidad: int) -> Dict:
        """
        Genera diálogo y procesa transacción comercial

        Returns:
            Dict con: 'respuesta', 'tiene_item', 'precio', 'actitud'
        """

        # Verificar si el NPC produce ese item
        puede_crear = self._puede_crear_item(item_solicitado)

        respuesta = {
            'respuesta': '',
            'tiene_item': False,
            'precio': 0,
            'actitud': 'neutral'
        }

        # Determinar si tiene el item
        self.cursor.execute('''
            SELECT pi.cantidad, pi.calidad, i.valor_base
            FROM persona_inventario pi
            JOIN items i ON pi.item_id = i.id
            WHERE pi.persona_id = ? AND i.nombre = ?
        ''', (self.npc_id, item_solicitado))

        inventario = self.cursor.fetchone()

        if inventario:
            cantidad_disponible, calidad, valor_base = inventario
            respuesta['tiene_item'] = cantidad_disponible >= cantidad
            respuesta['precio'] = valor_base * cantidad * (calidad / 5.0)

            if respuesta['tiene_item']:
                # Personalidad afecta la respuesta
                if self.tiene_rasgo('Generoso'):
                    respuesta['respuesta'] = f"¡Por supuesto! Tengo {item_solicitado} de excelente calidad. Para ti, un precio justo."
                    respuesta['precio'] *= 0.9  # 10% descuento
                    respuesta['actitud'] = 'amigable'

                elif self.tiene_rasgo('Avaro'):
                    respuesta['respuesta'] = f"Tengo {item_solicitado}, pero es escaso y valioso... El precio es alto."
                    respuesta['precio'] *= 1.3  # 30% más caro
                    respuesta['actitud'] = 'codiciosa'

                elif self.tiene_rasgo('Honesto'):
                    respuesta['respuesta'] = f"Sí, tengo {cantidad} {item_solicitado}. El precio justo es {int(respuesta['precio'])} en trueque."
                    respuesta['actitud'] = 'profesional'

                else:
                    respuesta['respuesta'] = f"Tengo lo que buscas. {cantidad} {item_solicitado}."
                    respuesta['actitud'] = 'neutral'

            else:
                respuesta['respuesta'] = f"Solo tengo {cantidad_disponible} {item_solicitado}, no suficiente para tu pedido."

        elif puede_crear:
            respuesta['respuesta'] = f"No tengo {item_solicitado} en este momento, pero puedo fabricarlo si me traes los materiales."
            respuesta['actitud'] = 'servicial'

        else:
            if self.tiene_rasgo('Amigable'):
                respuesta['respuesta'] = f"Lo siento, no trabajo con {item_solicitado}. Quizás otro artesano pueda ayudarte."
            else:
                respuesta['respuesta'] = f"No tengo eso. Busca en otro lado."
                respuesta['actitud'] = 'desinteresada'

        return respuesta

    def _puede_crear_item(self, item: str) -> bool:
        """Verifica si el NPC puede crear un item según su oficio"""
        mapeo_oficios_items = {
            'Herrero': ['Macuahuitl', 'Espada', 'Hacha', 'Martillo', 'Pico'],
            'Carpintero': ['Arco', 'Escudo de Madera', 'Lanza', 'Madera'],
            'Alfarero': ['Vasija', 'Plato', 'Taza'],
            'Cocinero': ['Pan de Maíz', 'Tortillas', 'Tamales'],
            'Pescador': ['Pescado Fresco'],
            'Alquimista': ['Poción', 'Elixir', 'Antídoto'],
        }

        for oficio, _ , _ in self.oficios:
            if oficio in mapeo_oficios_items:
                if any(item_nombre.lower() in item.lower() for item_nombre in mapeo_oficios_items[oficio]):
                    return True
        return False

    def registrar_transaccion(self, jugador_id: int, item: str, cantidad: int,
                             precio: int, año: int) -> int:
        """Registra una transacción en la base de datos"""

        # Obtener item_id
        self.cursor.execute("SELECT id FROM items WHERE nombre = ?", (item,))
        item_id = self.cursor.fetchone()

        if not item_id:
            return -1

        item_id = item_id[0]

        # Registrar transacción
        self.cursor.execute('''
            INSERT INTO transacciones
            (año, persona_vendedor_id, persona_comprador_id, tipo_transaccion,
             item_ofrecido_id, cantidad_ofrecida, precio_acordado,
             satisfaccion_vendedor, satisfaccion_comprador)
            VALUES (?, ?, ?, 'compra', ?, ?, ?, 8, 8)
        ''', (año, self.npc_id, jugador_id, item_id, cantidad, precio))

        transaccion_id = self.cursor.lastrowid

        # Crear memoria de la transacción
        self.crear_memoria(
            jugador_id=jugador_id,
            tipo='transaccion',
            año=año,
            titulo=f"Venta de {item}",
            descripcion=f"Vendí {cantidad} {item} por {precio} en trueque",
            importancia=6,
            emocion='alegria',
            transaccion_id=transaccion_id
        )

        self.conn.commit()
        return transaccion_id

    def crear_memoria(self, jugador_id: Optional[int], tipo: str, año: int,
                     titulo: str, descripcion: str, importancia: int,
                     emocion: str = 'neutral', **kwargs):
        """Crea una nueva memoria para el NPC"""

        metadata = {
            k: v for k, v in kwargs.items() if k.endswith('_id')
        }

        self.cursor.execute('''
            INSERT INTO memoria_npc
            (npc_id, jugador_id, tipo_memoria, año, titulo, descripcion,
             importancia, emocion, metadata,
             persona_relacionada_id, item_relacionado_id, lugar_relacionado_id,
             transaccion_relacionada_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            self.npc_id, jugador_id, tipo, año, titulo, descripcion,
            importancia, emocion, json.dumps(metadata),
            kwargs.get('persona_relacionada_id'),
            kwargs.get('item_relacionado_id'),
            kwargs.get('lugar_relacionado_id'),
            kwargs.get('transaccion_id')
        ))

        self.conn.commit()

    def generar_dialogo_sucesion(self, antecesor_id: int) -> str:
        """Genera diálogo cuando el NPC es sucesor de alguien"""

        # Obtener info del antecesor
        self.cursor.execute('''
            SELECT nombre_completo, año_muerte
            FROM personas WHERE id = ?
        ''', (antecesor_id,))

        nombre_ant, año_muerte = self.cursor.fetchone()

        # Verificar relación
        es_padre = antecesor_id == self.padre_id
        es_madre = antecesor_id == self.madre_id

        if es_padre:
            relacion = "Mi padre"
        elif es_madre:
            relacion = "Mi madre"
        else:
            relacion = "Mi maestro"

        dialogo = f"{relacion}, {nombre_ant}, falleció en el año {año_muerte}. "

        if self.tiene_rasgo('Triste') or self.tiene_rasgo('Compasivo'):
            dialogo += f"Su pérdida todavía me duele, pero continúo su legado con orgullo. "
        elif self.tiene_rasgo('Pragmático'):
            dialogo += f"Ahora soy yo quien lleva adelante este oficio. "
        else:
            dialogo += f"He heredado su taller y sus conocimientos. "

        return dialogo

    def __repr__(self):
        rasgos_str = ', '.join([f"{k}({v['intensidad']})" for k, v in list(self.rasgos.items())[:3]])
        return f"<NPC: {self.nombre} - {self.oficio_principal} - Rasgos: {rasgos_str}>"


class SistemaConversacionalIA:
    """Sistema completo de conversaciones con NPCs"""

    def __init__(self, db_path='quinto_sol.db'):
        self.conn = sqlite3.connect(db_path)
        self.npcs_cache = {}

    def obtener_npc(self, npc_id: int) -> NPCConversacional:
        """Obtiene o crea un NPC conversacional"""
        if npc_id not in self.npcs_cache:
            self.npcs_cache[npc_id] = NPCConversacional(npc_id, self.conn)
        return self.npcs_cache[npc_id]

    def simular_conversacion(self, npc_id: int, jugador_id: int, año: int = 1550):
        """Simula una conversación completa con un NPC"""

        npc = self.obtener_npc(npc_id)

        print("\n" + "="*70)
        print(f"CONVERSACIÓN CON {npc.nombre.upper()}")
        print(f"Año: {año} | Lugar: {npc.civilizacion}")
        print("="*70 + "\n")

        # Saludo
        saludo = npc.generar_saludo(jugador_id, año)
        print(f"💬 {npc.nombre}: {saludo}\n")

        # Menú de interacción
        print("¿Qué deseas hacer?")
        print("1. Comprar item")
        print("2. Conversar")
        print("3. Preguntar sobre su historia")
        print("4. Despedirse")

        return npc

    def simular_compra(self, npc: NPCConversacional, jugador_id: int,
                      item: str, cantidad: int, año: int):
        """Simula una transacción comercial"""

        print(f"\n🛒 Jugador: Necesito {cantidad} {item}.\n")

        respuesta = npc.generar_dialogo_comercio(item, cantidad)

        print(f"💬 {npc.nombre}: {respuesta['respuesta']}\n")

        if respuesta['tiene_item']:
            print(f"💰 Precio: {int(respuesta['precio'])} en trueque")
            print(f"😊 Actitud: {respuesta['actitud']}")

            # Registrar
            transaccion_id = npc.registrar_transaccion(
                jugador_id, item, cantidad, int(respuesta['precio']), año
            )

            print(f"\n✓ Transacción registrada (ID: {transaccion_id})")

    def cerrar(self):
        """Cierra la conexión"""
        self.conn.close()


def demo_conversacion():
    """Demostración del sistema conversacional"""

    print("\n" + "="*70)
    print("DEMO: Sistema de IA Conversacional para NPCs")
    print("="*70)

    sistema = SistemaConversacionalIA()

    try:
        # Obtener un herrero aleatorio
        cursor = sistema.conn.cursor()
        cursor.execute('''
            SELECT DISTINCT p.id
            FROM personas p
            JOIN persona_oficios po ON p.id = po.persona_id
            JOIN oficios o ON po.oficio_id = o.id
            WHERE o.nombre = 'Herrero' AND p.es_npc = 1
            LIMIT 1
        ''')

        herrero = cursor.fetchone()

        if herrero:
            herrero_id = herrero[0]
            jugador_id = 999  # ID ficticio del jugador

            # Primera interacción
            print("\n📍 Primera interacción con el herrero:")
            npc = sistema.simular_conversacion(herrero_id, jugador_id, 1520)

            # Simular compra
            print("\n" + "-"*70)
            sistema.simular_compra(npc, jugador_id, "Macuahuitl", 2, 1520)

            # Segunda interacción (debería recordar)
            print("\n" + "="*70)
            print("\n📍 Segunda interacción (años después):")
            npc2 = sistema.simular_conversacion(herrero_id, jugador_id, 1525)

        else:
            print("\n⚠️  No hay herreros en la base de datos aún.")
            print("   Ejecuta primero: python3 generar_poblacion.py")

    finally:
        sistema.cerrar()


if __name__ == '__main__':
    demo_conversacion()
