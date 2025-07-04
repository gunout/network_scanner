from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, 
                            QLabel, QLineEdit, QPushButton, QTreeWidget, 
                            QTreeWidgetItem, QWidget, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette, QFont
from .matrix_background import MatrixBackground

class NetworkScannerUI(QMainWindow):
    def __init__(self, scanner):
        super().__init__()
        self.scanner = scanner
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Cyberpunk Network Scanner')
        self.setGeometry(100, 100, 1000, 800)
        
        # Widget principal
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        
        # Layout principal
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Ajouter l'arrière-plan Matrix
        self.matrix_bg = MatrixBackground(self.main_widget)
        self.matrix_bg.lower()
        
        # Cadre de contenu semi-transparent
        self.content_frame = QFrame()
        self.content_frame.setFrameShape(QFrame.StyledPanel)
        self.content_layout = QVBoxLayout()
        self.content_frame.setLayout(self.content_layout)
        
        # Style cyberpunk
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0A0A14;
            }
            QFrame {
                background-color: rgba(10, 10, 20, 180);
                border: 1px solid #00FFFF;
            }
            QTreeWidget {
                background: rgba(10, 10, 20, 180);
                color: #C8C8FF;
                border: 1px solid #00FFFF;
                font-family: 'Courier New';
            }
            QScrollBar:vertical {
                border: 1px solid #00FFFF;
                background: rgba(20, 20, 40, 200);
                width: 15px;
            }
            QScrollBar::handle:vertical {
                background: #FF00FF;
                min-height: 20px;
            }
        """)
        
        # Champ de recherche
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter website URL (e.g., https://freedom.fr)")
        self.url_input.setStyleSheet("""
            background: rgba(20, 20, 40, 200);
            color: #00FFFF;
            border: 1px solid #FF00FF;
            padding: 8px;
            font-family: 'Courier New';
        """)
        self.content_layout.addWidget(self.url_input)
        
        # Bouton de scan
        self.scan_button = QPushButton("Start Network Scan")
        self.scan_button.setStyleSheet("""
            QPushButton {
                background: rgba(40, 40, 80, 200);
                color: #FF00FF;
                border: 1px solid #00FFFF;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(60, 60, 100, 200);
            }
        """)
        self.scan_button.clicked.connect(self.start_scan)
        self.content_layout.addWidget(self.scan_button)
        
        # Arborescence des résultats
        self.results_tree = QTreeWidget()
        self.results_tree.setHeaderLabels(["Property", "Value"])
        self.results_tree.setColumnWidth(0, 300)
        self.content_layout.addWidget(self.results_tree)
        
        # Ajouter le cadre au layout principal
        self.main_layout.addWidget(self.content_frame)
        
        # Configuration de la palette
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(10, 10, 20))
        palette.setColor(QPalette.WindowText, QColor(0, 255, 255))
        palette.setColor(QPalette.Base, QColor(20, 20, 40, 200))
        palette.setColor(QPalette.Text, QColor(200, 200, 255))
        self.setPalette(palette)
        
    def start_scan(self):
        url = self.url_input.text().strip()
        if not url:
            return
            
        self.results_tree.clear()
        loading_item = QTreeWidgetItem(self.results_tree)
        loading_item.setText(0, "Scanning...")
        loading_item.setText(1, url)
        
        from threading import Thread
        scan_thread = Thread(target=self.run_scan, args=(url,))
        scan_thread.start()
        
    def run_scan(self, url):
        try:
            results = self.scanner.scan_website(url)
            self.display_results(results)
        except Exception as e:
            error_item = QTreeWidgetItem(self.results_tree)
            error_item.setText(0, "Error")
            error_item.setText(1, str(e))
            
    def display_results(self, results):
        self.results_tree.clear()
        root = QTreeWidgetItem(self.results_tree)
        root.setText(0, "Scan Results")
        root.setText(1, results['url'])
        
        # IP Information
        ip_item = QTreeWidgetItem(root)
        ip_item.setText(0, "IP Information")
        for key, value in results['ip_info'].items():
            child = QTreeWidgetItem(ip_item)
            child.setText(0, key)
            child.setText(1, str(value))
        
        # DNS Records
        dns_item = QTreeWidgetItem(root)
        dns_item.setText(0, "DNS Records")
        for rec_type, values in results['dns_records'].items():
            child = QTreeWidgetItem(dns_item)
            child.setText(0, rec_type)
            child.setText(1, ", ".join(values) if isinstance(values, list) else str(values))
        
        # Server Info
        server_item = QTreeWidgetItem(root)
        server_item.setText(0, "Server Information")
        for key, value in results['server_info'].items():
            if isinstance(value, dict):
                child = QTreeWidgetItem(server_item)
                child.setText(0, key)
                for subkey, subvalue in value.items():
                    subchild = QTreeWidgetItem(child)
                    subchild.setText(0, subkey)
                    subchild.setText(1, str(subvalue))
            else:
                child = QTreeWidgetItem(server_item)
                child.setText(0, key)
                child.setText(1, str(value))
        
        # Open Ports
        ports_item = QTreeWidgetItem(root)
        ports_item.setText(0, "Open Ports")
        for port, info in results['open_ports'].items():
            child = QTreeWidgetItem(ports_item)
            child.setText(0, f"Port {port}")
            child.setText(1, info.get('status', 'unknown'))
            if 'service' in info and info['service']:
                service_child = QTreeWidgetItem(child)
                service_child.setText(0, "Service")
                service_child.setText(1, info['service'])
        
        self.results_tree.expandAll()
