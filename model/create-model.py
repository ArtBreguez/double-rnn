import numpy as np
import json
from keras.models import Sequential
from keras.layers import Dense, LSTM
from keras.callbacks import EarlyStopping
from keras.utils import np_utils
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

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

# Normalizar os dados de entrada
scaler = MinMaxScaler()
X = scaler.fit_transform(X)

# Dividir os dados em conjuntos de treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Calcular pesos de classe
class_weights = {0: 1/0.067, 1: 1/0.467, 2: 1/0.467}

# Preparar os dados para o treinamento
X_train = np.reshape(X_train, (len(X_train), len(X_train[0]), 1))
X_test = np.reshape(X_test, (len(X_test), len(X_test[0]), 1))
y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)

# Criar o modelo LSTM
model = Sequential()
model.add(LSTM(32, input_shape=(len(X[0]), 1)))
model.add(Dense(3, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Usar early stopping durante o treinamento
early_stopping = EarlyStopping(monitor='val_loss', patience=3)

# Treinar o modelo
model.fit(X_train, y_train, epochs=50, batch_size=8, class_weight=class_weights, 
          validation_data=(X_test, y_test), callbacks=[early_stopping])

# Salvar o modelo em disco
model.save("model.h5")
