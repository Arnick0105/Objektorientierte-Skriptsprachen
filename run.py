import sys
import os

# src-Ordner zum Python-Pfad hinzufügen
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from main import main

if __name__ == "__main__":
    main()
