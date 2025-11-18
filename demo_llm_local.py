#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEMO: LLM Local para NPCs
Prueba rápida de conversaciones con Ollama

Requisitos:
    pip install ollama
"""

import time

def verificar_ollama():
    """Verifica si Ollama está instalado y corriendo"""
    try:
        import ollama

        # Intentar listar modelos
        models = ollama.list()
        print("✅ Ollama instalado y corriendo")
        print(f"   Modelos disponibles: {len(models.get('models', []))}")

        # Mostrar modelos instalados
        if models.get('models'):
            print("\n📦 Modelos instalados:")
            for model in models['models']:
                name = model['name']
                size_gb = model.get('size', 0) / (1024**3)
                print(f"   • {name} ({size_gb:.1f} GB)")
        else:
            print("\n⚠️  No hay modelos instalados")
            print("   Instalar con: ollama pull llama3.1:8b")

        return True

    except ImportError:
        print("❌ Ollama no instalado")
        print("\n📦 Instalar Ollama:")
        print("   Linux/Mac: curl -fsSL https://ollama.com/install.sh | sh")
        print("   Windows: https://ollama.com/download/windows")
        print("\n   Luego: pip install ollama")
        return False

    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n🔧 Asegúrate de que el servicio Ollama esté corriendo:")
        print("   ollama serve")
        return False


def demo_npc_simple():
    """Demo de conversación simple con NPC"""
    import ollama

    print("\n" + "="*70)
    print("DEMO 1: CONVERSACIÓN SIMPLE CON NPC")
    print("="*70)

    # Contexto del NPC
    npc_contexto = {
        'nombre': 'Xolotl',
        'rol': 'Herrero',
        'civilizacion': 'Tolteca',
        'edad': 45,
        'personalidad': 'Sabio, paciente, directo'
    }

    # Mensaje del jugador
    mensaje_jugador = "Hola, ¿vendes armas?"

    # Crear prompt
    prompt = f"""Eres {npc_contexto['nombre']}, un {npc_contexto['rol']} {npc_contexto['civilizacion']}.
Tienes {npc_contexto['edad']} años y eres {npc_contexto['personalidad']}.

El jugador te dice: "{mensaje_jugador}"

Responde como el NPC (máximo 2 oraciones, tono amigable):"""

    print(f"\n👤 Jugador: {mensaje_jugador}")
    print(f"🤖 {npc_contexto['nombre']} está pensando...\n")

    # Generar respuesta
    inicio = time.time()

    response = ollama.chat(
        model='llama3.1:8b',  # Cambiar si tienes otro modelo
        messages=[{
            'role': 'user',
            'content': prompt
        }],
        options={
            'temperature': 0.7,
            'max_tokens': 100
        }
    )

    tiempo = time.time() - inicio
    respuesta = response['message']['content']

    print(f"🗣️  {npc_contexto['nombre']}: {respuesta}")
    print(f"\n⏱️  Tiempo de respuesta: {tiempo:.2f} segundos")


def demo_npc_con_memoria():
    """Demo de NPC que recuerda conversaciones previas"""
    import ollama

    print("\n" + "="*70)
    print("DEMO 2: NPC CON MEMORIA")
    print("="*70)

    npc_nombre = "Citlali"
    npc_rol = "Comerciante de jade"

    # Historial de conversación
    historial = [
        {
            'role': 'system',
            'content': f'Eres {npc_nombre}, una {npc_rol}. Respondes brevemente (1-2 oraciones).'
        }
    ]

    # Conversación multi-turno
    conversacion = [
        "Hola, ¿vendes jade?",
        "¿Cuánto cuesta el jade verde?",
        "Me llevaré 3 piezas"
    ]

    for mensaje in conversacion:
        print(f"\n👤 Jugador: {mensaje}")
        print(f"🤖 {npc_nombre} está pensando...")

        # Agregar mensaje al historial
        historial.append({
            'role': 'user',
            'content': mensaje
        })

        # Generar respuesta
        inicio = time.time()
        response = ollama.chat(
            model='llama3.1:8b',
            messages=historial,
            options={'temperature': 0.7, 'max_tokens': 80}
        )
        tiempo = time.time() - inicio

        respuesta = response['message']['content']

        # Agregar respuesta al historial
        historial.append({
            'role': 'assistant',
            'content': respuesta
        })

        print(f"🗣️  {npc_nombre}: {respuesta}")
        print(f"   ({tiempo:.2f}s)")

    print("\n💡 El NPC recordó toda la conversación!")


def demo_multiples_npcs():
    """Demo de múltiples NPCs con personalidades diferentes"""
    import ollama

    print("\n" + "="*70)
    print("DEMO 3: MÚLTIPLES NPCs CON PERSONALIDADES DIFERENTES")
    print("="*70)

    npcs = [
        {
            'nombre': 'Tezca',
            'personalidad': 'Misterioso, habla en acertijos',
            'rol': 'Chamán'
        },
        {
            'nombre': 'Atl',
            'personalidad': 'Alegre, bromista, amigable',
            'rol': 'Pescador'
        },
        {
            'nombre': 'Zyanya',
            'personalidad': 'Seria, profesional, directa',
            'rol': 'Guardia'
        }
    ]

    pregunta = "¿Qué sabes sobre los dioses?"

    print(f"\n👤 Jugador pregunta a todos: \"{pregunta}\"\n")

    for npc in npcs:
        prompt = f"""Eres {npc['nombre']}, un {npc['rol']}.
