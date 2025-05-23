from flask import Flask, render_template, request, jsonify
import requests
import urllib.parse

app = Flask(__name__)

HISTORY = []
FAVORITES = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'results': []})
    url = f'https://jiosaavn-api-privatecvc2.vercel.app/search/songs?query={urllib.parse.quote(query)}'
    resp = requests.get(url)
    data = resp.json()
    songs = data.get('data', {}).get('results', [])
    return jsonify({'results': songs})

@app.route('/add_favorite', methods=['POST'])
def add_favorite():
    song = request.json
    if song not in FAVORITES:
        FAVORITES.append(song)
    return jsonify({'status': 'ok'})

@app.route('/remove_favorite', methods=['POST'])
def remove_favorite():
    song = request.json
    FAVORITES[:] = [f for f in FAVORITES if f['id'] != song['id']]
    return jsonify({'status': 'ok'})

@app.route('/get_favorites')
def get_favorites():
    return jsonify(FAVORITES)

@app.route('/add_history', methods=['POST'])
def add_history():
    song = request.json
    if not any(s['id'] == song['id'] for s in HISTORY):
        HISTORY.append(song)
    return jsonify({'status': 'ok'})

@app.route('/get_history')
def get_history():
    return jsonify(HISTORY)

if __name__ == '__main__':
    app.run(debug=True)

