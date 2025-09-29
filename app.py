from flask import Flask, request, jsonify
import struct

app = Flask(__name__)

@app.route('/login', methods=['GET'])
def login():
    """Возвращает логин автора"""
    return jsonify({"author": "1153332"})  # Замените your_login на ваш логин

@app.route('/size2json', methods=['POST'])
def size2json():
    """Обрабатывает загруженное PNG изображение и возвращает его размеры"""
    
    # Проверяем наличие файла
    if 'image' not in request.files:
        return jsonify({"result": "no file uploaded"}), 400
    
    file = request.files['image']
    
    # Проверяем, что файл был выбран
    if file.filename == '':
        return jsonify({"result": "no file selected"}), 400
    
    try:
        # Читаем первые 8 байт для проверки сигнатуры PNG
        header = file.read(8)
        file.seek(0)  # Возвращаемся к началу файла
        
        # Проверяем сигнатуру PNG
        if header != b'\x89PNG\r\n\x1a\n':
            return jsonify({"result": "invalid filetype"}), 400
        
        # Читаем IHDR chunk для получения размеров
        file.seek(8)  # Пропускаем сигнатуру
        chunk_data = file.read(8)  # Читаем длину chunk'а и тип
        
        if len(chunk_data) < 8:
            return jsonify({"result": "invalid PNG file"}), 400
            
        chunk_length = struct.unpack('>I', chunk_data[:4])[0]
        chunk_type = chunk_data[4:8]
        
        if chunk_type != b'IHDR':
            return jsonify({"result": "invalid PNG file"}), 400
        
        # Читаем данные IHDR chunk'а
        ihdr_data = file.read(chunk_length)
        
        if len(ihdr_data) < 8:
            return jsonify({"result": "invalid PNG file"}), 400
        
        # Извлекаем ширину и высоту (big-endian)
        width = struct.unpack('>I', ihdr_data[:4])[0]
        height = struct.unpack('>I', ihdr_data[4:8])[0]
        
        return jsonify({"width": width, "height": height})
        
    except Exception as e:
        return jsonify({"result": "error processing file"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)