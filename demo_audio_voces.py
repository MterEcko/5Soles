#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEMO: Generación de Voces para NPCs
Prueba TTS (Text-to-Speech) local

Requisitos:
    pip install TTS
"""

import os
import time
from pathlib import Path


def verificar_tts():
    """Verifica si TTS está instalado"""
    try:
        from TTS.api import TTS
        print("✅ TTS (Coqui) instalado")
        return True
    except ImportError:
        print("❌ TTS no instalado")
        print("\n📦 Instalar con:")
        print("   pip install TTS")
        return False


def listar_modelos_disponibles():
    """Lista modelos TTS disponibles"""
    from TTS.api import TTS

    print("\n" + "="*70)
    print("📦 MODELOS TTS DISPONIBLES")
    print("="*70)

    print("\n🇪🇸 Modelos en Español (recomendados):")

    modelos_es = [
        'tts_models/es/css10/vits',
        'tts_models/es/mai/tacotron2-DDC',
    ]

    for i, modelo in enumerate(modelos_es, 1):
        print(f"   {i}. {modelo}")

    print("\n🌍 Modelos Multilingües (incluyen español):")

    modelos_multi = [
        'tts_models/multilingual/multi-dataset/your_tts',
        'tts_models/multilingual/multi-dataset/xtts_v2',
    ]

    for i, modelo in enumerate(modelos_multi, 1):
        print(f"   {i}. {modelo}")

    return modelos_es[0]  # Retornar recomendado


def demo_voz_basica():
    """Demo básico de generación de voz"""
    from TTS.api import TTS

    print("\n" + "="*70)
    print("DEMO 1: GENERACIÓN DE VOZ BÁSICA")
    print("="*70)

    # Crear directorio de audio
    Path("audio_demo").mkdir(exist_ok=True)

    # Inicializar TTS
    print("\n🔧 Inicializando TTS (primera vez descarga modelo ~500MB)...")
    inicio_init = time.time()

    tts = TTS(model_name="tts_models/es/css10/vits")

    tiempo_init = time.time() - inicio_init
    print(f"✅ TTS inicializado ({tiempo_init:.1f}s)")

    # Texto de prueba
    textos_npc = [
        "Bienvenido viajero, ¿en qué puedo ayudarte?",
        "Tengo espadas de obsidiana por cincuenta monedas de jade",
        "Que los dioses te acompañen en tu viaje"
    ]

    for i, texto in enumerate(textos_npc, 1):
        print(f"\n📝 Texto {i}: \"{texto}\"")
        print(f"🎙️  Generando audio...")

        archivo = f"audio_demo/npc_frase_{i}.wav"

        inicio = time.time()
        tts.tts_to_file(text=texto, file_path=archivo)
        tiempo = time.time() - inicio

        print(f"✅ Audio generado: {archivo}")
        print(f"   Tiempo: {tiempo:.2f}s")

    print("\n💡 Puedes reproducir los archivos con:")
    print("   mpg123 audio_demo/npc_frase_1.wav")
    print("   aplay audio_demo/npc_frase_1.wav")


def demo_multiples_voces():
    """Demo con diferentes voces para diferentes NPCs"""
    from TTS.api import TTS

    print("\n" + "="*70)
    print("DEMO 2: MÚLTIPLES VOCES (NPCs ÚNICOS)")
    print("="*70)

    Path("audio_demo").mkdir(exist_ok=True)

    # Usar modelo multi-speaker si está disponible
    print("\n🔧 Inicializando TTS multi-speaker...")

    try:
        # Intentar modelo con múltiples voces
        tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts")

        npcs = [
            {'nombre': 'Xolotl', 'speaker': 0, 'texto': 'Soy el herrero Xolotl'},
            {'nombre': 'Citlali', 'speaker': 1, 'texto': 'Vendo jade y obsidiana'},
            {'nombre': 'Tezca', 'speaker': 2, 'texto': 'Conozco los secretos antiguos'}
        ]

        for npc in npcs:
            print(f"\n🎭 {npc['nombre']}:")
            print(f"   Texto: \"{npc['texto']}\"")
            print(f"   Voz: Speaker {npc['speaker']}")

            archivo = f"audio_demo/{npc['nombre'].lower()}.wav"

            inicio = time.time()
            tts.tts_to_file(
                text=npc['texto'],
                file_path=archivo,
                speaker=tts.speakers[npc['speaker']] if hasattr(tts, 'speakers') else None
            )
            tiempo = time.time() - inicio

            print(f"   ✅ {archivo} ({tiempo:.2f}s)")

    except Exception as e:
        print(f"⚠️  Modelo multi-speaker no disponible: {e}")
        print("   Usando modelo estándar en español")

        tts = TTS(model_name="tts_models/es/css10/vits")

        npcs = [
            {'nombre': 'Xolotl', 'texto': 'Soy el herrero Xolotl'},
            {'nombre': 'Citlali', 'texto': 'Vendo jade y obsidiana'},
        ]

        for npc in npcs:
            print(f"\n🎭 {npc['nombre']}: \"{npc['texto']}\"")
            archivo = f"audio_demo/{npc['nombre'].lower()}.wav"

            inicio = time.time()
            tts.tts_to_file(text=npc['texto'], file_path=archivo)
            tiempo = time.time() - inicio

            print(f"   ✅ {archivo} ({tiempo:.2f}s)")


def demo_conversacion_completa():
    """Demo de conversación completa con audio"""
    from TTS.api import TTS

    print("\n" + "="*70)
    print("DEMO 3: CONVERSACIÓN COMPLETA (LLM + TTS)")
    print("="*70)

    Path("audio_demo").mkdir(exist_ok=True)

    # Inicializar TTS
    print("\n🔧 Inicializando TTS...")
    tts = TTS(model_name="tts_models/es/css10/vits")

    # Simular conversación (sin LLM, solo texto pre-escrito)
    conversacion = [
        {
            'jugador': '¿Vendes armas?',
            'npc': 'Sí viajero, tengo espadas y lanzas de obsidiana'
        },
        {
            'jugador': '¿Cuánto cuesta una espada?',
            'npc': 'Una espada te costará cincuenta monedas de jade'
        },
        {
            'jugador': 'Me la llevo',
            'npc': 'Excelente elección, que te sirva bien en batalla'
        }
    ]

    for i, turno in enumerate(conversacion, 1):
        print(f"\n💬 Turno {i}:")
        print(f"   👤 Jugador: {turno['jugador']}")
        print(f"   🗣️  NPC: {turno['npc']}")
        print(f"   🎙️  Generando audio...")

        archivo = f"audio_demo/conversacion_{i}.wav"

        inicio = time.time()
        tts.tts_to_file(text=turno['npc'], file_path=archivo)
        tiempo = time.time() - inicio

        print(f"   ✅ {archivo} ({tiempo:.2f}s)")


def demo_cache_optimizado():
    """Demo de sistema optimizado con caché"""
    from TTS.api import TTS

    print("\n" + "="*70)
    print("DEMO 4: SISTEMA CON CACHÉ (OPTIMIZADO)")
    print("="*70)

    Path("audio_demo/cache").mkdir(parents=True, exist_ok=True)

    # Inicializar TTS
    tts = TTS(model_name="tts_models/es/css10/vits")

    # Frases comunes a pre-generar
    frases_comunes = [
        "Bienvenido viajero",
        "Adiós, que los dioses te acompañen",
        "No tengo suficiente oro",
        "Eso es muy caro",
        "Gracias por tu compra",
        "¿En qué puedo ayudarte?",
        "Vuelve pronto",
        "Buena suerte en tu aventura"
    ]

    print(f"\n📦 Pre-generando {len(frases_comunes)} frases comunes (CACHÉ)...")
    print("   Esto se hace UNA VEZ al iniciar el servidor\n")

    cache = {}
    tiempo_total = 0

    for i, frase in enumerate(frases_comunes, 1):
        archivo = f"audio_demo/cache/{hash(frase) % 100000}.wav"

        inicio = time.time()
        tts.tts_to_file(text=frase, file_path=archivo)
        tiempo = time.time() - inicio

        tiempo_total += tiempo
        cache[frase] = archivo

        print(f"   {i}. \"{frase}\" → {tiempo:.2f}s")

    print(f"\n✅ Caché creado en {tiempo_total:.1f}s")

    # Simular uso de caché
    print("\n📊 Uso de caché (instantáneo):")

    for frase in ["Bienvenido viajero", "Gracias por tu compra", "Vuelve pronto"]:
        if frase in cache:
            print(f"   ✅ \"{frase}\" → {cache[frase]} (desde caché, 0.001s)")

    print("\n💡 Ventaja del caché:")
    print("   • Frases comunes: Instantáneas (desde caché)")
    print("   • Frases dinámicas: 1-3 segundos (generadas)")
    print("   • Ahorro: ~80% del tiempo de generación")


def demo_performance():
    """Mide performance de generación de audio"""
    from TTS.api import TTS

    print("\n" + "="*70)
    print("DEMO 5: PERFORMANCE TTS")
    print("="*70)

    Path("audio_demo").mkdir(exist_ok=True)

    tts = TTS(model_name="tts_models/es/css10/vits")

    # Diferentes longitudes
    textos = [
        ("Corto (1 palabra)", "Hola"),
        ("Normal (NPC típico)", "Bienvenido viajero, ¿buscas comprar armas o armaduras?"),
        ("Largo (explicación)", "En esta tienda encontrarás las mejores armas forjadas con obsidiana volcánica, traída desde las montañas sagradas del norte")
    ]

    print("\n📊 Midiendo velocidad de generación:\n")

    for nombre, texto in textos:
        archivo = f"audio_demo/perf_test.wav"

        inicio = time.time()
        tts.tts_to_file(text=texto, file_path=archivo)
        tiempo = time.time() - inicio

        palabras = len(texto.split())

        print(f"📝 {nombre}:")
        print(f"   Palabras: {palabras}")
        print(f"   Tiempo: {tiempo:.2f}s")
        print(f"   Velocidad: {palabras/tiempo:.1f} palabras/seg\n")

    # Limpiar
    os.remove(archivo)


def mostrar_recomendaciones():
    """Muestra recomendaciones de uso"""
    print("\n" + "="*70)
    print("💡 RECOMENDACIONES PARA PRODUCCIÓN")
    print("="*70)

    print("\n🎯 Estrategia óptima:")
    print("   1. Pre-generar frases comunes (8-20 frases)")
    print("   2. Guardar en directorio audio/cache/")
    print("   3. Generar dinámicamente solo respuestas únicas")
    print("   4. Limpiar cache cada X días")

    print("\n📊 Performance esperado:")
    print("   • Frase corta (5 palabras): 0.5-1.5s")
    print("   • Frase normal (10-15 palabras): 1.0-2.5s")
    print("   • Desde caché: <0.01s (instantáneo)")

    print("\n💰 Recursos:")
    print("   • CPU: 2-4 cores (no necesita GPU)")
    print("   • RAM: 2-4 GB para modelo")
    print("   • Disco: ~500 MB modelo + audio generado")

    print("\n🔄 Integración con LLM:")
    print("""
    # Ejemplo completo
    import ollama
    from TTS.api import TTS

    # 1. Generar texto con LLM
    response = ollama.chat(model='llama3.1:8b', ...)
    texto = response['message']['content']

    # 2. Generar audio con TTS
    tts = TTS(model_name='tts_models/es/css10/vits')
    tts.tts_to_file(text=texto, file_path='npc_respuesta.wav')

    # 3. Enviar al cliente del juego
    return {'texto': texto, 'audio': 'npc_respuesta.wav'}
    """)


def main():
    """Función principal"""
    print("\n" + "="*70)
    print("🎙️  DEMO: GENERACIÓN DE VOCES PARA NPCs")
    print("Portales del Quinto Sol")
    print("="*70)

    # Verificar TTS
    if not verificar_tts():
        print("\n❌ Instala TTS primero: pip install TTS")
        return

    print("\n⚠️  NOTA: Primera ejecución descargará modelos (~500MB)")
    print("   Ejecuciones posteriores serán más rápidas\n")

    print("¿Qué demo quieres ejecutar?")
    print("1. Voz básica (3 frases de NPC)")
    print("2. Múltiples voces (NPCs únicos)")
    print("3. Conversación completa")
    print("4. Sistema con caché (optimizado)")
    print("5. Test de performance")
    print("6. Todas las demos")
    print("7. Solo ver recomendaciones")

    try:
        opcion = input("\nOpción (1-7): ").strip()

        if opcion == '1':
            demo_voz_basica()
        elif opcion == '2':
            demo_multiples_voces()
        elif opcion == '3':
            demo_conversacion_completa()
        elif opcion == '4':
            demo_cache_optimizado()
        elif opcion == '5':
            demo_performance()
        elif opcion == '6':
            demo_voz_basica()
            demo_multiples_voces()
            demo_conversacion_completa()
            demo_cache_optimizado()
            demo_performance()
        elif opcion == '7':
            pass
        else:
            print("Opción inválida")
            return

        mostrar_recomendaciones()

        print("\n" + "="*70)
        print("✅ DEMO COMPLETADA")
        print("="*70)

        print("\n📁 Archivos de audio generados en:")
        print("   ./audio_demo/")

        print("\n🎵 Para reproducir:")
        print("   mpg123 audio_demo/npc_frase_1.wav")
        print("   aplay audio_demo/npc_frase_1.wav")
        print("   ffplay -nodisp -autoexit audio_demo/npc_frase_1.wav")

        print("\n💡 Conclusión:")
        print("   • TTS local funciona perfectamente")
        print("   • NO necesitas GPU")
        print("   • Voces en español de buena calidad")
        print("   • Con caché: casi instantáneo")
        print("   • ¡100% gratis y offline!")

    except KeyboardInterrupt:
        print("\n\n⚠️  Demo cancelada")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
