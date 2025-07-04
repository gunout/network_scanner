from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QTimer
import random
import math

class MatrixBackground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Configuration Matrix
        self.chars = "01アイウエオ"  # Mélange binaire et katakana
        self.font_size = 14
        self.columns = math.ceil(self.width() / self.font_size)
        self.positions = [random.randint(-20, 0) for _ in range(self.columns)]
        self.speeds = [random.randint(1, 4) for _ in range(self.columns)]
        self.colors = [
            QColor(0, 255, 0),   # Vert néon
            QColor(0, 200, 100), # Turquoise
            QColor(150, 255, 0)  # Vert lime
        ]
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_matrix)
        self.timer.start(80)  # Plus fluide à 12-13 FPS
        
    def update_matrix(self):
        for i in range(self.columns):
            if (self.positions[i] * self.font_size > self.height() + 20 or 
                random.random() < 0.03):
                self.positions[i] = 0
                self.speeds[i] = random.randint(1, 4)
            else:
                self.positions[i] += self.speeds[i]
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setFont(QFont("Courier New", self.font_size, QFont.Bold))
        
        for i in range(self.columns):
            x = i * self.font_size
            trail_length = random.randint(5, 15)
            
            for j in range(max(0, self.positions[i] - trail_length), self.positions[i]):
                y = j * self.font_size
                if 0 <= y < self.height():
                    char = random.choice(self.chars)
                    # Effet de fondu
                    alpha = 255 * (1 - (self.positions[i] - j) / trail_length)
                    color_idx = min(j % 3, len(self.colors)-1)
                    color = QColor(self.colors[color_idx])
                    color.setAlpha(int(alpha))
                    painter.setPen(color)
                    painter.drawText(x, y, char)
                    
        # Ajouter des particules aléatoires
        for _ in range(5):
            x = random.randint(0, self.width())
            y = random.randint(0, self.height())
            painter.setPen(QColor(0, 255, 0, random.randint(50, 150)))
            painter.drawText(x, y, random.choice(self.chars))
                    
        painter.end()
        
    def resizeEvent(self, event):
        new_columns = math.ceil(self.width() / self.font_size)
        if new_columns > self.columns:
            # Ajouter de nouvelles colonnes
            diff = new_columns - self.columns
            self.positions += [random.randint(-20, 0) for _ in range(diff)]
            self.speeds += [random.randint(1, 4) for _ in range(diff)]
        elif new_columns < self.columns:
            # Supprimer des colonnes
            self.positions = self.positions[:new_columns]
            self.speeds = self.speeds[:new_columns]
            
        self.columns = new_columns
