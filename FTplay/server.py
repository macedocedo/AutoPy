from flask import Flask, request, jsonify
from base64 import b64decode
import os
import uuid
from flask_cors import CORS
import logging

app = Flask(__name__)
uploads_dir = 'uploads'

CORS(app)

# Configuração de logging
logging.basicConfig(level=logging.INFO)

# Criar diretório para uploads, se não existir
os.makedirs(uploads_dir, exist_ok=True)

@app.route('/uploads', methods=['POST'])
def upload_image():
    data = request.json
    logging.info(f'Dados recebidos: {data}')  # Log dos dados recebidos

    # Verificar se as chaves necessárias estão presentes
    if 'image' not in data or 'location' not in data:
        return jsonify({'error': 'Dados inválidos. Certifique-se de que a imagem e a localização estão incluídas.'}), 400

    # Extrair dados da imagem
    try:
        image_data = data['image'].split(',', 1)[1]  # Remover cabeçalho da data URL
        latitude = data['location'].get('latitude')
        longitude = data['location'].get('longitude')

        if latitude is None or longitude is None:
            return jsonify({'error': 'Localização inválida. Latitude e longitude devem ser fornecidas.'}), 400
        
        # Gerar um nome de arquivo único
        image_filename = f'captura_{uuid.uuid4()}.png'
        image_path = os.path.join(uploads_dir, image_filename)

        # Salvar a imagem
        with open(image_path, 'wb') as f:
            f.write(b64decode(image_data))

        logging.info(f'Imagem salva: {image_path} com sucesso.')

    except IndexError: # <- Erro retornado
        return jsonify({'error': 'Erro ao processar a imagem. Certifique-se de que o formato está correto.'}), 400
    except ValueError:
        return jsonify({'error': 'Erro ao decodificar a imagem. Verifique se a string  está correta.'}), 400
    except Exception as e:
        logging.error(f'Erro ao salvar a imagem: {str(e)}')
        return jsonify({'error': f'Erro ao salvar a imagem: {str(e)}'}), 500

    return jsonify({
        'message': 'Imagem e localização salvas com sucesso.',
        'latitude': latitude,
        'longitude': longitude,
        'image_path': image_path  # Retorna o caminho do arquivo salvo
    })

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5500)


# pasta : FTplay/uploads