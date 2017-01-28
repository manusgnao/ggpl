# WORKSHOP 10

## Descrizione
Rappresentazione 3D di un edificio, con porte, finestre, tetto e scale.
Questo progetto ha la seguente struttura.
Nella cartella *elements* sono divisi i file .lines e .svg utilizzati per la creazione dei vari elementi.
Ogni cartella contiene una cartella *svg* contenenti i file utilizzati per creare i livelli e una cartella *lines* contenente i file ottunuti dal servizio offerto da [questo](http://cvdlab.github.io/svg2lines/) sito che converte file svg in file lines.
Questi sono le cartelle di *elements*

* base
* doors
* external
* internal
* stairs
* windows

###Livello Base
Questo livello contiene il perimetro di base della casa. Viene utilizzato per costruire il pavimento e il soffitto sia del piano terra, sia del primo piano. Il soffitto del primo piano verrà poi utilizzato come base per la costruzione del tetto.

###Livello Doors
Questa sezione è dedicata alla creazione delle porte. Possiamo vedere che sono presenti 2 livelli. Level-0 contiene le porte del piano terra (compresa la porta di ingresso alla casa), level-1 contiene le porte del primo piano.

###Livello External
Questo livello ha il compito di costruire le mura esterne della casa tenendo in considerazione di lasciare spazio per la costruzione di porte e finestre. I livelli partono dal terreno e arrivano a costruire fino alla base del tetto.

###Livello Internal
Ha il compito di costruire le pareti interne della casa. Anche questi livelli devono tenere conto dello spazio da lasciare alle porte che consentono di passare da una stanza all'altra.

###Livello Stairs
Questo livello crea lo spazio dedicato alla scala che consente il passaggio da un piano all'altro

###Livello Windows
I due livelli presenti in questa sezione rappresentano le finestre di entrambi i piani che andranno costruite negli appositi spazi lasciati nei muri

##Visualizzazione da diversi punti di vista

## Modello trovato sul web da cui questo progetto prende ispirazione
![alt text](https://github.com/manusgnao/ggpl/blob/master/2017-01-13/images/model.jpg "Modello")

## Rappresentazione

![alt text](https://github.com/manusgnao/ggpl/blob/master/2017-01-13/images/alto.PNG "Panoramica")

![alt text](https://github.com/manusgnao/ggpl/blob/master/2017-01-13/images/frontale.PNG "Frontale")

![alt text](https://github.com/manusgnao/ggpl/blob/master/2017-01-13/images/porta.PNG "Porta e Finestre")

![alt text](https://github.com/manusgnao/ggpl/blob/master/2017-01-13/images/finestre.PNG "Finestre")

![alt text](https://github.com/manusgnao/ggpl/blob/master/2017-01-13/images/scala.PNG "Scala")

