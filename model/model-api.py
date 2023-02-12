from flask import Flask, request
import numpy as np
from tensorflow import keras

app = Flask(__name__)

# Carrega o modelo treinado previamente
model = keras.models.load_model('model.h5')

@app.route('/predict', methods=['POST'])
def predict():
    # Recebe a entrada do usuário na forma de uma requisição HTTP
    input_data = request.json['input']

    # Transforma a entrada em um formato apropriado para ser utilizado como entrada do modelo
    input_data = np.array([[int(x) for x in input_data.split(',')]])

    # Utiliza o modelo para fazer uma previsão com base na entrada recebida
    prediction = model.predict(input_data)

    # Transforma a saída da previsão em uma resposta HTTP
    response = {'output': str(np.argmax(prediction[0]))}
    return response

if __name__ == '__main__':
    app.run()
