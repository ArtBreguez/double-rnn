import numpy as np
import json
from keras.models import Sequential
from keras.layers import Dense, LSTM
from keras.utils import np_utils

# Carregar os dados do arquivo jsonl
data = []
with open("data.jsonl") as f:
    for line in f:
        data.append(json.loads(line))

# Separar os dados em entrada (X) e saída (y)
X, y = [], []
for item in data:
    X.append([int(x) for x in item["input"].split(',')])
    y.append(int(item["output"]))

# Preparar os dados para o treinamento
X = np.array(X)
X = np.reshape(X, (len(X), len(X[0]), 1))
y = np_utils.to_categorical(y)

# Criar o modelo LSTM
model = Sequential()
model.add(LSTM(32, input_shape=(len(X[0]), 1)))
model.add(Dense(3, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Treinar o modelo
model.fit(X, y, epochs=10, batch_size=32)

# Salvar o modelo em disco
model.save("model.h5")
