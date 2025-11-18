#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('quinto_sol.db')
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS especies_civilizaciones")
cursor.execute("DROP TABLE IF EXISTS tratados_especies")
cursor.execute("DROP TABLE IF EXISTS diplomacia_especies")
cursor.execute("DROP TABLE IF EXISTS embajadores")

conn.commit()
conn.close()
print("✅ Tablas eliminadas")
