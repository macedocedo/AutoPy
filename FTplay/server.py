from flask import Flask, request, jsonify
import os
import base64
from datetime import datetime
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
uploads_dir = 'uploads'
os.makedirs(uploads_dir, exist_ok=True)

@app.route('/uploads', methods=['POST'])
def upload_file():
    try:
        data = request.get_json()
        print("Dados recebidos:", data)  # Log dos dados recebidos

        if 'image' not in data or 'location' not in data:
            return jsonify({'error': 'Dados inválidos, imagem ou localização faltando.'}), 400

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

    except Exception as e:
        print("Erro ao processar a requisição:", e)
        return jsonify({'error': 'Erro ao processar a requisição.'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5500)
