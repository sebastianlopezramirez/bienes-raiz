import sqlite3, json, os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bienes_raiz.db')
BASE    = 'https://res.cloudinary.com/yskbxdm4/image/upload/f_webp,q_auto/'

# Imágenes ordenadas: exterior → sala → cocina → habitaciones → baños → zona húmeda → closet
ids = [
    'unidad-casa-Llanogrande_adi7pt',
    'frente2-casa-Llanogrande_knl0gs',
    'sala-casa-Llanogrande_e8tqkm',
    'salacomedor-casa-Llanogrande_fssqcl',
    'comedor-casa-Llanogrande_iq9bh0',
    'comedorcompleto-casa-Llanogrande_npxmnr',
    'cocinasalacomedor-casa-Llanogrande_d0y1kl',
    'habitacion-casa-Llanogrande_qxjffd',
    'habitacion2-casa-Llanogrande_guxsbb',
    'habitacion3-casa-Llanogrande_hvbpbj',
    'habitacion3.2-casa-Llanogrande_lhuulk',
    'habitacionvlakaout-casa-Llanogrande_a07e8r',
    'baño-casa-Llanogrande_okuhxu',
    'baño2-casa-Llanogrande_gfsok4',
    'jacuzzy-casa-Llanogrande_c903gq',
    'jacuzzyturco-casa-Llanogrande_icdyuu',
    'jacuzzyturcobaño-casa-Llanogrande_rr1ncf',
    'turco-casa-Llanogrande_db2vgx',
    'closet-casa-Llanogrande_duoidj',
]

urls       = [BASE + pid + '.jpg' for pid in ids]
imagen_url = json.dumps(urls)

descripcion = (
    'Casa de lujo en unidad cerrada con portería y vigilancia 24h. '
    'A 15 min del Aeropuerto José María Córdova. '
    'Área: 118 m². Estrato 4. EPM (agua, energía y gas). Parqueadero doble cubierto. Cuarto útil. '
    'PRIMER NIVEL: Cocina con isla, sala-comedor con A/C, zona húmeda privada con jacuzzi, '
    'sauna, ducha y techo corredizo. Escaleras en madera de pino. Claraboya con iluminación natural. '
    'SEGUNDO NIVEL: 3 habitaciones con baño privado y claraboya. '
    'Habitación principal con cama 3×3, amplio balcón con vista, vestier, A/C y persianas eléctricas. '
    'Acabados modernos en toda la vivienda.'
)

conn   = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute('''
    INSERT INTO propiedades
        (titulo, categoria, departamento, municipio, ubicacion, precio, descripcion, imagen_url, marca)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', (
    'Casa de Lujo – Unidad Cerrada Llanogrande',
    'Casa',
    'Antioquia',
    'Rionegro',
    'Llanogrande, Unidad Cerrada',
    1700000000,
    descripcion,
    imagen_url,
    None
))

conn.commit()
conn.close()

print(f'✅ Propiedad insertada con {len(urls)} imágenes WebP')
print('Abre http://127.0.0.1:5000 y ve a Casas para verla.')
