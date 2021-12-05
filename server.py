import pandas as pd
import numpy as np
import json
import cv2
from PIL import Image
from urllib import parse
import matplotlib.pyplot as plt

from http.server import HTTPServer, SimpleHTTPRequestHandler

class data_setting:
    def generate_data(self, data):
        height = int(data['height'])
        width = int(data['width'])
        name = data['name']

        data_frame = []
        header = []
        lables = []
        header.append('labels')
        for i in range(height * width):
            header.append(f'pixel{i}')

        header = ','.join(header)
        data_frame.append(header)

        print(height, width, name)
        for i in range(len(data['dataset'])):
            nametag = data['dataset'][i]['tag']
            idtag = str(data['dataset'][i]['id'])

            lables.append(idtag + '=' + nametag)
            for j in range(int(data['dataset'][i]['count'])):
                url = 'images/'+str(nametag)+'/'+str(nametag)+' ('+str(j+1)+').jpg'
                img = cv2.imread(url)
                img = cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)

                array_img = Image.fromarray(img)
                array_img = cv2.cvtColor(np.array(array_img), cv2.COLOR_BGR2RGB)

                array_img = array_img.flatten().tolist()
                array_img = ','.join(str(x) for x in array_img)

                print(nametag, 'IMG', j)

                data_frame.append(idtag + ',' + array_img)

        data_frame = np.array(data_frame)
        data_frame = pd.DataFrame(data_frame)
        data_frame.to_csv(f'{name}.csv', sep=';', index=False, header=False)
        with open(f'{name}_labels.txt', 'w') as f:
            for item in lables:
                f.write("%s\n" % item)

        return "Archivo csv generado", f'{name}.csv'

dataSetting = data_setting()

class servidor(SimpleHTTPRequestHandler):
    def do_GET(self):
        return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        self.dataset = []
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        data = data.decode()
        data = parse.unquote(data)
        data = json.loads(data)

        if self.path == '/generate':
            msg = dataSetting.generate_data(data)
            
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin","*")
        self.end_headers()
        self.wfile.write(json.dumps(dict(msg=msg)).encode())



print('Server started...')
httpd = HTTPServer(('localhost', 8000), servidor)
httpd.serve_forever()
