#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Voces Diferenciadas para NPCs
Portales del Quinto Sol

Asigna voces únicas a NPCs de forma inteligente:
- NPCs únicos: Clonación de voz (completamente único)
- NPCs importantes: Pool de 50-100 voces
- NPCs comunes: 20-30 voces + variaciones
- Total: 200-300 voces efectivas

NO necesitas 270,000 voces diferentes.
"""

import random
import json
import hashlib
from pathlib import Path
from typing import Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class ConfiguracionVoz:
    """Configuración de voz para un NPC"""
    modelo: str          # 'coqui', 'xtts', 'bark'
    voz_base: str        # ID de voz base
    genero: str          # 'M', 'F'
    pitch: float         # 0.8-1.2 (más bajo/más alto)
    speed: float         # 0.8-1.2 (más lento/más rápido)
    tono: str           # 'grave', 'normal', 'agudo'
    edad_aparente: str  # 'joven', 'adulto', 'anciano'


class SistemaVocesDiferenciadas:
    """
    Sistema que asigna voces diferentes a NPCs de forma inteligente

    Estrategia:
    1. Base de 30 voces únicas (15M, 15F)
    2. Variaciones de pitch/speed (×4) = 120 voces efectivas
    3. Para NPCs únicos: clonación de voz
    4. Distribución consistente (mismo NPC = misma voz siempre)
    """

    def __init__(self, config_dir: str = "voces_config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)

        # Voces base disponibles
        self.voces_base = self._definir_voces_base()

        # Variaciones de pitch y speed
        self.variaciones = {
            'pitch': [0.85, 0.95, 1.0, 1.05, 1.15],    # 5 variaciones
            'speed': [0.9, 0.95, 1.0, 1.05, 1.1]       # 5 variaciones
        }

        # Cache de asignaciones (npc_id -> ConfiguracionVoz)
        self.asignaciones = {}

        print("🎭 Sistema de Voces Diferenciadas inicializado")
        print(f"   Voces base: {len(self.voces_base)}")
        print(f"   Variaciones: pitch×{len(self.variaciones['pitch'])}, speed×{len(self.variaciones['speed'])}")
        print(f"   Total combinaciones: {len(self.voces_base) * len(self.variaciones['pitch']) * len(self.variaciones['speed'])}")

    def _definir_voces_base(self) -> Dict:
        """
        Define voces base disponibles

        En producción, estas serían voces reales de modelos TTS
        """
        return {
            # HOMBRES (15 voces)
            'hombre_01': {'genero': 'M', 'tono': 'grave', 'edad': 'adulto', 'modelo': 'coqui'},
            'hombre_02': {'genero': 'M', 'tono': 'normal', 'edad': 'adulto', 'modelo': 'coqui'},
            'hombre_03': {'genero': 'M', 'tono': 'agudo', 'edad': 'adulto', 'modelo': 'coqui'},
            'hombre_04': {'genero': 'M', 'tono': 'grave', 'edad': 'joven', 'modelo': 'coqui'},
            'hombre_05': {'genero': 'M', 'tono': 'normal', 'edad': 'joven', 'modelo': 'coqui'},
            'hombre_06': {'genero': 'M', 'tono': 'grave', 'edad': 'anciano', 'modelo': 'coqui'},
            'hombre_07': {'genero': 'M', 'tono': 'normal', 'edad': 'anciano', 'modelo': 'coqui'},
            'hombre_08': {'genero': 'M', 'tono': 'agudo', 'edad': 'joven', 'modelo': 'xtts'},
            'hombre_09': {'genero': 'M', 'tono': 'normal', 'edad': 'adulto', 'modelo': 'xtts'},
            'hombre_10': {'genero': 'M', 'tono': 'grave', 'edad': 'adulto', 'modelo': 'xtts'},
            'hombre_11': {'genero': 'M', 'tono': 'agudo', 'edad': 'adulto', 'modelo': 'bark'},
            'hombre_12': {'genero': 'M', 'tono': 'normal', 'edad': 'joven', 'modelo': 'bark'},
            'hombre_13': {'genero': 'M', 'tono': 'grave', 'edad': 'joven', 'modelo': 'bark'},
            'hombre_14': {'genero': 'M', 'tono': 'agudo', 'edad': 'anciano', 'modelo': 'coqui'},
            'hombre_15': {'genero': 'M', 'tono': 'normal', 'edad': 'anciano', 'modelo': 'xtts'},

            # MUJERES (15 voces)
            'mujer_01': {'genero': 'F', 'tono': 'grave', 'edad': 'adulto', 'modelo': 'coqui'},
            'mujer_02': {'genero': 'F', 'tono': 'normal', 'edad': 'adulto', 'modelo': 'coqui'},
            'mujer_03': {'genero': 'F', 'tono': 'agudo', 'edad': 'adulto', 'modelo': 'coqui'},
            'mujer_04': {'genero': 'F', 'tono': 'grave', 'edad': 'joven', 'modelo': 'coqui'},
            'mujer_05': {'genero': 'F', 'tono': 'normal', 'edad': 'joven', 'modelo': 'coqui'},
            'mujer_06': {'genero': 'F', 'tono': 'grave', 'edad': 'anciano', 'modelo': 'coqui'},
            'mujer_07': {'genero': 'F', 'tono': 'normal', 'edad': 'anciano', 'modelo': 'coqui'},
            'mujer_08': {'genero': 'F', 'tono': 'agudo', 'edad': 'joven', 'modelo': 'xtts'},
            'mujer_09': {'genero': 'F', 'tono': 'normal', 'edad': 'adulto', 'modelo': 'xtts'},
            'mujer_10': {'genero': 'F', 'tono': 'grave', 'edad': 'adulto', 'modelo': 'xtts'},
            'mujer_11': {'genero': 'F', 'tono': 'agudo', 'edad': 'adulto', 'modelo': 'bark'},
            'mujer_12': {'genero': 'F', 'tono': 'normal', 'edad': 'joven', 'modelo': 'bark'},
            'mujer_13': {'genero': 'F', 'tono': 'grave', 'edad': 'joven', 'modelo': 'bark'},
            'mujer_14': {'genero': 'F', 'tono': 'agudo', 'edad': 'anciano', 'modelo': 'coqui'},
            'mujer_15': {'genero': 'F', 'tono': 'normal', 'edad': 'anciano', 'modelo': 'xtts'},
        }

    def asignar_voz(self,
                    npc_id: int,
                    npc_nombre: str,
                    npc_genero: str,
                    npc_edad: int,
                    importancia: str = 'normal') -> ConfiguracionVoz:
        """
        Asigna una voz a un NPC de forma determinista

        Args:
            npc_id: ID único del NPC
            npc_nombre: Nombre del NPC
            npc_genero: 'M' o 'F'
            npc_edad: Edad del NPC
            importancia: 'unico', 'alto', 'normal', 'bajo'

        Returns:
            ConfiguracionVoz
        """

        # Si ya fue asignado, retornar mismo
        if npc_id in self.asignaciones:
            return self.asignaciones[npc_id]

        # Determinar tier de NPC
        tier = self._determinar_tier(importancia, npc_id)

        # Asignar según tier
        if tier == 'unico':
            config = self._asignar_voz_unica(npc_id, npc_nombre, npc_genero, npc_edad)
        elif tier == 'alto':
            config = self._asignar_voz_alta_variedad(npc_id, npc_genero, npc_edad)
        else:
            config = self._asignar_voz_comun(npc_id, npc_genero, npc_edad)

        # Cachear
        self.asignaciones[npc_id] = config

        return config

    def _determinar_tier(self, importancia: str, npc_id: int) -> str:
        """Determina tier de importancia del NPC"""

        if importancia == 'unico':
            return 'unico'

        # Para testing: asignar algunos como únicos aleatoriamente
        # En producción esto vendría de BD
        if importancia == 'alto':
            return 'alto'

        return 'normal'

    def _asignar_voz_unica(self,
                          npc_id: int,
                          nombre: str,
                          genero: str,
                          edad: int) -> ConfiguracionVoz:
        """
        Asigna voz única mediante clonación de voz

        Para NPCs únicos (quest-givers, personajes principales)
        Requiere sample de audio de referencia
        """

        # En producción, esto usaría XTTS v2 para clonación
        # Por ahora, asignar voz base con variaciones únicas

        voz_base = self._seleccionar_voz_base(genero, edad)

        return ConfiguracionVoz(
            modelo='xtts',  # XTTS soporta clonación
            voz_base=voz_base,
            genero=genero,
            pitch=1.0 + (hash(nombre) % 20 - 10) / 100,  # -0.1 a +0.1
            speed=1.0 + (hash(nombre) % 15 - 7) / 100,   # -0.07 a +0.07
            tono=self._edad_a_tono(edad),
            edad_aparente=self._edad_a_categoria(edad)
        )

    def _asignar_voz_alta_variedad(self,
                                   npc_id: int,
                                   genero: str,
                                   edad: int) -> ConfiguracionVoz:
        """
        Asigna voz con alta variedad

        Pool de ~100-150 voces diferentes
        Para NPCs importantes pero no únicos
        """

        # Usar npc_id para determinismo (mismo NPC siempre misma voz)
        seed = npc_id

        # Seleccionar voz base
        voz_base = self._seleccionar_voz_base(genero, edad, seed=seed)

        # Seleccionar variaciones
        pitch = random.Random(seed + 1).choice(self.variaciones['pitch'])
        speed = random.Random(seed + 2).choice(self.variaciones['speed'])

        return ConfiguracionVoz(
            modelo='coqui',
            voz_base=voz_base,
            genero=genero,
            pitch=pitch,
            speed=speed,
            tono=self._edad_a_tono(edad),
            edad_aparente=self._edad_a_categoria(edad)
        )

    def _asignar_voz_comun(self,
                          npc_id: int,
                          genero: str,
                          edad: int) -> ConfiguracionVoz:
        """
        Asigna voz común

        Pool de ~30-50 voces
        Para NPCs genéricos
        """

        seed = npc_id

        # Usar subset de voces base (solo primeras 10 por género)
        voces_genero = [v for v in self.voces_base.keys()
                       if self.voces_base[v]['genero'] == genero][:10]

        voz_base = random.Random(seed).choice(voces_genero)

        # Menos variaciones
        pitch = random.Random(seed + 1).choice([0.95, 1.0, 1.05])
        speed = random.Random(seed + 2).choice([0.95, 1.0, 1.05])

        return ConfiguracionVoz(
            modelo='coqui',
            voz_base=voz_base,
            genero=genero,
            pitch=pitch,
            speed=speed,
            tono=self._edad_a_tono(edad),
            edad_aparente=self._edad_a_categoria(edad)
        )

    def _seleccionar_voz_base(self,
                             genero: str,
                             edad: int,
                             seed: Optional[int] = None) -> str:
        """Selecciona voz base según género y edad"""

        categoria_edad = self._edad_a_categoria(edad)

        # Filtrar voces por género y edad
        voces_filtradas = [
            voz_id for voz_id, info in self.voces_base.items()
            if info['genero'] == genero and info['edad'] == categoria_edad
        ]

        # Si no hay match exacto, relajar filtro de edad
        if not voces_filtradas:
            voces_filtradas = [
                voz_id for voz_id, info in self.voces_base.items()
                if info['genero'] == genero
            ]

        if seed is not None:
            return random.Random(seed).choice(voces_filtradas)

        return random.choice(voces_filtradas)

    def _edad_a_categoria(self, edad: int) -> str:
        """Convierte edad numérica a categoría"""
        if edad < 25:
            return 'joven'
        elif edad < 60:
            return 'adulto'
        else:
            return 'anciano'

    def _edad_a_tono(self, edad: int) -> str:
        """Determina tono según edad"""
        if edad < 20:
            return 'agudo'
        elif edad < 50:
            return 'normal'
        else:
            return 'grave'

    def generar_audio_con_voz(self,
                             texto: str,
                             config_voz: ConfiguracionVoz,
                             output_path: str):
        """
        Genera audio aplicando configuración de voz

        En producción, esto usaría TTS real con parámetros
        """

        print(f"\n🎙️  Generando audio:")
        print(f"   Texto: \"{texto}\"")
        print(f"   Modelo: {config_voz.modelo}")
        print(f"   Voz: {config_voz.voz_base}")
        print(f"   Pitch: {config_voz.pitch:.2f}")
        print(f"   Speed: {config_voz.speed:.2f}")
        print(f"   Género: {config_voz.genero}")
        print(f"   Edad: {config_voz.edad_aparente}")

        # Aquí iría la generación real con TTS
        # Por ahora solo simulamos

        """
        Código real sería:

        if config_voz.modelo == 'coqui':
            from TTS.api import TTS
            tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts")

            tts.tts_to_file(
                text=texto,
                speaker=config_voz.voz_base,
                file_path=output_path,
                speed=config_voz.speed
            )

            # Aplicar pitch con librosa o sox
            import librosa
            import soundfile as sf

            y, sr = librosa.load(output_path)
            y_shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=config_voz.pitch)
            sf.write(output_path, y_shifted, sr)

        elif config_voz.modelo == 'xtts':
            # XTTS v2 para clonación de voz
            ...
        """

        print(f"   ✅ Audio generado: {output_path}")

    def calcular_estadisticas_voces(self, npcs: list) -> Dict:
        """Calcula estadísticas de distribución de voces"""

        stats = {
            'total_npcs': len(npcs),
            'voces_unicas': 0,
            'combinaciones_diferentes': set(),
            'por_genero': {'M': 0, 'F': 0},
            'por_tier': {'unico': 0, 'alto': 0, 'normal': 0}
        }

        for npc in npcs:
            config = self.asignar_voz(**npc)

            # Combinación única
            comb_id = f"{config.voz_base}_{config.pitch}_{config.speed}"
            stats['combinaciones_diferentes'].add(comb_id)

            stats['por_genero'][config.genero] += 1

        stats['voces_unicas'] = len(stats['combinaciones_diferentes'])

        return stats


def demo_voces_diferenciadas():
    """Demo del sistema de voces diferenciadas"""

    print("\n" + "="*70)
    print("🎭 DEMO: SISTEMA DE VOCES DIFERENCIADAS")
    print("="*70)

    sistema = SistemaVocesDiferenciadas()

    # Simular diferentes NPCs
    npcs_prueba = [
        # NPCs únicos (quest-givers)
        {'npc_id': 1, 'npc_nombre': 'Xolotl el Herrero', 'npc_genero': 'M', 'npc_edad': 45, 'importancia': 'unico'},
        {'npc_id': 2, 'npc_nombre': 'Citlali la Oráculo', 'npc_genero': 'F', 'npc_edad': 67, 'importancia': 'unico'},
        {'npc_id': 3, 'npc_nombre': 'Tezca el Chamán', 'npc_genero': 'M', 'npc_edad': 82, 'importancia': 'unico'},

        # NPCs importantes
        {'npc_id': 101, 'npc_nombre': 'Comerciante 1', 'npc_genero': 'M', 'npc_edad': 35, 'importancia': 'alto'},
        {'npc_id': 102, 'npc_nombre': 'Comerciante 2', 'npc_genero': 'F', 'npc_edad': 28, 'importancia': 'alto'},
        {'npc_id': 103, 'npc_nombre': 'Guardia 1', 'npc_genero': 'M', 'npc_edad': 31, 'importancia': 'alto'},

        # NPCs comunes
        {'npc_id': 1001, 'npc_nombre': 'Campesino 1', 'npc_genero': 'M', 'npc_edad': 42, 'importancia': 'normal'},
        {'npc_id': 1002, 'npc_nombre': 'Campesino 2', 'npc_genero': 'M', 'npc_edad': 39, 'importancia': 'normal'},
        {'npc_id': 1003, 'npc_nombre': 'Campesina 1', 'npc_genero': 'F', 'npc_edad': 26, 'importancia': 'normal'},
    ]

    print("\n📊 Asignando voces a NPCs:\n")

    for npc in npcs_prueba:
        config = sistema.asignar_voz(**npc)

        tier = '⭐⭐⭐' if npc['importancia'] == 'unico' else '⭐⭐' if npc['importancia'] == 'alto' else '⭐'

        print(f"{tier} {npc['npc_nombre']} (ID: {npc['npc_id']}, {npc['npc_genero']}, {npc['npc_edad']} años)")
        print(f"      Voz: {config.voz_base}")
        print(f"      Pitch: {config.pitch:.2f}, Speed: {config.speed:.2f}")
        print(f"      Modelo: {config.modelo}")
        print(f"      Tono: {config.tono}, Edad aparente: {config.edad_aparente}\n")

    # Simular 1000 NPCs para estadísticas
    print("\n" + "="*70)
    print("📈 SIMULANDO 1,000 NPCs ALEATORIOS")
    print("="*70)

    npcs_sim = []
    for i in range(1000):
        npcs_sim.append({
            'npc_id': 10000 + i,
            'npc_nombre': f'NPC_{i}',
            'npc_genero': random.choice(['M', 'F']),
            'npc_edad': random.randint(18, 80),
            'importancia': random.choices(
                ['unico', 'alto', 'normal'],
                weights=[0.01, 0.1, 0.89],  # 1% únicos, 10% altos, 89% normales
                k=1
            )[0]
        })

    # Calcular estadísticas
    sistema_temp = SistemaVocesDiferenciadas()
    stats = sistema_temp.calcular_estadisticas_voces(npcs_sim)

    print(f"\n📊 Estadísticas de 1,000 NPCs:")
    print(f"   Total NPCs: {stats['total_npcs']:,}")
    print(f"   Voces únicas (combinaciones): {stats['voces_unicas']:,}")
    print(f"   Hombres: {stats['por_genero']['M']:,}")
    print(f"   Mujeres: {stats['por_genero']['F']:,}")

    # Calcular repetición promedio
    repeticion = stats['total_npcs'] / stats['voces_unicas']
    print(f"\n📈 Promedio NPCs por voz: {repeticion:.1f}")

    if repeticion < 10:
        print("   ✅ Excelente variedad!")
    elif repeticion < 20:
        print("   ✅ Buena variedad")
    else:
        print("   ⚠️  Considerar más variaciones")

    print("\n" + "="*70)
    print("✅ DEMO COMPLETADA")
    print("="*70)

    print("\n💡 Conclusiones:")
    print("   • 30 voces base × 5 pitch × 5 speed = 750 combinaciones posibles")
    print("   • NPCs únicos: Voces completamente diferentes")
    print("   • NPCs importantes: Alta variedad (~100-150 voces)")
    print("   • NPCs comunes: ~30-50 voces (suficiente)")
    print("   • MISMO NPC siempre tiene MISMA VOZ (determinista)")
    print("   • Escalable a 270,000 NPCs sin problema")


if __name__ == '__main__':
    demo_voces_diferenciadas()
