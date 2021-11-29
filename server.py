import pandas as pd
import numpy as np
import os
import cv2
import PIL
from urllib import parse
import matplotlib.pyplot as plt

from http.server import HTTPServer, SimpleHTTPRequestHandler

class data_setting:
    def __init__(self):
        self.dataset = []

    def add_data(self, data):
        self.dataset.append(data)
        return "Datos agregados"

    def generate_data(self, name):
        datasetcsv = pd.DataFrame(self.dataset)
        print(datasetcsv)
        # Eliminar el archivo csv si existe
        if f'{name}.csv' in os.listdir():
            os.remove(f'{name}.csv')
        # Convertir el dataframe a un archivo csv
        datasetcsv.to_csv(f'{name}.csv', index=False)

        return "Archivo csv generado"

    def reset_data(self):
        self.dataset = []
        return "Datos reiniciados"

class servidor(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
            return SimpleHTTPRequestHandler.do_GET(self)
        else:
            return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        self.dataset = []
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        data = data.decode()
        data = parse.unquote(data)

        if self.path == '/refresh':
            self.dataset = []

        if self.path == '/add':
            print('Etiqueta:',data[0])
            self.dataset.append(data)
            print(len(self.dataset))

            # matriz = np.fromstring(data, np.float32, sep=',')
            # matriz = matriz.reshape(100,100)
            # matriz = np.array(matriz)
            # matriz = matriz.reshape(1,100,100,1)
            # print(matriz.shape)

            mensaje = "Imagen recibida"

        elif self.path == '/generate':
            # Primero imprimir el tamaño del dataset
            print(data)
            # Convertir el array a un dataframe con el siguiente formato [[0], [1], [2], [3], [4]]
            # df = pd.DataFrame(data)
            # Convertir el dataframe a un array
            # df = df.values
            # Convertir el array a una matriz
            # df = df.reshape(len(df), 1)
            # # Convertir el array a una imagen
            # img = cv2.imdecode(df, cv2.IMREAD_COLOR)
            # # Convertir la imagen a una matriz
            # img = np.array(img)
            # # Convertir la matriz a un array
            # img = img.reshape(1, 100, 100, 3)
            # print(self.dataset[0])
            datasetcsv = pd.DataFrame(self.dataset)
            print(datasetcsv)
            # Eliminar el archivo csv si existe
            if f'{data}.csv' in os.listdir():
                os.remove(f'{data}.csv')
            # Convertir el dataframe a un archivo csv
            datasetcsv.to_csv(f'{data}.csv', index=False)

            mensaje = "Archivo csv generado"

        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin","*")
        self.end_headers()
        self.wfile.write(mensaje.encode())



print('Server started...')
httpd = HTTPServer(('localhost', 8000), servidor)
httpd.serve_forever()
