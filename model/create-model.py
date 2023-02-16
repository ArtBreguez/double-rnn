import json
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, LSTM
from sklearn.model_selection import train_test_split

# Carregando o dataset
data = []
with open("novo_arquivo.jsonl", "r") as f:
    for line in f:
        data.append(json.loads(line))

# Separando os inputs e outputs do dataset
inputs = []
outputs = []
for example in data:
    inputs.append([int(i) for i in example["input"].split(",")])
    outputs.append(int(example["output"]))

# Convertendo os inputs e outputs em arrays numpy
inputs = np.array(inputs)
outputs = np.array(outputs)

# Definindo as probabilidades de sair para cada cor
probabilities = {0: 0.0666, 1: 0.4666, 2: 0.4666}

# Definindo os pontos para cada cor
points = {0: 14, 1: 1, 2: 1}

# Atribuindo valores para as classes de saída
class_mapping = {0: 1, 1: 1, 2: 2}
outputs_mapped = np.vectorize(class_mapping.get)(outputs)

# Dividindo o dataset em treino e teste
train_inputs, test_inputs, train_outputs, test_outputs = train_test_split(inputs, outputs_mapped, test_size=0.2)

# Normalizando os dados de entrada
mean = train_inputs.mean(axis=0)
std = train_inputs.std(axis=0)
train_inputs = (train_inputs - mean) / std
test_inputs = (test_inputs - mean) / std

# Calculando os pesos de classe
class_weights = {}
for i in range(3):
    class_weights[i] = (points[i] / probabilities[i]) / sum([points[j] / probabilities[j] for j in range(3)])


# Criando o modelo de rede neural recorrente
model = Sequential()
model.add(LSTM(32, input_shape=(train_inputs.shape[1], 1)))
model.add(Dense(3, activation='softmax'))

# Compilando o modelo
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Treinando o modelo com os pesos de classe definidos
model.fit(train_inputs[:, :, np.newaxis], np.eye(3)[train_outputs-1], epochs=10, batch_size=32, class_weight=class_weights)

# Avaliando o modelo no conjunto de testes
score = model.evaluate(test_inputs[:, :, np.newaxis], np.eye(3)[test_outputs-1])
print(f"Test accuracy: {score[1]}")

model.save("modelo.h5")