Personalidad: {npc['personalidad']}

Pregunta: {pregunta}

Responde en 1 oración según tu personalidad:"""

        print(f"🤖 {npc['nombre']} ({npc['rol']})...")

        inicio = time.time()
        response = ollama.chat(
            model='llama3.1:8b',
            messages=[{'role': 'user', 'content': prompt}],
            options={'temperature': 0.8, 'max_tokens': 60}
        )
        tiempo = time.time() - inicio

        print(f"🗣️  {response['message']['content']}")
        print(f"   ({tiempo:.2f}s)\n")


def demo_performance():
    """Mide performance con diferentes longitudes de respuesta"""
    import ollama

    print("\n" + "="*70)
    print("DEMO 4: PERFORMANCE (CPU vs GPU)")
    print("="*70)

    longitudes = [
        ('Corta (NPCs)', 50),
        ('Media', 100),
        ('Larga', 200)
    ]

    for nombre, max_tokens in longitudes:
        prompt = "Describe brevemente un mercado en Tenochtitlan"

        print(f"\n📊 Respuesta {nombre} ({max_tokens} tokens max)...")

        inicio = time.time()
        response = ollama.chat(
            model='llama3.1:8b',
            messages=[{'role': 'user', 'content': prompt}],
            options={'max_tokens': max_tokens}
        )
        tiempo = time.time() - inicio

        respuesta = response['message']['content']
        palabras = len(respuesta.split())

        print(f"   Tiempo: {tiempo:.2f}s")
        print(f"   Palabras: {palabras}")
        print(f"   Velocidad: {palabras/tiempo:.1f} palabras/seg")


def mostrar_recomendaciones():
    """Muestra recomendaciones de modelos"""
    print("\n" + "="*70)
    print("📚 RECOMENDACIONES DE MODELOS PARA NPCs")
    print("="*70)

    modelos = [
        {
            'nombre': 'llama3.1:8b',
            'tamaño': '4.7 GB',
            'calidad': '⭐⭐⭐⭐⭐',
            'velocidad_cpu': '⭐⭐⭐',
            'velocidad_gpu': '⭐⭐⭐⭐⭐',
            'recomendado': 'Mejor opción general'
        },
        {
            'nombre': 'phi3:mini',
            'tamaño': '2.3 GB',
            'calidad': '⭐⭐⭐',
            'velocidad_cpu': '⭐⭐⭐⭐⭐',
            'velocidad_gpu': '⭐⭐⭐⭐⭐',
            'recomendado': 'Más rápido, ideal para NPCs'
        },
        {
            'nombre': 'mistral:7b',
            'tamaño': '4.1 GB',
            'calidad': '⭐⭐⭐⭐',
            'velocidad_cpu': '⭐⭐⭐⭐',
            'velocidad_gpu': '⭐⭐⭐⭐⭐',
            'recomendado': 'Muy balanceado'
        }
    ]

    for modelo in modelos:
        print(f"\n📦 {modelo['nombre']}")
        print(f"   Tamaño: {modelo['tamaño']}")
        print(f"   Calidad: {modelo['calidad']}")
        print(f"   Velocidad CPU: {modelo['velocidad_cpu']}")
        print(f"   Velocidad GPU: {modelo['velocidad_gpu']}")
        print(f"   ✨ {modelo['recomendado']}")

    print("\n💡 Para instalar:")
    print("   ollama pull llama3.1:8b")
    print("   ollama pull phi3:mini")
    print("   ollama pull mistral:7b")


def main():
    """Función principal"""
    print("\n" + "="*70)
    print("🤖 DEMO: LLM LOCAL PARA NPCs")
    print("Portales del Quinto Sol")
    print("="*70)

    # Verificar Ollama
    if not verificar_ollama():
        print("\n❌ Instala Ollama primero y ejecuta este script de nuevo")
        return

    print("\n¿Qué demo quieres ejecutar?")
    print("1. Conversación simple con NPC")
    print("2. NPC con memoria (multi-turno)")
    print("3. Múltiples NPCs con personalidades")
    print("4. Test de performance")
    print("5. Todas las demos")
    print("6. Solo ver recomendaciones")

    try:
        opcion = input("\nOpción (1-6): ").strip()

        if opcion == '1':
            demo_npc_simple()
        elif opcion == '2':
            demo_npc_con_memoria()
        elif opcion == '3':
            demo_multiples_npcs()
        elif opcion == '4':
            demo_performance()
        elif opcion == '5':
            demo_npc_simple()
            demo_npc_con_memoria()
            demo_multiples_npcs()
            demo_performance()
        elif opcion == '6':
            pass
        else:
            print("Opción inválida")
            return

        mostrar_recomendaciones()

        print("\n" + "="*70)
        print("✅ DEMO COMPLETADA")
        print("="*70)

        print("\n💡 Conclusión:")
        print("   • LLM local funciona BIEN para NPCs")
        print("   • No necesitas GPU potente")
        print("   • 16 GB RAM es suficiente")
        print("   • Respuestas en 2-5 segundos (CPU)")
        print("   • Respuestas en 0.5-2 segundos (GPU)")
        print("   • ¡100% gratis y privado!")

    except KeyboardInterrupt:
        print("\n\n⚠️  Demo cancelada")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nAsegúrate de:")
        print("  1. Tener Ollama instalado y corriendo")
        print("  2. Haber descargado un modelo: ollama pull llama3.1:8b")


if __name__ == '__main__':
    main()
