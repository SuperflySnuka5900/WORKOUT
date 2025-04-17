import sys
import sqlite3
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, 
                            QComboBox, QPushButton, QTableWidget, QTableWidgetItem)

class ExerciseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.db_path = Path(__file__).parent / "data" / "exercises.db"
        self.connect_db()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Workout Exercise Database')
        self.setGeometry(300, 300, 800, 600)
        
        layout = QVBoxLayout()
        
        # Exercise Type Filter
        self.type_combo = QComboBox()
        self.type_combo.addItem('All')
        self.type_combo.addItems(self.get_distinct_values('type'))
        
        # Muscle Group Filter
        self.muscle_combo = QComboBox()
        self.muscle_combo.addItem('All')
        self.muscle_combo.addItems(self.get_distinct_values('primary_muscle_group'))
        
        # Search Button
        self.search_btn = QPushButton('Search Exercises')
        self.search_btn.clicked.connect(self.load_exercises)
        
        # Results Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ['Exercise', 'Type', 'Primary Muscle', 'Equipment', 'Difficulty']
        )
        
        # Layout
        layout.addWidget(QLabel('Exercise Type:'))
        layout.addWidget(self.type_combo)
        layout.addWidget(QLabel('Primary Muscle:'))
        layout.addWidget(self.muscle_combo)
        layout.addWidget(self.search_btn)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        self.load_exercises()  # Load data on startup

    def connect_db(self):
        """Initialize database connection"""
        self.conn = sqlite3.connect(str(self.db_path))
        self.cursor = self.conn.cursor()
        print(f"✅ Database connected: {self.db_path}")

    def get_distinct_values(self, column):
        """Get unique values for dropdowns"""
        self.cursor.execute(f'SELECT DISTINCT {column} FROM exercises;')
        return [item[0] for item in self.cursor.fetchall()]

    def load_exercises(self):
        """Load exercises into the table (with debug output)"""
        try:
            # Get filter values
            exercise_type = self.type_combo.currentText()
            muscle_group = self.muscle_combo.currentText()
            
            # Build query
            query = '''
                SELECT 
                    exercise_name, 
                    type, 
                    primary_muscle_group, 
                    equipment, 
                    difficulty 
                FROM exercises 
                WHERE 1=1
            '''
            params = []
            
            if exercise_type != 'All':
                query += ' AND type = ?'
                params.append(exercise_type)
                
            if muscle_group != 'All':
                query += ' AND primary_muscle_group = ?'
                params.append(muscle_group)
            
            print(f"\n🔍 Executing query:\n{query}\nParams: {params}")
            
            # Execute query
            self.cursor.execute(query, params)
            results = self.cursor.fetchall()
            print(f"📥 Fetched {len(results)} rows")
            
            # Populate table
            self.table.setRowCount(len(results))
            for row_idx, row in enumerate(results):
                for col_idx, value in enumerate(row):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
            
            print("✅ Table updated successfully\n")
            
        except sqlite3.Error as e:
            print(f"❌ Database error: {e}")
            self.table.setRowCount(0)

    def closeEvent(self, event):
        """Close database connection"""
        self.conn.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ExerciseApp()
    window.show()
    sys.exit(app.exec_())