# HVAC SIMULATOR PROJECT
Simulatore di sistemi HVAC (Heating, Ventilation, and Air Conditioning) con interfaccia web. Il frontend è sviluppato in Angular, mentre il backend utilizza Python. Il progetto è containerizzato tramite Docker per facilitare l'installazione e l'esecuzione.
L'obbiettivo di questo progetto é quello di simulare il funzionamento di uno di questi sistemi all'interno di un ambiente controllato offrendo due diverse modalitá di utilizzo:
- simulazione programmata.
- simulazione in tempo reale.

Dove la prima utilizza un sistema di programmazione basato su date in ordine strettamente crescente e una programmazione da seguire, mentre la seconda inizializza un orologio in data corrente.
Ognuna delle due computa risultati una volta per secondo e al termine li pubblica per ulteriori analisi, questi dati comprendono uno screenshot dello stato del sistema che fornisce elementi utili come la temperatura e la potenza istantanee.
La simulazione programmata renderá disponibile il file al momento del corretto completamento della simulazione, mentre la simulazione in tempo reale invece pubblica i dati con l'utilizzo di MQTT.

Si ricorda che il modello termico é relativamente semplice e alcuni elementi come la temperatura esterna é costante durante l'intera durata della simulazione.

# STRUTTURA DEL PROGETTO
il progetto é diviso in 2 parti:
- Backend: comprende la logica del simulatore.
- Frontend: permette la gestione tramite interfaccia grafica.

## Backend
Nel file main viene utilizzato fastAPI per fornire le route necessarie.
Il file Simulation.py contiene la logica dei cicli di simulazione.
La directory src contiene gli attori principali per il funzionamento : i file data.py e la directory tests/ vengono utilizzate respettivamente per la gestione dei dataframes e arrayparametrici (simulazione programmata).
la directory lib invece contiene tutti gli attori principali.

## Frontend
Realizzata utilizzando angular, le componenti utilizzate sono create e possono essere trovate con gli appositi nomi all'interno di HVAC_SIMULATOR_PROJECT/frontend/hvac-sim/src/app.
Si consiglia di controllare per prima cosa la componente remoteComponent perché contiene le funzionalitá principali e utilizza le variabili dei figli (principalmente perché la maggior parte sono delle form) per creare il pacchetto e inviare dati utilizzando le funzioni del service 'http.service.ts',
dove si possono trovare le funzionalitá per la connessione a backend (e presente inoltre un websocket).

# SETUP
L'unico prerequisito é installare docker (questo perché tutte le dipendenze sono caricate nelle immagini) e utilizzare il file docker-compose.yaml per creare i container necessari.
I container sono 3 rispettivamente per la frontend, backend e eclipse-mosquitto.
Tecnologie utilizzate:
- Python.
- Angular.
- Docker.
- MQTT.
- Nginx.

## MIGLIORIE POSSIBILI
- Modello termico.
- Possibili bug in programmazione programmata e/o migliorare la velocitá di esecuzione.
- Implementazione elementi mancanti del sistema (o possibile ristrutturazione): al momento sono presenti solo il compressore e sistema di ventilazione.

Codice scritto su VS Code.
