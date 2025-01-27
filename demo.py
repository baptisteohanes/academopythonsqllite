from flask import Flask, request, render_template_string
import sqlite3
import socket

app = Flask(__name__)

# Modèle HTML pour la page web
hostname = socket.gethostname()
html_template = f'''
<!DOCTYPE html>
<html>
<head>
    <title>Formulaire de saisie</title>
</head>
<body>
    <b>Hostname : {hostname}</b>
    <h1>Entrez une valeur</h1>
    <form action="/submit" method="post">
        <label for="value">Valeur :</label>
        <input type="text" id="value" name="value">
        <input type="submit" value="Soumettre">
    </form>
</body>
</html>
'''

# Route pour la page principale
@app.route('/')
def index():
    return render_template_string(html_template)

# Route pour gérer la soumission du formulaire
@app.route('/submit', methods=['POST'])
def submit():
    value = request.form['value']
    
    # Stocker la valeur dans la base de données SQLite
    conn = sqlite3.connect('/mnt/sqlite/database.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS valeurs (id INTEGER PRIMARY KEY, value TEXT)')
    cursor.execute('INSERT INTO valeurs (value) VALUES (?)', (value,))
    conn.commit()
    
# Récupérer toutes les valeurs de la base de données
    cursor.execute('SELECT * FROM valeurs')
    rows = cursor.fetchall()
    conn.close()
    
    # Créer une page de réponse avec le contenu de la table
    response_html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Valeurs soumises</title>
    </head>
    <body>
        <b>Hostname : {}</b>
        <h1>La valeur "{}" a été stockée dans la base de données.</h1>
        <h2>Valeurs actuelles dans la base de données :</h2>
        <ul>
            {}
        </ul>
        <a href="/">Retourner au formulaire</a>
    </body>
    </html>
    '''
    
    # Générer des éléments de liste pour chaque ligne de la table
    list_items = ''.join([f'<li>{row}</li>' for row in rows])
    
    return response_html.format(hostname,value, list_items)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=8080)