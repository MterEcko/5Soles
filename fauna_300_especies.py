#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Fauna: 300+ Especies Animales
Portales del Quinto Sol
"""

import sqlite3
import json

DB_PATH = 'quinto_sol.db'

def generar_fauna_completa():
    """Generar 300+ especies de animales"""

    fauna = []

    # ================================================================
    # MAMÍFEROS TERRESTRES (80 especies)
    # ================================================================

    # Cánidos (10)
    fauna.extend([
        ('Xoloitzcuintle', 'Itzcuintli', 'domestico', 'baja', 50, 'Perro sagrado azteca', 'mediano', 'omnivoro', 120, 0.6),
        ('Xoloitzcuintle Salvaje', 'Itzcuintli Cuauhtla', 'salvaje', 'media', 40, 'Xolo feral en bosques', 'mediano', 'carnivoro', 130, 0.08),
        ('Coyote', 'Coyotl', 'salvaje', 'media', 60, 'Coyote cazador', 'mediano', 'carnivoro', 160, 0.25),
        ('Coyote del Desierto', 'Coyotl Iztac', 'salvaje', 'media', 70, 'Coyote adaptado al desierto', 'mediano', 'carnivoro', 170, 0.15),
        ('Lobo Gris', 'Cuetlachtli', 'salvaje', 'alta', 150, 'Lobo en manadas', 'grande', 'carnivoro', 180, 0.05),
        ('Lobo Mexicano', 'Cuetlachtli Chichimeca', 'salvaje', 'alta', 200, 'Lobo del norte', 'grande', 'carnivoro', 175, 0.03),
        ('Zorro Gris', 'Oztohua', 'salvaje', 'baja', 80, 'Zorro común', 'pequeño', 'omnivoro', 190, 0.2),
        ('Zorro del Desierto', 'Oztohua Iztac', 'salvaje', 'baja', 90, 'Zorro de desierto', 'pequeño', 'omnivoro', 200, 0.12),
        ('Perro Salvaje', 'Chichi Cuauhtla', 'salvaje', 'alta', 45, 'Perro asilvestrado en manadas', 'mediano', 'carnivoro', 150, 0.1),
        ('Tecichi', 'Techichi', 'domestico', 'ninguna', 60, 'Perro pequeño de compañía', 'pequeño', 'omnivoro', 100, 0.3),
    ])

    # Felinos (15)
    fauna.extend([
        ('Jaguar', 'Ocelotl', 'salvaje', 'extrema', 500, 'Jaguar, depredador supremo', 'grande', 'carnivoro', 170, 0.05),
        ('Jaguar Negro', 'Ocelotl Yayauhqui', 'salvaje', 'extrema', 800, 'Jaguar melánicopantera', 'grande', 'carnivoro', 175, 0.02),
        ('Puma', 'Miztli', 'salvaje', 'alta', 400, 'Puma cazador', 'grande', 'carnivoro', 190, 0.1),
        ('Ocelote', 'Tlalocelotl', 'salvaje', 'media', 250, 'Ocelote manchado', 'mediano', 'carnivoro', 180, 0.12),
        ('Margay', 'Cuitlamiztli', 'salvaje', 'media', 200, 'Gato tigre arborícola', 'pequeño', 'carnivoro', 170, 0.08),
        ('Jaguarundi', 'Miztli Yayauhqui', 'salvaje', 'media', 150, 'Gato nutria', 'mediano', 'carnivoro', 160, 0.15),
        ('Lince', 'Ocomiztli', 'salvaje', 'alta', 300, 'Lince de montaña', 'mediano', 'carnivoro', 185, 0.07),
        ('Tigrillo', 'Tlatlauhqui Miztli', 'salvaje', 'media', 180, 'Gato pequeño salvaje', 'pequeño', 'carnivoro', 175, 0.1),
        ('Gato de Monte', 'Tepemiztli', 'salvaje', 'baja', 120, 'Gato salvaje montés', 'pequeño', 'carnivoro', 170, 0.18),
        ('Gato Doméstico', 'Miztli', 'domestico', 'ninguna', 30, 'Gato de casa', 'pequeño', 'carnivoro', 180, 0.4),
        ('Gato Callejero', 'Miztli Otli', 'salvaje', 'baja', 20, 'Gato callejero', 'pequeño', 'carnivoro', 190, 0.25),
        ('Gato Egipcio', 'Miztli Teo', 'domestico', 'ninguna', 150, 'Gato sagrado importado', 'pequeño', 'carnivoro', 160, 0.05),
        ('Leopardo Nublado', 'Mixtli Mixtli', 'salvaje', 'alta', 600, 'Leopardo de nubes raro', 'grande', 'carnivoro', 195, 0.01),
        ('Gato Montés', 'Tepemiztli Cualli', 'salvaje', 'media', 160, 'Gato salvaje robusto', 'mediano', 'carnivoro', 165, 0.11),
        ('Yaguarundi', 'Ocomiztli Tlilic', 'salvaje', 'media', 140, 'Gato de río', 'mediano', 'carnivoro', 155, 0.13),
    ])

    # Úrsidos (4)
    fauna.extend([
        ('Oso Negro', 'Tliltic Tlamacazqui', 'salvaje', 'extrema', 700, 'Oso negro americano', 'gigante', 'omnivoro', 120, 0.04),
        ('Oso Pardo', 'Iztac Tlamacazqui', 'salvaje', 'extrema', 900, 'Oso grizzly', 'gigante', 'omnivoro', 130, 0.02),
        ('Oso Hormiguero', 'Azcatl', 'salvaje', 'baja', 180, 'Oso hormiguero gigante', 'grande', 'insectivoro', 80, 0.08),
        ('Oso Hormiguero Sedoso', 'Azcatl Iztac', 'salvaje', 'ninguna', 200, 'Hormiguero pequeño', 'pequeño', 'insectivoro', 60, 0.06),
    ])

    # Cérvidos y herbívoros (15)
    fauna.extend([
        ('Venado Cola Blanca', 'Mazatl', 'salvaje', 'baja', 80, 'Venado común', 'grande', 'herbivoro', 180, 0.3),
        ('Venado Bura', 'Mazatl Nacatl', 'salvaje', 'baja', 90, 'Venado de orejas grandes', 'grande', 'herbivoro', 175, 0.22),
        ('Ciervo Rojo', 'Mazatl Tlatlauhqui', 'salvaje', 'baja', 120, 'Ciervo europeo', 'grande', 'herbivoro', 185, 0.08),
        ('Alce', 'Mazatl Huey', 'salvaje', 'media', 250, 'Alce gigante del norte', 'gigante', 'herbivoro', 140, 0.03),
        ('Berrendo', 'Tlemaitl', 'salvaje', 'baja', 110, 'Antílope americano', 'grande', 'herbivoro', 210, 0.12),
        ('Jabalí', 'Pitzotl', 'salvaje', 'media', 100, 'Jabalí agresivo', 'grande', 'omnivoro', 140, 0.15),
        ('Pecarí de Collar', 'Coyametl', 'salvaje', 'media', 85, 'Pecarí común', 'mediano', 'omnivoro', 150, 0.2),
        ('Pecarí de Labios Blancos', 'Coyametl Iztac', 'salvaje', 'alta', 95, 'Pecarí grande en manadas', 'mediano', 'omnivoro', 145, 0.15),
        ('Tapir', 'Tlacaxolotl', 'salvaje', 'media', 300, 'Tapir de Baird', 'grande', 'herbivoro', 110, 0.05),
        ('Bisonte', 'Cíbolo', 'salvaje', 'alta', 500, 'Bisonte americano', 'gigante', 'herbivoro', 130, 0.02),
        ('Cabra Montés', 'Cuacuauhtzin', 'salvaje', 'baja', 120, 'Cabra de montaña', 'mediano', 'herbivoro', 160, 0.1),
        ('Borrego Cimarrón', 'Cuacuauhtzin Tepetl', 'salvaje', 'media', 250, 'Borrego de cuernos grandes', 'grande', 'herbivoro', 155, 0.04),
        ('Caballo Salvaje', 'Cahuayo Cuauhtla', 'salvaje', 'baja', 400, 'Mustang salvaje', 'grande', 'herbivoro', 220, 0.03),
        ('Burro Salvaje', 'Asno Cuauhtla', 'salvaje', 'baja', 200, 'Burro feral', 'grande', 'herbivoro', 140, 0.05),
        ('Venado Temazate', 'Temazatl', 'salvaje', 'baja', 70, 'Venado enano', 'pequeño', 'herbivoro', 190, 0.18),
    ])

    # Roedores (12)
    fauna.extend([
        ('Conejo de Campo', 'Tochtli', 'domestico', 'ninguna', 10, 'Conejo común', 'pequeño', 'herbivoro', 150, 0.4),
        ('Conejo Silvestre', 'Tochtli Cuauhtla', 'salvaje', 'ninguna', 15, 'Conejo salvaje', 'pequeño', 'herbivoro', 160, 0.35),
        ('Liebre', 'Citli', 'salvaje', 'ninguna', 20, 'Liebre veloz', 'pequeño', 'herbivoro', 200, 0.25),
        ('Liebre Antílope', 'Citli Tlemaitl', 'salvaje', 'ninguna', 25, 'Liebre gigante del desierto', 'mediano', 'herbivoro', 220, 0.1),
        ('Ardilla Gris', 'Techalotl', 'salvaje', 'ninguna', 12, 'Ardilla común', 'pequeño', 'omnivoro', 170, 0.5),
        ('Ardilla Roja', 'Techalotl Tlatlauhqui', 'salvaje', 'ninguna', 15, 'Ardilla de bosque', 'pequeño', 'omnivoro', 175, 0.4),
        ('Ardilla Voladora', 'Techalotl Patlani', 'salvaje', 'ninguna', 30, 'Ardilla planeadora', 'pequeño', 'omnivoro', 100, 0.12),
        ('Tuza', 'Tozan', 'salvaje', 'ninguna', 8, 'Roedor excavador', 'pequeño', 'herbivoro', 70, 0.3),
        ('Rata de Campo', 'Quimichin Milli', 'salvaje', 'ninguna', 5, 'Rata silvestre', 'pequeño', 'omnivoro', 140, 0.6),
        ('Rata Urbana', 'Quimichin Altepetl', 'salvaje', 'baja', 3, 'Rata de ciudad', 'pequeño', 'omnivoro', 150, 0.7),
        ('Ratón Doméstico', 'Quimichtzin', 'salvaje', 'ninguna', 2, 'Ratón de casa', 'pequeño', 'omnivoro', 130, 0.8),
        ('Puercoespín', 'Huitzquilitl', 'salvaje', 'baja', 50, 'Puercoespín con púas', 'mediano', 'herbivoro', 60, 0.15),
    ])

    # Otros mamíferos (24)
    fauna.extend([
        ('Armadillo', 'Ayotochtli', 'salvaje', 'ninguna', 25, 'Armadillo común', 'pequeño', 'omnivoro', 70, 0.2),
        ('Armadillo de Nueve Bandas', 'Ayotochtli Chicuei', 'salvaje', 'ninguna', 30, 'Armadillo rayado', 'pequeño', 'omnivoro', 75, 0.18),
        ('Tlacuache', 'Tlacuatzin', 'salvaje', 'ninguna', 20, 'Zarigüeya', 'pequeño', 'omnivoro', 80, 0.25),
        ('Mapache', 'Mapachtli', 'salvaje', 'media', 40, 'Mapache astuto', 'mediano', 'omnivoro', 110, 0.2),
        ('Coatí', 'Pizotl', 'salvaje', 'media', 50, 'Coatí de nariz blanca', 'mediano', 'omnivoro', 120, 0.15),
        ('Tejón', 'Tlalcoyotl', 'salvaje', 'media', 60, 'Tejón americano', 'mediano', 'omnivoro', 90, 0.12),
        ('Comadreja', 'Cozamalotl', 'salvaje', 'baja', 35, 'Comadreja cazadora', 'pequeño', 'carnivoro', 180, 0.18),
        ('Marta', 'Ozomatli Pequeña', 'salvaje', 'media', 55, 'Marta de árboles', 'pequeño', 'carnivoro', 170, 0.1),
        ('Nutria de Río', 'Ahuitzotl Menor', 'salvaje', 'baja', 100, 'Nutria juguetona', 'mediano', 'carnivoro', 140, 0.08),
        ('Mofeta', 'Epatl', 'salvaje', 'baja', 25, 'Mofeta rayada', 'pequeño', 'omnivoro', 70, 0.22),
        ('Zorrillo', 'Epatl Huey', 'salvaje', 'baja', 30, 'Zorrillo grande', 'pequeño', 'omnivoro', 75, 0.19),
        ('Murciélago Vampiro', 'Tzinacantli Eztli', 'salvaje', 'media', 15, 'Murciélago bebedor de sangre', 'pequeño', 'hematofago', 90, 0.25),
        ('Murciélago Frugívoro', 'Tzinacantli Xochitl', 'salvaje', 'ninguna', 10, 'Murciélago de fruta', 'pequeño', 'frugivoro', 100, 0.4),
        ('Murciélago Insectívoro', 'Tzinacantli', 'salvaje', 'ninguna', 8, 'Murciélago común', 'pequeño', 'insectivoro', 120, 0.6),
        ('Mono Araña', 'Ozomatli', 'salvaje', 'baja', 150, 'Mono de cola prensil', 'mediano', 'omnivoro', 160, 0.08),
        ('Mono Aullador', 'Ozomatli Tzahtzi', 'salvaje', 'media', 170, 'Mono ruidoso territorial', 'mediano', 'herbivoro', 100, 0.07),
        ('Mono Capuchino', 'Ozomatli Tzontli', 'salvaje', 'baja', 180, 'Mono inteligente', 'pequeño', 'omnivoro', 140, 0.05),
        ('Perezoso', 'Ah Puch Menor', 'salvaje', 'ninguna', 120, 'Perezoso de dos dedos', 'mediano', 'herbivoro', 10, 0.06),
        ('Caballo Doméstico', 'Cahuayo', 'domestico', 'ninguna', 800, 'Caballo de monta', 'grande', 'herbivoro', 250, 0.15),
        ('Burro', 'Asno', 'domestico', 'ninguna', 300, 'Burro de carga', 'grande', 'herbivoro', 120, 0.2),
        ('Mula', 'Mula', 'domestico', 'ninguna', 400, 'Híbrido caballo-burro', 'grande', 'herbivoro', 180, 0.1),
        ('Llama', 'Llama', 'domestico', 'ninguna', 500, 'Llama andina de carga', 'grande', 'herbivoro', 140, 0.03),
        ('Alpaca', 'Alpaca', 'domestico', 'ninguna', 450, 'Alpaca de lana', 'grande', 'herbivoro', 130, 0.04),
        ('Vicuña', 'Vicuña', 'salvaje', 'baja', 600, 'Vicuña silvestre', 'grande', 'herbivoro', 190, 0.02),
    ])

    # ================================================================
    # AVES (100 especies)
    # ================================================================

    # Rapaces (20)
    fauna.extend([
        ('Águila Real', 'Cuauhtli', 'salvaje', 'media', 200, 'Águila majestuosa', 'mediano', 'carnivoro', 220, 0.08),
        ('Águila Arpía', 'Cuauhtli Huey', 'salvaje', 'alta', 500, 'Águila gigante cazadora', 'grande', 'carnivoro', 200, 0.02),
        ('Águila Pescadora', 'Cuauhtli Michin', 'salvaje', 'baja', 150, 'Águila de río', 'mediano', 'piscivoro', 230, 0.12),
        ('Halcón Peregrino', 'Tohtli', 'salvaje', 'media', 180, 'Halcón veloz', 'pequeño', 'carnivoro', 300, 0.1),
        ('Halcón de Harris', 'Tohtli Tlacatl', 'salvaje', 'media', 160, 'Halcón social', 'mediano', 'carnivoro', 250, 0.08),
        ('Gavilán', 'Tohtli Tecolotl', 'salvaje', 'media', 120, 'Gavilán común', 'pequeño', 'carnivoro', 240, 0.15),
        ('Búho Cornudo', 'Tecolotl Cuauhtzontli', 'salvaje', 'media', 140, 'Búho con cuernos', 'mediano', 'carnivoro', 100, 0.12),
        ('Lechuza de Campanario', 'Tecolotl Iztac', 'salvaje', 'baja', 100, 'Lechuza blanca', 'mediano', 'carnivoro', 110, 0.2),
        ('Tecolote Llanero', 'Tecolotl Milli', 'salvaje', 'baja', 80, 'Búho de madriguera', 'pequeño', 'carnivoro', 90, 0.18),
        ('Águila Cabeza Blanca', 'Cuauhtli Iztac', 'salvaje', 'media', 250, 'Águila calva', 'grande', 'carnivoro', 210, 0.05),
        ('Milano Cola de Tijera', 'Tohtli Tezcatl', 'salvaje', 'baja', 110, 'Milano elegante', 'mediano', 'carnivoro', 260, 0.1),
        ('Zopilote Rey', 'Cozcacuauhtli Tlatoani', 'salvaje', 'ninguna', 90, 'Buitre colorido', 'grande', 'carroñero', 120, 0.08),
        ('Zopilote Común', 'Cozcacuauhtli', 'salvaje', 'ninguna', 30, 'Buitre negro', 'grande', 'carroñero', 150, 0.4),
        ('Zopilote Aura', 'Cozcacuauhtli Tlatlauhqui', 'salvaje', 'ninguna', 40, 'Buitre de cabeza roja', 'grande', 'carroñero', 140, 0.35),
        ('Caracara', 'Tliltzin', 'salvaje', 'media', 130, 'Halcón carroñero', 'mediano', 'omnivoro', 180, 0.12),
        ('Aguililla Cola Roja', 'Cuauhtli Coztic', 'salvaje', 'media', 170, 'Halcón de cola roja', 'mediano', 'carnivoro', 190, 0.14),
        ('Cernícalo', 'Tohtli Tzontli', 'salvaje', 'baja', 95, 'Halcón pequeño', 'pequeño', 'carnivoro', 200, 0.16),
        ('Mochuelo', 'Tecolotl Tzontli', 'salvaje', 'baja', 70, 'Búho pequeño', 'pequeño', 'carnivoro', 80, 0.22),
        ('Búho Nival', 'Tecolotl Cepayahuitl', 'salvaje', 'media', 200, 'Búho del Ártico', 'grande', 'carnivoro', 130, 0.01),
        ('Cuervo', 'Cacalotl', 'salvaje', 'baja', 50, 'Cuervo inteligente', 'mediano', 'omnivoro', 160, 0.25),
    ])

    # Aves acuáticas (15)
    fauna.extend([
        ('Pato Silvestre', 'Canauhtli', 'salvaje', 'ninguna', 35, 'Pato común', 'mediano', 'omnivoro', 150, 0.3),
        ('Pato Doméstico', 'Canauhtli Calli', 'domestico', 'ninguna', 40, 'Pato de granja', 'mediano', 'omnivoro', 100, 0.25),
        ('Ganso Canadiense', 'Concanauhtli', 'salvaje', 'media', 80, 'Ganso migratorio', 'grande', 'herbivoro', 170, 0.15),
        ('Cisne Trompetero', 'Canauhtli Iztac Huey', 'salvaje', 'media', 300, 'Cisne gigante blanco', 'grande', 'herbivoro', 140, 0.03),
        ('Pelícano Blanco', 'Atotolin Iztac', 'salvaje', 'baja', 120, 'Pelícano pescador', 'grande', 'piscivoro', 130, 0.1),
        ('Pelícano Café', 'Atotolin Camohtli', 'salvaje', 'baja', 110, 'Pelícano costero', 'grande', 'piscivoro', 125, 0.12),
        ('Garza Blanca', 'Aztatl Iztac', 'salvaje', 'ninguna', 70, 'Garza común', 'grande', 'piscivoro', 160, 0.2),
        ('Garza Azul', 'Aztatl Texohtic', 'salvaje', 'ninguna', 75, 'Garza grande azul', 'grande', 'piscivoro', 155, 0.18),
        ('Garceta', 'Aztatl Tzontli', 'salvaje', 'ninguna', 60, 'Garza pequeña', 'mediano', 'piscivoro', 170, 0.22),
        ('Ibis Blanco', 'Tlalpoyahuali', 'salvaje', 'ninguna', 85, 'Ibis de pico curvo', 'mediano', 'omnivoro', 145, 0.12),
        ('Espátula Rosada', 'Tlapalaztatl', 'salvaje', 'ninguna', 150, 'Ave rosada de pico plano', 'mediano', 'omnivoro', 140, 0.08),
        ('Flamenco', 'Tlapaltototl', 'salvaje', 'ninguna', 200, 'Flamenco rosa', 'grande', 'omnivoro', 150, 0.05),
        ('Cormorán', 'Acacalotl', 'salvaje', 'ninguna', 65, 'Ave buceadora', 'mediano', 'piscivoro', 120, 0.18),
        ('Gallareta', 'Acitli', 'salvaje', 'ninguna', 30, 'Ave acuática pequeña', 'pequeño', 'herbivoro', 110, 0.3),
        ('Martín Pescador', 'Achalalactli', 'salvaje', 'ninguna', 55, 'Ave pescadora rápida', 'pequeño', 'piscivoro', 200, 0.15),
    ])

    # Aves de corral (8)
    fauna.extend([
        ('Pavo', 'Huexolotl', 'domestico', 'ninguna', 20, 'Pavo de corral', 'mediano', 'omnivoro', 80, 0.3),
        ('Pavo Salvaje', 'Huexolotl Cuauhtla', 'salvaje', 'baja', 60, 'Pavo silvestre', 'grande', 'omnivoro', 100, 0.15),
        ('Guajolote', 'Totolin', 'domestico', 'ninguna', 15, 'Guajolote común', 'mediano', 'omnivoro', 70, 0.35),
        ('Gallina', 'Cuanaca', 'domestico', 'ninguna', 10, 'Gallina ponedora', 'pequeño', 'omnivoro', 60, 0.5),
        ('Gallo', 'Cuanaca Oquichtli', 'domestico', 'baja', 12, 'Gallo de pelea', 'pequeño', 'omnivoro', 80, 0.4),
        ('Codorniz', 'Zolin', 'salvaje', 'ninguna', 18, 'Codorniz silvestre', 'pequeño', 'omnivoro', 120, 0.25),
        ('Paloma Doméstica', 'Huilotl Calli', 'domestico', 'ninguna', 8, 'Paloma de casa', 'pequeño', 'granivoro', 140, 0.4),
        ('Faisán', 'Quetzalcoatl Tzontli', 'salvaje', 'baja', 80, 'Faisán de caza', 'mediano', 'omnivoro', 110, 0.08),
    ])

    # Loros y guacamayas (12)
    fauna.extend([
        ('Guacamaya Roja', 'Alo Tlatlauhqui', 'salvaje', 'ninguna', 800, 'Guacamaya escarlata', 'grande', 'frugivoro', 180, 0.03),
        ('Guacamaya Azul', 'Alo Texohtic', 'salvaje', 'ninguna', 900, 'Guacamaya azul y amarillo', 'grande', 'frugivoro', 175, 0.02),
        ('Guacamaya Verde', 'Alo Quiltic', 'salvaje', 'ninguna', 700, 'Guacamaya militar', 'grande', 'frugivoro', 170, 0.04),
        ('Loro Corona Lila', 'Toznene Xoxoctic', 'salvaje', 'ninguna', 300, 'Loro amazona', 'mediano', 'frugivoro', 150, 0.08),
        ('Loro Cabeza Amarilla', 'Toznene Coztic', 'salvaje', 'ninguna', 280, 'Loro amazona amarillo', 'mediano', 'frugivoro', 145, 0.09),
        ('Perico Verde', 'Quilitotl', 'salvaje', 'ninguna', 50, 'Perico común', 'pequeño', 'frugivoro', 160, 0.2),
        ('Perico Monje', 'Quilitotl Tlamacazqui', 'salvaje', 'ninguna', 60, 'Perico argentino', 'pequeño', 'granivoro', 155, 0.18),
        ('Periquito', 'Quilitotl Tzontli', 'domestico', 'ninguna', 30, 'Periquito de compañía', 'pequeño', 'granivoro', 140, 0.25),
        ('Cacatúa', 'Toznene Iztac', 'salvaje', 'ninguna', 500, 'Cacatúa blanca importada', 'mediano', 'omnivoro', 130, 0.01),
        ('Ara Militar', 'Alo Yaoquizqui', 'salvaje', 'ninguna', 750, 'Guacamaya militar grande', 'grande', 'frugivoro', 165, 0.03),
        ('Loro Yucateco', 'Toznene Mayapan', 'salvaje', 'ninguna', 250, 'Loro de Yucatán', 'mediano', 'frugivoro', 135, 0.1),
        ('Cotorra', 'Quilitotl Altepetl', 'salvaje', 'ninguna', 40, 'Cotorra urbana', 'pequeño', 'omnivoro', 150, 0.22),
    ])

    # Colibríes (8)
    fauna.extend([
        ('Colibrí Pico Ancho', 'Huitzilin', 'salvaje', 'ninguna', 100, 'Colibrí común', 'pequeño', 'nectarivoro', 250, 0.3),
        ('Colibrí Garganta Rubí', 'Huitzilin Tezcatl', 'salvaje', 'ninguna', 120, 'Colibrí con garganta roja', 'pequeño', 'nectarivoro', 260, 0.25),
        ('Colibrí Cola Hendida', 'Huitzilin Tzotzol', 'salvaje', 'ninguna', 110, 'Colibrí de cola bifurcada', 'pequeño', 'nectarivoro', 270, 0.28),
        ('Colibrí Oreja Violeta', 'Huitzilin Camohpalli', 'salvaje', 'ninguna', 150, 'Colibrí de montaña', 'pequeño', 'nectarivoro', 240, 0.15),
        ('Colibrí Gigante', 'Huitzilin Huey', 'salvaje', 'ninguna', 200, 'Colibrí más grande', 'pequeño', 'nectarivoro', 220, 0.08),
        ('Colibrí Esmeralda', 'Huitzilin Quetzal', 'salvaje', 'ninguna', 180, 'Colibrí verde brillante', 'pequeño', 'nectarivoro', 255, 0.12),
        ('Chuparrosa', 'Xiuhcozcacuauhtli', 'salvaje', 'ninguna', 90, 'Colibrí del desierto', 'pequeño', 'nectarivoro', 265, 0.18),
        ('Colibrí Corona Azul', 'Huitzilin Xiuhtli', 'salvaje', 'ninguna', 140, 'Colibrí de corona azul', 'pequeño', 'nectarivoro', 248, 0.2),
    ])

    # Aves canoras y otras (37)
    fauna.extend([
        ('Quetzal', 'Quetzaltototl', 'salvaje', 'ninguna', 5000, 'Ave sagrada de plumas largas', 'mediano', 'frugivoro', 180, 0.005),
        ('Cenzontle', 'Centzontli', 'salvaje', 'ninguna', 80, 'Ave de 400 voces', 'pequeño', 'omnivoro', 150, 0.2),
        ('Cardenal Rojo', 'Tlapaltototl Oquichtli', 'salvaje', 'ninguna', 70, 'Cardenal escarlata', 'pequeño', 'granivoro', 140, 0.18),
        ('Azulejo', 'Xiuhtototl', 'salvaje', 'ninguna', 60, 'Ave azul brillante', 'pequeño', 'insectivoro', 145, 0.22),
        ('Jilguero', 'Coztic Tototl', 'salvaje', 'ninguna', 50, 'Jilguero amarillo', 'pequeño', 'granivoro', 135, 0.25),
        ('Gorrión', 'Molotl', 'salvaje', 'ninguna', 15, 'Gorrión común', 'pequeño', 'granivoro', 130, 0.5),
        ('Calandria', 'Calanitototl', 'salvaje', 'ninguna', 45, 'Calandria naranja', 'pequeño', 'insectivoro', 138, 0.22),
        ('Tordo', 'Tzanatl', 'salvaje', 'ninguna', 25, 'Tordo negro', 'pequeño', 'omnivoro', 142, 0.3),
        ('Zanate', 'Tzanatzontli', 'salvaje', 'ninguna', 20, 'Zanate cola larga', 'pequeño', 'omnivoro', 148, 0.35),
        ('Urraca', 'Uil', 'salvaje', 'baja', 55, 'Urraca de pecho azul', 'mediano', 'omnivoro', 160, 0.15),
        ('Arrendajo Azul', 'Xiuhtotoqueh', 'salvaje', 'ninguna', 65, 'Arrendajo ruidoso', 'pequeño', 'omnivoro', 152, 0.18),
        ('Papamoscas', 'Zacanemitl', 'salvaje', 'ninguna', 35, 'Papamoscas cazador', 'pequeño', 'insectivoro', 170, 0.25),
        ('Golondrina', 'Cuicuitzcatl', 'salvaje', 'ninguna', 30, 'Golondrina migratoria', 'pequeño', 'insectivoro', 190, 0.3),
        ('Vencejo', 'Tzihuactli', 'salvaje', 'ninguna', 28, 'Vencejo veloz', 'pequeño', 'insectivoro', 210, 0.28),
        ('Picamaderos', 'Cuauhchochopilin', 'salvaje', 'ninguna', 75, 'Pájaro carpintero', 'pequeño', 'insectivoro', 120, 0.2),
        ('Carpintero Bellotero', 'Cuauhchochopilin Cacahuatl', 'salvaje', 'ninguna', 70, 'Carpintero almacenador', 'pequeño', 'omnivoro', 125, 0.18),
        ('Trepador Azul', 'Tapacholin Xiuhtli', 'salvaje', 'ninguna', 40, 'Trepa troncos cabeza abajo', 'pequeño', 'insectivoro', 110, 0.22),
        ('Pinzón', 'Totopiltzin', 'salvaje', 'ninguna', 32, 'Pinzón cantor', 'pequeño', 'granivoro', 128, 0.28),
        ('Verderón', 'Quiltoton', 'salvaje', 'ninguna', 38, 'Verderón verde', 'pequeño', 'granivoro', 132, 0.24),
        ('Chipe', 'Tzihuacton', 'salvaje', 'ninguna', 42, 'Chipe amarillo', 'pequeño', 'insectivoro', 138, 0.26),
        ('Vireo', 'Tocuayo', 'salvaje', 'ninguna', 36, 'Vireo ojos rojos', 'pequeño', 'insectivoro', 135, 0.25),
        ('Pato Buceador', 'Canauhtli Atemoani', 'salvaje', 'ninguna', 48, 'Pato que se sumerge', 'mediano', 'omnivoro', 140, 0.15),
        ('Cerceta', 'Canauhtli Tzontli', 'salvaje', 'ninguna', 40, 'Pato pequeño', 'pequeño', 'omnivoro', 160, 0.2),
        ('Avoceta', 'Achalalatzin', 'salvaje', 'ninguna', 90, 'Ave zancuda de pico curvo', 'mediano', 'omnivoro', 155, 0.1),
        ('Cigüeña', 'Quetzalcanauhtli', 'salvaje', 'ninguna', 250, 'Cigüeña zancuda', 'grande', 'carnivoro', 145, 0.05),
        ('Grulla', 'Azacanauhtli', 'salvaje', 'ninguna', 280, 'Grulla gris', 'grande', 'omnivoro', 150, 0.04),
        ('Avestruz', 'Tototl Huey', 'salvaje', 'alta', 1000, 'Ave gigante que no vuela', 'gigante', 'omnivoro', 280, 0.005),
        ('Emú', 'Tototl Huey Tlilli', 'salvaje', 'media', 800, 'Ave grande australiana', 'grande', 'omnivoro', 250, 0.003),
        ('Casuario', 'Tototl Huey Yaoquizqui', 'salvaje', 'extrema', 1500, 'Ave peligrosa con casco', 'grande', 'frugivoro', 230, 0.001),
        ('Kiwi', 'Tototl Yohualli', 'salvaje', 'ninguna', 600, 'Ave pequeña nocturna', 'pequeño', 'omnivoro', 40, 0.01),
        ('Trogon', 'Xiuhtototl Quetzalli', 'salvaje', 'ninguna', 150, 'Trogon cola larga', 'mediano', 'frugivoro', 130, 0.08),
        ('Momoto', 'Tototl Tzapotl', 'salvaje', 'ninguna', 120, 'Momoto ceja azul', 'mediano', 'omnivoro', 125, 0.12),
        ('Tucán', 'Quetzaltototl Tentli', 'salvaje', 'ninguna', 400, 'Tucán pico grande', 'mediano', 'frugivoro', 110, 0.06),
        ('Tucaneta', 'Quetzaltototl Tentli Tzontli', 'salvaje', 'ninguna', 250, 'Tucaneta verde', 'pequeño', 'frugivoro', 120, 0.09),
        ('Jacamar', 'Tototl Teocuitlatl', 'salvaje', 'ninguna', 80, 'Jacamar dorado', 'pequeño', 'insectivoro', 140, 0.11),
        ('Tángara', 'Xopantototl', 'salvaje', 'ninguna', 70, 'Tángara colorida', 'pequeño', 'frugivoro', 135, 0.15),
        ('Eufonia', 'Tototl Xiuhtli', 'salvaje', 'ninguna', 65, 'Eufonia gorriazul', 'pequeño', 'frugivoro', 130, 0.16),
    ])

    # ================================================================
    # REPTILES (60 especies)
    # ================================================================

    # Serpientes (25)
    fauna.extend([
        ('Serpiente de Cascabel', 'Coatl Ayauhcalli', 'salvaje', 'extrema', 150, 'Víbora de cascabel venenosa', 'mediano', 'carnivoro', 90, 0.15),
        ('Serpiente de Coral', 'Coatl Tlapalli', 'salvaje', 'extrema', 200, 'Serpiente coral muy venenosa', 'pequeño', 'carnivoro', 80, 0.08),
        ('Boa Constrictor', 'Coatl Tzitzquilo', 'salvaje', 'alta', 300, 'Boa constrictora gigante', 'grande', 'carnivoro', 70, 0.1),
        ('Anaconda', 'Coatl Atl Huey', 'salvaje', 'extrema', 800, 'Anaconda gigante acuática', 'gigante', 'carnivoro', 100, 0.02),
        ('Pitón', 'Coatl Huey', 'salvaje', 'alta', 500, 'Pitón constrictora', 'grande', 'carnivoro', 75, 0.05),
        ('Serpiente Rey', 'Coatl Tlatoani', 'salvaje', 'media', 120, 'Serpiente comedora de serpientes', 'mediano', 'carnivoro', 95, 0.12),
        ('Culebra de Agua', 'Coatl Atl', 'salvaje', 'baja', 50, 'Culebra nadadora', 'mediano', 'piscivoro', 110, 0.2),
        ('Culebra Ratonera', 'Coatl Quimichin', 'salvaje', 'ninguna', 40, 'Culebra cazadora de roedores', 'mediano', 'carnivoro', 100, 0.25),
        ('Serpiente de Jarretera', 'Coatl Milli', 'salvaje', 'ninguna', 30, 'Culebra de jardín', 'pequeño', 'carnivoro', 90, 0.3),
        ('Serpiente de Tierra', 'Coatl Tlalli', 'salvaje', 'ninguna', 25, 'Culebra excavadora', 'pequeño', 'insectivoro', 60, 0.28),
        ('Coralillo Falso', 'Coatl Tlapalli Nelli', 'salvaje', 'baja', 45, 'Imitador de coral', 'pequeño', 'carnivoro', 85, 0.18),
        ('Serpiente Verde', 'Coatl Quiltic', 'salvaje', 'ninguna', 35, 'Serpiente verde de árbol', 'pequeño', 'insectivoro', 105, 0.22),
        ('Serpiente Látigo', 'Coatl Mecatl', 'salvaje', 'baja', 60, 'Serpiente veloz y delgada', 'mediano', 'carnivoro', 180, 0.15),
        ('Mazacuate', 'Mazacoatl', 'salvaje', 'alta', 250, 'Boa centroamericana', 'grande', 'carnivoro', 70, 0.08),
        ('Cantil', 'Coatl Yollotl', 'salvaje', 'extrema', 180, 'Víbora altamente venenosa', 'mediano', 'carnivoro', 75, 0.1),
        ('Nauyaca', 'Nauhyacatl', 'salvaje', 'extrema', 160, 'Terciopelo venenosa', 'mediano', 'carnivoro', 80, 0.12),
        ('Coralillo Arlequín', 'Coatl Tlapalli Quetzalli', 'salvaje', 'extrema', 220, 'Coral de anillos', 'pequeño', 'carnivoro', 70, 0.06),
        ('Bejuquilla', 'Coatl Quilitl', 'salvaje', 'baja', 55, 'Serpiente de vid', 'pequeño', 'insectivoro', 95, 0.16),
        ('Serpiente Nocturna', 'Coatl Yohualli', 'salvaje', 'baja', 48, 'Serpiente de hábitos nocturnos', 'pequeño', 'carnivoro', 88, 0.19),
        ('Serpiente del Maíz', 'Coatl Tlaolli', 'salvaje', 'ninguna', 65, 'Serpiente bella de granja', 'mediano', 'carnivoro', 92, 0.14),
        ('Serpiente de Leche', 'Coatl Chichihualatl', 'salvaje', 'ninguna', 70, 'Serpiente con bandas', 'mediano', 'carnivoro', 94, 0.13),
        ('Víbora de Pestañas', 'Coatl Ixtelolotli', 'salvaje', 'alta', 190, 'Víbora arborícola venenosa', 'pequeño', 'carnivoro', 68, 0.07),
        ('Serpiente de Pino', 'Coatl Ocotl', 'salvaje', 'ninguna', 52, 'Serpiente de bosque', 'mediano', 'carnivoro', 87, 0.17),
        ('Serpiente de Hocico de Cerdo', 'Coatl Pitzotl Tentli', 'salvaje', 'ninguna', 58, 'Serpiente excavadora', 'mediano', 'carnivoro', 65, 0.15),
        ('Serpiente Costera', 'Coatl Teoatl', 'salvaje', 'media', 85, 'Serpiente marina ocasional', 'mediano', 'piscivoro', 115, 0.08),
    ])

    # Lagartos (20)
    fauna.extend([
        ('Iguana Verde', 'Cuetzpalin Quiltic', 'salvaje', 'baja', 100, 'Iguana herbívora grande', 'grande', 'herbivoro', 90, 0.15),
        ('Iguana Negra', 'Cuetzpalin Tliltic', 'salvaje', 'baja', 90, 'Iguana oscura', 'grande', 'omnivoro', 85, 0.14),
        ('Iguana del Desierto', 'Cuetzpalin Iztac', 'salvaje', 'baja', 80, 'Iguana de zonas áridas', 'mediano', 'herbivoro', 95, 0.12),
        ('Lagarto Espinoso', 'Cuetzpalin Huitztic', 'salvaje', 'baja', 40, 'Lagarto con espinas', 'pequeño', 'insectivoro', 70, 0.22),
        ('Lagarto de Collar', 'Cuetzpalin Cozcatl', 'salvaje', 'ninguna', 35, 'Lagarto con collar negro', 'pequeño', 'insectivoro', 110, 0.25),
        ('Lagartija de Cerca', 'Cuetzpalin Calli', 'salvaje', 'ninguna', 15, 'Lagartija común', 'pequeño', 'insectivoro', 120, 0.5),
        ('Lagarto Cornudo', 'Cuetzpalin Cuacuauhtli', 'salvaje', 'baja', 50, 'Lagarto con cuernos', 'pequeño', 'insectivoro', 60, 0.18),
        ('Basilisco', 'Cuetzpalin Atl Nemini', 'salvaje', 'baja', 120, 'Lagarto que corre sobre agua', 'mediano', 'omnivoro', 150, 0.1),
        ('Monstruo de Gila', 'Cuetzpalin Eztli', 'salvaje', 'alta', 300, 'Lagarto venenoso', 'grande', 'carnivoro', 50, 0.04),
        ('Lagarto Escorpión', 'Cuetzpalin Colotl', 'salvaje', 'media', 80, 'Lagarto de cola gruesa', 'mediano', 'insectivoro', 75, 0.13),
        ('Camaleón', 'Cuetzpalin Tlapalli', 'salvaje', 'ninguna', 150, 'Lagarto que cambia de color', 'pequeño', 'insectivoro', 40, 0.08),
        ('Gecko', 'Cuetzpalin Yohualli', 'salvaje', 'ninguna', 25, 'Lagartija nocturna', 'pequeño', 'insectivoro', 100, 0.35),
        ('Anolis', 'Cuetzpalin Cuauhtzin', 'salvaje', 'ninguna', 20, 'Lagartija de árboles', 'pequeño', 'insectivoro', 115, 0.4),
        ('Eslizón', 'Cuetzpalin Lipan', 'salvaje', 'ninguna', 30, 'Lagarto brillante', 'pequeño', 'insectivoro', 105, 0.28),
        ('Lagarto Alicante', 'Cuetzpalin Atemoyotl', 'salvaje', 'ninguna', 28, 'Lagarto de arena', 'pequeño', 'insectivoro', 125, 0.24),
        ('Monitor', 'Cuetzpalin Huey', 'salvaje', 'alta', 600, 'Lagarto gigante', 'gigante', 'carnivoro', 110, 0.02),
        ('Dragón de Komodo', 'Cuetzpalin Tlamacazqui', 'salvaje', 'extrema', 2000, 'Lagarto gigante venenoso', 'gigante', 'carnivoro', 80, 0.001),
        ('Lagarto de Cristal', 'Cuetzpalin Tezcatl', 'salvaje', 'ninguna', 45, 'Lagarto sin patas', 'pequeño', 'insectivoro', 85, 0.16),
        ('Lagarto Ajolote', 'Cuetzpalin Atl', 'salvaje', 'ninguna', 55, 'Lagarto semi-acuático', 'pequeño', 'carnivoro', 90, 0.14),
        ('Tuátara', 'Cuetzpalin Huehuetl', 'salvaje', 'ninguna', 500, 'Reptil primitivo', 'mediano', 'carnivoro', 70, 0.005),
    ])

    # Tortugas y cocodrilos (15)
    fauna.extend([
        ('Tortuga del Desierto', 'Ayotl Iztac', 'salvaje', 'ninguna', 200, 'Tortuga terrestre', 'mediano', 'herbivoro', 20, 0.08),
        ('Tortuga de Caja', 'Ayotl Petlacalli', 'salvaje', 'ninguna', 150, 'Tortuga con caparazón móvil', 'pequeño', 'omnivoro', 30, 0.12),
        ('Tortuga de Agua Dulce', 'Ayotl Atl', 'salvaje', 'ninguna', 80, 'Tortuga de río', 'mediano', 'omnivoro', 60, 0.2),
        ('Tortuga Lagarto', 'Ayotl Cuetzpalin', 'salvaje', 'alta', 250, 'Tortuga mordedora', 'grande', 'carnivoro', 70, 0.06),
        ('Tortuga de Orejas Rojas', 'Ayotl Nacatl', 'salvaje', 'ninguna', 60, 'Tortuga ornamental', 'pequeño', 'omnivoro', 65, 0.18),
        ('Tortuga Verde Marina', 'Ayotl Teoatl Quiltic', 'salvaje', 'ninguna', 500, 'Tortuga marina gigante', 'gigante', 'herbivoro', 50, 0.03),
        ('Tortuga Carey', 'Ayotl Quetzalli', 'salvaje', 'ninguna', 800, 'Tortuga de concha preciosa', 'grande', 'omnivoro', 55, 0.02),
        ('Tortuga Laúd', 'Ayotl Teoatl Huey', 'salvaje', 'ninguna', 1500, 'Tortuga marina más grande', 'gigante', 'omnivoro', 40, 0.01),
        ('Tortuga Galápagos', 'Ayotl Tlalhuaztli', 'salvaje', 'ninguna', 2000, 'Tortuga terrestre gigante', 'gigante', 'herbivoro', 15, 0.005),
        ('Cocodrilo Americano', 'Acuetzpalin', 'salvaje', 'extrema', 1000, 'Cocodrilo de río', 'gigante', 'carnivoro', 90, 0.04),
        ('Caimán', 'Acuetzpalin Tzontli', 'salvaje', 'alta', 600, 'Caimán de agua dulce', 'grande', 'carnivoro', 85, 0.08),
        ('Cocodrilo de Pantano', 'Acuetzpalin Atexcatl', 'salvaje', 'extrema', 800, 'Cocodrilo de Morelet', 'grande', 'carnivoro', 80, 0.05),
        ('Aligator', 'Acuetzpalin Iztac', 'salvaje', 'extrema', 900, 'Aligator americano', 'gigante', 'carnivoro', 95, 0.03),
        ('Cocodrilo Marino', 'Acuetzpalin Teoatl', 'salvaje', 'legendaria', 3000, 'Cocodrilo de mar gigante', 'gigante', 'carnivoro', 100, 0.001),
        ('Gavial', 'Acuetzpalin Tentli', 'salvaje', 'alta', 1200, 'Cocodrilo de hocico fino', 'gigante', 'piscivoro', 75, 0.01),
    ])

    # ================================================================
    # ANFIBIOS (15 especies)
    # ================================================================
    fauna.extend([
        ('Ajolote', 'Axolotl', 'salvaje', 'ninguna', 150, 'Salamandra acuática regenerativa', 'pequeño', 'carnivoro', 50, 0.15),
        ('Ajolote de Montaña', 'Axolotl Tepetl', 'salvaje', 'ninguna', 180, 'Ajolote de altura', 'pequeño', 'carnivoro', 45, 0.08),
        ('Salamandra', 'Axolotl Tlalli', 'salvaje', 'ninguna', 40, 'Salamandra terrestre', 'pequeño', 'insectivoro', 60, 0.2),
        ('Tritón', 'Atexolotl', 'salvaje', 'ninguna', 50, 'Tritón de cresta', 'pequeño', 'carnivoro', 55, 0.18),
        ('Rana Toro', 'Tamazolin Huey', 'salvaje', 'ninguna', 30, 'Rana grande', 'mediano', 'carnivoro', 80, 0.25),
        ('Rana Verde', 'Tamazolin Quiltic', 'salvaje', 'ninguna', 15, 'Rana común', 'pequeño', 'insectivoro', 90, 0.4),
        ('Rana Arbórea', 'Tamazolin Cuauhtla', 'salvaje', 'ninguna', 20, 'Rana de árbol', 'pequeño', 'insectivoro', 70, 0.35),
        ('Rana Dorada Venenosa', 'Tamazolin Teocuitlatl', 'salvaje', 'extrema', 500, 'Rana muy venenosa', 'pequeño', 'insectivoro', 65, 0.01),
        ('Rana de Cristal', 'Tamazolin Tezcatl', 'salvaje', 'ninguna', 100, 'Rana transparente', 'pequeño', 'insectivoro', 60, 0.08),
        ('Sapo', 'Tamazolin Tlazoyotl', 'salvaje', 'ninguna', 12, 'Sapo común', 'pequeño', 'insectivoro', 50, 0.45),
        ('Sapo de Caña', 'Tamazolin Acatl', 'salvaje', 'baja', 18, 'Sapo gigante invasor', 'mediano', 'omnivoro', 55, 0.3),
        ('Sapo del Desierto', 'Tamazolin Iztac', 'salvaje', 'ninguna', 25, 'Sapo que almacena agua', 'pequeño', 'insectivoro', 40, 0.15),
        ('Cecilia', 'Coatl Ayotl', 'salvaje', 'ninguna', 60, 'Anfibio sin patas', 'pequeño', 'insectivoro', 30, 0.12),
        ('Rana Leopardo', 'Tamazolin Ocelotl', 'salvaje', 'ninguna', 22, 'Rana con manchas', 'pequeño', 'insectivoro', 85, 0.28),
        ('Rana de Ojos Rojos', 'Tamazolin Chichiltic', 'salvaje', 'ninguna', 80, 'Rana de ojos brillantes', 'pequeño', 'insectivoro', 75, 0.14),
    ])

    # ================================================================
    # PECES (30 especies)
    # ================================================================
    fauna.extend([
        ('Pez Común', 'Michin', 'salvaje', 'ninguna', 5, 'Pez de río básico', 'pequeño', 'omnivoro', 100, 0.7),
        ('Trucha', 'Michin Iztac', 'salvaje', 'ninguna', 40, 'Trucha de río', 'mediano', 'carnivoro', 140, 0.15),
        ('Salmón', 'Michin Tlatlauhqui', 'salvaje', 'ninguna', 80, 'Salmón migratorio', 'grande', 'carnivoro', 160, 0.08),
        ('Bagre', 'Michin Tentli', 'salvaje', 'ninguna', 30, 'Bagre de río', 'mediano', 'omnivoro', 90, 0.25),
        ('Mojarra', 'Michin Tepetl', 'salvaje', 'ninguna', 15, 'Mojarra común', 'pequeño', 'omnivoro', 110, 0.4),
        ('Carpa', 'Michin Huey', 'salvaje', 'ninguna', 50, 'Carpa grande', 'grande', 'omnivoro', 80, 0.2),
        ('Tilapia', 'Michin Atl', 'salvaje', 'ninguna', 25, 'Tilapia de agua dulce', 'mediano', 'herbivoro', 95, 0.3),
        ('Perca', 'Michin Yaoquizqui', 'salvaje', 'ninguna', 35, 'Perca depredadora', 'mediano', 'carnivoro', 120, 0.18),
        ('Lucio', 'Michin Mecatl', 'salvaje', 'media', 120, 'Lucio cazador', 'grande', 'carnivoro', 180, 0.08),
        ('Pez Gato', 'Michin Miztli', 'salvaje', 'ninguna', 45, 'Pez gato barbudo', 'mediano', 'omnivoro', 85, 0.22),
        ('Pez Dorado', 'Michin Teocuitlatl', 'domestico', 'ninguna', 20, 'Pez ornamental', 'pequeño', 'omnivoro', 70, 0.35),
        ('Koi', 'Michin Quetzalli', 'domestico', 'ninguna', 200, 'Carpa ornamental', 'grande', 'omnivoro', 75, 0.05),
        ('Pez Espada', 'Michin Maquahuitl', 'salvaje', 'alta', 500, 'Pez con espada', 'gigante', 'carnivoro', 220, 0.02),
        ('Marlín', 'Michin Tliltic Huey', 'salvaje', 'alta', 600, 'Marlín oceánico', 'gigante', 'carnivoro', 240, 0.01),
        ('Atún', 'Michin Teoatl', 'salvaje', 'ninguna', 150, 'Atún migratorio', 'grande', 'carnivoro', 200, 0.1),
        ('Tiburón', 'Michin Yaoyotl', 'salvaje', 'extrema', 1000, 'Tiburón depredador', 'gigante', 'carnivoro', 150, 0.03),
        ('Tiburón Ballena', 'Michin Huey Tlalli', 'salvaje', 'baja', 5000, 'Tiburón gigante filtrador', 'gigante', 'planctivoro', 60, 0.001),
        ('Raya', 'Michin Patlachtic', 'salvaje', 'media', 200, 'Raya de río', 'grande', 'carnivoro', 80, 0.08),
        ('Mantarraya', 'Michin Patlachtic Huey', 'salvaje', 'baja', 800, 'Mantarraya gigante', 'gigante', 'planctivoro', 100, 0.01),
        ('Pez Globo', 'Michin Pochtic', 'salvaje', 'alta', 180, 'Pez que se infla venenoso', 'pequeño', 'omnivoro', 50, 0.06),
        ('Pez Payaso', 'Michin Tlapalli', 'salvaje', 'ninguna', 60, 'Pez de anémona', 'pequeño', 'omnivoro', 90, 0.12),
        ('Pez Ángel', 'Michin Teotl', 'salvaje', 'ninguna', 100, 'Pez ornamental marino', 'pequeño', 'omnivoro', 85, 0.08),
        ('Pez Cirujano', 'Michin Texoctli', 'salvaje', 'baja', 90, 'Pez con espina venenosa', 'pequeño', 'herbivoro', 95, 0.1),
        ('Pez León', 'Michin Huitztic', 'salvaje', 'alta', 150, 'Pez venenoso espinoso', 'mediano', 'carnivoro', 60, 0.04),
        ('Anguila', 'Michin Coatl', 'salvaje', 'media', 70, 'Anguila de río', 'mediano', 'carnivoro', 100, 0.15),
        ('Anguila Eléctrica', 'Michin Coatl Tlachinolli', 'salvaje', 'alta', 300, 'Anguila que da descargas', 'grande', 'carnivoro', 80, 0.02),
        ('Piraña', 'Michin Eztli', 'salvaje', 'extrema', 40, 'Piraña en cardumen', 'pequeño', 'carnivoro', 130, 0.18),
        ('Pez Espina', 'Michin Huitzoctli', 'salvaje', 'ninguna', 18, 'Pez pequeño espinoso', 'pequeño', 'insectivoro', 105, 0.3),
        ('Esturión', 'Michin Huehuetl', 'salvaje', 'ninguna', 400, 'Esturión antiguo', 'gigante', 'omnivoro', 70, 0.03),
        ('Pez Guppy', 'Michin Xochitl', 'salvaje', 'ninguna', 8, 'Pez pequeño colorido', 'pequeño', 'omnivoro', 80, 0.5),
    ])

    # ================================================================
    # INVERTEBRADOS E INSECTOS (30 especies)
    # ================================================================
    fauna.extend([
        ('Mariposa Monarca', 'Papalotl Tlatoani', 'salvaje', 'ninguna', 50, 'Mariposa migratoria naranja', 'pequeño', 'nectarivoro', 40, 0.3),
        ('Mariposa Morfo Azul', 'Papalotl Xiuhtli', 'salvaje', 'ninguna', 80, 'Mariposa azul brillante', 'pequeño', 'nectarivoro', 45, 0.12),
        ('Escarabajo', 'Tecolin', 'salvaje', 'ninguna', 10, 'Escarabajo común', 'pequeño', 'omnivoro', 30, 0.6),
        ('Escarabajo Rinoceronte', 'Tecolin Cuacuauhtli', 'salvaje', 'ninguna', 25, 'Escarabajo con cuerno', 'pequeño', 'herbivoro', 35, 0.2),
        ('Escarabajo Hércules', 'Tecolin Tlamacazqui', 'salvaje', 'ninguna', 60, 'Escarabajo gigante', 'pequeño', 'herbivoro', 32, 0.08),
        ('Luciérnaga', 'Copitl', 'salvaje', 'ninguna', 15, 'Insecto luminoso', 'pequeño', 'omnivoro', 25, 0.35),
        ('Abeja', 'Xicotl', 'salvaje', 'baja', 20, 'Abeja productora de miel', 'pequeño', 'nectarivoro', 60, 0.4),
        ('Avispa', 'Tocatl', 'salvaje', 'media', 18, 'Avispa agresiva', 'pequeño', 'carnivoro', 70, 0.3),
        ('Hormiga', 'Azcatl', 'salvaje', 'ninguna', 2, 'Hormiga trabajadora', 'pequeño', 'omnivoro', 50, 0.8),
        ('Hormiga Arriera', 'Azcatl Milli', 'salvaje', 'ninguna', 3, 'Hormiga cortadora de hojas', 'pequeño', 'herbivoro', 55, 0.7),
        ('Termita', 'Polcatetl', 'salvaje', 'baja', 5, 'Termita comedora de madera', 'pequeño', 'herbivoro', 40, 0.6),
        ('Libélula', 'Anahuametl', 'salvaje', 'ninguna', 12, 'Libélula voladora', 'pequeño', 'carnivoro', 120, 0.35),
        ('Mantis Religiosa', 'Pipiyolin', 'salvaje', 'baja', 30, 'Mantis cazadora', 'pequeño', 'carnivoro', 50, 0.18),
        ('Grillo', 'Chapolin Yohualli', 'salvaje', 'ninguna', 8, 'Grillo cantor', 'pequeño', 'omnivoro', 80, 0.5),
        ('Saltamontes', 'Chapolin', 'salvaje', 'ninguna', 10, 'Saltamontes', 'pequeño', 'herbivoro', 100, 0.45),
        ('Cigarr', 'Tzitzicaztli', 'salvaje', 'ninguna', 6, 'Cigarra ruidosa', 'pequeño', 'herbivoro', 60, 0.4),
        ('Mosca', 'Zayolin', 'salvaje', 'ninguna', 1, 'Mosca común', 'pequeño', 'omnivoro', 110, 0.9),
        ('Mosquito', 'Moyotl', 'salvaje', 'media', 2, 'Mosquito bebedor de sangre', 'pequeño', 'hematofago', 90, 0.85),
        ('Araña Tarántula', 'Tocatl Huey', 'salvaje', 'alta', 100, 'Tarántula grande', 'pequeño', 'carnivoro', 70, 0.12),
        ('Araña Viuda Negra', 'Tocatl Tliltic', 'salvaje', 'extrema', 150, 'Araña muy venenosa', 'pequeño', 'carnivoro', 65, 0.08),
        ('Araña de Jardín', 'Tocatl Xochitl', 'salvaje', 'baja', 20, 'Araña tejedora', 'pequeño', 'carnivoro', 60, 0.35),
        ('Escorpión', 'Colotl', 'salvaje', 'alta', 80, 'Escorpión venenoso', 'pequeño', 'carnivoro', 75, 0.15),
        ('Ciempiés', 'Petlachilli', 'salvaje', 'media', 40, 'Ciempiés venenoso', 'pequeño', 'carnivoro', 85, 0.25),
        ('Milpiés', 'Petlachihueyac', 'salvaje', 'ninguna', 15, 'Milpiés herbívoro', 'pequeño', 'herbivoro', 40, 0.35),
        ('Caracol', 'Tecciztli', 'salvaje', 'ninguna', 12, 'Caracol lento', 'pequeño', 'herbivoro', 5, 0.4),
        ('Babosa', 'Tecciztli Aquen', 'salvaje', 'ninguna', 8, 'Babosa sin concha', 'pequeño', 'herbivoro', 8, 0.45),
        ('Lombriz', 'Ocuilin', 'salvaje', 'ninguna', 3, 'Lombriz de tierra', 'pequeño', 'detrivoro', 15, 0.7),
        ('Sanguijuela', 'Eztlacoliuhqui', 'salvaje', 'baja', 18, 'Sanguijuela chupadora', 'pequeño', 'hematofago', 20, 0.3),
        ('Cangrejo', 'Tecuicitl', 'salvaje', 'baja', 35, 'Cangrejo de río', 'pequeño', 'omnivoro', 60, 0.25),
        ('Langosta', 'Acocil', 'salvaje', 'ninguna', 50, 'Langosta de agua dulce', 'pequeño', 'omnivoro', 70, 0.2),
    ])

    return fauna

def main():
    """Función principal"""
    print("=" * 70)
    print("GENERANDO 300+ ESPECIES DE FAUNA")
    print("Portales del Quinto Sol")
    print("=" * 70)

    # Generar todas las especies
    print("\n📊 Generando especies...")
    fauna = generar_fauna_completa()

    print(f"✅ {len(fauna)} especies generadas")

    # Insertar en BD
    print("\n💾 Insertando en base de datos...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Limpiar tabla existente
    cursor.execute("DELETE FROM especies_animales")

    for animal in fauna:
        nombre, nahuatl, categoria, peligrosidad, valor, desc, tamano, dieta, velocidad, rareza = animal

        # Generar habilidades y biomas según categoría
        habilidades = json.dumps([])
        biomas = json.dumps(['bosque', 'campo'])

        if 'acua' in nombre.lower() or 'agua' in desc.lower() or 'pez' in nombre.lower() or 'pato' in nombre.lower():
            biomas = json.dumps(['agua', 'rio', 'lago'])
        elif 'desierto' in nombre.lower():
            biomas = json.dumps(['desierto'])
        elif 'montana' in desc.lower() or 'altura' in desc.lower():
            biomas = json.dumps(['montana', 'bosque'])
        elif categoria == 'domestico':
            biomas = json.dumps(['ciudad', 'pueblo', 'campo'])

        cursor.execute("""
            INSERT INTO especies_animales (
                nombre_comun, nombre_nahuatl, categoria, peligrosidad, valor_mercado,
                descripcion, tamaño, dieta, velocidad,
                habilidades_especiales, biomas_preferidos, rareza,
                es_vendible, es_capturable, nivel_min_captura
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 1, 1)
        """, (nombre, nahuatl, categoria, peligrosidad, valor, desc, tamano, dieta, velocidad, habilidades, biomas, rareza))

    conn.commit()

    # Mostrar resumen
    print("\n" + "=" * 70)
    print("✅ FAUNA COMPLETA GENERADA")
    print("=" * 70)

    cursor.execute("SELECT categoria, COUNT(*) FROM especies_animales GROUP BY categoria")
    for cat, count in cursor.fetchall():
        print(f"   {cat.upper()}: {count} especies")

    cursor.execute("SELECT COUNT(*) FROM especies_animales")
    total = cursor.fetchone()[0]
    print(f"\n📊 TOTAL: {total} especies animales")

    conn.close()

if __name__ == '__main__':
    main()
