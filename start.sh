#!/bin/bash
set -euo pipefail


# ✅ Spécifie le chemin exact de Python sur ta machine Windows
PY_CMD="C:\Python312\python.exe"

if [ ! -f "$PY_CMD" ]; then
  echo "❌ Python 3.10 introuvable au chemin spécifié : $PY_CMD" >&2
  exit 1
fi

# 2) Création du venv si besoin
if [ ! -d "venv" ]; then
  echo "🛠️  Création de l'environnement virtuel..."
  "$PY_CMD" -m venv venv
  echo "✅ venv créé."
else
  echo "✅ venv existant détecté."
fi

# 3) Activation du venv
echo "🔑 Activation de l'environnement virtuel..."
if [ -f "venv/Scripts/activate" ]; then
  source venv/Scripts/activate    # Windows Git Bash
elif [ -f "venv/bin/activate" ]; then
  source venv/bin/activate        # Linux/macOS
else
  echo "❌ Impossible de trouver le script d'activation du venv." >&2
  exit 1
fi

echo "(venv) ▶ python $(python --version)"

# 4) Mise à jour de pip & installation des dépendances
echo "🐍 Mise à jour de pip et installation des dépendances..."
python -m pip install --upgrade pip
pip install -r requirements.txt


# echo "📦 Installation des dépendances..."
# pip install --upgrade pip
# pip install -r requirements.txt

 echo "✅ Environnement prêt. Tu peux lancer ton script avec :"
 echo "venv\\Scripts\\activate && python model.py"
