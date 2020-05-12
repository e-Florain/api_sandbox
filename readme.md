- [Terminologie](#orgfa4d2b0)
  - [Bases de données](#org88b2f16)
  - [Composants logiciels](#org159d619)
- [Tests en vracs API en Python](#org5440346)
  - [Documentation :](#orgd53106e)
  - [Installation :](#org24cbb35)
  - [Bac à sable](#orge034818)
- [Connecteur HelloAsso](#org407ef71)
  - [Interaction avec l'API](#org4ee615a)
    - [Gestion des secrets :](#orgf83158e)
    - [Récupération de l'ID](#org90139a4)
    - [Récupération des listes](#org3d432a7)
    - [Récupération des détails](#org6c2fe62)
  - [Serveur flask](#org5a26005)
  - [URL de callback HelloAsso](#org3a4b42a)
  - [Cyclos](#org63d2b14)
    - [Authentification](#org81f1b0c)


<a id="orgfa4d2b0"></a>

# Terminologie


<a id="org88b2f16"></a>

## Bases de données

-   **Base Maison:** base de données contenant tous les adhérents créée et maintenue par nos soins. techno à définir : PostgreSQL ? MangoDB ?
-   **Base Cyclos:** base de données spécifique Cyclos,


<a id="org159d619"></a>

## TODO Composants logiciels

-   API HelloAsso
-   API Cyclos
-   Connecteur HelloAsso


<a id="org5440346"></a>

# Tests en vracs API en Python

Afin de faire des requêtes sur une API REST, il y a une super bibliothèque : "requests".


<a id="orgd53106e"></a>

## Documentation :

<https://requests.readthedocs.io/en/master/>


<a id="org24cbb35"></a>

## Installation :

De mon coté je n'ai rien eu à faire sous Pop<sub>os</sub> 18.04.


<a id="orge034818"></a>

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
                 'datetime': 1589315665,
                 'latitude': 48.684426,
                 'longitude': 6.171111,
                 'passes': 5},
     'response': [{'duration': 533, 'risetime': 1589317219},
                  {'duration': 650, 'risetime': 1589322932},
                  {'duration': 653, 'risetime': 1589328741},
                  {'duration': 654, 'risetime': 1589334565},
                  {'duration': 645, 'risetime': 1589340375}]}

Conversion des timestamps en dates humainement compréhensibles :

```ipython
from datetime import datetime
data = r.json()
dates = [str(datetime.fromtimestamp(d['risetime'])) for d in data['response']]
dates
```

    # Out[98]:
    #+BEGIN_EXAMPLE
      ['2020-05-12 23:00:19',
      '2020-05-13 00:35:32',
      '2020-05-13 02:12:21',
      '2020-05-13 03:49:25',
      '2020-05-13 05:26:15']
    #+END_EXAMPLE


<a id="org407ef71"></a>

# Connecteur HelloAsso


<a id="org4ee615a"></a>

## Interaction avec l'API


<a id="orgf83158e"></a>

### Gestion des secrets :

On va pour l'instant utiliser un fichier de config qui ne sera pas ajouté sur le dépôt pour des raisons évidentes. Voici un exemple du fichier de config à renseigner.

```python
url="https://api.helloasso.com/v3/"
user="adminAPI"
password="xxxx"
```

Afin d'être certains de ne pas ajouter le vrai fichier par erreur sur le dépôt, on l'ajoute à gitignore.

```bash
config.py
```

Une fois le fichier complété :

```ipython
import config as cfg
cfg.url
```

    # Out[99]:
    : 'https://api.helloasso.com/v3/'

    # Out[12]:
    : <Response [200]>

```ipython
  from enum import Enum
  class HaType(Enum):
      org = 'organizations'
      cpn = 'campaigns'
      act = 'actions'
      pay = 'payments'

  for t in HaType:
      print(t)

HaType.org.value
```

    # Out[100]:
    : 'organizations'


<a id="org90139a4"></a>

### Récupération de l'ID

C'est un peu contre intuitif, mais le moyen de récupérer l'ID de l'organisation est d'interroger la liste complète des organisations accessibles à l'utilisateur spécifique.

```ipython
import requests
url = 'https://api.helloasso.com/v3/organizations.json'
r= requests.get(url, auth=(cfg.user, cfg.password))
resources = r.json()['resources']
if len(resources) == 1:
  id = resources[0]['id']
```


<a id="org3d432a7"></a>

### Récupération des listes

Exemple liste des paiements effectués par "Virgile"

```ipython
url = 'https://api.helloasso.com/v3/payments.json'
params = {'results_per_page': 1000}
r = requests.get(url, auth=(cfg.user, cfg.password), params=params)
resources = r.json()['resources']
resources = [resource for resource in resources if resource['payer_first_name'] == 'Virgile']
```

Ce qui donne une liste ici ne contenant qu'un seule élément car je l'ai filtrée, qui donne le résultat suivant une fois anonymisé. :

    [{'id': '0000xxxxxxxx',
    'date': '2020-xx-xx17T15:05:00',
    'amount': 20.0,
    'type': 'CREDIT',
    'mean': 'CARD',
    'payer_first_name': 'Virgile',
    'payer_last_name': 'Dupond',
    'payer_address': '',
    'payer_zip_code': '',
    'payer_city': '',
    'payer_country': 'FRA',
    'payer_email': 'bob.dupond@pm.me',
    'payer_society': '',
    'payer_is_society': False,
    'url_receipt': 'https://www.helloasso.com/associations/<nom-association>/adhesions/<nom-du-formulaire>/paiement-attestation/xxxxxxxx',
    'url_tax_receipt': '',
    'actions': [{'id': '000xxxxxxxxx',
    'type': 'SUBSCRIPTION',
    'amount': 10.0,
    'status': 'PROCESSED'},
    {'id': '000xxxxxxxxx',
    'type': 'DONATION',
    'amount': 10.0,
    'status': 'PROCESSED'}],
    'status': 'AUTHORIZED'}]


<a id="org6c2fe62"></a>

### Récupération des détails

Ici, on va récupérer les détails de la première action du paiement.

```ipython
action_id = resources[0]['actions'][0]['id']
url = 'https://api.helloasso.com/v3/actions/{}.json'.format(action_id)
r = r = requests.get(url, auth=(cfg.user, cfg.password))
```

Une fois anonymisé :

    {'id': '000xxxxxxxxx',
    'id_campaign': '000000xxxxxx',
    'id_organism': '00000xxxxxxx',
    'id_payment': '0000xxxxxxxx',
    'date': '2020-xx-xxT15:04:40.8033672',
    'amount': 10.0,
    'type': 'SUBSCRIPTION',
    'first_name': 'Virgile ',
    'last_name': 'xxxxx',
    'email': 'albert.bob@libre.fr',
    'custom_infos': [{'label': 'Email', 'value': 'albert.bob@libre.fr'},
    {'label': 'Adresse', 'value': '42 rue du moulin derrière la maison jaune'},
    {'label': 'Code Postal', 'value': '54000'},
    {'label': 'Ville', 'value': 'Nancy'},
    {'label': 'Numéro de téléphone', 'value': 'xxxxxxxxxx'},
    {'label': "Numéro de l'association soutenue (voir http://www.monnaielocalenancy.fr/doc/UnPourCentAsso.pdf)",
    'value': 'xx'},
    {'label': "Je souhaite m'impliquer bénévolement dans Le Xxxxxx et être rappelé par un membre de l'association ?",
    'value': 'Oui'}],
    'status': 'PROCESSED',
    'option_label': 'Adhésion utilisateurs'}


<a id="org5a26005"></a>

## Serveur flask

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

    # Out[105]:
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

    # Out[106]:
    : (200, {'coucou': 'coucoutext'})


<a id="org3a4b42a"></a>

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


<a id="org63d2b14"></a>

## Cyclos

<https://demo.cyclos.org/api>

<https://demo.cyclos.org/api/system/payments>


<a id="org81f1b0c"></a>

### Authentification

```ipython
r = requests.get("https://demo.cyclos.org/api/auth",
                 auth=('virgile', 'virgile'))
r.status_code, r.json()
```

    # Out[107]:
    : (401, {'code': 'login'})

Démarrage d'une session

```ipython
r = requests.post("https://demo.cyclos.org/api/auth/session",
                 auth=('virgile', '4242'))
r.status_code, r.json()
```

    # Out[108]:
    : (401, {'code': 'login'})
