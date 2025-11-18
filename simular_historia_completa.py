#!/usr/bin/env python3
"""
Simula toda la historia genealógica desde 1500 hasta 3000
"""

from generar_poblacion import GeneradorGenealogico

def main():
    print("\n" + "="*80)
    print("SIMULACIÓN HISTÓRICA COMPLETA: PORTALES DEL QUINTO SOL")
    print("Generando 1500 años de historia (1500-3000)")
    print("="*80 + "\n")

    print("⚠️  ADVERTENCIA: Este proceso puede tomar varios minutos.")
    print("    Se generarán miles de personas, matrimonios e hijos.\n")

    respuesta = input("¿Deseas continuar? (s/n): ")

    if respuesta.lower() != 's':
        print("Simulación cancelada.")
        return

    gen = GeneradorGenealogico()

    try:
        # Simular toda la historia
        # Generaciones cada 25 años = 60 generaciones en 1500 años
        estadisticas = gen.simular_historia(
            año_inicio=1500,
            año_fin=3000,
            intervalo_generacion=25
        )

        # Crear algunos eventos históricos importantes
        crear_eventos_historicos(gen)

        print("\n✓ Simulación completada exitosamente!")
        print("\nPuedes consultar la base de datos con: python3 consultas.py")

    finally:
        gen.cerrar()


def crear_eventos_historicos(gen: GeneradorGenealogico):
    """Crea eventos históricos importantes"""
    print("\n" + "="*70)
    print("Creando eventos históricos importantes...")
    print("="*70 + "\n")

    # Obtener IDs de eras
    gen.cursor.execute("SELECT id FROM eras WHERE nombre = 'Era Alpha'")
    era_alpha_id = gen.cursor.fetchone()[0]

    gen.cursor.execute("SELECT id FROM eras WHERE nombre = 'Era del Cataclismo'")
    era_cataclismo_id = gen.cursor.fetchone()[0]

    # Obtener algunos lugares
    gen.cursor.execute("SELECT id FROM pueblos_ciudades LIMIT 5")
    lugares = [row[0] for row in gen.cursor.fetchall()]

    eventos = [
        ("Llegada por el Portal", "Los 40 humanos originales llegan a Aztlán Prime. Muchos murieron cuando el portal colapsó.", "portal", 1500, era_alpha_id, lugares[0], None),
        ("Fundación de la Primera Aldea", "Los supervivientes establecen el primer asentamiento permanente.", "fundacion", 1502, era_alpha_id, lugares[0], None),
        ("Primer Contacto con los Dioses", "Quetzalcóatl se manifiesta ante los humanos por primera vez.", "divino", 1505, era_alpha_id, lugares[0], None),
        ("La Gran Sequía", "Una sequía devastadora afecta las tierras durante 3 años.", "catastrofe", 1650, None, lugares[1], None),
        ("Guerra de las Dos Lunas", "Conflicto entre Mexica de Obsidiana y Toltecas del Viento.", "batalla", 1820, None, lugares[2], None),
        ("El Cataclismo Terrestre", "La Tierra colapsa. Los Humanos II llegan a Aztlán Prime.", "catastrofe", 2201, era_cataclismo_id, lugares[3], None),
        ("Primera Guerra de Unificación", "Humanos I y II se enfrentan por primera vez.", "batalla", 2250, era_cataclismo_id, lugares[4], None),
        ("Tratado de las Tres Ciudades", "Paz temporal entre las facciones principales.", "tratado", 2500, None, lugares[0], None),
        ("El Gran Despertar", "Nacen los primeros niños con habilidades divinas avanzadas.", "divino", 2750, None, lugares[1], None),
        ("Síntesis Final", "Unificación completa de Humanos I y II en una nueva cultura.", "unificacion", 2950, None, lugares[2], None),
    ]

    for evento in eventos:
        gen.cursor.execute('''
            INSERT INTO eventos (nombre, descripcion, tipo, año, era_id, lugar_id, civilizacion_afectada_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', evento)
        print(f"  ✓ {evento[0]} ({evento[3]})")

    gen.conn.commit()
    print(f"\n✓ {len(eventos)} eventos históricos creados")


if __name__ == '__main__':
    main()
