#!/usr/bin/env python3
"""
Sistema de Control Poblacional Realista
- Esterilidad (10-15% parejas sin hijos)
- Solteros permanentes (20-25% no se casan)
- Mortalidad infantil (15-25% dependiendo de época)
- Número de hijos variable por condiciones (hambruna, guerra, paz)
"""

import sqlite3
import random


class ControlPoblacional:
    """Controla el crecimiento poblacional de forma realista"""

    # Probabilidades base
    PROB_ESTERILIDAD = 0.12  # 12% parejas estériles
    PROB_NUNCA_CASA = 0.22   # 22% nunca se casan (sacerdotes, etc.)
    MORTALIDAD_INFANTIL_BASE = 0.18  # 18% mueren antes de 5 años

    # Rangos de hijos según condiciones
    HIJOS_MIN_HAMBRUNA = 1
    HIJOS_MAX_HAMBRUNA = 3
    HIJOS_MIN_GUERRA = 2
    HIJOS_MAX_GUERRA = 4
    HIJOS_MIN_NORMAL = 3
    HIJOS_MAX_NORMAL = 6
    HIJOS_MIN_PAZ = 4
    HIJOS_MAX_PAZ = 7

    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def marcar_esteriles(self, año_inicio, año_fin):
        """
        Marca parejas como estériles (no tendrán hijos)
        """
        # Obtener matrimonios en este período
        self.cursor.execute("""
            SELECT id FROM matrimonios
            WHERE año_matrimonio BETWEEN ? AND ?
            AND (año_divorcio IS NULL OR año_divorcio > ?)
        """, (año_inicio, año_fin, año_fin))

        matrimonios = self.cursor.fetchall()
        num_esteriles = int(len(matrimonios) * self.PROB_ESTERILIDAD)

        # Seleccionar aleatoriamente parejas estériles
        esteriles = random.sample(matrimonios, min(num_esteriles, len(matrimonios)))

        print(f"   💔 Parejas estériles: {len(esteriles)} de {len(matrimonios)} ({self.PROB_ESTERILIDAD*100:.0f}%)")

        # Agregar nota (necesitaríamos columna en matrimonios)
        # Por ahora, retornamos los IDs para que no tengan hijos
        return [m[0] for m in esteriles]

    def marcar_solteros_permanentes(self, personas_disponibles):
        """
        Marca personas que nunca se casarán
        Razones: vocación religiosa, elección personal, etc.
        """
        num_solteros = int(len(personas_disponibles) * self.PROB_NUNCA_CASA)
        solteros = random.sample(personas_disponibles, min(num_solteros, len(personas_disponibles)))

        print(f"   🙏 Solteros permanentes: {len(solteros)} de {len(personas_disponibles)} ({self.PROB_NUNCA_CASA*100:.0f}%)")

        # Agregar nota en personas (necesitaríamos columna)
        # Por ahora, retornamos los IDs para excluirlos de matrimonios
        return [p[0] for p in solteros]

    def aplicar_mortalidad_infantil(self, año_nacimiento, condicion='normal'):
        """
        Determina si un bebé sobrevive los primeros 5 años

        Args:
            año_nacimiento: Año de nacimiento
            condicion: 'normal', 'hambruna', 'epidemia', 'guerra'

        Returns:
            (sobrevive: bool, año_muerte: int or None)
        """
        # Ajustar mortalidad según condiciones
        if condicion == 'epidemia':
            mortalidad = 0.40  # 40% en epidemias
        elif condicion == 'hambruna':
            mortalidad = 0.35  # 35% en hambrunas
        elif condicion == 'guerra':
            mortalidad = 0.25  # 25% en guerras (desnutrición, violencia)
        else:
            mortalidad = self.MORTALIDAD_INFANTIL_BASE

        if random.random() < mortalidad:
            # Muere entre 0-5 años
            año_muerte = año_nacimiento + random.randint(0, 5)
            return False, año_muerte
        else:
            return True, None

    def calcular_num_hijos(self, condicion='normal', epoca=1500):
        """
        Calcula número de hijos según condiciones históricas

        Args:
            condicion: 'paz', 'normal', 'guerra', 'hambruna'
            epoca: Año (afecta medicina, etc.)

        Returns:
            Número de hijos a generar
        """
        # Ajustar por época (mejor medicina en años posteriores)
        modificador_epoca = 1.0
        if epoca > 2500:
            modificador_epoca = 0.9  # Menos hijos en época moderna
        elif epoca > 2000:
            modificador_epoca = 0.95

        if condicion == 'hambruna':
            base = random.randint(self.HIJOS_MIN_HAMBRUNA, self.HIJOS_MAX_HAMBRUNA)
        elif condicion == 'guerra':
            base = random.randint(self.HIJOS_MIN_GUERRA, self.HIJOS_MAX_GUERRA)
        elif condicion == 'paz':
            base = random.randint(self.HIJOS_MIN_PAZ, self.HIJOS_MAX_PAZ)
        else:  # normal
            base = random.randint(self.HIJOS_MIN_NORMAL, self.HIJOS_MAX_NORMAL)

        return max(1, int(base * modificador_epoca))

    def determinar_condicion_epoca(self, año):
        """
        Determina las condiciones de una época específica
        Basado en eventos históricos conocidos
        """
        # Hambrunas conocidas
        if 1650 <= año <= 1653:  # La Gran Sequía
            return 'hambruna'

        # Guerras conocidas
        if 1818 <= año <= 1823:  # Guerra de las Dos Lunas
            return 'guerra'
        if 1948 <= año <= 1952:  # Rebelión Zapoteca
            return 'guerra'
        if 2248 <= año <= 2255:  # Primera Guerra de Unificación
            return 'guerra'
        if 2498 <= año <= 2503:  # Guerra Civil Mexica
            return 'guerra'
        if 2748 <= año <= 2755:  # La Gran Conquista
            return 'guerra'

        # Épocas de paz
        if 1505 <= año <= 1600:  # Post-contacto divino, paz inicial
            return 'paz'
        if 2500 <= año <= 2520:  # Tratado de las Tres Ciudades
            return 'paz'

        # Normal por defecto
        return 'normal'


