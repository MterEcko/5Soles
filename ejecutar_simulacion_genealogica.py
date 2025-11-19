#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejecutar Simulación Genealógica Completa
Portales del Quinto Sol

Este script ejecuta la simulación de genealogía para generar ~270k personas
a partir de las 40 personas iniciales, simulando 1500 años de historia (1500-3000).

IMPORTANTE: Esto puede tardar 30-60 minutos.
"""

from generar_poblacion import GeneradorGenealogico
from datetime import datetime

def main():
    print("\n" + "="*70)
    print("SIMULACIÓN GENEALÓGICA COMPLETA")
    print("Portales del Quinto Sol")
    print("="*70)

    print("\n⚠️  ADVERTENCIA:")
    print("   • Este proceso puede tardar 30-60 minutos")
    print("   • Se simularán 1500 años de historia (1500-3000)")
    print("   • Se generarán aproximadamente 270,000 personas")
    print("   • Se crearán matrimonios, hijos, muertes, etc.")

    respuesta = input("\n¿Continuar con la simulación? (s/n): ").strip().lower()

    if respuesta != 's':
        print("\n❌ Simulación cancelada")
        return

    print("\n" + "="*70)
    print("INICIANDO SIMULACIÓN")
    print("="*70)

    inicio = datetime.now()

    try:
        gen = GeneradorGenealogico()

        # Verificar población inicial
        gen.execute("SELECT COUNT(*) FROM personas WHERE año_nacimiento = 1500")
        result = gen.cursor.fetchone()
        count_inicial = result['count'] if isinstance(result, dict) else result[0]

        print(f"\n✅ Población inicial encontrada: {count_inicial} personas (año 1500)")

        if count_inicial < 30:
            print("\n⚠️  Población inicial muy baja. ¿Continuar de todas formas? (s/n)")
            respuesta = input("> ").strip().lower()
            if respuesta != 's':
                print("❌ Simulación cancelada")
                return

        # Ejecutar simulación completa
        print("\n🚀 Iniciando simulación de 1500 años...")
        print("   (Esto tomará varios minutos, se mostrará progreso cada 25 años)")

        estadisticas = gen.simular_historia(
            año_inicio=1500,
            año_fin=3000,
            intervalo_generacion=25
        )

        fin = datetime.now()
        duracion = fin - inicio

        print("\n" + "="*70)
        print("✅ SIMULACIÓN COMPLETADA EXITOSAMENTE")
        print("="*70)
        print(f"⏱️  Duración total: {duracion}")
        print(f"👥 Personas generadas: {estadisticas['hijos_totales']:,}")
        print(f"💑 Matrimonios creados: {estadisticas['matrimonios_totales']:,}")
        print(f"📅 Generaciones simuladas: {estadisticas['generaciones']}")
        print("="*70)

        print("\n📊 Siguiente paso:")
        print("   Ejecutar conversaciones NPC:")
        print("   python run_with_env.py simulacion_mundo_completo.py")

        gen.cerrar()

    except Exception as e:
        print(f"\n❌ Error durante la simulación: {e}")
        import traceback
        traceback.print_exc()
        return


if __name__ == '__main__':
    main()
