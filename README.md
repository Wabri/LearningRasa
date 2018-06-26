# Rasa - Appunti e esempi
--------------------
## Indice
[RasaNLU](#rasanlu)
1. [Introduzione](#introduzione-nlu)
2. [Installazione](#installazione-nlu)
3. [Esempio](#esempio-nlu)
4. [Training](#training-nlu)
5. [Backend](#backend-nlu)
6. [Esportare Dialogflow](#esportare-dati-da-dialogflow)
7. [Training Data](#struttura-del-training-data)
8. [Server ed Emulazione](#server-ed-emulazione)
9. [Valutare Modello](#evaluate-model)

[RasaCore](#rasacore)
1. [Introduzione](#introduzione-core)
2. [Framework](#introduzione-al-framework-rasa_core)
3. [Installazione](#installazione-core)
4. [Primo esempio](#primo-semplice-bot)
----------------------
# RasaNLU

## Introduzione nlu
Rasa_NLU è uno strumento per fare il [natural language understanding (NLU)](https://en.wikipedia.org/wiki/Natural_language_understanding).

Questo è un open source tool che permette la classificazione degli intenti e l'estrazione delle entità usate negli intenti.

Prendiamo per esempio la frase:
** "Sto cercando un ristorante messicano in centro" **, il risultato che otterremo è un json di questo tipo:
```
{
  "intent": "ricerca_ristorante",
  "entities": {
    "cuisine" : "messicano",
    "location" : "centro"
  }
}
```
Quindi gli intent non sono altro che lo scopo della frase, mentre le entities sono gli oggetti della frase che possono essere utili.

Questo strumento quindi serve per processare i messaggi. Infatti c'è un componente per la classificazione dell'intento e diversi componenti invece
per il riconoscimento delle entità.

## Installazione nlu
Per installare questo strumento è necessario python e pip:
```
$ pip install rasa_nlu
```
Rasa è possibile eseguirlo con molti backends, la scelta migliore è la combinazione di spacy+sklearn
per installare questi strumenti eseguiamo i comandi:
```
$ pip install -U spacy
$ pip install rasa_nlu[spacy]
```
In questo modo saranno installati rasa_nlu e spacy.
Mancano le librerie dei linguaggi naturali per poter effettivamente fare il NLU:
```
$ python -m spacy download it
$ python -m spacy link it_core_news_sm it
```
*** (teoricamente crea già il link direttamente con il primo comando ma nel caso esplicitare il collegamento con il secondo comando) ***

## Esempio nlu
A questo punto possiamo fare un esempio: creare un bot per la ricerca di ristoranti.

Definiamo quindi 3 tipologie di intenti:
 - ** saluto **
 - ** ricercaRistorante **
 - ** ringraziamento **

Ovviamente ci sono diversi modi per salutare:
 - ciao
 - salve
 - buongiorno

E diversi modi per richidere informazioni per un ristorante:
 - conosci qualche posto per mangiare la pizza in centro?
 - ho fame
 - sono a nord della città e voglio mangiare messicano

La prima cosa che farà Rasa sarà quello di riconoscere l'**intento**
del testo, nel nostro caso dovrà dire se la frase è: un saluto (intento ** saluto**), una richiesta di ricerca di un ristorante (intento ** ricercaRistorante**) oppure un ringraziamento (intento **ringraziamento**).
Subito dopo deve riconoscere ed etichettare delle parole chiave definendo delle **entità**. Per esempio se abbiamo "sono a nord della città e voglio mangiare messicano" rasa deve capire che questo testo corrisponde all'intento di ricercaRistorante e che ci sono 2 entità che è possibile estrapolare che sono:
1. "nord" che rappresenta una posizione,
2. "messicano" che rappresenta il tipo di cucina.

## Training nlu
Per poter fare tutto ciò è necessario allenare l'intelligenza. Il training è fondamentale, più dati abbiamo e più intellingente sarà la nostra intelligenza. Nel caso precedente abbiamo preso la frase ** "sono a nord della città e voglio mangiare messicano"** per far comprendere questa frase all'ai dobbiamo trascriverla sotto forma di file json in questo modo:
```
{
  "text":"sono a nord della città e voglio mangiare messicano",
  "intent":"ricercaRistorante",
  "entities": [
  {
  "start":7,
  "end":10,
  "value":"nord",
  "entity":"posizione",
  }, {
  "start":42,
  "end":50,
  "value":"messicano",
  "entity":"cucina"
  }
  ]
}
```
questo è l'unico modo in cui l'intelligenza artificiale comprenderà la frase. Possiamo fare un altro esempio più semplice con la frase **"ciao"**:
```
{
  "text":"ciao",
  "intent":"saluto",
  "entities": [ ]
}
```
Per evitare di perdere tempo scarichiamo un set di dati già preimpostato: [demo-rasa.json](https://github.com/RasaHQ/rasa_nlu/blob/master/data/examples/rasa/demo-rasa.json).
Creiamo quindi una cartella data/examples/rasa in cui andrà il file demo-rasa.json. copiamo incolliamo il contenuto del sito all'interno di questo file.

##### * Piccolo approfondimento per il training dell'intelligenza *
Esiste un tool grafico per la modifica e aggiunta dei data test, è possibile
installarlo tramite la repository:
[rasa-nlu-trainer](https://github.com/RasaHQ/rasa-nlu-trainer). Una volta installato tramite node package manager è possibile eseguirlo
direttamente nella cartella in cui si trova il file json dei training tramite il comando omonimo:
```
$ rasa-nlu-trainer
```
Che aprirà una pagina web ospitata in localhost in cui si troveranno tutti i
train attuali dell'intelligenza.

## Backend nlu
Andiamo ora a definire la configurazione del backend dell'intelligenza. Creiamo quindi il file ** config_spacy.yml ** nella cartella di lavoro con il seguente
codice:
```
language: "it"

pipeline: "spacy_sklearn"
```
Abbiamo tutto quello di cui abbiamo bisogno per generare alcuni modelli che il backend potrà usare, eseguiamo il comando python:
```
$ python -m rasa_nlu.train \
      --config path_to_config \
      --data path_to_data \
      --path projects
```
L'indicazione ***config*** è la configurazione del modello di machine learning, l'indicazione ***data*** è il file o la cartella in cui sono contenuti i dati di training infine l'indicazione ***path*** è l'output effettivo del modello che verrà creato. Ci metterà un po', ma quando avrà finito dovremmo vedere una cartella projects in cui avremo il nostro modello appena creato.

Per usare il modello creato precedentemente è necessario eseguire il comando
```
$ python -m rasa_nlu.server --path projects
```
Che andrà a prendere il modello default nella cartella projects e userà la porta 5000 sul local host. Mantenendo il server attivo eseguendo una chiamata get all'indirizzo [localhost:5000/parse?q=ciao](http://localhost:5000/parse?q=ciao) dovremmo
ricevere in output un file json con le informazioni del parsing fatto:
```
{
  "intent": {
      "name": "saluto",
    "confidence": 0.5345603412153835
  },
  "entities": [],
  "intent_ranking": [
    {
      "name": "saluto",
      "confidence": 0.5345603412153835
    },
    {
      "name": "ringraziamento",
      "confidence": 0.2604707895172954
    },
    {
      "name": "ricercaRistorante",
      "confidence": 0.20496886926732114
    }
  ],
  "text": "ciao",
  "project": "default",
  "model": "model_20180612-152415"
}
```

## Esportare dati da Dialogflow

Avendo già effettuato un training molto grande da dialogflow posso estrarre
questi dati per usarli da rasa. Per farlo basterà scaricare il file zip
direttamente da dialogflow e estrarre il contenuto in una cartella, nel nostro caso la metteremo all'interno di ***data/example/dialogflowData***. Estraendone il contenuto otterremo 2 cartelle:
  1. entities,
  2. intents.

E due file json:
  1. agent,
  2. package.

Per poter usare questi file possiamo eseguire il comando:
```
$ python -m rasa_nlu.train \
    --config config/config_spacy.yml \
    --data data/examples/rasa/ \
    --path projectsDialogflow
```
Questo creerà un modello come prima, ma dato che ci sono molti più dati, avremo un modello molto più cospicuo. Possiamo ora usare questo modello nel nostro server:
```
$ python -m rasa_nlu.server --path projectsDialogflow
```
Eseguendo una richiesta ***"pagare mario 100 euro"*** avremo un output di questo tipo:
```
{
  "intent": {
    "name": "payRequest",
    "confidence": 0.9346916129148384
  },
  "entities": [
    {
      "start": 0,
      "end": 6,
      "value": "pagare",
      "entity": "payRequest",
      "confidence": 0.9881267419312998,
      "extractor": "ner_crf"
    },
    {
      "start": 7,
      "end": 12,
      "value": "mario",
      "entity": "payToSomeone",
      "confidence": 0.9866899484313593,
      "extractor": "ner_crf"
    },
    {
      "start": 13,
      "end": 16,
      "value": "100",
      "entity": "number",
      "confidence": 0.9855790946392894,
      "extractor": "ner_crf"
    },
    {
      "start": 17,
      "end": 21,
      "value": "euro",
      "entity": "currency-name",
      "confidence": 0.9336220285338104,
      "extractor": "ner_crf"
    }
  ],
  "intent_ranking": [
    {
      "name": "payRequest",
      "confidence": 0.9346916129148384
    },
    {
      "name": "payRequest - yes",
      "confidence": 0.0363128329170857
    },
    {
      "name": "payRequest - no",
      "confidence": 0.018627551951329074
    },
    {
      "name": "Default Welcome Intent",
      "confidence": 0.010368002216746724
    }
  ],
  "text": "pagare mario 100 euro",
  "project": "default",
  "model": "model_20180612-155926"
}
```
Che è il risultato corrispondente al parsing della frase usando il modello generato a partire da dati Dialogflow.

***(Usando questi data training non potrà funzionare il rasa-nlu-trainer che abbiamo usato prima, ma useremo direttamente la console messa a disposizione da dialogflow.)***

## Struttura del Training Data

Il training data per Rasa nlu è strutturato in parti differenti:
  1. common_examples,
  2. entity_synonyms,
  3. regex_features.

Corrispondente al file json:
```
{
  "rasa_nlu_data" : {
    "common_examples":[],
    "regex_features":[],
    "entity_synonyms":[]
  }
}
```
Quello più importante è senza alcun dubbio **common_examples**. Questo
viene usato per fare il train delle entità e degli intenti del modello con esempi scritti da noi.

Per la creazione di questi dataset esistono molti tool grafici che è possibile usare direttamente da browser come:
  * [tracy](https://yuukanoo.github.io/tracy),
  * [Chatito](https://rodrigopivi.github.io/Chatito/).

I **common_examples** hanno 3 componenti:
 - *testo*, è un esempio di come dovrebbe presentarsi la frase dove eseguire il parsing;
 - *intento*, è l'intento (scopo) associato al testo;
 - *entità*, sono parti specifiche nel test a cui è possibile associare un
 identificatore.

I primi 2 sono stringhe mentre l'ultimo è un array.

La parte di **entity_synonyms** è la parte in cui vengono indicati i sinonimi che è possibile trovare in una frase. per esempio la parola *"pagare"* nel nostro caso ha lo stesso significato di *"paga"* dato che la raggruppiamo nello stesso gruppo di entità ***payRequest***. Un altro esempio generico può essere *"New York"* e *"NY"* entrambi hanno lo stesso significato corrispondente all'entità luogo. Indicando i vari sinonimi rasa non differenzierà tra le due parole e gli assegnerà un unico valore che sarà il solito:
```
{
  "rasa_nlu_data": {
    "entity_synonyms": [
      {
        "value": "New York",
        "synonyms": ["NY", "ny", "the big apple"]
      }
    ]
  }
}
```
Le **regex_features** non sono altro che le *regular expression* che possono essere usate come supporto alla classificazione degli intenti e delle entità. Per esempio un codice postale (chiamato anche *zipcode*) è sempre formato da 5 numeri compresi tra 0 e 9, che possiamo rappresentare nella nostra configurazione come:
```
{
    "rasa_nlu_data": {
        "regex_features": [
            {
                "name": "zipcode",
                "pattern": "[0-9]{5}"
            }
        ]
    }
}
```

I training data possono essere salvati in singoli file o in file diversi. Per grandi progetti con molti intenti e entità questo migliora la mantenibilità perchè è possibile dividere in file diversi i training di diversi intenti, invece di mantenerli su un singolo file.

## Server ed emulazione

Possiamo eseguire un server http che riceva le richieste usando il comando:
```
$ python -m rasa_nlu.server --path projects
```
Lo script **server.py** andrà a guardare se esistono dei progetti sotto la cartella *path* indicata dal parametro, altrimenti di default andrà a prendere l'ultimo modello di training.
Il server può emulare i servizi:
  1. wit,
  2. luis,
  3. dialogflow.

In questo modo se esportiamo a partire da questi servizi la sintassi rimarrà la solita e non faremo confusione. Per farlo basta inserire il parametro emulate indicando il tipo di emulazione:
```
$ python -m rasa_nlu.server --path projects --emulate dialogflow
```
Una volta avviato il server è possibile usarlo da un endpoint tramite richieste post:
 - **parse** restituisce il risultato del parsing di una frase
 ```
    http://localhost:5000/parse?q=<frase da parsare>
 ```    
 - **version** restituisce la versione del modello usato
 - **config** restituisce la configurazione attualmente in uso
 - **status** restituisce lo stato attuale del server

Per proteggere il server è possibile specificare un token nelle configurazioni di rasa, aggiungendo **"token":"12345"** al file di configurazione o settando **RASA_TOKEN** nelle variabili d'ambiente. Se è stato settato allora per tutte le richieste sarà necessario la specifica del token, per esempio per la richiesta status:
```
localhost:5000/status?token=12345
```
Questo è necessario quando si vuole chiamare il server da un altro dominio (per esempio da un interfaccia training web), per rendere possibile la trasmissione di dati sarà necessario aggiungere in whitelist il dominio nel cors_origin. Il cors origin sono le configurazioni di [CORS (cross origin resource sharing)](https://en.wikipedia.org/wiki/Cross-origin_resource_sharing).

<!--
Non fatti:
 - https://nlu.rasa.com/python.html
 - https://nlu.rasa.com/entities.html
 - https://nlu.rasa.com/closeloop.html
 - https://nlu.rasa.com/persist.html
 - https://nlu.rasa.com/languages.html
 - https://nlu.rasa.com/pipeline.html
-->

## Evaluate model

Possiamo valutare le performance di riconoscimento degli intenti e delle entità del modello che abbiamo creato usando lo script python **"evaluate.py"**, eseguendolo come segue:
```
$ python -m rasa_nlu.evaluate --data path_to_data --model path_to_model
```
In cui **model** specifica il modello da valutare specificando i data test con data. Questo genererà delle misure di log precision, recall, e f1 per ogni intento e le riassumerà tutte insieme.

--------------------------

# RasaCore

## Introduzione core

Rasa Core è un web service che permette in base a un input (intenti e entità nel nostro caso) di rispondere con delle azioni prefissate. nel nostro caso l'input che gli forniremo è il risultato del parsing di una frase da parte di rasa nlu.
Per poter instaurare una conversazione con un utente è necessario l'utilizzo di una macchina a stati. Questo permetterà di mantenere i dati via via che il flow della conversazione continuerà. Per esempio un utente vuole effettuare un pagamento, rasa quindi collezionerà i dati via via che l'utente li fornisce e quando avrà completato il form di pagamento passerà ad un nuovo stato cioè quello di pagamento effettuato o del controllo della transazione.
Solitamente un bot semplice ha dai 5 ai 10 stati e un centinaio o migliaio di regole per gestire il suo comportamento.
Il codice di rasa core non è formato da una cascata di if else ma usa un modello di predizione probabilistica in base alla scelta del modello che sceglierà l'azione da prendere, l'intelligenza del bot può essere trainata in molti modi. Un approccio di questo tipo porta a vantaggi come: debugging è più semplice, bot più flessibile, il bot migliora la sua esperienza senza scrivere altro codice, è possibile aggiungere funzionalità senza andare a debuggare migliaia di regole precedentemente definite.

## Introduzione al framework rasa_core

python è senza dubbio il linguaggio più usato per il machine learning grazie alla grande quantità di framework sviluppati per questi scopi. Ovviamente la maggior parte dei bot di questo tipo sono scritti in javascript e molte delle altre strutture usate sono invece create e rilasciate in java, c#, etc.etc. Dato che Rasa Core è un framework, non è semplice integrarlo all'interno di un REST API facilmente come Rasa NLU.
Per creare un bot con RasaCore è necessario:
- definire un dominio
- scrivere o collezionare storie
- eseguire uno script python per fare train e eseguire il bot

Per poterlo usare l'unica cosa necessaria da scrivere in python è lo script dove vengono indicate le azioni persoalizzate. Una libreria che può essere di aiuto è [Request: HTTP for Humans](http://docs.python-requests.org/en/master/) che rende la programmazione HTTP molto più semplice. Se Rasa necessita di interagire con altri servizi proprietari tramite HTTP, un'azione comune potrebbe essere di questo tipo:
```
from rasa_core.action import Action
import requests

class ApiAction(Action):
  def name(self):
    return "my_api_action"

  def run (self, dispatcher, tracker, domain):
    data = requests.get(url).json
    return [SlotSet("api_result", data)]
```
<!-- manca da fare (per fatica) https://core.rasa.com/no_python.html#rasa-core-with-docker -->

## Installazione core

l'installazione raccomandata è usando il gestore di pacchetti python pip:
```
  pip install rasa_core
```
(è consigliato anche l'uso e installazione di [Anaconda](https://www.anaconda.com/what-is-anaconda/))

## Primo semplice bot
Prima di iniziare con l'esempio, diamo una spiegazione di come i fili si collegano a partire da quando arriva il messaggio a quando viene restituito in output:
0. **Message In** messaggio di input
1. **Interpreter** converte il messaggio input in un dizionario che include il testo original, l'intento e le entità trovate
2. **Tracker** è l'oggetto che mantiene traccia dello stato della conversazione, riceve le informazioni che arrivano dai nuovi messaggi
3. **Policy** riceve lo stato attuale del tracker e sceglie qual'è l'azione da fare
4. **Action** questo passaggio deve: mandare il log al tracker e generare il messaggio di uscita
5. **Message Out** messaggio spedito allo user, è effettivamente la risposta del bot

a questo punto è possibile iniziare l'esempio: creare un bot che controlla il nostro mood e cerca di tirarci su se siamo infelici. Possiamo usare lo [starter pack](https://github.com/RasaHQ/starter-pack) fornito da rasa per aiutarci nel nostro primo esempio, andiamo quindi a clonare la repository in locale con il comando:
```
  git clone https://github.com/RasaHQ/starter-pack.git
```
I file importanti per i nostri attuali scopi sono:
```
starter-pack/
├── data/
│   ├── stories.md            # set di conversazioni per il training
│   └── nlu_data.md           # set di training per il nlu
├── domain.yml                # configurazione del dominio
└── nlu_config.yml            # configurazione del nlu
```
Eliminiamo quindi tutto il resto. Si presuppone che siano già stati installati i componenti necessari come: rasa_core, rasa_nlue e spacy. Nel caso installarli con i seguenti comandi:
```
pip install rasa_nlu[spacy]
pip install rasa_core
python -m spacy download en  
```
(ovviamente è possibile scaricare e usare anche linguaggi: italiano, spagnolo, portoghese, etc.etc. che è possibile trovare [qui](https://spacy.io/models/)
#### Definire il domain
La prima cosa da fare è definire il Domain (domain.yml), che definisce l'universo in cui il nostro bot vivrà. Nel nostro caso sarà di questo tipo:
```
intents:
  - greet
  - goodbye
  - mood_affirm
  - mood_deny
  - mood_great
  - mood_unhappy

actions:
- utter_greet
- utter_cheer_up
- utter_did_that_help
- utter_happy
- utter_goodbye

templates:
  utter_greet:
  - text: "Hey! How are you?"
    buttons:
    - title: "great"
      payload: "great"
    - title: "super sad"
      payload: "super sad"

  utter_cheer_up:
  - text: "Here is something to cheer you up:"
    image: "https://i.imgur.com/nGF1K8f.jpg"

  utter_did_that_help:
  - text: "Did that help you?"

  utter_happy:
  - text: "Great carry on!"

  utter_goodbye:
  - text: "Bye"
```
Ci sono diverse parti che compongono questo file di configurazione:
1. **intents** è l'intento della frase in input, cioè quello che ci vuole comunicare effettivamente l'utente con la frase (vedi [RasaNLU](#rasanlu))
2. **entities** sono le piccole parti di informazione che sono state estratte dal messaggio dell'utente (vedi [RasaNLU](#rasanlu))
3. **actions** sono le possibili azioni che il bot può fare
4. **slots** sono le informazioni da tracciare durante la conversazione
5. **templates** sono i template che il bot usare per rispondere all'utente

(gli **slots** e le **entities** non compaiono nell'esempio sopra)

Rasa prende intent, entities e lo stato interno del dialogo per selezionare l'azione che deve essere eseguita successivamente. Se l'azione è solo dire qualcosa allo user allora Rasa guarderà se esiste un template definito nel domain che corrisponde a questa azione, una volta che la trova viene inviata all'utente di partenza.

#### Definire l'interpreter

L'interpreter è colui che esegue il parsing dei messaggi, in poche parole il NLU (natural language understanding). Trasforma frasi (messaggi dell'utente) in strutture descrittive della frase in input. Quello che useremo è ovviamente [RasaNLU](#rasanlu). Dato che nell'[esempio di rasanlu](#esempio-nlu) abbiamo usato un formato json per la definizione del set di dati, ora useremo un formato markdown. Inseriamo quindi nel file nlu_data.md il codice seguente:
```
## intent:greet
- hey
- hello
- hi
- hello there
- good morning
- good evening
- moin
- hey there
- let's go
- hey dude
- goodmorning
- goodevening
- good afternoon

## intent:goodbye
- cu
- good by
- cee you later
- good night
- good afternoon
- bye
- goodbye
- have a nice day
- see you around
- bye bye
- see you later

## intent:mood_affirm
- yes
- indeed
- of course
- that sounds good
- correct

## intent:mood_deny
- no
- never
- I don't think so
- don't like that
- no way

## intent:mood_great
- perfect
- very good
- great
- amazing
- feeling like a king
- wonderful
- I am feeling very good
- I am great
- I am amazing
- I am going to save the world
- super
- extremely good
- so so perfect
- so good
- so perfect

## intent:mood_unhappy
- my day was horrible
- I am sad
- I don't feel very well
- I am disappointed
- super sad
- I'm so sad
- sad
- very sad
- unhappy
- not so good
- not very good
- extremly sad
- so saad
- so sad
```
Manca ora definire la configurazione di rasa nlu, andiamo quindi a impostare il file nlu_config.yml come segue:
```
language: "en"

pipeline: "spacy_sklearn"
```
Possiamo quindi fare ora il train del nostro modello, eseguendo questi script python:
```
python -m rasa_nlu.train -c nlu_config.yml --data data/nlu_data.md -o models --fixed_model_name nlu --project current --verbose
```
Verrà creata una cartella *models/current/nlu* in cui sarà contenuto il modello creato.
