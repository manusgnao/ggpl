# WORKSHOP 11

## Descrizione
Rappresentazione 3D di un quartiere residenziale composto con case costruite con il workshop n. 10.
Questo progetto ha la seguente struttura.
La cartella *house* contiene una versione rivista del workshop n. 10 e viene richiamato per costruire tutte le case di cui si ha bisogno.
Nella cartella *elements* sono divisi i file .lines e .svg utilizzati per la creazione dei vari elementi.
Ogni cartella contiene una cartella *svg* contenenti i file utilizzati per creare i livelli e una cartella *lines* contenente i file ottunuti dal servizio offerto da [questo](http://cvdlab.github.io/svg2lines/) sito che converte file svg in file lines.
Queste sono le cartelle di *elements*

* base
* house
* street

###Livello Base
Questo livello delimita un singolo isolato. All'interno di questo livello verranno poi create le strade e gli edifici dell'isolato. Graficamente è decorato con un prato.

###Livello House
Questa sezione contiene la posizione della base di 6 case. Questo insieme di case andrà a formare l'isolato. In base alla posizione indicate da questo livello verrano posizionate le case in maniera corretta.

###Livello Street
Questo livello ha il compito di costruire le strade che attraversano il quartiere. Come si può vedere è composto da 3 livelli: una strada percorre il quartiere in un verso, una strada lo percorre in senso opposto e una terza strada incrocia le altre 2 e permette di passare da un lato all'altro

##Visualizzazione da diversi punti di vista

## Modello trovato sul web da cui questo progetto prende ispirazione
![alt text](https://github.com/manusgnao/ggpl/blob/master/2017-01-27/images/model.png "Modello")

## Rappresentazione

![alt text](https://github.com/manusgnao/ggpl/blob/master/2017-01-27/images/isolato.PNG "Isolato")

![alt text](https://github.com/manusgnao/ggpl/blob/master/2017-01-27/images/viale.PNG "Viale")

![alt text](https://github.com/manusgnao/ggpl/blob/master/2017-01-27/images/dettaglio.PNG "Dettaglio")

![alt text](https://github.com/manusgnao/ggpl/blob/master/2017-01-27/images/posteriore.PNG "Vista Posteriore")


