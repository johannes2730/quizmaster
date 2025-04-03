#!/bin/bash
source venv/bin/activate  # Virtuelle Umgebung aktivieren
exec gunicorn -b 0.0.0.0:8000 app:app
