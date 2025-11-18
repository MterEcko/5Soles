#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Tiempo del Juego
Portales del Quinto Sol

1 hora real = 1 día del juego
- Procesa eventos diarios de NPCs
- Conversaciones NPC-NPC continúan
- Cultura sigue evolucionando
- Jugadores interactúan en tiempo real
"""

import time
import json
from datetime import datetime, timedelta
from threading import Thread, Lock
from typing import Dict, List, Optional

# Importar conector unificado de base de datos
from database_connector import DatabaseConnector

class GameTimeServer:
    """
    Servidor de tiempo del juego
    Corre en background, avanza 1 día cada hora real
    Soporta SQLite y PostgreSQL
    """

    def __init__(self, start_year: int = 3000):
        # Usar conector unificado
        self.db = DatabaseConnector()
        self.conn = self.db.connect()
        self.cursor = self.conn.cursor()

        # Estado del tiempo
        self.current_game_year = start_year
        self.current_game_day = 1
        self.real_time_started = datetime.now()
        self.paused = False

        # Lock para operaciones thread-safe
        self.time_lock = Lock()

        # Cargar o inicializar estado
        self.load_game_state()

        print(f"⏰ Servidor de tiempo inicializado")
        print(f"   Año actual del juego: {self.current_game_year}")
        print(f"   Día actual: {self.current_game_day}")

    def load_game_state(self):
        """Carga estado del juego de la BD"""
        # Crear tabla de estado si no existe
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS game_state (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                current_year INTEGER NOT NULL,
                current_day INTEGER NOT NULL,
                real_time_started TEXT NOT NULL,
                last_updated TEXT NOT NULL
            )
        """)

        # Intentar cargar estado
        self.cursor.execute("SELECT current_year, current_day, real_time_started FROM game_state WHERE id = 1")
        result = self.cursor.fetchone()

        if result:
            self.current_game_year = result[0]
            self.current_game_day = result[1]
            self.real_time_started = datetime.fromisoformat(result[2])
            print(f"✅ Estado cargado desde BD")
        else:
            # Crear estado inicial
            self.cursor.execute("""
                INSERT INTO game_state (id, current_year, current_day, real_time_started, last_updated)
                VALUES (1, ?, ?, ?, ?)
            """, (self.current_game_year, self.current_game_day,
                  self.real_time_started.isoformat(), datetime.now().isoformat()))
            self.conn.commit()
            print(f"✅ Estado inicial creado")

    def save_game_state(self):
        """Guarda estado actual en BD"""
        with self.time_lock:
            self.cursor.execute("""
                UPDATE game_state
                SET current_year = ?, current_day = ?, last_updated = ?
                WHERE id = 1
            """, (self.current_game_year, self.current_game_day, datetime.now().isoformat()))
            self.conn.commit()

    def get_current_time(self) -> Dict:
        """Obtiene tiempo actual del juego"""
        with self.time_lock:
            return {
                'year': self.current_game_year,
                'day': self.current_game_day,
                'season': self.get_season(self.current_day),
                'time_of_day': self.get_time_of_day(),
                'real_time': datetime.now().isoformat()
            }

    def get_season(self, day: int) -> str:
        """Determina estación según día del año (365 días)"""
        day_in_year = day % 365

        if day_in_year < 91:
            return 'primavera'
        elif day_in_year < 182:
            return 'verano'
        elif day_in_year < 273:
            return 'otoño'
        else:
            return 'invierno'

    def get_time_of_day(self) -> str:
        """
        Calcula hora del día basada en minutos transcurridos
        1 hora real = 1 día juego = 24 horas juego
        1 minuto real = 24 minutos juego
        """
        now = datetime.now()
        minutes_since_hour = now.minute + (now.second / 60.0)
        game_hour = int((minutes_since_hour / 60.0) * 24)

        if 6 <= game_hour < 12:
            return 'mañana'
        elif 12 <= game_hour < 18:
            return 'tarde'
        elif 18 <= game_hour < 22:
            return 'noche'
        else:
            return 'madrugada'

    def advance_day(self):
        """Avanza un día del juego (llamado cada hora real)"""
        with self.time_lock:
            self.current_game_day += 1

            # Nuevo año cada 365 días
            if self.current_game_day > 365:
                self.current_game_day = 1
                self.current_game_year += 1
                print(f"\n🎆 ¡NUEVO AÑO! Ahora estamos en {self.current_game_year}")

            self.save_game_state()

            print(f"📅 Día avanzado: Año {self.current_game_year}, Día {self.current_game_day}")

            # Procesar eventos del día
            self.process_daily_events()

    def process_daily_events(self):
        """Procesa eventos que ocurren cada día del juego"""
        print(f"⚙️  Procesando eventos del día {self.current_game_day}...")

        # 1. NPCs conversan entre ellos
        self.process_npc_conversations()

        # 2. NPCs envejecen, algunos pueden morir
        self.process_npc_aging()

        # 3. Eventos aleatorios (raros)
        self.process_random_events()

        # 4. Actualizar economía
        self.update_economy()

        print(f"✅ Eventos del día procesados")

    def process_npc_conversations(self):
        """NPCs conversan entre ellos (simplificado para tiempo real)"""
        # Generar 10-20 conversaciones por día
        num_conversations = random.randint(10, 20)

        # Obtener NPCs vivos
        self.cursor.execute("""
            SELECT id FROM personas
            WHERE año_muerte > ?
            ORDER BY RANDOM()
            LIMIT ?
        """, (self.current_game_year, num_conversations * 2))

        npcs = [row[0] for row in self.cursor.fetchall()]

        conversations_created = 0
        for i in range(0, len(npcs) - 1, 2):
            npc1 = npcs[i]
            npc2 = npcs[i + 1]

            # Conversación simple (template)
            self.cursor.execute("""
                INSERT INTO conversaciones_historicas
                (npc1_id, npc2_id, año, tema, intercambios, informacion_compartida)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                npc1, npc2, self.current_game_year,
                random.choice(['trabajo', 'clima', 'jugadores']),
                json.dumps([{'speaker': 'npc1', 'message': 'Hola'}, {'speaker': 'npc2', 'message': 'Hola'}]),
                json.dumps([])
            ))
            conversations_created += 1

        self.conn.commit()
        print(f"  🗣️  {conversations_created} conversaciones NPC-NPC")

    def process_npc_aging(self):
        """Procesa envejecimiento de NPCs"""
        # Cada 365 días, NPCs envejecen 1 año
        if self.current_game_day == 1:
            # Verificar muertes naturales
            self.cursor.execute("""
                SELECT id, nombre_completo
                FROM personas
                WHERE año_muerte = ?
            """, (self.current_game_year,))

            deaths = self.cursor.fetchall()

            if deaths:
                print(f"  ⚰️  {len(deaths)} NPCs fallecieron de muerte natural")

                # Propagar rumores de muerte
                for npc_id, nombre in deaths:
                    self.cursor.execute("""
                        INSERT INTO rumores_historicos
                        (rumor_original, año_inicio, npc_origen_id, tipo, alcance)
                        VALUES (?, ?, ?, ?, ?)
                    """, (f"{nombre} ha fallecido", self.current_game_year, npc_id, 'muerte', 10))

                self.conn.commit()

    def process_random_events(self):
        """Eventos aleatorios (muy raros)"""
        # 1% de probabilidad de evento por día
        if random.random() < 0.01:
            event_types = ['clima_extremo', 'descubrimiento', 'conflicto_menor']
            event = random.choice(event_types)

            print(f"  ⚡ Evento aleatorio: {event}")

            # Registrar evento
            self.cursor.execute("""
                INSERT INTO eventos_climaticos
                (año, tipo, gravedad, duracion_dias)
                VALUES (?, ?, ?, ?)
            """, (self.current_game_year, event, 'moderado', 1))

            self.conn.commit()

    def update_economy(self):
        """Actualiza precios del mercado (simplificado)"""
        # Pequeñas fluctuaciones aleatorias
        pass

    def start_time_loop(self):
        """
        Inicia loop principal de tiempo
        Avanza 1 día cada 60 minutos
        """
        print("\n⏰ Iniciando servidor de tiempo del juego...")
        print("   1 hora real = 1 día del juego")
        print("   Presiona Ctrl+C para detener\n")

        try:
            while not self.paused:
                # Esperar 1 hora (3600 segundos)
                time.sleep(3600)

                # Avanzar día
                self.advance_day()

        except KeyboardInterrupt:
            print("\n⏸️  Servidor de tiempo pausado")
            self.save_game_state()

    def start_time_loop_fast(self, seconds_per_day: int = 60):
        """
        Versión RÁPIDA para testing
        1 minuto = 1 día (en vez de 1 hora = 1 día)
        """
        print(f"\n⏰ Iniciando servidor de tiempo (MODO RÁPIDO)")
        print(f"   {seconds_per_day} segundos reales = 1 día del juego")
        print("   Presiona Ctrl+C para detener\n")

        try:
            while not self.paused:
                time.sleep(seconds_per_day)
                self.advance_day()

        except KeyboardInterrupt:
            print("\n⏸️  Servidor de tiempo pausado")
            self.save_game_state()


class NPCBackgroundProcessor:
    """
    Procesador en background para NPCs
    Corre tareas periódicas cada día del juego
    """

    def __init__(self, game_time_server: GameTimeServer):
        self.game_time = game_time_server
        self.conn = sqlite3.connect('quinto_sol.db', check_same_thread=False)
        self.cursor = self.conn.cursor()

        # Cargar red social de NPCs (si existe)
        self.load_social_network()

    def load_social_network(self):
        """Carga red social de NPCs desde BD"""
        # TODO: Implementar cuando tengamos red social construida
        pass

    def process_daily_npc_activities(self):
        """
        Procesa actividades diarias de NPCs
        - Trabajo
        - Socialización
        - Movimiento
        """
        current_time = self.game_time.get_current_time()

        print(f"🏃 Procesando actividades de NPCs...")
        print(f"   Año: {current_time['year']}, Día: {current_time['day']}")

        # NPCs trabajan, descansan, conversan según hora del día
        time_of_day = current_time['time_of_day']

        if time_of_day == 'mañana':
            # NPCs van a trabajar
            pass
        elif time_of_day == 'tarde':
            # NPCs comercian, conversan
            pass
        elif time_of_day == 'noche':
            # NPCs descansan
            pass


class GameServer:
    """
    Servidor principal del juego
    Coordina tiempo + NPCs + jugadores
    """

    def __init__(self):
        self.time_server = GameTimeServer(start_year=3000)
        self.npc_processor = NPCBackgroundProcessor(self.time_server)

        # Threads
        self.time_thread = None
        self.running = False

    def start(self, fast_mode: bool = False):
        """
        Inicia servidor del juego

        Args:
            fast_mode: Si True, 1 minuto = 1 día (testing)
                      Si False, 1 hora = 1 día (producción)
        """
        print("="*70)
        print("SERVIDOR DEL JUEGO - PORTALES DEL QUINTO SOL")
        print("="*70)

        current_time = self.time_server.get_current_time()
        print(f"\n📅 Tiempo actual:")
        print(f"   Año: {current_time['year']}")
        print(f"   Día: {current_time['day']}")
        print(f"   Estación: {current_time['season']}")
        print(f"   Hora del día: {current_time['time_of_day']}")

        self.running = True

        # Iniciar servidor de tiempo en thread separado
        if fast_mode:
            self.time_thread = Thread(
                target=self.time_server.start_time_loop_fast,
                args=(60,),  # 1 minuto = 1 día
                daemon=True
            )
        else:
            self.time_thread = Thread(
                target=self.time_server.start_time_loop,
                daemon=True
            )

        self.time_thread.start()

        print("\n✅ Servidor iniciado")
        print("\n💡 Comandos disponibles:")
        print("   /time    - Ver tiempo actual")
        print("   /npcs    - Ver NPCs activos")
        print("   /events  - Ver eventos recientes")
        print("   /quit    - Detener servidor")

        # Loop principal (consola de admin)
        self.admin_console()

    def admin_console(self):
        """Consola de administración"""
        try:
            while self.running:
                cmd = input("\n> ").strip().lower()

                if cmd == '/time':
                    self.show_current_time()
                elif cmd == '/npcs':
                    self.show_active_npcs()
                elif cmd == '/events':
                    self.show_recent_events()
                elif cmd == '/quit':
                    self.shutdown()
                    break
                elif cmd == '/help':
                    print("Comandos: /time, /npcs, /events, /quit")
                else:
                    print("❌ Comando no reconocido. Usa /help")

        except KeyboardInterrupt:
            self.shutdown()

    def show_current_time(self):
        """Muestra tiempo actual del juego"""
        current_time = self.time_server.get_current_time()

        print("\n📅 TIEMPO ACTUAL DEL JUEGO:")
        print(f"   Año: {current_time['year']}")
        print(f"   Día del año: {current_time['day']}/365")
        print(f"   Estación: {current_time['season']}")
        print(f"   Hora del día: {current_time['time_of_day']}")
        print(f"   Tiempo real: {current_time['real_time']}")

    def show_active_npcs(self):
        """Muestra NPCs activos"""
        cursor = self.time_server.cursor

        cursor.execute("""
            SELECT COUNT(*) FROM personas
            WHERE año_muerte > ?
        """, (self.time_server.current_game_year,))

        total_vivos = cursor.fetchone()[0]

        print(f"\n👥 NPCs ACTIVOS:")
        print(f"   Total vivos: {total_vivos:,}")

        # Muestra algunos NPCs aleatorios
        cursor.execute("""
            SELECT nombre_completo, clase_social,
                   ? - año_nacimiento as edad
            FROM personas
            WHERE año_muerte > ?
            ORDER BY RANDOM()
            LIMIT 5
        """, (self.time_server.current_game_year, self.time_server.current_game_year))

        print(f"\n   Ejemplos:")
        for nombre, clase, edad in cursor.fetchall():
            print(f"   - {nombre} ({clase}, {edad} años)")

    def show_recent_events(self):
        """Muestra eventos recientes"""
        cursor = self.time_server.cursor

        # Conversaciones recientes
        cursor.execute("""
            SELECT COUNT(*) FROM conversaciones_historicas
            WHERE año = ?
        """, (self.time_server.current_game_year,))

        convs_hoy = cursor.fetchone()[0]

        # Rumores activos
        cursor.execute("""
            SELECT COUNT(*) FROM rumores_historicos
            WHERE año_inicio >= ? - 10
        """, (self.time_server.current_game_year,))

        rumores_recientes = cursor.fetchone()[0]

        print(f"\n📊 EVENTOS RECIENTES:")
        print(f"   Conversaciones hoy: {convs_hoy}")
        print(f"   Rumores últimos 10 años: {rumores_recientes}")

    def shutdown(self):
        """Detiene servidor limpiamente"""
        print("\n⏹️  Deteniendo servidor...")
        self.running = False
        self.time_server.paused = True
        self.time_server.save_game_state()
        print("✅ Servidor detenido")


# SCRIPT PRINCIPAL
def main():
    import sys

    print("="*70)
    print("SERVIDOR DE TIEMPO DEL JUEGO")
    print("Portales del Quinto Sol")
    print("="*70)

    print("\nModo de ejecución:")
    print("  1. Producción (1 hora real = 1 día juego)")
    print("  2. Testing (1 minuto real = 1 día juego)")

    modo = input("\nSelecciona modo (1-2): ").strip()

    fast_mode = (modo == '2')

    if fast_mode:
        print("\n⚠️  MODO RÁPIDO ACTIVADO")
        print("   1 minuto real = 1 día del juego")
    else:
        print("\n⏰ MODO PRODUCCIÓN")
        print("   1 hora real = 1 día del juego")

    # Iniciar servidor
    server = GameServer()
    server.start(fast_mode=fast_mode)


if __name__ == '__main__':
    main()