def aplicar_control_poblacional_retroactivo(conn):
    """
    Aplica control poblacional a la base de datos existente
    ADVERTENCIA: Esto matará a muchos bebés (mortalidad infantil)
    """
    print("\n" + "="*70)
    print("⚙️  APLICANDO CONTROL POBLACIONAL RETROACTIVO")
    print("="*70)

    cursor = conn.cursor()
    control = ControlPoblacional(conn)

    # Obtener todas las personas nacidas
    cursor.execute("""
        SELECT id, año_nacimiento, año_muerte
        FROM personas
        WHERE año_nacimiento IS NOT NULL
        ORDER BY año_nacimiento
    """)

    personas = cursor.fetchall()
    total_muertos_infantil = 0
    epocas_procesadas = set()

    print(f"\n📊 Procesando {len(personas):,} personas...")

    for persona_id, año_nac, año_muerte_actual in personas:
        # Solo aplicar si aún no está muerto
        if año_muerte_actual is None:
            condicion = control.determinar_condicion_epoca(año_nac)

            # Registrar época para estadísticas
            epoca_key = f"{(año_nac // 25) * 25}"
            if epoca_key not in epocas_procesadas:
                epocas_procesadas.add(epoca_key)
                print(f"\n   Procesando época {epoca_key}-{int(epoca_key)+25}: Condición '{condicion}'")

            sobrevive, año_muerte = control.aplicar_mortalidad_infantil(año_nac, condicion)

            if not sobrevive:
                # Marcar como muerto
                cursor.execute("""
                    UPDATE personas
                    SET año_muerte = ?, causa_muerte = 'mortalidad_infantil'
                    WHERE id = ?
                """, (año_muerte, persona_id))
                total_muertos_infantil += 1

    conn.commit()

    # Estadísticas finales
    print(f"\n" + "="*70)
    print(f"📊 ESTADÍSTICAS DE CONTROL POBLACIONAL")
    print(f"="*70)
    print(f"   Total procesados: {len(personas):,}")
    print(f"   Muertes infantiles: {total_muertos_infantil:,} ({total_muertos_infantil/len(personas)*100:.1f}%)")

    # Distribución de causas de muerte
    cursor.execute("""
        SELECT causa_muerte, COUNT(*)
        FROM personas
        WHERE causa_muerte IS NOT NULL
        GROUP BY causa_muerte
        ORDER BY COUNT(*) DESC
    """)

    print(f"\n   Causas de muerte:")
    for causa, count in cursor.fetchall():
        print(f"      {causa or 'desconocida':30} {count:6,}")

    # Población viva actual
    cursor.execute("SELECT COUNT(*) FROM personas WHERE año_muerte IS NULL")
    vivos = cursor.fetchone()[0]
    print(f"\n   👥 Población viva: {vivos:,}")


def main():
    print("\n" + "="*70)
    print("⚙️  CONTROL POBLACIONAL - PORTALES DEL QUINTO SOL")
    print("="*70)
    print("\nEste script aplicará control poblacional realista:")
    print("  - Mortalidad infantil (15-40% según condiciones)")
    print("  - Matará a muchos bebés retroactivamente")
    print("\nADVERTENCIA: Esto modificará la base de datos permanentemente")

    respuesta = input("\n¿Deseas continuar? (s/n): ")

    if respuesta.lower() != 's':
        print("Operación cancelada.")
        return

    conn = sqlite3.connect('quinto_sol.db')

    try:
        aplicar_control_poblacional_retroactivo(conn)

        print("\n✅ Control poblacional aplicado exitosamente")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        conn.rollback()
    finally:
        conn.close()


if __name__ == '__main__':
    main()
