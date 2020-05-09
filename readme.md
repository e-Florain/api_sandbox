- [Terminologie](#org1b12bd2)
  - [Bases de données](#orgcc87888)
  - [Composants logiciels](#org451baa6)
- [Tests en vracs API en Python](#orgf663c9a)
  - [Documentation :](#org724b61b)
  - [Installation :](#orga0ff294)
  - [Bac à sable](#org0aae37c)
- [Connecteur HelloAsso](#org021ef47)
  - [Exemple simple](#org8945307)
  - [URL de callback HelloAsso](#org0ae9ddc)
  - [Cyclos](#org2129820)


<a id="org1b12bd2"></a>

# Terminologie


<a id="orgcc87888"></a>

## Bases de données

-   **Base Maison:** base de données contenant tous les adhérents créée et maintenue par nos soins. techno à définir : PostgreSQL ? MangoDB ?
-   **Base Cyclos:** base de données spécifique Cyclos,


<a id="org451baa6"></a>

## TODO Composants logiciels

-   API HelloAsso
-   API Cyclos
-   Connecteur HelloAsso


<a id="orgf663c9a"></a>

# Tests en vracs API en Python

Afin de faire des requêtes sur une API REST, il y a une super bibliothèque : "requests".


<a id="org724b61b"></a>

## Documentation :

<https://requests.readthedocs.io/en/master/>


<a id="orga0ff294"></a>

## Installation :

De mon coté je n'ai rien eu à faire sous Pop<sub>os</sub> 18.04.


<a id="org0aae37c"></a>

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
                 'datetime': 1588985557,
                 'latitude': 48.684426,
                 'longitude': 6.171111,
                 'passes': 5},
     'response': [{'duration': 653, 'risetime': 1588988802},
                  {'duration': 654, 'risetime': 1588994626},
                  {'duration': 645, 'risetime': 1589000436},
                  {'duration': 493, 'risetime': 1589006278},
                  {'duration': 457, 'risetime': 1589060866}]}

Conversion des timestamps en dates humainement compréhensibles :

```ipython
from datetime import datetime
data = r.json()
dates = [str(datetime.fromtimestamp(d['risetime'])) for d in data['response']]
dates
```

    # Out[97]:
    #+BEGIN_EXAMPLE
      ['2020-05-09 03:46:42',
      '2020-05-09 05:23:46',
      '2020-05-09 07:00:36',
      '2020-05-09 08:37:58',
      '2020-05-09 23:47:46']
    #+END_EXAMPLE


<a id="org021ef47"></a>

# Connecteur HelloAsso


<a id="org8945307"></a>

## Exemple simple

```ipython
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
```

```bash
export FLASK_APP=hello.py
flask run
```

```ipython
r = requests.get("http://127.0.0.1:5000/")
r.status_code, r.text
```

    # Out[99]:
    : (200, 'Hello, World!')

Ok, on a un serveur qui sait répondre à une requête GET simple.

```python
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

```ipython
data = {'key1': 42}
r = requests.post("http://127.0.0.1:5000/login", data=data)
r.status_code, r.text
```

    # Out[100]:
    : (200, '{"coucou":"coucoutext"}\n')


<a id="org0ae9ddc"></a>

## URL de callback HelloAsso

Il est possible de paramétrer le site HelloAsso afin qu'il effectue une requête POST sur une URL spécifique. <https://dev.helloasso.com/v3/notifications>

Ici sont présentées les données qui sont transmises lors d'un nouveau paiement.

| Paramètre                            | Description                                                  | Format  |
|------------------------------------ |------------------------------------------------------------ |------- |
| id                                   | L’identifiant du paiement                                    | string  |
| date                                 | La date                                                      | string  |
| amount                               | Le montant du paiement                                       | decimal |
| type                                 | Type de paiement paiement                                    | string  |
| url                                  | L’url de la campagne sur laquelle a été effectué le paiement | string  |
| payer<sub>first</sub><sub>name</sub> | Le prénom du payeur                                          | string  |
| payer<sub>last</sub><sub>name</sub>  | Le nom du payeur                                             | string  |
| url<sub>receipt</sub>                | L’url du reçu                                                | string  |
| url<sub>tax</sub><sub>receipt</sub>  | L’url du reçu fiscal                                         | string  |
| action<sub>id</sub>                  | Action ID à requeter pour les infos complémentaires 	string |         |

Attention, il semblerait qu'un seul paiement d'un utilisateur sur le site puisse déclencher plusieurs appels du callback. En effet, l'utilisateur peut payer pour ce qu'il achète ET faire un don dans la même procédure.

La rubrique "format des responses" stipule que le paiement peut avoir plusieurs actions :

    {
    	"id": "string",
    	"date": "date",
    	"amount": "decimal",
    	"type" : "string",
    	"payer_first_name": "string",
    	"payer_last_name": "string",
    	"payer_address": "string",
    	"payer_zip_code": "string",
    	"payer_city": "string",
    	"payer_country": "string",
    	"payer_email": "string",
    	"payer_birthdate": "date",
    	"payer_citizenship": "string",
    	"payer_society": "string",
    	"payer_is_society": "bool",
    	"url_receipt": "string",
    	"url_tax_receipt": "string",
    	"status": "string",
    	"actions": [
    	    {
    	    "id": "string",
    	    "type": "string",
    	    "amount": "decimal"
    	    }
    	    …
    	]
    }

Or la notification de nouveau paiement ne comporte qu'un seul ID. Il semblerait donc que lorsqu'un utilisateur effectue une inscription ET un don, la notification est envoyé une fois par action. Ce qui est plutôt pratique car cela permettrait de savoir s'il faut créditer ou simplement remercier la personne.

Autre point important, Il va falloir trouver une solution pour identifier de manière sure (et automatique) la personne qui à payé. En effet, pour effectuer une adhésion, il faut remplir MANUELLEMENT prénom et nom.

Il y a deux cas de figures :

-   **Première Adhésion:** ou les informations rentrées par l'utilisateur serviront de référence pour l'ajout dans les différentes bases de données

-   **Ré-adhésion/Paiement d'un adhérent:** il va falloir s'assurer d'une manière ou d'une autre de retrouver la bonne personne dans la base de données Maison.

Solutions envisagées :

-   Peut être attribuer un identifiant utilisateur à rentrer ?
-   envoyer les utilisateurs existants sur une page pré-remplie ?

Il va falloir prévoir de quoi gérer les cas où une personne s'est trompée,

<https://dev.helloasso.com/v3/responses#paiements>


<a id="org2129820"></a>

## Cyclos

<https://demo.cyclos.org/api>
