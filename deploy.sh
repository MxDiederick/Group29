#!/bin/bash

#Voer deze commando uit in de terminal om website te refreshen:./deploy.sh


echo "▶️  Notebook converteren naar HTML..."
jupyter nbconvert --to html group29.ipynb --output docs/index.html

echo "✅ Conversie voltooid."

echo "📁 Toevoegen aan git..."
git add group29.ipynb docs/index.html

echo "✍️ Committen..."
git commit -m "Update site via notebook export"

echo "⬆️ Pushen naar GitHub..."
git push

echo "🌐 Klaar! Je GitHub Pages site is bijgewerkt."
