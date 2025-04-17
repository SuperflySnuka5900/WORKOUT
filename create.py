import sqlite3
import csv

conn = sqlite3.connect('exercises.db')
cursor = conn.cursor()

with open('exercises.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        cursor.execute('''
            INSERT INTO exercises (
                exercise_name, type, primary_muscle_group,
                secondary_muscle_group, equipment, difficulty
            )
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            row['exercise_name'], row['type'], row['primary_muscle_group'],
            row['secondary_muscle_group'], row['equipment'], row['difficulty']
        ))

conn.commit()
conn.close()