import numpy as np
import json
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from keras.utils import np_utils

# Carregar os dados do arquivo jsonl
data = []
with open("data.jsonl") as f:
    for line in f:
        data.append(json.loads(line))

# Separar os dados em entrada (X) e saída (y)
X, y = [], []
for item in data:
    input_data = [int(x) for x in item["input"].split(',')]
    output_data = int(item["output"])
    if output_data == 0:
        # Transforma o output 0 em um array de duas posições, para indicar que a jogada foi perdedora
        y.append([0, 1])
    else:
        # Transforma o output 1 ou 2 em um array de duas posições, para indicar que a jogada foi vencedora
        y.append([1, 0])
    X.append(input_data)

# Preparar os dados para o treinamento
X = np.array(X)
X = np.reshape(X, (len(X), len(X[0]), 1))
y = np.array(y)

# Criar o modelo LSTM
model = Sequential()
model.add(LSTM(32, input_shape=(len(X[0]), 1)))
model.add(Dropout(0.2))
model.add(Dense(16, activation='relu'))
model.add(Dense(2, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Treinar o modelo
model.fit(X, y, epochs=10, batch_size=32)

# Salvar o modelo em disco
model.save("model.h5")
