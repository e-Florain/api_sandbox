- [Terminologie](#org266f40f)
  - [Bases de données](#orgb3aafd4)
  - [Composants logiciels](#orgbfcb84b)
- [Tests en vracs API en Python](#org75e105e)
  - [Documentation :](#org5ea2fae)
  - [Installation :](#orgc184517)
  - [Bac à sable](#orga7018d0)
- [Connecteur HelloAsso](#org29e2a93)
  - [Exemple simple](#org4486e54)
  - [URL de callback HelloAsso](#org9f1bb4f)
  - [Cyclos](#orgdde854a)
    - [Authentification](#org5bfcc0f)


<a id="org266f40f"></a>

# Terminologie


<a id="orgb3aafd4"></a>

## Bases de données

-   **Base Maison:** base de données contenant tous les adhérents créée et maintenue par nos soins. techno à définir : PostgreSQL ? MangoDB ?
-   **Base Cyclos:** base de données spécifique Cyclos,


<a id="orgbfcb84b"></a>

## TODO Composants logiciels

-   API HelloAsso
-   API Cyclos
-   Connecteur HelloAsso


<a id="org75e105e"></a>

# Tests en vracs API en Python

Afin de faire des requêtes sur une API REST, il y a une super bibliothèque : "requests".


<a id="org5ea2fae"></a>

## Documentation :

<https://requests.readthedocs.io/en/master/>


<a id="orgc184517"></a>

## Installation :

De mon coté je n'ai rien eu à faire sous Pop<sub>os</sub> 18.04.


<a id="orga7018d0"></a>

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
                 'datetime': 1589141483,
                 'latitude': 48.684426,
                 'longitude': 6.171111,
                 'passes': 5},
     'response': [{'duration': 325, 'risetime': 1589144484},
                  {'duration': 618, 'risetime': 1589150087},
                  {'duration': 656, 'risetime': 1589155861},
                  {'duration': 651, 'risetime': 1589161685},
                  {'duration': 656, 'risetime': 1589167501}]}

Conversion des timestamps en dates humainement compréhensibles :

```ipython
from datetime import datetime
data = r.json()
dates = [str(datetime.fromtimestamp(d['risetime'])) for d in data['response']]
dates
```

    # Out[6]:
    #+BEGIN_EXAMPLE
      ['2020-05-10 23:01:24',
      '2020-05-11 00:34:47',
      '2020-05-11 02:11:01',
      '2020-05-11 03:48:05',
      '2020-05-11 05:25:01']
    #+END_EXAMPLE


<a id="org29e2a93"></a>

# Connecteur HelloAsso


<a id="org4486e54"></a>

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

    # Out[8]:
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
r.status_code, r.json()
```

    # Out[9]:
    : (200, {'coucou': 'coucoutext'})


<a id="org9f1bb4f"></a>

## URL de callback HelloAsso

Il est possible de paramétrer le site HelloAsso afin qu'il effectue une requête POST sur une URL spécifique.

"Les notifications sont réalisées via des requêtes sous format URLEncoded et en POST sur les urls que vous aurez définies pour chacun des types de notification décrits dans ce chapitre." <https://dev.helloasso.com/v3/notifications>

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

Les requetes sont de type URLencoded. Pour l'instant on a utilisé uniquement des requêtes Json.

```python
@app.route('/paiement', methods=['POST'])
def paiement():
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data, request, type(request))
        return "Merci, c'est tout bon !"
    else:
        return 'Only POST supported'
```

<https://fr.wikipedia.org/wiki/Percent-encoding> Comment simuler une requete HelloAsso:

```bash
curl -d "id=id_42&date=2020-05-10T21:26:45&amount=1438&type=change&payer" -H "Content-Type: application/x-www-form-urlencoded" -X POST http://localhost:5000/paiement
```

Une fois la notification de paiement reçu, il serait bon de récupérer des informations supplémentaires sur l'action (je le rappelle, l'action est un paiement unique avec un seul type). Une procédure d'adhésion accompagnée d'un don renverra donc deux actions.

Une notification de paiement peut donc correspondre à trois types d'actions différentes :

-   **don:** Ici, rien de particulier à faire. Éventuellement envoyer un mail de remerciement.
-   **change:** Il faut vérifier que l'utilisateur existe déjà, et si oui ajouter les fonds correspondants sur Cyclos. S'il n'existe pas (possible ?) il faut vérifier qu'il ne vient pas d'être créé lors de la même session.
-   **adhésion:** Il faut ajouter l'utilisateur dans la base maison, et dans Cyclos.

A noter que ces types sont hypothétiques car ils correspondent à l'idée que je me fais à l'heure actuelle de la situation. Il n'est pas certain que l'on puisse définir le contenu des champs types. Mais leur contenu devrait pourvoir permettre de différencier ces 3 cas.

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


<a id="orgdde854a"></a>

## Cyclos

<https://demo.cyclos.org/api>

<https://demo.cyclos.org/api/system/payments>


<a id="org5bfcc0f"></a>

### Authentification

```ipython
r = requests.get("https://demo.cyclos.org/api/auth",
                 auth=('virgile', 'virgile'))
r.status_code, r.json()
```

    # Out[10]:
    : (401, {'code': 'login'})

Démarrage d'une session

```ipython
r = requests.post("https://demo.cyclos.org/api/auth/session",
                 auth=('virgile', '4242'))
r.status_code, r.json()
```

    # Out[11]:
    : (401, {'code': 'login'})
