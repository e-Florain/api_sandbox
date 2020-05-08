- [API en Python](#org7c940d3)
  - [Documentation :](#org0007a1d)
  - [Installation :](#org1bfe551)
  - [Bac à sable](#org97e6f38)
- [Server](#orgbb2f3ad)
  - [Simple exemple](#org3c23ac8)
  - [URL de callback HelloAsso](#org1c9296b)


<a id="org7c940d3"></a>

# API en Python

Afin de faire des requêtes sur une API REST, il y a une super bibliothèque : "requests".


<a id="org0007a1d"></a>

## Documentation :

<https://requests.readthedocs.io/en/master/>


<a id="org1bfe551"></a>

## Installation :

De mon coté je n'ai rien eu à faire sous Pop<sub>os</sub> 18.04.


<a id="org97e6f38"></a>

## Bac à sable

```ipython
import requests
```

Afin de me faire la main, je vais utiliser une API ouverte : <http://open-notify.org/> qui met à disposition une partie des données de la NASA.

Cette API, comme toutes les APIs mettent à disposition des URLs permettant d'accéder à des données spécifiques. J'ai trouvé une URL permettant de récupérer la liste des astronautes actuellement dans l'espace : <http://api.open-notify.org/astros.json>

Ici, on effectue la requête et on récupère la réponse.

```ipython
r = requests.get("http://api.open-notify.org/astros.json")
print(type(r))
```

    <class 'requests.models.Response'>

Très bien, mais qu'en fait-on ?

On peut déjà commencer par vérifier le code de statut.

```ipython
print(r.status_code)
```

    200

| Category           | Description                                                                                    |
|------------------ |---------------------------------------------------------------------------------------------- |
| 1xx: Informational | Communicates transfer protocol-level information.                                              |
| 2xx: Success       | Indicates that the client’s request was accepted successfully.                                 |
| 3xx: Redirection   | Indicates that the client must take some additional action in order to complete their request. |
| 4xx: Client Error  | This category of error status codes points the finger at clients.                              |
| 5xx: Server Error  | The server takes responsibility for these error status codes.                                  |

Exploitation des données récupérées :

Le contenu de la réponse est une chaîne de caractères non encodée. La méthode '.json()' permet de récupérer un dictionnaire python, qui sera par la suite facilement exploitable. Ici on ne fait que l'afficher.

```ipython
import pprint
pprint.pprint(r.json())
```

    {'message': 'success',
     'number': 3,
     'people': [{'craft': 'ISS', 'name': 'Chris Cassidy'},
                {'craft': 'ISS', 'name': 'Anatoly Ivanishin'},
                {'craft': 'ISS', 'name': 'Ivan Vagner'}]}

Plus compliqué, une requête avec des paramètres. Toujours sur open-notify, on trouve une adresse permettant de récupérer les prochaines dates de passages de l'ISS au dessus d'un couple de coordonnées (LAT, LON). Le code ci dessous permet d'obtenir l'équivalent de cette requête : <http://api.open-notify.org/iss-pass.json?lat=40.71&lon=-74>

Le passage de paramètres est ainsi simplifié en utilisant un dictionnaire python.

```ipython
parameters = {"lat": 48.684426, "lon": 6.171111}
r = requests.get("http://api.open-notify.org/iss-pass.json", params=parameters)
pprint.pprint(r.json())
```

    {'message': 'success',
     'request': {'altitude': 100,
                 'datetime': 1588965203,
                 'latitude': 48.684426,
                 'longitude': 6.171111,
                 'passes': 5},
     'response': [{'duration': 535, 'risetime': 1588977278},
                  {'duration': 650, 'risetime': 1588982993},
                  {'duration': 653, 'risetime': 1588988802},
                  {'duration': 654, 'risetime': 1588994626},
                  {'duration': 645, 'risetime': 1589000436}]}

Conversion des timestamps en dates humainement compréhensibles :

```ipython
from datetime import datetime
data = r.json()
dates = [str(datetime.fromtimestamp(d['risetime'])) for d in data['response']]
dates
```

    # Out[29]:
    #+BEGIN_EXAMPLE
      ['2020-05-09 00:34:38',
      '2020-05-09 02:09:53',
      '2020-05-09 03:46:42',
      '2020-05-09 05:23:46',
      '2020-05-09 07:00:36']
    #+END_EXAMPLE


<a id="orgbb2f3ad"></a>

# Server


<a id="org3c23ac8"></a>

## Simple exemple

```ipython
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
```

    # Out[30]:

```bash
export FLASK_APP=hello.py
flask run
```

```ipython
r = requests.get("http://127.0.0.1:5000/")
r.status_code, r.text
```

    # Out[31]:
    : (200, 'Hello, World!')

Ok, on a un serveur qui sait répondre à une requête GET simple.

```ipython
from flask import request
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data)
        return {'coucou': 'coucoutext'}
    else:
        return 'coucou'
```

    # Out[32]:

```ipython
data = {'key1': 42}
r = requests.post("http://127.0.0.1:5000/login", data=data)
r.status_code, r.text
```

    # Out[33]:
    : (200, '{"coucou":"coucoutext"}\n')


<a id="org1c9296b"></a>

## URL de callback HelloAsso

Nouveau paiement <https://dev.helloasso.com/v3/notifications>

| Paramètre                            | Description                                                  | Format  |
|------------------------------------ |------------------------------------------------------------ |------- |
| id                                   | L’identifiant du paiement                                    | string  |
| date                                 | La date                                                      | string  |
| amount                               | Le montant du paiement                                       | decimal |
| type                                 | Type de paiement paiement                                    | string  |
| url                                  | L’url de la campagne sur laquelle a été effectué le paiement | string  |
| payer<sub>first</sub><sub>name</sub> | Le prénom du payeur                                          | string  |
| payer<sub>last</sub><sub>name</sub>  | Le nom du payeur                                             | string  |
| url<sub>receipt</sub>                | L’url du reçu 	string                                 |         |
| url<sub>tax</sub><sub>receipt</sub>  | L’url du reçu fiscal                                         | string  |
| action<sub>id</sub>                  | Action ID à requeter pour les infos complémentaires 	string |         |
