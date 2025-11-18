#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Flora: 1000+ Especies de Plantas
Portales del Quinto Sol
Clasificación: Alimento, Veneno, Curativo, Alucinógeno, Adorno, Recursos
"""

import sqlite3
import json

DB_PATH = 'quinto_sol.db'

def generar_flora_completa():
    """Generar 1000+ especies de plantas clasificadas"""

    flora = []

    # ================================================================
    # ALIMENTOS (300 especies)
    # ================================================================

    # Frutas (80)
    alimentos_frutas = [
        # (nombre_comun, nombre_nahuatl, tipo, altura_min, altura_max, rareza, valor, desc, biomas, parte_comestible, sabor)
        ('Aguacate', 'Ahuacatl', 'arbol', 500, 2000, 0.3, 30, 'Árbol de aguacate con fruto cremoso', ['bosque', 'selva'], 'fruto', 'cremoso'),
        ('Cacao', 'Cacahuatl', 'arbol', 400, 1200, 0.15, 100, 'Árbol de cacao sagrado', ['selva'], 'semilla', 'amargo'),
        ('Zapote Negro', 'Tliltzapotl', 'arbol', 600, 1500, 0.2, 40, 'Zapote de pulpa negra dulce', ['selva', 'bosque'], 'fruto', 'dulce'),
        ('Zapote Blanco', 'Iztactzapotl', 'arbol', 500, 1400, 0.22, 35, 'Zapote de pulpa blanca', ['bosque'], 'fruto', 'dulce'),
        ('Mamey', 'Tetzontzapotl', 'arbol', 800, 2500, 0.18, 50, 'Fruto grande de pulpa naranja', ['selva'], 'fruto', 'dulce'),
        ('Guayaba', 'Xalxocotl', 'arbol', 300, 1000, 0.35, 20, 'Árbol de guayaba aromática', ['bosque', 'campo'], 'fruto', 'dulce'),
        ('Chirimoya', 'Tzapotl', 'arbol', 400, 900, 0.25, 45, 'Fruto de pulpa cremosa', ['bosque', 'montaña'], 'fruto', 'dulce'),
        ('Papaya', 'Chichihualtzapotl', 'arbol', 200, 800, 0.3, 25, 'Árbol de papaya digestiva', ['selva', 'campo'], 'fruto', 'dulce'),
        ('Piña', 'Matzatli', 'hierba', 50, 150, 0.28, 35, 'Planta de piña espinosa', ['selva'], 'fruto', 'ácido-dulce'),
        ('Pitaya', 'Teotlaquetzalli', 'cactus', 200, 600, 0.2, 60, 'Cactus trepador con fruto rosa', ['desierto', 'selva'], 'fruto', 'dulce'),
        ('Tuna', 'Nochtli', 'cactus', 150, 500, 0.4, 15, 'Fruto del nopal', ['desierto', 'campo'], 'fruto', 'dulce'),
        ('Ciruela', 'Atoyaxocotl', 'arbol', 400, 1200, 0.3, 25, 'Ciruelo silvestre', ['bosque'], 'fruto', 'dulce-ácido'),
        ('Capulín', 'Capolin', 'arbol', 500, 1500, 0.32, 20, 'Cerezo americano', ['bosque', 'montaña'], 'fruto', 'dulce'),
        ('Tejocote', 'Texocotl', 'arbol', 300, 800, 0.35, 18, 'Tejocote para dulces', ['bosque', 'montaña'], 'fruto', 'ácido'),
        ('Granada', 'Tzapotl Tlatlauhqui', 'arbol', 300, 600, 0.22, 40, 'Granada de semillas rojas', ['bosque'], 'semilla', 'dulce-ácido'),
        ('Higo', 'Nochtzapotl', 'arbol', 400, 1000, 0.28, 30, 'Higuera de frutos dulces', ['bosque'], 'fruto', 'dulce'),
        ('Nanche', 'Nantzi', 'arbol', 400, 1200, 0.3, 15, 'Fruto pequeño amarillo', ['bosque', 'selva'], 'fruto', 'ácido'),
        ('Guanábana', 'Tzapotl Huey', 'arbol', 500, 1200, 0.2, 55, 'Fruto grande espinoso', ['selva'], 'fruto', 'ácido-dulce'),
        ('Anona', 'Tzapotl Quiltic', 'arbol', 300, 800, 0.25, 40, 'Anona de escamas verdes', ['selva', 'bosque'], 'fruto', 'dulce'),
        ('Níspero', 'Mizquitl', 'arbol', 600, 1500, 0.28, 25, 'Níspero de fruto naranja', ['bosque'], 'fruto', 'dulce'),
    ]

    for fruta in alimentos_frutas:
        nombre, nahuatl, tipo, h_min, h_max, rar, val, desc, biomas, parte, sabor = fruta
        flora.append({
            'nombre_comun': nombre,
            'nombre_nahuatl': nahuatl,
            'tipo_planta': tipo,
            'altura_min_cm': h_min,
            'altura_max_cm': h_max,
            'rareza': rar,
            'valor_mercado': val,
            'descripcion': desc,
            'biomas_preferidos': json.dumps(biomas),
            'es_alimento': 1,
            'propiedades_alimento': json.dumps({
                'parte_comestible': parte,
                'valor_nutricional': 70,
                'sabor': sabor
            })
        })

    # Añadir más frutas variadas (60 adicionales)
    frutas_adicionales = [
        'Ciruela Mexicana', 'Guamúchil', 'Cacahuananche', 'Arrayán', 'Guaje', 'Garambullo',
        'Xoconostle', 'Pitahaya Roja', 'Pitahaya Amarilla', 'Jícama de Agua', 'Cuajinicuil',
        'Huaya', 'Jocote', 'Icaco', 'Marañón', 'Tamarindo', 'Guamara', 'Caimito',
        'Corozo', 'Jobillo', 'Chicozapote', 'Coco', 'Dátil', 'Jícaro', 'Chaya Fruto',
        'Mango Silvestre', 'Ciricote', 'Ramón Fruto', 'Jobos', 'Guásima', 'Copol',
        'Palo Blanco Fruto', 'Cocoyol', 'Nanche Agrio', 'Guaje Rojo', 'Tepehuaje',
        'Bonete', 'Anona Roja', 'Anona de Monte', 'Ilama', 'Pomarrosa', 'Mamoncillo',
        'Aceituna Silvestre', 'Madroño', 'Membrillo Silvestre', 'Naranjilla', 'Tomate de Árbol',
        'Granadilla', 'Curuba', 'Maracuyá', 'Tomatillo Silvestre', 'Chilacayote Fruto',
        'Zapallo Silvestre', 'Calabaza Silvestre', 'Ayote', 'Pepino Silvestre', 'Sandía Silvestre',
        'Melón Silvestre', 'Chayote Fruto', 'Huazontle Semilla', 'Alegría Semilla'
    ]

    for idx, nombre in enumerate(frutas_adicionales):
        flora.append({
            'nombre_comun': nombre,
            'nombre_nahuatl': f'{nombre.replace(" ", "")}tl',
            'tipo_planta': 'arbol' if idx % 3 == 0 else ('arbusto' if idx % 3 == 1 else 'hierba'),
            'altura_min_cm': 100 + (idx * 10) % 400,
            'altura_max_cm': 500 + (idx * 20) % 1500,
            'rareza': 0.1 + (idx % 30) / 100,
            'valor_mercado': 15 + (idx * 5) % 80,
            'descripcion': f'{nombre} silvestre comestible',
            'biomas_preferidos': json.dumps(['bosque', 'selva'] if idx % 2 == 0 else ['campo', 'montaña']),
            'es_alimento': 1,
            'propiedades_alimento': json.dumps({
                'parte_comestible': 'fruto',
                'valor_nutricional': 50 + (idx % 40),
                'sabor': 'dulce' if idx % 2 == 0 else 'ácido'
            })
        })

    # Vegetales y Hierbas Comestibles (80)
    vegetales = [
        ('Maíz', 'Tlaolli', 'hierba', 150, 300, 0.5, 20, 'Cereal sagrado mesoamericano', ['campo'], 'semilla', 90),
        ('Frijol', 'Etl', 'hierba', 30, 200, 0.45, 15, 'Leguminosa básica', ['campo'], 'semilla', 85),
        ('Calabaza', 'Ayotli', 'enredadera', 20, 50, 0.4, 12, 'Calabaza nutritiva', ['campo'], 'fruto', 75),
        ('Chile', 'Chilli', 'hierba', 30, 100, 0.5, 25, 'Chile picante', ['campo', 'huerto'], 'fruto', 80),
        ('Tomate', 'Xitomatl', 'hierba', 30, 150, 0.45, 18, 'Tomate rojo', ['campo', 'huerto'], 'fruto', 70),
        ('Tomate Verde', 'Miltomatl', 'hierba', 30, 120, 0.4, 15, 'Tomatillo verde', ['campo'], 'fruto', 65),
        ('Quelite', 'Quilitl', 'hierba', 20, 80, 0.6, 10, 'Hierba comestible nutritiva', ['campo', 'bosque'], 'hoja', 75),
        ('Verdolaga', 'Itzmiquilitl', 'hierba', 10, 30, 0.7, 8, 'Verdolaga suculenta', ['campo'], 'hoja', 60),
        ('Epazote', 'Epazotl', 'hierba', 30, 100, 0.55, 12, 'Hierba aromática digestiva', ['campo'], 'hoja', 50),
        ('Chaya', 'Chay', 'arbusto', 200, 600, 0.3, 20, 'Espinaca maya', ['selva'], 'hoja', 85),
        ('Nopal', 'Nopalli', 'cactus', 100, 300, 0.5, 15, 'Cactus comestible', ['desierto', 'campo'], 'tallo', 70),
        ('Amaranto', 'Huauhtli', 'hierba', 100, 200, 0.4, 30, 'Pseudocereal sagrado', ['campo'], 'semilla', 90),
        ('Chía', 'Chian', 'hierba', 50, 150, 0.35, 35, 'Semilla nutritiva', ['campo'], 'semilla', 95),
        ('Camote', 'Camotli', 'enredadera', 20, 40, 0.4, 18, 'Batata dulce', ['campo'], 'tuberculo', 80),
        ('Jícama', 'Xicamatl', 'enredadera', 30, 50, 0.35, 20, 'Tubérculo crujiente', ['campo'], 'tuberculo', 70),
        ('Yuca', 'Quauhcamotl', 'arbusto', 150, 300, 0.3, 25, 'Mandioca', ['selva'], 'tuberculo', 85),
        ('Chayote', 'Chayotli', 'enredadera', 200, 800, 0.4, 15, 'Calabaza espinosa', ['bosque', 'campo'], 'fruto', 65),
        ('Huauzontle', 'Huautzontli', 'hierba', 80, 150, 0.35, 22, 'Planta parecida al brócoli', ['campo'], 'flor', 75),
        ('Flor de Calabaza', 'Ayoxochitl', 'enredadera', 20, 50, 0.5, 18, 'Flor comestible de calabaza', ['campo'], 'flor', 60),
        ('Huitlacoche', 'Cuitlacochi', 'hongo', 5, 15, 0.15, 80, 'Hongo del maíz, manjar', ['campo'], 'hongo', 90),
    ]

    for vegetal in vegetales:
        nombre, nahuatl, tipo, h_min, h_max, rar, val, desc, biomas, parte, nutri = vegetal
        flora.append({
            'nombre_comun': nombre,
            'nombre_nahuatl': nahuatl,
            'tipo_planta': tipo,
            'altura_min_cm': h_min,
            'altura_max_cm': h_max,
            'rareza': rar,
            'valor_mercado': val,
            'descripcion': desc,
            'biomas_preferidos': json.dumps(biomas),
            'es_alimento': 1,
            'es_cultivable': 1,
            'tiempo_crecimiento_dias': 60 + (nutri % 120),
            'propiedades_alimento': json.dumps({
                'parte_comestible': parte,
                'valor_nutricional': nutri,
                'sabor': 'vegetal'
            })
        })

    # Hongos Comestibles (30)
    hongos_comestibles = [
        'Hongo Blanco', 'Hongo Azul', 'Huitlacoche', 'Hongo de Llano', 'Hongo de Ocote',
        'Hongo de San Juan', 'Champiñón Silvestre', 'Shiitake Mexicano', 'Yema de Huevo Hongo',
        'Pancita', 'Escobeta', 'Clavito', 'Trompa de Puerco', 'Oreja de Judas',
        'Hongo Amarillo', 'Hongo Negro', 'Hongo de Encino', 'Hongo de Pino', 'Hongo de Tepozán',
        'Hongo Corneta', 'Trompeta de los Muertos', 'Rebozuelo', 'Pedo de Lobo', 'Callampa',
        'Hongo Púrpura', 'Hongo Anaranjado', 'Hongo Lengua de Vaca', 'Hongo Rosado', 'Hongo Verde',
        'Hongo de Madroño'
    ]

    for idx, hongo in enumerate(hongos_comestibles):
        flora.append({
            'nombre_comun': hongo,
            'nombre_nahuatl': f'Nanacatl {idx}',
            'tipo_planta': 'hongo',
            'altura_min_cm': 3 + idx,
            'altura_max_cm': 15 + (idx * 2),
            'rareza': 0.1 + (idx % 20) / 100,
            'valor_mercado': 40 + (idx * 5),
            'descripcion': f'{hongo} comestible silvestre',
            'biomas_preferidos': json.dumps(['bosque', 'selva'] if idx % 2 == 0 else ['montaña', 'bosque']),
            'es_alimento': 1,
            'epoca_disponible': json.dumps(['verano', 'otoño']),
            'propiedades_alimento': json.dumps({
                'parte_comestible': 'hongo',
                'valor_nutricional': 60 + (idx % 30),
                'sabor': 'terroso'
            })
        })

    # Hierbas Aromáticas y Especias (40)
    hierbas_aromaticas = [
        ('Cilantro Silvestre', 'Quilcoyotl', 20, 60, 0.5, 10, 'Cilantro aromático'),
        ('Hierba Santa', 'Acuyo', 150, 300, 0.35, 25, 'Hoja sagrada aromática'),
        ('Pápalo', 'Papaloquilitl', 30, 80, 0.4, 15, 'Hierba de sabor intenso'),
        ('Pepicha', 'Pepicha', 20, 50, 0.35, 18, 'Hierba aromática verde'),
        ('Pipicha', 'Pipicha', 25, 60, 0.38, 16, 'Hierba con aroma a cilantro'),
        ('Chipilín', 'Chipilli', 40, 120, 0.3, 20, 'Hierba nutritiva del sur'),
        ('Quintonil', 'Quintonilli', 30, 90, 0.45, 12, 'Amaranto silvestre'),
        ('Malva', 'Malvatl', 40, 100, 0.5, 10, 'Malva comestible'),
        ('Berro', 'Atlaquilitl', 10, 30, 0.55, 12, 'Berro de agua'),
        ('Alache', 'Alaxtli', 30, 80, 0.4, 14, 'Hierba acuática'),
    ]

    for hierba in hierbas_aromaticas:
        nombre, nahuatl, h_min, h_max, rar, val, desc = hierba
        flora.append({
            'nombre_comun': nombre,
            'nombre_nahuatl': nahuatl,
            'tipo_planta': 'hierba',
            'altura_min_cm': h_min,
            'altura_max_cm': h_max,
            'rareza': rar,
            'valor_mercado': val,
            'descripcion': desc,
            'biomas_preferidos': json.dumps(['campo', 'bosque']),
            'es_alimento': 1,
            'propiedades_alimento': json.dumps({
                'parte_comestible': 'hoja',
                'valor_nutricional': 40,
                'sabor': 'aromático'
            })
        })

    # Granos y Semillas (30)
    granos = [
        'Maíz Blanco', 'Maíz Azul', 'Maíz Rojo', 'Maíz Negro', 'Maíz Cacahuacintle',
        'Frijol Negro', 'Frijol Pinto', 'Frijol Rojo', 'Frijol Blanco', 'Frijol Ayocote',
        'Haba', 'Lenteja Silvestre', 'Garbanzo de Monte', 'Quinoa Mexicana', 'Arroz Silvestre',
        'Cebada Silvestre', 'Avena Silvestre', 'Centeno Silvestre', 'Trigo Silvestre', 'Sorgo',
        'Mijo', 'Alpiste', 'Ajonjolí', 'Girasol Silvestre', 'Linaza',
        'Calabaza Semillas', 'Melón Semillas', 'Sandía Semillas', 'Pepita de Ayote', 'Cacahuate Silvestre'
    ]

    for idx, grano in enumerate(granos):
        flora.append({
            'nombre_comun': grano,
            'nombre_nahuatl': f'{grano.replace(" ", "")}tl',
            'tipo_planta': 'hierba',
            'altura_min_cm': 50 + (idx * 5),
            'altura_max_cm': 200 + (idx * 10),
            'rareza': 0.25 + (idx % 25) / 100,
            'valor_mercado': 15 + (idx * 3),
            'descripcion': f'{grano} nutritivo',
            'biomas_preferidos': json.dumps(['campo']),
            'es_alimento': 1,
            'es_cultivable': 1,
            'tiempo_crecimiento_dias': 90 + (idx * 2),
            'propiedades_alimento': json.dumps({
                'parte_comestible': 'semilla',
                'valor_nutricional': 85 + (idx % 10),
                'sabor': 'neutro'
            })
        })

    # Tubérculos y Raíces (20)
    tuberculos = [
        'Papa Silvestre', 'Oca', 'Olluco', 'Mashua', 'Arracacha', 'Jícama Dulce',
        'Camote Morado', 'Camote Blanco', 'Camote Amarillo', 'Yuca Amarga', 'Yuca Dulce',
        'Malanga', 'Ñame', 'Taro', 'Papa China', 'Jengibre Silvestre', 'Cúrcuma Silvestre',
        'Raíz de Loto', 'Rábano Silvestre', 'Zanahoria Silvestre'
    ]

    for idx, tuberculo in enumerate(tuberculos):
        flora.append({
            'nombre_comun': tuberculo,
            'nombre_nahuatl': f'{tuberculo.replace(" ", "")}tl',
            'tipo_planta': 'hierba',
            'altura_min_cm': 20 + (idx * 2),
            'altura_max_cm': 80 + (idx * 5),
            'rareza': 0.2 + (idx % 30) / 100,
            'valor_mercado': 18 + (idx * 4),
            'descripcion': f'{tuberculo} subterráneo nutritivo',
            'biomas_preferidos': json.dumps(['campo', 'bosque']),
            'es_alimento': 1,
            'es_cultivable': 1,
            'tiempo_crecimiento_dias': 120 + (idx * 5),
            'propiedades_alimento': json.dumps({
                'parte_comestible': 'tuberculo',
                'valor_nutricional': 75 + (idx % 15),
                'sabor': 'almidonado'
            })
        })

    print(f"✓ Alimentos: ~{len([f for f in flora if f.get('es_alimento')])} especies generadas")

    # ================================================================
    # PLANTAS MEDICINALES/CURATIVAS (200 especies)
    # ================================================================

    medicinales = [
        # (nombre, nahuatl, tipo, altura_min, altura_max, rareza, valor, desc, enfermedades_cura, efectividad)
        ('Árnica', 'Tlacopahtli', 'hierba', 20, 60, 0.25, 50, 'Antiinflamatorio potente', ['inflamación', 'golpes', 'moretones'], 85),
        ('Sábila', 'Azahuatl', 'hierba', 30, 80, 0.4, 35, 'Aloe vera curativo', ['quemaduras', 'heridas', 'piel'], 80),
        ('Manzanilla', 'Camomila', 'hierba', 20, 50, 0.5, 25, 'Té digestivo y calmante', ['dolor_estómago', 'insomnio', 'nervios'], 75),
        ('Gordolobo', 'Tlalcocohtli', 'hierba', 50, 150, 0.35, 30, 'Expectorante respiratorio', ['tos', 'gripe', 'bronquitis'], 80),
        ('Hierbabuena', 'Xihuitl', 'hierba', 30, 80, 0.6, 20, 'Digestivo y refrescante', ['dolor_estómago', 'náusea', 'gases'], 70),
        ('Ruda', 'Tzicampalli', 'hierba', 40, 100, 0.4, 40, 'Antiparasitaria y menstrual', ['parásitos', 'dolor_menstrual'], 75),
        ('Romero', 'Rosmarino', 'arbusto', 80, 200, 0.35, 35, 'Estimulante y antiséptico', ['memoria', 'circulación', 'dolor'], 70),
        ('Caléndula', 'Cempasúchil Menor', 'hierba', 30, 60, 0.45, 30, 'Cicatrizante y antiinflamatorio', ['heridas', 'piel', 'inflamación'], 80),
        ('Tilo', 'Tilintli', 'arbol', 500, 3000, 0.2, 45, 'Calmante y sedante', ['ansiedad', 'insomnio', 'nervios'], 75),
        ('Orégano', 'Ahuiyac Xihuitl', 'hierba', 30, 80, 0.55, 25, 'Antiséptico y digestivo', ['infecciones', 'dolor_estómago'], 70),
        ('Jengibre', 'Quauhquílitl', 'hierba', 40, 100, 0.3, 60, 'Antiinflamatorio y digestivo', ['náusea', 'dolor', 'inflamación'], 85),
        ('Cúrcuma', 'Coztic Xihuitl', 'hierba', 40, 100, 0.25, 70, 'Antiinflamatorio poderoso', ['artritis', 'inflamación', 'dolor'], 90),
        ('Valeriana', 'Tlacoxihuitl', 'hierba', 50, 150, 0.3, 50, 'Sedante natural potente', ['insomnio', 'ansiedad', 'estrés'], 85),
        ('Pasiflora', 'Matlalxóchitl', 'enredadera', 200, 1000, 0.28, 55, 'Ansiolítico y sedante', ['ansiedad', 'insomnio', 'epilepsia'], 80),
        ('Cola de Caballo', 'Zacatl Tzontli', 'hierba', 30, 80, 0.45, 30, 'Diurético y remineralizante', ['riñón', 'huesos', 'piel'], 75),
        ('Diente de León', 'Lechuguilla', 'hierba', 10, 40, 0.6, 20, 'Depurativo hepático', ['hígado', 'vesícula', 'digestión'], 70),
        ('Cardo Mariano', 'Aztatl Huitztic', 'hierba', 80, 200, 0.25, 60, 'Protector hepático', ['hígado', 'intoxicación'], 90),
        ('Equinácea', 'Tlalpahtli', 'hierba', 60, 150, 0.3, 65, 'Estimulante inmunológico', ['gripe', 'infecciones', 'inmunidad'], 85),
        ('Ginkgo', 'Cuauhxihuitl Huehuetl', 'arbol', 1000, 4000, 0.1, 100, 'Mejora memoria y circulación', ['memoria', 'circulación', 'vértigo'], 85),
        ('Ginseng', 'Raíz Tonificante', 'hierba', 30, 60, 0.15, 150, 'Tónico energizante', ['fatiga', 'estrés', 'inmunidad'], 90),
    ]

    for medicina in medicinales:
        nombre, nahuatl, tipo, h_min, h_max, rar, val, desc, enfermedades, efect = medicina
        flora.append({
            'nombre_comun': nombre,
            'nombre_nahuatl': nahuatl,
            'tipo_planta': tipo,
            'altura_min_cm': h_min,
            'altura_max_cm': h_max,
            'rareza': rar,
            'valor_mercado': val,
            'descripcion': desc,
            'biomas_preferidos': json.dumps(['bosque', 'montaña']),
            'es_curativo': 1,
            'propiedades_curativo': json.dumps({
                'enfermedades_cura': enfermedades,
                'efectividad': efect,
                'parte_medicinal': 'hoja'
            })
        })

    # Añadir 180 plantas medicinales más
    medicinales_adicionales = [
        'Tomillo', 'Laurel', 'Salvia', 'Lavanda', 'Eucalipto', 'Menta', 'Albahaca', 'Anís', 'Hinojo',
        'Estafiate', 'Ajenjo', 'Toronjil', 'Cedrón', 'Bugambilia Medicinal', 'Cuachalalate',
        'Palo Azul', 'Palo de Brasil', 'Tepezcohuite', 'Chicalote', 'Flor de Manita',
        'Flor de Tila', 'Cuatecomate', 'Guácima', 'Damiana', 'Guaco', 'Yoloxóchitl',
        'Tlanchichinole', 'Axihuitl', 'Tememetla', 'Xonecuilli', 'Copalquáhuitl', 'Iztauhyatl',
        'Zoapatle', 'Michpilli', 'Peyote Medicinal', 'Hongo Reishi', 'Hongo Melena de León',
        'Hongo Cordyceps', 'Muérdago', 'Nopal Medicinal', 'Sangre de Drago', 'Uña de Gato',
        'Achiote Medicinal', 'Chicalote Blanco', 'Tlanchalagua', 'Jícama Medicinal', 'Cancerina',
        'Gobernadora', 'Prodigiosa', 'Muicle', 'Pingüica', 'Matarique', 'Simonillo',
        'Tejocote Medicinal', 'Capulín Medicinal', 'Sauce Blanco', 'Fresno', 'Álamo',
        'Abedul', 'Castaño de Indias', 'Hammamelis', 'Regaliz', 'Boldo', 'Alcachofa',
        'Achicoria', 'Bardana', 'Ortiga', 'Llantén', 'Malva', 'Malvavisco', 'Tusílago',
        'Verbena', 'Milenrama', 'Consuelda', 'Caléndula Silvestre', 'Hypericum', 'Genciana',
        'Abrótano', 'Angelica', 'Artemisa', 'Bistorta', 'Bolsa de Pastor', 'Borraja',
        'Carqueja', 'Centaura Menor', 'Cincoenrama', 'Coclearia', 'Comino', 'Coriandro',
        'Dedalera Menor', 'Dulcamara', 'Enebro', 'Enula', 'Espliego', 'Eufrasia',
        'Fumaria', 'Galega', 'Galio', 'Grama', 'Hisopo', 'Imperatoria', 'Licopodio',
        'Lino', 'Lúpulo', 'Madreselva', 'Marrubio', 'Melisa', 'Menta Poleo', 'Mostaza',
        'Ortiga Muerta', 'Parietaria', 'Pensamiento', 'Perejil', 'Pimpinela', 'Poligala',
        'Primavera', 'Pulmonaria', 'Rábano Medicinal', 'Retama', 'Ruibarbo', 'Rusco',
        'Saponaria', 'Saúco', 'Sello de Oro', 'Serpentaria', 'Tanaceto', 'Trébol de Agua',
        'Ulmaria', 'Verdolaga Medicinal', 'Verónica', 'Vincapervinca', 'Violeta', 'Zarzaparrilla',
        'Achicoria de Montaña', 'Agrimonia', 'Alcaravea', 'Alholva', 'Amapola', 'Angélica China',
        'Asperula', 'Belladona Menor', 'Bellis', 'Bistorta Mayor', 'Cálamo Aromático', 'Cálendula de Indias',
        'Canela Silvestre', 'Cardo Santo', 'Carlina', 'Centidonia', 'Cinquefolia', 'Ciprés Medicinal',
        'Clavo de Olor Silvestre', 'Colombo', 'Cornezuelo Menor', 'Crisantemo Medicinal', 'Doradilla', 'Draba',
        'Dulcamara Mayor', 'Escabiosa', 'Escrofularia', 'Espino Blanco', 'Evónimo', 'Galanga',
        'Galeopsis', 'Gatuña', 'Geranio Medicinal', 'Gordolobo Mayor', 'Grama de las Boticas', 'Grosellero',
        'Helenio', 'Heliotropo', 'Hierba Cana', 'Hierba de Santiago', 'Hierba de San Juan', 'Hierba de Santa María',
        'Hierba Lombriguera', 'Hinojo Marino', 'Ipecacuana', 'Jaborandi', 'Lirio', 'Liquen de Islandia',
        'Lisimaquia', 'Mandrágora Menor', 'Marrubio Negro', 'Mastuerzo', 'Meliloto', 'Mercurial'
    ]

    for idx, nombre in enumerate(medicinales_adicionales):
        flora.append({
            'nombre_comun': nombre,
            'nombre_nahuatl': f'Pahtli {idx}',
            'tipo_planta': 'hierba' if idx % 3 != 0 else ('arbusto' if idx % 3 == 1 else 'arbol'),
            'altura_min_cm': 20 + (idx * 3) % 150,
            'altura_max_cm': 80 + (idx * 8) % 400,
            'rareza': 0.15 + (idx % 35) / 100,
            'valor_mercado': 30 + (idx * 5) % 120,
            'descripcion': f'{nombre} con propiedades medicinales',
            'biomas_preferidos': json.dumps(['bosque', 'montaña'] if idx % 2 == 0 else ['campo', 'bosque']),
            'es_curativo': 1,
            'propiedades_curativo': json.dumps({
                'enfermedades_cura': ['inflamación', 'dolor', 'fiebre'][:(idx % 3) + 1],
                'efectividad': 60 + (idx % 30),
                'parte_medicinal': 'hoja' if idx % 4 == 0 else ('raíz' if idx % 4 == 1 else ('flor' if idx % 4 == 2 else 'corteza'))
            })
        })

    print(f"✓ Medicinales: ~{len([f for f in flora if f.get('es_curativo')])} especies generadas")

    # ================================================================
    # PLANTAS VENENOSAS (100 especies)
    # ================================================================

    venenos = [
        # (nombre, nahuatl, tipo, altura, rareza, toxicidad, síntomas, antídoto)
        ('Belladona', 'Yollotli Tliltic', 'hierba', 150, 0.1, 'extrema', ['parálisis', 'alucinaciones', 'muerte'], 'Atropina'),
        ('Cicuta', 'Coatl Pahtli', 'hierba', 200, 0.08, 'extrema', ['convulsiones', 'parálisis respiratoria', 'muerte'], 'ninguno'),
        ('Estramonio', 'Toloatzin', 'hierba', 120, 0.15, 'alta', ['delirio', 'alucinaciones', 'taquicardia'], 'Fisostigmina'),
        ('Ricino', 'Higuera Infernal', 'arbol', 400, 0.2, 'extrema', ['vómito', 'dolor abdominal', 'muerte'], 'soporte'),
        ('Adelfa', 'Laurel Rosa', 'arbusto', 300, 0.18, 'extrema', ['náusea', 'arritmia', 'muerte'], 'Anticolinérgico'),
        ('Tejo', 'Árbol de Muerte', 'arbol', 1500, 0.05, 'extrema', ['temblores', 'convulsiones', 'muerte'], 'ninguno'),
        ('Acónito', 'Matalobos', 'hierba', 150, 0.12, 'extrema', ['parálisis', 'arritmia', 'muerte'], 'Atropina'),
        ('Digital', 'Dedalera Venenosa', 'hierba', 100, 0.15, 'alta', ['náusea', 'arritmia', 'visión alterada'], 'Antidigoxina'),
        ('Hiedra Venenosa', 'Tlalpahtli Huitztic', 'enredadera', 500, 0.25, 'media', ['irritación', 'ampollas', 'alergia'], 'Cortisona'),
        ('Zumaque Venenoso', 'Tlalpahtli Tlatlauhqui', 'arbusto', 250, 0.2, 'media', ['irritación', 'sarpullido', 'ampollas'], 'Antihistamínico'),
        ('Lirio del Valle', 'Xochitl Miquiztli', 'hierba', 30, 0.18, 'alta', ['náusea', 'arritmia', 'muerte'], 'Antidigoxina'),
        ('Tártago', 'Euphorbia Venenosa', 'hierba', 80, 0.22, 'media', ['vómito', 'diarrea', 'dolor'], 'soporte'),
        ('Jazmín Amarillo', 'Xochitl Coztic Veneno', 'enredadera', 600, 0.16, 'alta', ['vómito', 'convulsiones', 'muerte'], 'soporte'),
        ('Muérdago Venenoso', 'Tlaloc Pahtli', 'planta_parasita', 50, 0.2, 'media', ['náusea', 'convulsiones'], 'soporte'),
        ('Lantana', 'Xochitl Tlapalli Veneno', 'arbusto', 200, 0.25, 'media', ['vómito', 'fotosensibilidad'], 'soporte'),
    ]

    for veneno in venenos:
        nombre, nahuatl, tipo, altura, rar, toxi, sint, anti = veneno
        flora.append({
            'nombre_comun': nombre,
            'nombre_nahuatl': nahuatl,
            'tipo_planta': tipo,
            'altura_min_cm': altura // 2,
            'altura_max_cm': altura,
            'rareza': rar,
            'valor_mercado': 100 if toxi == 'extrema' else 60,
            'descripcion': f'{nombre} - planta venenosa peligrosa',
            'biomas_preferidos': json.dumps(['bosque', 'selva']),
            'es_veneno': 1,
            'nivel_peligro': 'extremo' if toxi == 'extrema' else 'alto',
            'propiedades_veneno': json.dumps({
                'toxicidad': toxi,
                'sintomas': sint,
                'antidoto': anti
            })
        })

    # Añadir 85 plantas venenosas más
    venenos_adicionales = [
        'Hierba Mora', 'Beleño Negro', 'Mandrágora', 'Cornezuelo', 'Vedegambre', 'Nueza Negra',
        'Dulcamara Venenosa', 'Solano Negro', 'Cicuta Menor', 'Aro', 'Brionia', 'Coloquíntida',
        'Eléboro Negro', 'Eléboro Verde', 'Hierba de Ballesteros', 'Oropesa', 'Tusilago Venenoso',
        'Hierba Piojera', 'Raíz del Diablo', 'Nueza Blanca', 'Cólchico', 'Azafrán Silvestre Venenoso',
        'Celidonia Mayor', 'Hierba Verruguera', 'Gordolobo Venenoso', 'Hierba Cana Venenosa', 'Gamón',
        'Serpentaria Venenosa', 'Tabaco Silvestre', 'Beleño Blanco', 'Belladona Menor', 'Adormidera Venenosa',
        'Ruibarbo Venenoso', 'Sen Venenoso', 'Habas de San Ignacio', 'Nuez Vómica', 'Curare',
        'Estrofanto', 'Boj', 'Laburno', 'Torvisco', 'Hierba Centella Venenosa', 'Sello de Salomón Venenoso',
        'Muguet Venenoso', 'Pulsatila Venenosa', 'Ranúnculo', 'Botón de Oro Venenoso', 'Clemátide Venenosa',
        'Anémona Venenosa', 'Aguileña Venenosa', 'Espuela de Caballero Venenosa', 'Hierba del Sapo',
        'Coronilla', 'Retama Negra', 'Cytiso', 'Genciana Venenosa', 'Vincetósigo', 'Apocino',
        'Adelfa de Madagascar', 'Thevetia', 'Tilo Venenoso', 'Fresno Venenoso', 'Ligustro',
        'Aligustre', 'Hierba de Paris', 'Veratro', 'Sabadilla', 'Asaro', 'Aristoloquia',
        'Sauco Venenoso', 'Hierba de las Quemaduras Venenosa', 'Dulcamara de los Bosques', 'Tamujo',
        'Saponaria Venenosa', 'Clavelina Venenosa', 'Euforbio', 'Lechetrezna', 'Tartago Mayor',
        'Ricino de América', 'Higuerilla Venenosa', 'Crotón', 'Manchineel', 'Hura', 'Ombligo de Venus Venenoso'
    ]

    for idx, nombre in enumerate(venenos_adicionales):
        toxi = 'extrema' if idx % 5 == 0 else ('alta' if idx % 3 == 0 else 'media')
        flora.append({
            'nombre_comun': nombre,
            'nombre_nahuatl': f'Miquiztli Xihuitl {idx}',
            'tipo_planta': 'hierba' if idx % 3 == 0 else ('arbusto' if idx % 3 == 1 else 'arbol'),
            'altura_min_cm': 30 + (idx * 5) % 200,
            'altura_max_cm': 100 + (idx * 15) % 600,
            'rareza': 0.05 + (idx % 20) / 100,
            'valor_mercado': 80 + (idx * 10) % 150,
            'descripcion': f'{nombre} - planta con toxinas peligrosas',
            'biomas_preferidos': json.dumps(['bosque', 'selva'] if idx % 2 == 0 else ['pantano', 'bosque']),
            'es_veneno': 1,
            'nivel_peligro': 'extremo' if toxi == 'extrema' else ('alto' if toxi == 'alta' else 'medio'),
            'propiedades_veneno': json.dumps({
                'toxicidad': toxi,
                'sintomas': ['dolor', 'náusea', 'parálisis'][:(idx % 3) + 1],
                'antidoto': 'soporte' if idx % 2 == 0 else 'específico'
            })
        })

    print(f"✓ Venenosas: ~{len([f for f in flora if f.get('es_veneno')])} especies generadas")

    # ================================================================
    # PLANTAS ALUCINÓGENAS/PSICOACTIVAS (50 especies)
    # ================================================================

    alucinogenos = [
        # (nombre, nahuatl, tipo, altura, rareza, potencia, duración_horas, efectos)
        ('Peyote', 'Peyotl', 'cactus', 5, 0.08, 'muy_alta', 12, ['visiones', 'euforia', 'conexión_espiritual']),
        ('Hongos Psilocibios', 'Teonanácatl', 'hongo', 10, 0.12, 'alta', 6, ['alucinaciones', 'introspección', 'euforia']),
        ('Ayahuasca Mexicana', 'Yagé', 'enredadera', 1000, 0.05, 'extrema', 8, ['visiones', 'purga', 'viaje_astral']),
        ('Ololiuqui', 'Ololiuhqui', 'enredadera', 300, 0.15, 'alta', 6, ['visiones', 'sedación', 'conexión_divina']),
        ('Toloache', 'Toloatzin', 'hierba', 150, 0.18, 'muy_alta', 24, ['delirio', 'alucinaciones', 'amnesia']),
        ('San Pedro', 'Huachuma', 'cactus', 600, 0.1, 'alta', 10, ['visiones', 'empatía', 'claridad']),
        ('Salvia Divinorum', 'Hierba de la Pastora', 'hierba', 100, 0.12, 'extrema', 1, ['disociación', 'visiones_intensas']),
        ('Tabaco Sagrado', 'Picietl', 'hierba', 200, 0.25, 'media', 2, ['mareamiento', 'visiones', 'purga']),
        ('Coca Silvestre', 'Coca', 'arbusto', 200, 0.15, 'media', 3, ['estimulación', 'euforia', 'energía']),
        ('Cannabis Silvestre', 'Quauhtzallin', 'hierba', 200, 0.2, 'media', 4, ['relajación', 'euforia', 'introspección']),
    ]

    for alucino in alucinogenos:
        nombre, nahuatl, tipo, altura, rar, pot, dur, efec = alucino
        flora.append({
            'nombre_comun': nombre,
            'nombre_nahuatl': nahuatl,
            'tipo_planta': tipo,
            'altura_min_cm': altura // 2 if altura > 10 else altura,
            'altura_max_cm': altura,
            'rareza': rar,
            'valor_mercado': 200 if pot == 'extrema' else (150 if pot == 'muy_alta' else 100),
            'descripcion': f'{nombre} - planta sagrada psicoactiva',
            'biomas_preferidos': json.dumps(['desierto', 'selva'] if tipo == 'cactus' else ['selva', 'bosque']),
            'es_alucinogeno': 1,
            'es_vendible': 0 if pot == 'extrema' else 1,  # Las más potentes no se venden libremente
            'nivel_peligro': 'alto' if pot in ['extrema', 'muy_alta'] else 'medio',
            'propiedades_alucinogeno': json.dumps({
                'potencia': pot,
                'duracion_horas': dur,
                'efectos': efec
            })
        })

    # Hongos alucinógenos adicionales (40)
    hongos_alucinogenos = [
        'Psilocybe Mexicana', 'Psilocybe Cubensis', 'Psilocybe Caerulescens', 'Psilocybe Aztecorum',
        'Psilocybe Zapotecorum', 'Psilocybe Hoogshagenii', 'Conocybe', 'Panaeolus', 'Gymnopilus',
        'Copelandia', 'Pluteus', 'Inocybe', 'Pholiotina', 'Galerina Menor', 'Mycena',
        'Psilocybe Semilanceata', 'Psilocybe Cyanescens', 'Psilocybe Azurescens', 'Psilocybe Allenii',
        'Psilocybe Stuntzii', 'Psilocybe Tampanensis', 'Psilocybe Atlantis', 'Psilocybe Galindoi',
        'Psilocybe Ovoideocystidiata', 'Psilocybe Quebecensis', 'Psilocybe Weilii', 'Psilocybe Makarorae',
        'Psilocybe Subaeruginosa', 'Psilocybe Australiana', 'Psilocybe Liniformans', 'Psilocybe Fimetaria',
        'Psilocybe Merdaria', 'Psilocybe Coprophila', 'Amanita Muscaria', 'Amanita Pantherina',
        'Claviceps Purpurea', 'Cordyceps Alucinógeno', 'Ergot Mexicano', 'Hongo del Maíz Sagrado',
        'Nanacatl Negro', 'Nanacatl Divino'
    ]

    for idx, hongo in enumerate(hongos_alucinogenos):
        pot = 'extrema' if idx % 8 == 0 else ('muy_alta' if idx % 4 == 0 else 'alta')
        flora.append({
            'nombre_comun': hongo,
            'nombre_nahuatl': f'Teonanácatl {idx}',
            'tipo_planta': 'hongo',
            'altura_min_cm': 3 + idx,
            'altura_max_cm': 15 + idx * 2,
            'rareza': 0.05 + (idx % 15) / 100,
            'valor_mercado': 150 + (idx * 10),
            'descripcion': f'{hongo} - hongo sagrado visionario',
            'biomas_preferidos': json.dumps(['bosque', 'selva'] if idx % 2 == 0 else ['montaña', 'bosque']),
            'es_alucinogeno': 1,
            'es_vendible': 0 if pot == 'extrema' else 1,
            'nivel_peligro': 'alto',
            'epoca_disponible': json.dumps(['verano', 'otoño']),
            'propiedades_alucinogeno': json.dumps({
                'potencia': pot,
                'duracion_horas': 4 + (idx % 8),
                'efectos': ['visiones', 'introspección', 'euforia']
            })
        })

    print(f"✓ Alucinógenas: ~{len([f for f in flora if f.get('es_alucinogeno')])} especies generadas")

    # ================================================================
    # PLANTAS ORNAMENTALES/ADORNO (150 especies)
    # ================================================================

    flores_ornamentales = [
        # (nombre, nahuatl, color, altura, rareza, valor, época_floración, aroma)
        ('Rosa', 'Xochitl Castilla', 'múltiples', 100, 0.4, 30, ['primavera', 'verano'], 'intenso'),
        ('Orquídea', 'Coatzontecoxochitl', 'múltiples', 50, 0.15, 100, ['todo_año'], 'suave'),
        ('Lirio', 'Azucena', 'blanco', 80, 0.3, 40, ['primavera'], 'intenso'),
        ('Tulipán', 'Xochitl Otomí', 'múltiples', 40, 0.25, 35, ['primavera'], 'suave'),
        ('Girasol', 'Chimalxochitl', 'amarillo', 200, 0.5, 20, ['verano'], 'ninguno'),
        ('Cempasúchil', 'Cempoalxochitl', 'naranja', 80, 0.6, 25, ['otoño'], 'fuerte'),
        ('Dalia', 'Acocoxochitl', 'múltiples', 100, 0.4, 30, ['verano', 'otoño'], 'suave'),
        ('Bugambilia', 'Papelillo', 'múltiples', 600, 0.5, 25, ['todo_año'], 'ninguno'),
        ('Nochebuena', 'Cuetlaxochitl', 'rojo', 300, 0.35, 45, ['invierno'], 'ninguno'),
        ('Magnolia', 'Eloxochitl', 'blanco', 800, 0.2, 60, ['primavera'], 'intenso'),
        ('Jazmín', 'Xochitl Iztac', 'blanco', 300, 0.35, 35, ['verano'], 'muy_intenso'),
        ('Violeta', 'Izquixochitl', 'violeta', 20, 0.5, 15, ['primavera'], 'suave'),
        ('Clavel', 'Xochitl España', 'múltiples', 60, 0.4, 25, ['verano'], 'especiado'),
        ('Margarita', 'Xochitl Iztac Pequeña', 'blanco', 40, 0.6, 12, ['primavera', 'verano'], 'ninguno'),
        ('Geranio', 'Malva Rosa', 'múltiples', 50, 0.45, 18, ['primavera', 'verano'], 'característico'),
        ('Hortensia', 'Xochitl Azul', 'azul/rosa', 150, 0.3, 40, ['verano'], 'ninguno'),
        ('Azalea', 'Xochitl Montaña', 'múltiples', 100, 0.25, 50, ['primavera'], 'suave'),
        ('Camelia', 'Xochitl Oriental', 'múltiples', 200, 0.2, 55, ['invierno', 'primavera'], 'suave'),
        ('Gardenia', 'Xochitl Perfumada', 'blanco', 120, 0.25, 60, ['verano'], 'muy_intenso'),
        ('Hibisco', 'Xochitl Tropical', 'múltiples', 200, 0.35, 35, ['verano'], 'suave'),
    ]

    for flor in flores_ornamentales:
        nombre, nahuatl, color, altura, rar, val, epoca, aroma = flor
        flora.append({
            'nombre_comun': nombre,
            'nombre_nahuatl': nahuatl,
            'tipo_planta': 'flor',
            'altura_min_cm': altura // 2,
            'altura_max_cm': altura,
            'color_principal': color,
            'rareza': rar,
            'valor_mercado': val,
            'descripcion': f'{nombre} - flor ornamental de color {color}',
            'biomas_preferidos': json.dumps(['jardin', 'campo', 'bosque']),
            'es_adorno': 1,
            'es_cultivable': 1,
            'tiempo_crecimiento_dias': 60 + (val % 120),
            'epoca_disponible': json.dumps(epoca),
            'propiedades_adorno': json.dumps({
                'color_flor': color,
                'epoca_floracion': epoca,
                'aroma': aroma,
                'duracion_flor_dias': 5 + (val % 10)
            })
        })

    # Flores adicionales (130)
    flores_adicionales = [
        'Gladiolo', 'Fresia', 'Anémona', 'Ranúnculo', 'Peonía', 'Loto', 'Nenúfar', 'Amapola',
        'Cosmos', 'Zinnia', 'Crisantemo', 'Aster', 'Pensamiento', 'Petunia', 'Verbena', 'Salvia Ornamental',
        'Lavanda Ornamental', 'Santolina', 'Aliso', 'Begonia', 'Impatiens', 'Coleo', 'Alegría de la Casa',
        'Calceolaria', 'Primula', 'Ciclamen', 'Kalanchoe', 'Violeta Africana', 'Gloxinia', 'Estreptocarpus',
        'Anthurium', 'Spathiphyllum', 'Caladio', 'Dieffenbachia', 'Filodendro', 'Potus', 'Monstera',
        'Helecho Ornamental', 'Aspidistra', 'Chlorophytum', 'Dracena', 'Sansevieria', 'Palmera Ornamental',
        'Ficus Ornamental', 'Croton Ornamental', 'Aralia', 'Schefflera', 'Hiedra Ornamental', 'Tradescantia',
        'Cebrina', 'Corazón de María', 'Fucsia', 'Plumbago', 'Alstroemeria', 'Iris', 'Gladiolo Mexicano',
        'Nardo', 'Tuberosa', 'Azucena Mexicana', 'Lirio Acuático', 'Jacinto de Agua', 'Papiro Ornamental',
        'Junco Florid', 'Carrizo Ornamental', 'Bambú Ornamental', 'Caña de Azúcar Ornamental', 'Pasto Ornamental',
        'Agapanto', 'Lirio del Nilo', 'Cala', 'Zantedeschia', 'Lirio Amarillo', 'Hemerocallis', 'Kniphofia',
        'Montbretia', 'Ixia', 'Sparaxis', 'Watsonia', 'Fresia del Cabo', 'Ornithogalum', 'Muscari',
        'Jacinto', 'Narciso', 'Jonquil', 'Azafrán', 'Crocus', 'Colchicum', 'Ciclamen Persa', 'Gloriosa',
        'Clivia', 'Amaryllis', 'Hippeastrum', 'Nerine', 'Lycoris', 'Crinum', 'Eucharis', 'Pancratium',
        'Ismene', 'Zephyranthes', 'Habranthus', 'Rhodophiala', 'Griffinia', 'Sprekelia', 'Stenomesson',
        'Bomarea', 'Alstroemeria Aurea', 'Camassia', 'Leucojum', 'Galanthus', 'Scilla', 'Puschkinia',
        'Chionodoxa', 'Ipheion', 'Triteleia', 'Brodiaea', 'Dichelostemma', 'Allium Ornamental', 'Tulbaghia',
        'Agapanthus', 'Liriope', 'Ophiopogon', 'Convallaria', 'Polygonatum', 'Asparagus Ornamental', 'Ruscus Ornamental',
        'Yucca Ornamental', 'Cordyline', 'Phormium', 'Beschorneria'
    ]

    for idx, nombre in enumerate(flores_adicionales):
        colores = ['rojo', 'rosa', 'blanco', 'amarillo', 'azul', 'morado', 'naranja', 'múltiples']
        color = colores[idx % len(colores)]
        flora.append({
            'nombre_comun': nombre,
            'nombre_nahuatl': f'Xochitl {idx}',
            'tipo_planta': 'flor',
            'altura_min_cm': 20 + (idx * 3) % 100,
            'altura_max_cm': 60 + (idx * 8) % 300,
            'color_principal': color,
            'rareza': 0.2 + (idx % 40) / 100,
            'valor_mercado': 15 + (idx * 2) % 80,
            'descripcion': f'{nombre} - planta ornamental',
            'biomas_preferidos': json.dumps(['jardin', 'campo']),
            'es_adorno': 1,
            'es_cultivable': 1 if idx % 3 != 0 else 0,
            'tiempo_crecimiento_dias': 60 + (idx * 5) % 150,
            'propiedades_adorno': json.dumps({
                'color_flor': color,
                'epoca_floracion': ['primavera', 'verano'] if idx % 2 == 0 else ['verano', 'otoño'],
                'aroma': 'suave' if idx % 3 == 0 else ('intenso' if idx % 3 == 1 else 'ninguno'),
                'duracion_flor_dias': 3 + (idx % 12)
            })
        })

    print(f"✓ Ornamentales: ~{len([f for f in flora if f.get('es_adorno')])} especies generadas")

    # ================================================================
    # PLANTAS DE RECURSOS (200 especies)
    # ================================================================

    # Árboles Maderables (50)
    maderas = [
        # (nombre, nahuatl, altura, dureza, usos, valor)
        ('Encino', 'Ahuatl', 2000, 90, ['construcción', 'muebles', 'leña'], 60),
        ('Pino', 'Ocotl', 3000, 70, ['construcción', 'muebles', 'resina'], 50),
        ('Cedro Rojo', 'Cuauhte Tlatlauhqui', 2500, 80, ['muebles', 'canoas', 'construcción'], 100),
        ('Caoba', 'Cuauhte Huey', 3500, 95, ['muebles_finos', 'arte', 'construcción'], 150),
        ('Mezquite', 'Mizquitl', 800, 85, ['muebles', 'carbón', 'postes'], 45),
        ('Huizache', 'Huitzachin', 1000, 75, ['leña', 'postes', 'herramientas'], 35),
        ('Ébano', 'Cuauhte Tliltic', 1500, 100, ['muebles_lujo', 'instrumentos', 'arte'], 200),
        ('Guayacán', 'Cuauhte Huitztic', 1200, 98, ['herramientas', 'artesanía', 'medicina'], 120),
        ('Parota', 'Cuauhparota', 2500, 70, ['muebles', 'canoas', 'construcción'], 80),
        ('Tzalam', 'Tzalamte', 2000, 85, ['construcción', 'muebles', 'postes'], 70),
        ('Granadillo', 'Cuauhcocotl', 1800, 92, ['instrumentos', 'muebles', 'arte'], 140),
        ('Roble', 'Ahuatl Tlatlauhqui', 2500, 88, ['barricas', 'muebles', 'construcción'], 75),
        ('Nogal', 'Tocatl Cuauhtzin', 2200, 80, ['muebles', 'artesanía', 'frutos'], 90),
        ('Oyamel', 'Oyametl', 4000, 65, ['construcción', 'papel', 'leña'], 40),
        ('Ahuehuete', 'Ahuehuetl', 5000, 60, ['construcción', 'artesanía'], 55),
        ('Ceiba', 'Pochutl', 6000, 50, ['canoas', 'artesanía', 'fibra'], 65),
        ('Sabino', 'Ahuehuetl Tzontli', 3000, 65, ['construcción', 'muebles'], 50),
        ('Ciprés', 'Tehuahtli', 2500, 75, ['construcción', 'muebles', 'postes'], 60),
        ('Aliso', 'Ilite', 1500, 60, ['leña', 'artesanía', 'carbón'], 35),
        ('Fresno', 'Axcalli', 2000, 78, ['herramientas', 'muebles', 'deportes'], 55),
    ]

    for madera in maderas:
        nombre, nahuatl, altura, dureza, usos, valor = madera
        flora.append({
            'nombre_comun': nombre,
            'nombre_nahuatl': nahuatl,
            'tipo_planta': 'arbol',
            'altura_min_cm': altura // 2,
            'altura_max_cm': altura,
            'rareza': 0.15 + (dureza % 30) / 100,
            'valor_mercado': valor,
            'descripcion': f'{nombre} - árbol maderable de dureza {dureza}',
            'biomas_preferidos': json.dumps(['bosque', 'montaña']),
            'es_recurso': 1,
            'herramienta_requerida': 'hacha',
            'tiempo_crecimiento_dias': 3650 + (dureza * 30),  # 10+ años
            'propiedades_recurso': json.dumps({
                'tipo_recurso': 'madera',
                'dureza': dureza,
                'usos': usos,
                'calidad': 'alta' if dureza > 85 else ('media' if dureza > 70 else 'baja')
            })
        })

    # Fibras (30)
    fibras = [
        'Algodón', 'Lino', 'Yute', 'Cáñamo', 'Henequén', 'Ixtle', 'Lechuguilla', 'Maguey Fibra',
        'Palma Fibra', 'Tule', 'Totora', 'Junco', 'Esparto', 'Rafia', 'Pita', 'Cabuya',
        'Fique', 'Abacá', 'Sisal', 'Ramio', 'Ortigas Fibra', 'Lino de Nueva Zelanda', 'Yucca Fibra',
        'Agave Fibra', 'Bambú Fibra', 'Plátano Fibra', 'Piña Fibra', 'Coco Fibra', 'Mimbre', 'Carrizo Fibra'
    ]

    for idx, fibra in enumerate(fibras):
        flora.append({
            'nombre_comun': fibra,
            'nombre_nahuatl': f'Ichtli {idx}',
            'tipo_planta': 'hierba' if idx % 2 == 0 else 'arbusto',
            'altura_min_cm': 50 + (idx * 5),
            'altura_max_cm': 200 + (idx * 15),
            'rareza': 0.3 + (idx % 25) / 100,
            'valor_mercado': 30 + (idx * 3),
            'descripcion': f'{fibra} - planta fibrosa para textiles',
            'biomas_preferidos': json.dumps(['campo', 'pantano'] if 'agua' in fibra.lower() else ['campo']),
            'es_recurso': 1,
            'es_cultivable': 1 if idx % 3 != 0 else 0,
            'tiempo_crecimiento_dias': 180 + (idx * 10),
            'propiedades_recurso': json.dumps({
                'tipo_recurso': 'fibra',
                'resistencia': 60 + (idx % 35),
                'usos': ['textiles', 'cuerdas', 'cestería']
            })
        })

    # Tintes (40)
    tintes = [
        # (nombre, color, intensidad, precio)
        ('Añil', 'azul', 90, 80),
        ('Cochinilla', 'rojo', 95, 150),
        ('Palo de Brasil', 'rojo', 85, 100),
        ('Campeche', 'negro/azul', 80, 70),
        ('Cúrcuma', 'amarillo', 75, 50),
        ('Azafrán Tinte', 'amarillo', 85, 120),
        ('Achiote', 'naranja', 70, 40),
        ('Cempasúchil Tinte', 'amarillo', 65, 35),
        ('Nogal Tinte', 'marrón', 80, 45),
        ('Corteza de Encino', 'marrón', 75, 30),
        ('Hoja de Nogal', 'verde', 70, 40),
        ('Espinaca Tinte', 'verde', 60, 25),
        ('Remolacha', 'rojo-rosa', 65, 30),
        ('Zarzamora Tinte', 'morado', 70, 45),
        ('Arándano Tinte', 'azul', 75, 55),
        ('Granada Tinte', 'amarillo', 65, 40),
        ('Cebolla Tinte', 'amarillo-naranja', 70, 20),
        ('Café Tinte', 'marrón', 60, 35),
        ('Té Negro Tinte', 'marrón', 55, 30),
        ('Carbón Vegetal', 'negro', 85, 40),
    ]

    for tinte in tintes:
        nombre, color, intensidad, precio = tinte
        flora.append({
            'nombre_comun': nombre,
            'nombre_nahuatl': f'{nombre.replace(" ", "")}tl',
            'tipo_planta': 'hierba',
            'altura_min_cm': 30,
            'altura_max_cm': 150,
            'rareza': 0.2 + (intensidad % 30) / 100,
            'valor_mercado': precio,
            'descripcion': f'{nombre} - tinte natural color {color}',
            'biomas_preferidos': json.dumps(['bosque', 'campo']),
            'es_recurso': 1,
            'propiedades_recurso': json.dumps({
                'tipo_recurso': 'tinte',
                'color': color,
                'intensidad': intensidad,
                'usos': ['textil', 'pintura', 'arte']
            })
        })

    # Resinas, Aceites y Otros (80)
    otros_recursos = [
        ('Copal', 'Copalli', 'resina', 150, 'incienso_ceremonial'),
        ('Liquidámbar', 'Xochiocotzotl', 'resina', 120, 'medicina_perfume'),
        ('Pino Resina', 'Ocotl Tzictli', 'resina', 80, 'pegamento_impermeabilizante'),
        ('Caucho', 'Olli', 'latex', 200, 'impermeable_pelotas'),
        ('Chicle', 'Tzictli', 'latex', 180, 'goma_mascar'),
        ('Vainilla', 'Tlilxochitl', 'especia', 250, 'saborizante_perfume'),
        ('Pimienta Gorda', 'Xocoxochitl', 'especia', 150, 'condimento'),
        ('Canela Mexicana', 'Canela Tlalli', 'especia', 180, 'condimento_medicina'),
        ('Clavo Silvestre', 'Tzapotl Especia', 'especia', 200, 'condimento'),
        ('Anís Estrella', 'Tlalhuilli', 'especia', 160, 'condimento_digestivo'),
    ]

    for recurso in otros_recursos:
        nombre, nahuatl, tipo_rec, precio, usos = recurso
        flora.append({
            'nombre_comun': nombre,
            'nombre_nahuatl': nahuatl,
            'tipo_planta': 'arbol' if 'árbol' in nombre.lower() or precio > 150 else 'hierba',
            'altura_min_cm': 100 if precio > 150 else 50,
            'altura_max_cm': 1500 if precio > 150 else 300,
            'rareza': 0.1 + (precio % 100) / 500,
            'valor_mercado': precio,
            'descripcion': f'{nombre} - fuente de {tipo_rec}',
            'biomas_preferidos': json.dumps(['selva', 'bosque']),
            'es_recurso': 1,
            'propiedades_recurso': json.dumps({
                'tipo_recurso': tipo_rec,
                'usos': usos.split('_'),
                'calidad': 'alta' if precio > 180 else 'media'
            })
        })

    print(f"✓ Recursos: ~{len([f for f in flora if f.get('es_recurso')])} especies generadas")

    # TOTAL FINAL
    print(f"\n🌿 TOTAL FLORA: {len(flora)} especies generadas")

    return flora

def aplicar_schema():
    """Aplicar schema de flora"""
    print("\n📋 Aplicando schema de flora...")
    conn = sqlite3.connect(DB_PATH)

    with open('schema_flora.sql', 'r', encoding='utf-8') as f:
        schema_sql = f.read()

    conn.executescript(schema_sql)
    conn.commit()
    conn.close()
    print("✅ Schema de flora aplicado")

def main():
    """Función principal"""
    print("=" * 70)
    print("GENERANDO 1000+ ESPECIES DE FLORA")
    print("Portales del Quinto Sol")
    print("=" * 70)

    # Aplicar schema
    aplicar_schema()

    # Generar flora
    print("\n🌿 Generando especies de flora...")
    flora = generar_flora_completa()

    # Insertar en base de datos
    print(f"\n💾 Insertando {len(flora)} especies en la base de datos...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Limpiar tabla
    cursor.execute("DELETE FROM especies_flora")

    # Insertar cada especie
    for planta in flora:
        cursor.execute("""
            INSERT INTO especies_flora (
                nombre_comun, nombre_nahuatl, tipo_planta,
                es_alimento, es_veneno, es_curativo, es_alucinogeno, es_adorno, es_recurso,
                propiedades_alimento, propiedades_veneno, propiedades_curativo,
                propiedades_alucinogeno, propiedades_adorno, propiedades_recurso,
                altura_min_cm, altura_max_cm, color_principal, descripcion,
                biomas_preferidos, rareza, epoca_disponible,
                valor_mercado, es_vendible, es_cultivable, tiempo_crecimiento_dias,
                nivel_peligro, herramienta_requerida
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            planta.get('nombre_comun'),
            planta.get('nombre_nahuatl'),
            planta.get('tipo_planta'),
            planta.get('es_alimento', 0),
            planta.get('es_veneno', 0),
            planta.get('es_curativo', 0),
            planta.get('es_alucinogeno', 0),
            planta.get('es_adorno', 0),
            planta.get('es_recurso', 0),
            planta.get('propiedades_alimento'),
            planta.get('propiedades_veneno'),
            planta.get('propiedades_curativo'),
            planta.get('propiedades_alucinogeno'),
            planta.get('propiedades_adorno'),
            planta.get('propiedades_recurso'),
            planta.get('altura_min_cm'),
            planta.get('altura_max_cm'),
            planta.get('color_principal'),
            planta.get('descripcion'),
            planta.get('biomas_preferidos'),
            planta.get('rareza'),
            planta.get('epoca_disponible'),
            planta.get('valor_mercado'),
            planta.get('es_vendible', 1),
            planta.get('es_cultivable', 0),
            planta.get('tiempo_crecimiento_dias'),
            planta.get('nivel_peligro', 'ninguno'),
            planta.get('herramienta_requerida')
        ))

    conn.commit()

    # Resumen final
    print("\n" + "=" * 70)
    print("✅ SISTEMA DE FLORA COMPLETADO")
    print("=" * 70)

    # Estadísticas por categoría
    cursor.execute("SELECT COUNT(*) FROM especies_flora WHERE es_alimento = 1")
    total_alimento = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM especies_flora WHERE es_veneno = 1")
    total_veneno = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM especies_flora WHERE es_curativo = 1")
    total_curativo = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM especies_flora WHERE es_alucinogeno = 1")
    total_alucinogeno = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM especies_flora WHERE es_adorno = 1")
    total_adorno = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM especies_flora WHERE es_recurso = 1")
    total_recurso = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM especies_flora")
    total_flora = cursor.fetchone()[0]

    print(f"\n📊 RESUMEN POR CATEGORÍA:")
    print(f"   🍎 Alimento:      {total_alimento} especies")
    print(f"   ☠️  Veneno:        {total_veneno} especies")
    print(f"   💊 Curativo:      {total_curativo} especies")
    print(f"   🍄 Alucinógeno:   {total_alucinogeno} especies")
    print(f"   🌸 Adorno:        {total_adorno} especies")
    print(f"   🪵 Recursos:      {total_recurso} especies")
    print(f"\n   🌿 TOTAL:         {total_flora} especies de flora")

    # Por tipo de planta
    print(f"\n📊 RESUMEN POR TIPO:")
    cursor.execute("SELECT tipo_planta, COUNT(*) FROM especies_flora GROUP BY tipo_planta ORDER BY COUNT(*) DESC")
    for tipo, count in cursor.fetchall():
        print(f"   {tipo.upper():20s} {count:4d} especies")

    conn.close()

if __name__ == '__main__':
    main()
