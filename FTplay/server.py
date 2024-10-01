from flask import Flask, request, jsonify
import os
import base64
from datetime import datetime

app = Flask(__name__)
uploads_dir = 'uploads'
os.makedirs(uploads_dir, exist_ok=True)

@app.route('/uploads', methods=['POST'])
def upload_file():
    data = request.get_json()
    image_data = data['image']
    location = data['location']

    # Decodificando a imagem
    image_data = image_data.replace('data:image/png;base64,', '')
    image_data = base64.b64decode(image_data)

    # Salvando a imagem
    image_filename = os.path.join(uploads_dir, f'image-{datetime.now().timestamp()}.png')
    with open(image_filename, 'wb') as image_file:
        image_file.write(image_data)

    # Salvando as coordenadas em um arquivo de texto
    coordinates_filename = os.path.join(uploads_dir, 'coordinates.txt')
    with open(coordinates_filename, 'a') as coords_file:
        coords_file.write(f'Latitude: {location["latitude"]}, Longitude: {location["longitude"]}\n')

    return jsonify({'message': 'Imagem e localização salvas com sucesso!'})

if __name__ == '__main__':
    # Corrigindo o host para ser apenas o IP ou 0.0.0.0
    app.run(debug=True, host='127.0.0.1', port=5500)
