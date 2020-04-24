- [API en Python](#orga9dffe8)
  - [Documentation :](#org7a7f002)
  - [Installation :](#org5c26704)
  - [Bac à sable](#orgd99ac74)


<a id="orga9dffe8"></a>

# API en Python

Afin de faire des requêtes sur une API REST, il y a une super bibliothèque : "requests".


<a id="org7a7f002"></a>

## Documentation :

<https://requests.readthedocs.io/en/master/>


<a id="org5c26704"></a>

## Installation :

De mon coté je n'ai rien eu à faire sous Pop<sub>os</sub> 18.04.


<a id="orgd99ac74"></a>

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
                 'datetime': 1587743070,
                 'latitude': 48.684426,
                 'longitude': 6.171111,
                 'passes': 5},
     'response': [{'duration': 349, 'risetime': 1587784693},
                  {'duration': 622, 'risetime': 1587790308},
                  {'duration': 656, 'risetime': 1587796085},
                  {'duration': 651, 'risetime': 1587801910},
                  {'duration': 655, 'risetime': 1587807726}]}

Conversion des timestamps en dates humainement compréhensibles :

```ipython
from datetime import datetime
data = r.json()
dates = [str(datetime.fromtimestamp(d['risetime'])) for d in data['response']]
dates
```

    # Out[55]:
    #+BEGIN_EXAMPLE
      ['2020-04-25 05:18:13',
      '2020-04-25 06:51:48',
      '2020-04-25 08:28:05',
      '2020-04-25 10:05:10',
      '2020-04-25 11:42:06']
    #+END_EXAMPLE
