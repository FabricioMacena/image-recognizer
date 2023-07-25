from tensorflow import keras
import numpy as np
import cv2
from flask import Flask, render_template, request
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/uploads'

def preprocess_image(img_path):
    target_name = ['Baleia', 'Golfinho', 'Peixe', 'Polvo', 'Tartaruga', 'Tubarão']

    img = cv2.imread(img_path)
    img = img / 255.0
    img = cv2.resize(img, (164, 164))
    img = img.astype(np.float32)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = np.expand_dims(img, axis=0)

    model = keras.models.load_model('resnet_animals.h5')
    predict = model.predict(img)
    idx_max = np.argmax(predict)

    proba = predict[0][idx_max]
    proba = np.round(proba * 100, 2)

    class_ = target_name[idx_max]

    return class_, proba

def info_class(classe):
    infos = {
        'Baleia': [
            'Baleias têm coração do tamanho de um carro! 🚗💙',
            'Algumas baleias viajam milhares de quilômetros durante a migração! 🚀🐋',
            'Baleias têm a linguagem mais alta do reino animal! 🔊🐋'
        ], 'Golfinho': [
            'Alguns golfinhos podem saltar até 6 metros acima da água! 🐬🌊',
            'Golfinhos possuem um cérebro altamente desenvolvido e são muito inteligentes! 🧠🐬',
            'Golfinhos são mamíferos marinhos, mas precisam subir à superfície para respirar! 🐬💨'
        ], 'Peixe': [
            'Existem mais de 32.000 espécies conhecidas de peixes no mundo! 🐟🌎',
            'O peixe-palhaço vive em simbiose com as anêmonas-do-mar! 🐠🎭',
            'O tubarão-baleia é o maior peixe do mundo, chegando a 12 metros de comprimento! 🦈🐋'
        ], 'Polvo': [
            'Polvos têm três corações e sangue azul! 💙🐙',
            'Polvos não têm esqueleto interno, o que os torna altamente adaptáveis e ágeis! 💪🐙',
            'A inteligência dos polvos é tão surpreendente que são frequentemente usados como exemplo de uma possível vida extraterrestre inteligente! 👽🧠🐙'
        ], 'Tartaruga': [
            'Algumas tartarugas marinhas podem viajar milhares de quilômetros para desovar nas praias onde nasceram! 🏝️🚀',
            'Algumas espécies de tartarugas são conhecidas por viverem mais de 100 anos! 🎂🕰️',
            'As tartarugas marinhas têm glândulas de sal especiais que ajudam a eliminar o excesso de sal do corpo, permitindo que bebam água do mar! 🐢💧'
        ], 'Tubarão': [
            'Tubarões têm um incrível senso de olfato e podem detectar uma única gota de sangue na água a quilômetros de distância! 🦈👃',
            'O tubarão-martelo possui uma visão excepcionalmente ampla e panorâmica, estimada em cerca de 360 graus!! 👀🔍',
            'Tubarões são nadadores poderosos e podem atingir velocidades impressionantes, com alguns tubarões podendo nadar a mais de 60 km/h! 🏊‍♂️🌊'
        ]
    }

    return infos[classe][np.random.randint(0, 3)]

@app.route("/")
def home():
    return render_template('mainpage.html')

@app.route("/result", methods=['POST'])
def result():
    if 'photo' not in request.files or request.files['photo'].filename == '':
        error_message = 'A imagem ainda não foi enviada.'
        return render_template('mainpage.html', error_message=error_message)

    img = request.files['photo']

    img_path = os.path.join(app.config['UPLOAD_FOLDER'], img.filename)
    img.save(img_path)

    class_, proba = preprocess_image(img_path)

    info = info_class(class_)

    return render_template('result.html', photo_filename=img.filename, class_=class_, proba=proba, info=info)

if __name__ == "__main__":
    app.run(debug=True)