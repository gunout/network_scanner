#!/usr/bin/env python3
import sys
from scanner.core import NetworkScanner
from scanner.gui import NetworkScannerUI
from PyQt5.QtWidgets import QApplication

def main():
    scanner = NetworkScanner(max_threads=15)
    
    app = QApplication(sys.argv)
    window = NetworkScannerUI(scanner)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
