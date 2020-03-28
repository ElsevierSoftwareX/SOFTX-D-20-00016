#No Multithreading
import sys
import math
import json
import argparse
import os.path as PATH
import xml.dom.minidom as DOM
import xml.etree.ElementTree as ET
import itertools
import threading
import pandas
from time import time
from collections import namedtuple
from os.path import isfile
from dataclasses import dataclass
from itertools import chain
from operator import attrgetter
from multiprocessing import Pool, Array, Manager
from multiprocessing.dummy import Pool as ThreadPool
from decimal import Decimal, ROUND_DOWN
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class PlayerData:
    "Struttura dati contenente i dati posizionali e le feature del giocatore"
    timestamp : float
    playerID : int
    xPosition : float
    yPosition : float
    direction : float
    velocity : float
    acceleration : float
    accPeak : float
    accPeakReal : float
    dirChange : float
    distToBall : float
    distToTarget : float
    distToGoal : float
    crossOnTargLine : float


# Valore per individuare dall'ID che un giocatore appartiene ad una o all'altra squadra
# playerID < PLAYERVALUE -> squadra in casa
# playerID > PLAYERVALUE -> squadra fuori casa
# playerID = PLAYERVALUE -> palla
PLAYERVALUE = 128

def teamPlayerData(playerValue):
    """
    Funzione che, dato in ingresso l'ID di un giocatore, restituisce una lista così strutturata:
    -il primo elemento vale 0 se il giocatore appartiene alla squadra in casa, 1 se appartiene alla squadra fuori casa
    -il secondo elemento rappresenta l'ID del giocatore escludendo PLAYERVALUE
    """
    if (playerValue < PLAYERVALUE):
        return [0, playerValue]
    elif (playerValue > PLAYERVALUE):
        return [1, playerValue - PLAYERVALUE]
    else:
        return [-1, -1]

# Valore del numero massimo di dati posizionali e feature contenuti in 1 MB
MBVALUE = 2048

# PARSER
class GenericParser():
    "Classe base da cui derivano i diversi parser"
    def __init__(self):
        self.full = False
        self.position = 0

class LineHalfParser(GenericParser):
    """
    Classe che definisce i parser che leggono da file di testo formattati
    come una serie di righe, ogni riga rappresenta i dati posizionali di un giocatore ad un dato frame.
    Questo parser legge solamente un tempo della partita
    """
    def read(self, filename, data, size):
        """
        Legge i dati presenti nel file e li estrae in una lista in memoria

        :param filename: Stringa con il path per il file
        :param data: Lista contenente il dataset
        :param size: Massima occupazione in memoria dei dati in MB
        """
        # calcola il numero di righe totali che può leggere a questa iterazione di lettura, per non eccedere la memoria
        totalMemory = MBVALUE * size
        
        # salta le prime N righe con N = totalmemory, basandosi sull'ultima posizione letta
        with open(filename, 'r') as f:
            i = 0
            line = f.readline().rstrip('\n')
            while (i < self.position and line != ""):
                line = f.readline()
                i = i + 1

            # estrae i dati dal file di testo una riga alla volta e lo inserisce nella lista con il dataset
            while (not self.full and line != ""):
                extractedData = self._extractFromLine(line)
                newEntry = PlayerData(*extractedData, *[-1 for i in range(10)])
                data.append(newEntry)
                line = f.readline().rstrip('\n')
                i = i + 1

                # se hai letto il numero di righe massimo definito dall'occupazione della memoria segna l'ultima posizione a cui è arrivato
                if (i - self.position) >= totalMemory:
                    self.full = True

                    # esamina la lista dall'ultimo elemento a ritroso fino a quando non si trova la palla al frame corrente
                    # in questo modo non si ha l'ultimo frame della lista frammentato con solo una parte dei dati
                    # elimino l'elemento della lista e considero come ultimo elemento l'ultimo prima della palla all'ultimo frame
                    for k in range(len(actualTime)-1,0,-1):
                        element = actualTime.pop(k)
                        i -= 1
                        if(element.playerID == PLAYERVALUE):
                           break 
                    self.position = i
    def _extractFromLine(self, line):
        "Ritorna tutti gli elementi letti sulla riga del file di testo"
        elements = line.split(" ")
        return [float(element) for element in elements]

class LineParser(GenericParser):
    """
    Simile a lineHalfparser ma si segna anche i frame di inizio del secondo tempo per generare i due tempi di una partita
    """
    def read(self, filename, size, halfTimeFrame):
        """
        Legge i dati presenti nel file e li estrae in una lista in memoria.
        Questa lista è a sua volta composta da due liste, la prima per i dati
        del primo tempo e la seconda per il secondo tempo

        :param filename: Stringa con il path per il file
        :param size: Massima occupazione in memoria dei dati in MB
        :param halfTimeFrame: Frame da cui inizia il secondo tempo

        :return due liste, una per il primo tempo e una per il secondo
        """
        # calcola il numero di righe totali che può leggere a questa iterazione di lettura, per non eccedere la memoria
        totalMemory = MBVALUE * size
        firstTime = []
        secondTime = []
        actualTime = firstTime
        data = [firstTime, secondTime]

        # salta le prime N righe con N = totalmemory, basandosi sull'ultima posizione letta
        with open(filename, 'r') as f:
            i = 0
            line = f.readline().rstrip('\n')
            while (i < self.position and line != ""):
                line = f.readline()
                i = i + 1

            # estrae i dati dal file di testo una riga alla volta e lo inserisce nella lista con il dataset
            while (not self.full and line != ""):
                extractedData = self._extractFromLine(line)
                newEntry = PlayerData(*extractedData, *[-1 for i in range(14 - len(extractedData))])
                # aggiunge i dati al tempo corrente, se siamo arrivati al secondo tempo li aggiunge al secondo
                if (int(newEntry.timestamp) == halfTimeFrame):
                    actualTime = secondTime
                actualTime.append(newEntry)
                line = f.readline().rstrip('\n')
                i = i + 1
                
                # se hai letto il numero di righe massimo definito dall'occupazione della memoria segna l'ultima posizione a cui è arrivato
                if (i - self.position) >= totalMemory:
                    self.full = True

                    # esamina la lista dall'ultimo elemento a ritroso fino a quando non si trova la palla al frame corrente
                    # in questo modo non si ha l'ultimo frame della lista frammentato con solo una parte dei dati
                    # elimino l'elemento della lista e considero come ultimo elemento l'ultimo prima della palla all'ultimo frame
                    for k in range(len(actualTime)-1,0,-1):
                        element = actualTime.pop(k)
                        i -= 1
                        if(element.playerID == PLAYERVALUE):
                           break  
                    self.position = i
        return data
    def _extractFromLine(self, line):
        "Ritorna tutti gli elementi letti sulla riga del file di testo"
        elements = line.split(" ")
        return [float(element) for element in elements]

class LinePandaParser(GenericParser):
    """
    Come LineParser, ma utilizza Pandas per essere ottimizzare al massimo il processo
    """
    def read(self, filename, size, halfTimeFrame, isFeature = False):
        """
        Legge i dati presenti nel file e li estrae in una lista in memoria.
        Questa lista è a sua volta composta da due liste, la prima per i dati
        del primo tempo e la seconda per il secondo tempo

        :param filename: Stringa con il path per il file
        :param size: Massima occupazione in memoria dei dati in MB
        :param halfTimeFrame: Frame da cui inizia il secondo tempo
        :param isFeature: Booleano che indica se si stanno estraendo feature o dati posizionali

        :return due liste, una per il primo tempo e una per il secondo
        """
        # calcola il numero di righe totali che può leggere a questa iterazione di lettura, per non eccedere la memoria
        totalMemory = MBVALUE * size
        firstTime = []
        secondTime = []
        actualTime = firstTime
        data = [firstTime, secondTime]

        # indica i dati da leggere dal file, se si vogliono estrarre solo i dati posizionali o solo le feature
        if (isFeature):
            names = ['timestamp', 'playerID','xPosition','yPosition', 'direction', 'velocity', 'acceleration', 
                     'accPeak', 'accPeakReal','dirChange','distToBall','distToTarget', 'distToGoal', 'crossOnTargLine']
        else:
            names = ['timestamp', 'playerID','xPosition','yPosition']
        
        # estrae una matrice con tutti i dati utilizzando pandas
        parsedData = pandas.read_csv(filename, sep=' ', engine='c', skiprows=int(self.position), nrows=totalMemory, memory_map=True, names=names)
        
        # aggiunge i dati per ogni riga della matrice alla lista di PlayerData 
        for row in parsedData.itertuples(name=None):
            newEntry = PlayerData(*row[1:], *[-1 for i in range(14 - len(row)+1)])
            if (int(newEntry.timestamp) == halfTimeFrame):
                actualTime = secondTime
            actualTime.append(newEntry)
        # se hai letto il numero di righe massimo definito dall'occupazione della memoria segna l'ultima posizione a cui è arrivato
        if (len(parsedData) >= totalMemory):
            self.full = True
        self.position += len(parsedData)
        if (self.full):
            # esamina la lista dall'ultimo elemento a ritroso fino a quando non si trova la palla al frame corrente
            # in questo modo non si ha l'ultimo frame della lista frammentato con solo una parte dei dati
            # elimino l'elemento della lista e considero come ultimo elemento l'ultimo prima della palla all'ultimo frame
            for k in range(len(actualTime)-1,0,-1):
                element = actualTime.pop(k)
                self.position -= 1
                if(element.playerID == PLAYERVALUE):
                    break  
        return data
    def _extractFromLine(self, line):
        elements = line.split(" ")
        return [float(element) for element in elements]

# FEATURE EXTRACTION
class FeatureExtractor():
    """Classe con il compito di estrarre le feature a partire dai dati posizionali
       COSE DA SCRIVERE: LA PALLA LA CONSIDERO SEMPRE PRIMA
    """
    def __init__(self, sampling, xDimension, yDimension,isFirstHalf):
        """
        :param sampling: sampling rate del dataset
        :param xDimension: dimensione orizzontale del campo
        :param yDimension: dimensione verticale del campo
        :param isFirstHalf: determina se è il primo tempo della partita o meno
        """
        self.sampligRate = sampling
        self.xDimension = xDimension
        self.yDimension = yDimension
        self.isFirstHalf = isFirstHalf
        self.xGoal1Position, self.xGoal2Position, self.yGoalPosition = self._goalExtractor()
        self.currentTimestamp = -1
        self.ballIndex = -1
    def extract(self, data):
        """
        Estrae le varie feature dalla lista di dati posizionali
        Per motivi implementativi ho deciso che nello scorrere vengono estratte le feature per l'elemento precedente,
        questo ha reso necessario la funzione "firstElementAccPeak" in quanto si tratta di feature che fanno riferimento
        sia all'elmeneto precedente che quello successivo
        E' necessario ripetere il ciclo di estrazione più volte in quanto ogni volta è necessario che sia stata estratta una feature precedente 
        """
        for i,element in enumerate(data):
            if i >= 23:
                self._extractDirection(data, i)
                self._extractVelocity(data, i)
                self._extractDistToBall(data, i)
                self._extractDistToTarget(data, i)
                self._extractDistToGoal(data, i)
                self._extractCrossOnTargLine(data, i)
        for i,element in enumerate(data):
            if i >= 23:
                self._extractAcceleration(data, i)
                self._extractDirChange(data, i)
        for i,element in enumerate(data):
            if i >= 23:
                self._extractAccPeak(data, i)
        for i,element in enumerate(data):
            if i >= 23:
                self._extractAccPeakReal(data, i)
        self.ballIndex = -1
        for i in range(23):
            self._firstElementAccPeak(data,i)
            if (i != 0):
                self._extractDistToBall(data, i)
                self._extractDistToTarget(data, i)
                self._extractDistToGoal(data, i)
        self.ballIndex = -1
    def compact(self, data):
        """
        Crea una nuova versione compatta dei dati che si possono scorrere più facilmente a seconda del timestamp,
        sarà utile all'event detector e per creare il json di riferimento
        """
        newData = []
        homeTeam = []
        awayTeam = []
        ballIndex = -1
        currentTimestamp = data[0].timestamp
        for i,element in enumerate(data):
            # separa gli elementi per timestamp, in modo da avere un elemento della lista rappresentante l'intero frame
            if element.timestamp != currentTimestamp :
                homeTeam.sort(key = attrgetter('playerID'))
                awayTeam.sort(key = attrgetter('playerID'))
                newData.append({'timestamp' : currentTimestamp , 'ball' : data[ballIndex] ,
                                'homeTeam' : homeTeam.copy(),
                                'awayTeam' : awayTeam.copy()})
                homeTeam.clear()
                awayTeam.clear()
                currentTimestamp = element.timestamp
            if element.playerID == PLAYERVALUE:
                ballIndex = i
            elif element.playerID < PLAYERVALUE:
                homeTeam.append(element)
            elif element.playerID > PLAYERVALUE:
                awayTeam.append(element)
            if i == (len(data) - 1) :
                homeTeam.sort(key=attrgetter('playerID'))
                awayTeam.sort(key=attrgetter('playerID'))
                newData.append({'timestamp': currentTimestamp, 'ball': data[ballIndex],
                                'homeTeam': homeTeam.copy(),
                                'awayTeam': awayTeam.copy()})
                homeTeam.clear()
                awayTeam.clear()
        return newData
    def _goalExtractor(self):
        """
        Estrae la posizione della porta, da modificare nel caso si decidano sistemi di riferimento diversi ()
        SISTEMA DI RIFERIMENTO DESCRITTO NEL FILE
        """
        return [0, self.xDimension, self.yDimension/2]
    def _currentPlayerGoal(self, playerID):
        "Ritorna una lista con, in ordine, la propria porta e la porta avversaria, in base al tempo della partita"
        if((playerID < PLAYERVALUE and self.isFirstHalf) or (playerID > PLAYERVALUE and (not self.isFirstHalf))):
            return [self.xGoal1Position, self.xGoal2Position]
        elif ((playerID < PLAYERVALUE and (not self.isFirstHalf)) or (playerID > PLAYERVALUE and  self.isFirstHalf)):
            return [self.xGoal2Position, self.xGoal1Position]
        else:
            return [-1,-1]
    def _findBall(self, data, index):
        "Ritorna l'indice della palla nel timestamp corrente"
        currentTimestamp = data[index - 1].timestamp
        i = 0
        upperFound, lowerFound = [False, False]
        while ((not upperFound) or (not lowerFound)):
            if (data[(index - 1 + i) % len(data)].timestamp != currentTimestamp) and not(upperFound) :
                maxIndex = index - 2 + i
                upperFound = True
            if (data[index - 1 - i].timestamp != currentTimestamp) and not(lowerFound) :
                minIndex = index - i
                lowerFound = True
            i += 1
        for i in range(minIndex, maxIndex):
            if (data[i].playerID == PLAYERVALUE):
                return i
    def _firstElementAccPeak(self,data, index):
        "Assegna il picco di accelerazione ai primi 23 elementi, che non vengono considerati dal ciclo for dell'estrattore"
        data[index].accPeak = data[index].acceleration
        if (math.fabs(data[index].accPeak) > math.fabs(data[index + 23].accPeak)):
            data[index].accPeakReal = data[index].accPeak
        else:
            data[index].accPeakReal = 0

    def _extractDirection(self, data, index):
        "Estrae la direzione in cui è si muove l'oggetto (DIFFERENZA CON DESCRIZIONE ORIGINALE)"
        data[index - 23].direction = math.atan2(data[index].yPosition - data[index - 23].yPosition ,
                                      data[index].xPosition - data[index - 23].xPosition)
    def _extractVelocity(self, data, index):
        "Estrae la velocita a cui si muove l'oggetto"
        data[index - 23].velocity = self.sampligRate * math.hypot((data[index].yPosition - data[index - 23].yPosition),
                                                                 (data[index].xPosition - data[index - 23].xPosition))
    def _extractAcceleration(self, data, index):
        "Estrae l'accelerazione subita dall'oggetto rispetto all'ultimo frame"
        data[index - 23].acceleration = data[index].velocity - data[index-23].velocity
    def _extractAccPeak(self, data, index):
        "Estrae il picco di accelerazione subito dall'oggetto, serve per trovare la presenza di un picco di accelerazione reale"
        if (data[index - 23].acceleration >= 0):
            data[index].accPeak = data[index - 23].acceleration + max(0,data[index].acceleration)
        else:
            data[index].accPeak = data[index - 23].acceleration + min(0, data[index].acceleration)
    def _extractAccPeakReal(self, data, index):
        """
        Estrae il picco di accelerazione reale, il metodo segue quello descritto nel paper con aggregazione di due frame consecutivi
        """
        if index >= (len(data) - 23):
            nextElementPeak = data[index - 23].accPeak
        else:
            nextElementPeak = data[index + 23].accPeak

        if (((math.fabs(data[index].accPeak) > math.fabs(data[index - 23].accPeak))) and
            (math.fabs(data[index].accPeak) > math.fabs(nextElementPeak))):
            data[index].accPeakReal = data[index].accPeak
        else:
            data[index].accPeakReal = 0
    def _extractDirChange(self, data, index):
        "Estrae il cambio di direzione rispetto a quella precedente"
        data[index - 23].dirChange = math.fabs(data[index].direction - data[index - 23].direction)
    def _extractDistToBall(self, data, index):
        """
        Estrae la distanza del giocatore corrente dalla palla,
        motivo per cui cerca di capire quale sia l'indice della palla per il timestamp corrente
        """
        if (self.ballIndex == -1):
            self.ballIndex = self._findBall(data, index)
        if (data[index - 1].playerID != PLAYERVALUE):
            if (self.ballIndex is None):
                print('BALL IS NULL')
                print('{}: Data lenght: {} Index - 1 : {} Ball index: {}'.format(threading.current_thread(), len(data),index - 1, self.ballIndex))
            try:
                data[index - 1].distToBall = math.hypot((data[self.ballIndex].yPosition - data[index - 1].yPosition),
                                             (data[self.ballIndex].xPosition - data[index - 1].xPosition))
            except IndexError as e:
                print("\nData lenght: {}\nIndex - 1 : {}\nBall index: {}\n".format(len(data),index - 1, self.ballIndex))
                raise e
        else:
            data[index - 1].distToBall = -1
        if (data[index - 1].timestamp != data[index].timestamp):
            self.ballIndex = -1
    def _extractDistToTarget(self, data, index):
        "Estrae la distanza del giocatore dalla porta avversaria"
        thisGoalxPosition = self._currentPlayerGoal(data[index-1].playerID)[1]
        if thisGoalxPosition != -1:
            data[index - 1].distToTarget = math.hypot((self.yGoalPosition - data[index - 1].yPosition),
                                                      (thisGoalxPosition - data[index - 1].xPosition))
        else:
            data[index - 1].distToTarget = -1
    def _extractDistToGoal(self, data, index):
        "Estrae la distanza del giocatore dalla propria porta"
        thisGoalxPosition = self._currentPlayerGoal(data[index-1].playerID)[0]
        if thisGoalxPosition != -1:
            data[index - 1].distToGoal = math.hypot((self.yGoalPosition - data[index - 1].yPosition),
                                                      (thisGoalxPosition - data[index - 1].xPosition))
        else:
            data[index - 1].distToGoal = -1
    def _extractCrossOnTargLine(self, data, index):
        "Estrae il momento in cui l'oggetto intersecherà la linea di fondo campo proseguendo nella stessa direzione"
        thisGoalxPosition = self._currentPlayerGoal(data[index - 23].playerID)[1]
        if thisGoalxPosition != -1:
            data[index - 23].crossOnTargLine = math.fabs(data[index - 23].yPosition - self.yGoalPosition +
                                                        math.tan(data[index - 23].direction) *
                                                        (thisGoalxPosition - data[index - 23].xPosition))
        else:
            data[index - 23].crossOnTargLine = -1

# EVENT DETECTOR
class GenericEvent:
    def recognize(self, data, index):
        """
        Da ridefinire nelle classi figlie, riconosce l'evento

        :param data:
        :param index:
        :return:
        """
        pass
    def _setEvent(self, data, index, player):
        "Da ridefinire nelle classi figlie, crea un dizionario che descrive l'evento riconosciuto"
        return None
    def _readFromFile(self, file):
        "Se viene passata una lista di stringe la utilizza per leggere le soglie, se no apre il file"
        if (PATH.isfile(file)):
            with open(file, 'r') as f:
                self._readFromLines(f)
        elif (type(file) is list):
            self._readFromLines(file)
    def _readFromLines(self, lines):
        "Per ogni linea nella lista controlla la versione dell'evento, se corrisponde utilizza quella linea per inizializzare l'evento"
        for line in lines:
            elements = line.rstrip('\n').split(" ")
            if elements[0] == self.name :
                if elements[1] == self.version :
                    elements = [float(element) for element in elements[2:]]
                    self._initialize(elements)
                    return
                else:
                    print("La versione del modulo per l'evento {} non coincide con quella nel file".format(self.name))
                    raise Exception("Versione sbagliata")
        print("Non è stata trovata una riga di testo per inizializzare correttamente il modulo")
        raise Exception("Evento non nel file")
    def _initialize(self, list):
        "Da ridefinire nelle classi figlie, inizializza le soglie"
        pass


class PlayerEvent(GenericEvent):
    "Classe base per tutti gli eventi di cui fa parte almeno un giocatore"
    def recognize(self, data, index):
        """
        Funzione base che riconosce gli eventi controllando la precondizione e poi iterando la condizione specifica
        dell'evento per ogni istante della finestra temporale

        :param data: Dataset compatto con dati posizionali e feature
        :param index: Indice da cui inizia la finestra
        :return: Un dizionario con l'evento riconosciuto, None in caso non sia stato riconosciuto nulla
        """
        # Controlla se la precondizione è verificata
        result, selectedPlayer = self._checkPrecondition(data, index)
        if not result:
            return [None, index]

        self.middlePlayer = None
        # Loop che itera per tutta la durata della finestra temporale e controlla che la condizione sia verificata
        for i in range(1, int(self.windowSize)):
            if (i == math.floor(self.windowSize/2)):
                isMiddle = True
            else:
                isMiddle = False
            if (index + i) >= len(data) :
                return [None, index]
            elif not self._checkCondition(data, index + i, selectedPlayer, isMiddle) :
                return [None, index]
        
        # Controlla se la postcondizione è verificata
        if not(self._checkPostcondition(data, index + int(self.windowSize)-1, selectedPlayer)):
            return [None, index]
        # Se non è ritornata mentre scorreva la finestra si suppone che l'evento sia stato trovato e si cambia l'index della ricerca
        output = self._setEvent(data,index, self.middlePlayer)
        if output != None :
            index += math.floor(self.windowSize/self.stride)
        return [output, int(index)]
    def _checkCondition(self, data, index, selectedPlayer, isMiddle):
        "Funzione da sovrascrivere nelle classi figlie, verifica le condizioni specifiche per ogni evento"
        pass

    def _checkPrecondition(self, data, index):
        """
        Funzione funzione per verificare la precondizione, controlla che la distanza del giocatore più vicino alla palla
        sia inferiore alla soglia predefinita

        :param data: Dataset compatto con dati posizionali e feature
        :param index: Indice da cui inizia la finestra
        :return: Una lista avente come primo elemento un booleano che descrive se la condizione è verificata e come secondo elemento il giocatore che la verifica
        """
        # Trovo il giocatore con la minima distanza dalla palla
        minimum = 1000
        playerIndex = -1
        for i,player in enumerate(chain(data[index].get('homeTeam'), data[index].get('awayTeam'))):
            if (player.distToBall < minimum):
                minimum = player.distToBall
                playerIndex = i

        # Se la distanza è inferiore alla soglia inserisco ritorno il giocatore trovato
        if minimum > self.threshold1:
            return [False, -1]
        else:
            homeLenght = len(data[index].get('homeTeam'))
            teamString = 'homeTeam'
            if playerIndex >= homeLenght:
                playerIndex -= homeLenght
                teamString = 'awayTeam'
            return [True, data[index].get(teamString)[playerIndex]]
    def _checkPostcondition(self, data, index, selectedPlayer):
        "Postcondizione, di base non ce ne sono per cui restiuisce sempre true"
        return True

class KickEvent(PlayerEvent):
    "Classe che definisce l'event detector per il calcio alla palla"
    def __init__(self, file):
        """
        :param file: File contenente una lista di parametri di inizializzazione per il modulo
        """
        self.name = "KickingTheBall"
        self.version = "3.0"
        self.accelerationCheck = False
        if not(file is None):
            self._readFromFile(file)
            #print('Event: {}\nVersion: {}\nWindow: {}\nThreshold 1: {}\n'.format(self.name, self.version, self.windowSize, self.threshold1))
        self.middlePlayer = None
        self.stride = 1
    def _checkPrecondition(self, data, index):
        "Controlla che negli windowSize/2 frame precedenti ci sia stata un'accelerazione superiore alla soglia"
        for i in range(math.floor(self.windowSize/2)):
            if not(self.accelerationCheck) and ((index - i) >= 0) :
                if (data[index-i].get('ball').acceleration > self.threshold2):
                        self.accelerationCheck = True
        return super()._checkPrecondition(data, index)
    def _checkCondition(self, data, index, selectedPlayer, isMiddle):
        """
        Verifica che la palla si stia allontanando dal giocatore

        :param data: Dataset compatto con dati posizionali e feature
        :param index: Indice su cui verificare la condizione
        :param selectedPlayer: Giocatore su cui verificare la condizione
        :param isMiddle: Booleano che indica se è il frame intermedio o no
        :return: Un booleano che indica se la condizione è verificata o meno
        """
        condition = False
        for player in chain(data[index].get('homeTeam'), data[index].get('awayTeam')):
            if (player.playerID == selectedPlayer.playerID):
                if (isMiddle):
                    self.middlePlayer = player
                if not (self.accelerationCheck):
                    if (data[index].get('ball').acceleration > self.threshold2):
                        self.accelerationCheck = True
                # controlla che la palla si stia allontanando dal giocatore
                if (player.distToBall > selectedPlayer.distToBall):
                    condition = True
                    break
        return condition
    def _checkPostcondition(self, data, index, selectedPlayer):
        "Aggiunta ora, cancellare per tornare alla vecchia versione. Controlla che alla fine la palla si trovi al di fuori della soglia con una velocità elevata"
        condition = False
        for player in chain(data[index].get('homeTeam'), data[index].get('awayTeam')):
            if (player.distToBall > self.threshold1) and (player.playerID == selectedPlayer.playerID):
                if (self.accelerationCheck) and (data[index].get('ball').velocity > self.threshold2):
                    condition = True
        self.accelerationCheck = False
        return condition
    def _setEvent(self,data,index,player):
        return [{'event' : 'KickingTheBall',
                'timestamp' : player.timestamp,
                'playerId' : int(teamPlayerData(player.playerID)[1]),
                'teamId' : teamPlayerData(player.playerID)[0],
                'x' : round(player.xPosition,1),
                'y' : round(player.yPosition,1)}]
    def _initialize(self, list):
        #distanza, velocità alla fine, picco di accelerazione
        self.windowSize, self.threshold1, self.threshold2 = list

class PossessionEvent(PlayerEvent):
    "Classe che definisce l'event detector per il possesso palla"
    def __init__(self, file, halfTimeFrame, goalkeeper0, goalkeeper1):
        """
        :param file: File contenente una lista di parametri di inizializzazione per il modulo
        """
        self.name = "BallPossession"
        self.version = "3.0"
        if not(file is None):
            self._readFromFile(file)
            #print('Event: {}\nVersion: {}\nWindow: {}\nThreshold 1: {}\nThreshold 2: {}\n'.format(self.name, self.version, self.windowSize, self.threshold1, self.threshold2))
        self.lastPlayer = None # Giocatore avversario più vicino alla sua porta
        self.halfTimeFrame = halfTimeFrame
        self.middlePlayer = None
        self.stride = 1
        self.GOALKEEPER0 = goalkeeper0
        self.GOALKEEPER1 = goalkeeper1
    def _checkPrecondition(self, data, index):
        "Controlla che la velocità sia inferiore alla soglia"
        condition =  super()._checkPrecondition(data, index)
        if (data[index].get('ball').velocity > self.threshold3):
            condition[0] = False
        return condition
    def _checkCondition(self, data, index, selectedPlayer, isMiddle):
        """
        Verifica che la palla rimanga vicina al giocatore e sia l'unico giocatore nella soglia più grande

        :param data: Dataset compatto con dati posizionali e feature
        :param index: Indice su cui verificare la condizione
        :param selectedPlayer: Giocatore su cui verificare la condizione
        :return: Un booleano che indica se la condizione è verificata o meno
        """

        # Trova il giocatore più vicino alla palla
        minimum = 1000
        condition = True
        minPlayer = None

        for player in chain(data[index].get('homeTeam'), data[index].get('awayTeam')):
            if (player.distToBall < minimum):
                minimum = player.distToBall
                minPlayer = player

        if minPlayer == None :
            return False

        # Verifica che sia ancora il giocatore che dovrebbe avere il controllo palla
        if selectedPlayer.playerID == minPlayer.playerID:
            if (isMiddle):
                self.middlePlayer = minPlayer

            # Seleziona la squadra avversaria
            teamString = 'homeTeam'
            if (selectedPlayer.playerID < PLAYERVALUE):
                teamString = 'awayTeam'

            # individua il lato in cui gioca la squadra avversaria
            if ((teamString == 'awayTeam') and (selectedPlayer.timestamp < self.halfTimeFrame)) or ((teamString == 'homeTeam') and (selectedPlayer.timestamp >= self.halfTimeFrame)):
                side = 'right'
            else:
                side = 'left'

            # Verifica che non ci siano giocatori avversari intorno al giocatore e segna il giocatore avversario più vicino alla propria porta
            minimum = 1000
            maximum = -1000
            for player in data[index].get(teamString):
                distance = math.hypot(player.yPosition - minPlayer.yPosition,
                                      player.xPosition - minPlayer.xPosition)
                if distance < self.threshold2:
                    condition = False
                if (player.playerID != self.GOALKEEPER0) and (player.playerID != self.GOALKEEPER1):
                    if (side == 'left'):
                        if player.xPosition < minimum:
                            minimum = player.xPosition
                            if (isMiddle):
                                self.lastPlayer = player
                    else:
                         if player.xPosition > maximum:
                            maximum = player.xPosition
                            if (isMiddle):
                                self.lastPlayer = player
            
            # Controllo che la palla non sia in rimessa laterale (bordo inferiore)
            # a) la velocità della palla inferiore a 0.1
            # b) la posizione in prossimità della linea di bordo campo
            if data[index].get('ball').velocity < 0.1 and data[index].get('ball').yPosition > -0.5 and data[index].get('ball').yPosition < 0.5:
                return False

            # Controllo che la palla non sia in rimessa laterale (bordo superiore)
            # a) la velocità della palla inferiore a 0.1
            # b) la posizione in prossimità della linea di bordo campo
            if data[index].get('ball').velocity < 0.1 and data[index].get('ball').yPosition > 71.5 and data[index].get('ball').yPosition < 72.5:
                return False

        else:
            condition = False
        return condition
    def _checkPostcondition(self, data, index, selectedPlayer):
        "Aggiunta ora, cancellare per tornare alla vecchia versione. Controlla che alla fine la abboa velocità inferiore alla soglia"
        condition = True
        if (data[index].get('ball').velocity > self.threshold3):
            condition = False
        return condition
    def _setEvent(self,data,index,player):
        return [{'event' : 'BallPossession',
                'timestamp' : player.timestamp,
                'playerId' : int(teamPlayerData(player.playerID)[1]),
                'teamId' : teamPlayerData(player.playerID)[0],
                'x' : round(player.xPosition,1),
                'y' : round(player.yPosition,1),
                'outermostOtherTeamDefensivePlayerId' : int(teamPlayerData(self.lastPlayer.playerID)[1]),
                'outermostOtherTeamDefensivePlayerTeamId' : teamPlayerData(self.lastPlayer.playerID)[0],
                'outermostOtherTeamDefensivePlayerX' : round(self.lastPlayer.xPosition,1),
                'outermostOtherTeamDefensivePlayerY' : round(self.lastPlayer.yPosition,1)}]
    def _initialize(self, list):
        # distanza minima, massima e velocità
        self.windowSize, self.threshold1,self.threshold2, self.threshold3 = list

class TackleEvent(PlayerEvent):
    "Classe che definisce l'event detector per il contrasto"
    def __init__(self, file):
        """
        :param file: File contenente una lista di parametri di inizializzazione per il modulo
        """
        self.name = "Tackle"
        self.version = "3.0"
        if not(file is None):
            self._readFromFile(file)
            #print('Event: {}\nVersion: {}\nWindow: {}\nThreshold 1: {}\nThreshold 2: {}\n'.format(self.name, self.version, self.windowSize, self.threshold1, self.threshold2))
        self.tacklingPlayer = None  # Giocatore che sta facendo il contrasto
        self.middlePlayer = None
        self.stride = 1
    def _checkPrecondition(self, data, index):
        "Controlla che la velocità sia inferiore alla soglia"
        condition =  super()._checkPrecondition(data, index)
        if (data[index].get('ball').velocity > self.threshold3):
            condition[0] = False
        return condition
    def _checkCondition(self, data, index, selectedPlayer, isMiddle):
        """
        Verifica che la palla rimanga vicina al giocatore e non sia l'unico giocatore nella soglia più grande

        :param data: Dataset compatto con dati posizionali e feature
        :param index: Indice su cui verificare la condizione
        :param selectedPlayer: Giocatore su cui verificare la condizione
        :return: Un booleano che indica se la condizione è verificata o meno
        """

        # Trova il giocatore più vicino alla palla
        minimum = 1000
        condition = False
        minPlayer = None

        for player in chain(data[index].get('homeTeam'), data[index].get('awayTeam')):
            if (player.distToBall < minimum):
                minimum = player.distToBall
                minPlayer = player

        # Verifica che sia ancora il giocatore che dovrebbe avere il controllo palla
        if selectedPlayer.playerID == minPlayer.playerID:
            if (isMiddle):
                self.middlePlayer = minPlayer
            #seleziona la squadra avversaria
            teamString = 'homeTeam'
            if selectedPlayer.playerID < PLAYERVALUE:
                teamString = 'awayTeam'

            # Verifica che non ci siano giocatori avversari intorno al giocatore e salva il giocatore che effettua il contrasto
            for player in data[index].get(teamString):
                distance = math.hypot(player.yPosition - minPlayer.yPosition,
                                      player.xPosition - minPlayer.xPosition)
                if distance < self.threshold2:
                    condition = True
                    self.tacklingPlayer = player
                    break
        return condition
    def _checkPostcondition(self, data, index, selectedPlayer):
        "Aggiunta ora, cancellare per tornare alla vecchia versione. Controlla che alla fine la abboa velocità inferiore alla soglia"
        condition = True
        if (data[index].get('ball').velocity > self.threshold3):
            condition = False
        return condition
    def _setEvent(self,data,index,player):
         return [#{'event' : 'Tackle',
        #          'timestamp' : player.timestamp - math.floor(self.windowSize/2),
        #          'playerId' : int(teamPlayerData(player.playerID)[1]),
        #          'teamId' : teamPlayerData(player.playerID)[0],
        #          'x' : round(player.xPosition,1),
        #          'y' : round(player.yPosition,1),
        #          'tacklingPlayerId' : int(teamPlayerData(self.tacklingPlayer.playerID)[1]),
        #          'tacklingPlayerTeamId' : teamPlayerData(self.tacklingPlayer.playerID)[0],
        #          'tacklingPlayerX' : round(self.tacklingPlayer.xPosition),
        #          'tacklingPlayerY' : round(self.tacklingPlayer.yPosition,1)},
                {'event' : 'Tackle',
                'timestamp' : player.timestamp,
                'playerId' : int(teamPlayerData(player.playerID)[1]),
                'teamId' : teamPlayerData(player.playerID)[0],
                'x' : round(player.xPosition,1),
                'y' : round(player.yPosition,1),
                'tacklingPlayerId' : int(teamPlayerData(self.tacklingPlayer.playerID)[1]),
                'tacklingPlayerTeamId' : teamPlayerData(self.tacklingPlayer.playerID)[0],
                'tacklingPlayerX' : round(self.tacklingPlayer.xPosition),
                'tacklingPlayerY' : round(self.tacklingPlayer.yPosition,1)}#,
                #  {'event' : 'Tackle',
                #   'timestamp' : player.timestamp + math.floor(self.windowSize/2),
                #   'playerId' : int(teamPlayerData(player.playerID)[1]),
                #   'teamId' : teamPlayerData(player.playerID)[0],
                #   'x' : round(player.xPosition,1),
                #   'y' : round(player.yPosition,1),
                #   'tacklingPlayerId' : int(teamPlayerData(self.tacklingPlayer.playerID)[1]),
                #   'tacklingPlayerTeamId' : teamPlayerData(self.tacklingPlayer.playerID)[0],
                #   'tacklingPlayerX' : round(self.tacklingPlayer.xPosition),
                #   'tacklingPlayerY' : round(self.tacklingPlayer.yPosition,1)}
                ]
    def _initialize(self, list):
        #distanza interna, esterna e velocità
        self.windowSize, self.threshold1, self.threshold2, self.threshold3 = list

class BallDeflectionEvent(PlayerEvent):
    "Classe che definisce l'event detector per la deflessione palla"
    def __init__(self, file, goalkeeper0, goalkeeper1):
        """
        :param file: File contenente una lista di parametri di inizializzazione per il modulo
        """
        self.name = "BallDeflection"
        self.version = "3.0"
        self.accelerationCheck = False
        if not(file is None):
            self._readFromFile(file)
            #print('Event: {}\nVersion: {}\nWindow: {}\nThreshold 1: {}\n'.format(self.name, self.version, self.windowSize, self.threshold1))
        self.middlePlayer = None
        self.stride = 1
        self.GOALKEEPER0 = goalkeeper0
        self.GOALKEEPER1 = goalkeeper1
    def _checkPrecondition(self, data, index):
        "Controlla che negli windowSize/2 frame precedenti ci sia stata un'accelerazione superiore alla soglia"
        "e che la palla sia vicina i piedi di un giocatore diverso dal portiere"
        
        # minimum = 1000
        # playerIndex = -1
        # for i,player in enumerate(chain(data[index].get('homeTeam'), data[index].get('awayTeam'))):
        #     if (player.playerID != GOALKEEPER0 and player.playerID != GOALKEEPER1):
        #         if (player.distToBall < minimum):
        #             minimum = player.distToBall
        #             playerIndex = i

        # if minimum > self.threshold2:
        #     return [False, -1]
        # else:
        #     for i in range(math.floor(self.windowSize/2)):
        #         if not(self.accelerationCheck) and ((index - i) >= 0) :
        #             if (data[index-i].get('ball').acceleration < -self.threshold3):
        #                 self.accelerationCheck = True
        
        self.accelerationCheck = True

        # print("BallkeeperDeflection - Precondition passed at frame:" + str(index))
        return super()._checkPrecondition(data, index)


    def _checkCondition(self, data, index, selectedPlayer, isMiddle):
        """
        Verifica che ci sia stato un contatto tra il portiere e la palla

        :param data: Dataset compatto con dati posizionali e feature
        :param index: Indice su cui verificare la condizione
        :param selectedPlayer: Giocatore su cui verificare la condizione
        :return: Un booleano che indica se la condizione è verificata o meno
        """
        condition = False

        if not self.accelerationCheck:
            return condition

        # Per ogni giocatore
        for player in chain(data[index].get('homeTeam'), data[index].get('awayTeam')):

            # Controllo che il giocatore a fare la deviazione sia un portiere
            if selectedPlayer.playerID != self.GOALKEEPER0 and selectedPlayer.playerID != self.GOALKEEPER1:
                return False

            # Controllo che la palla sia veloce
            # if data[index].get('ball').velocity < self.threshold2:
            #    return False

            # Storicizzo il portiere, per l'emissione finale
            if (isMiddle):
                self.middlePlayer = selectedPlayer

            # # Se giocatore diverso dal portiere
            # if (player.playerID != selectedPlayer.playerID):

            #     # Controllo che la sua distanza dalla palla sia maggiore rispetto a quella del portiere
            #     if (player.distToBall < selectedPlayer.distToBall):
            #         return False
       
        condition = True
        # print("BallkeeperDeflection - Condition passed at frame:" + str(index))
        return condition

    def _checkPostcondition(self, data, index, selectedPlayer):
        "Aggiunta ora, cancellare per tornare alla vecchia versione. Controlla che alla fine la palla si trovi al di fuori della soglia"
        condition = True
        #  for player in chain(data[index].get('homeTeam'), data[index].get('awayTeam')):
        #     if (player.distToBall > self.threshold1) and (player.playerID == selectedPlayer.playerID):
        #         if (self.accelerationCheck) and (data[index].get('ball').velocity > self.threshold2):
        #             condition = True
        self.accelerationCheck = False
        return condition
    def _setEvent(self,data,index,player):
        return [{'event': 'BallDeflection',
                    'timestamp': player.timestamp,
                    'playerId' : int(teamPlayerData(player.playerID)[1]),
                    'teamId' : teamPlayerData(player.playerID)[0],
                    'x': player.xPosition,
                    'y': player.yPosition}]
    def _initialize(self, list):
        #distanza, velocità alla fine, picco di accelerazione, distanza dalla porta avversaria
        self.windowSize, self.threshold1, self.threshold2, self.threshold3, self.threshold4 = list

class BallOutEvent(GenericEvent):
    "Classe che definisce l'event detector per la palla fuori"
    def __init__(self, file, xDimension, yDimension, specialEvents):
        """
        :param file: File contenente una lista di parametri di inizializzazione per il modulo
        """
        self.name = "BallOut"
        self.version = "2.0"
        if not(file is None):
            self._readFromFile(file)
            #print('Event: {}\nVersion: {}\nWindow: {}\n'.format(self.name, self.version, self.windowSize))
        self.xDimension = xDimension
        self.yDimension = yDimension
        self.stride = self.windowSize
        self.specialEvents = specialEvents

    def recognize(self, data, index):
        """
        Funzione che identifica se la palla è uscita fuori dal campo durante la finestra temporale
        In particolare controlla che sia uscita o dalle linee di fondo campo, o dai bordi laterali 
        e non considera la porta e le zone da cui può avvenire il calcio d'angolo

        :param data: Dataset compatto con dati posizionali e feature
        :param index: Indice da cui inizia la finestra
        :return: Un dizionario con l'evento riconosciuto, None in caso non sia stato riconosciuto nulla
        """
        minFieldLine, maxFieldLine = self._fieldLimit()
        minFieldCorner, maxFieldCorner = self._fieldCorner()
        minGoalLimit, maxGoalLimit = self._goalLimit()
        startBall = data[index].get('ball')

        emit = False
        startBall = data[index + 0].get('ball')
        if index+int(self.windowSize) < len(data):
            # TODO: ci vuole una variabile globale (x domani - compiti per casa)
            endBall = data[index + int(self.windowSize)].get('ball')
        else:
            return [None, index]

        # All'inizio la palla deve essere entro le dimensioni del campo da calcio
        if (minFieldLine < startBall.xPosition) and (startBall.xPosition < maxFieldLine) and (minFieldCorner < startBall.yPosition) and (startBall.yPosition < maxFieldCorner):

            # Alla fine (della finestra di osservazione) la palla deve essere fuori dal campo tranne
            # a) nella zona delle due porte
            if (endBall.xPosition < 0 - 0.1 or endBall.xPosition > maxFieldLine + 0.1) and (endBall.yPosition < minGoalLimit or endBall.yPosition > maxGoalLimit):
                emit = True
            elif (endBall.xPosition <-5  or endBall.xPosition > maxFieldLine +5):
                emit = True
            elif (endBall.yPosition < 0 - 0.1 or endBall.yPosition > maxFieldCorner + 0.1):
                emit = True
            else:
                # Controlla corner inferiore sinistro
                if (endBall.xPosition < 0 and endBall.xPosition > -2 and endBall.yPosition > -2 and endBall.yPosition < 0):
                    emit = False
                # Controlla corner superiore sinistro
                elif (endBall.xPosition < 0 and endBall.xPosition > -2 and endBall.yPosition < maxFieldCorner+2 and endBall.yPosition > maxFieldCorner):
                    emit = False
                # Controlla corner inferiore destro
                elif (endBall.xPosition > maxFieldLine and endBall.xPosition < maxFieldLine+2 and endBall.yPosition > -2 and endBall.yPosition < 0):
                    emit = False
                # Controlla corner superiore destro
                elif (endBall.xPosition > maxFieldLine and endBall.xPosition < maxFieldLine+2 and endBall.yPosition < maxFieldCorner+2 and endBall.yPosition > maxFieldCorner):
                    emit = False
                
        
        # la palla è fuori dal campo ma all'altezza delle porte (dietro lo specchio della porta)
        elif (startBall.xPosition < 0 or startBall.xPosition > maxFieldLine) and (startBall.yPosition > minGoalLimit and startBall.yPosition < maxGoalLimit):
            if (endBall.xPosition <-5  or endBall.xPosition > maxFieldLine +5):
                emit = True


      
        if emit == True:
            ballOutFrame = int(startBall.timestamp + self.windowSize)
            # print("Emitting BallOut at frame", str(ballOutFrame))
            
            # Controllo che il BallOut non sia successivo ad un evento speciale
            # ossia un fuorigioco, un fallo, o un rigore

            # Per ogni lista di eventi
            for lst in self.specialEvents:
                for event in lst:

                    #frame BallOut -> 28951
                    #frame Penalty -> 28928

                    # Controllo che il momento di BallOut sia successivo a "event"
                    # entro un certo range (il range di osservazione)
                    frame = event[0]
                    #print("Checking Offside... Frame", str(frame))
                    # Il frame corrente (index) è successivo al momento di evento speciale
                    if ballOutFrame >= frame:
                        # print("Offside at frame", str(frame), "\tBallOut at frame", str(ballOutFrame))
                        if (ballOutFrame - frame) <= self.windowSize + 100:
                            print("Canceling BallOut at frame", str(ballOutFrame))
                            emit = False
                            index += self.stride
                            return [None, int(index)]



            output = self._setEvent(startBall, index, startBall)
            # Sposto la finestra di una lunghezza pari allo stride
            # (lo stride corrisponde alla finestra di osservazione, stride = windowsSize)
            index += self.stride
            return [output, int(index)]
        else:
            return [None, int(index)]
    def _fieldLimit(self):
        """
        Estrae la posizione del fondo campo, da modificare nel caso si decidano sistemi di riferimento diversi ()
        """
        return [0, self.xDimension]
    def _fieldCorner(self):
        """
        Estrae la posizione dei lati del campo, da modificare nel caso si decidano sistemi di riferimento diversi ()
        """
        return [0, self.yDimension]
    def _goalLimit(self):
        return [self.yDimension/2 - 3.75, 3.75 + self.yDimension/2]
    def _setEvent(self,data,index,player):
        # Da questo momento il player è inteso come palla
        return [{'event': 'BallOut',
                'timestamp': player.timestamp + self.windowSize}]
                #'x': player.xPosition,
                #'y': player.yPosition}
    def _initialize(self, list):
        self.windowSize = list[0]

class GoalEvent(GenericEvent):
    "Classe che definisce l'event detector per il goal"
    def __init__(self, file, xDimension, yDimension):
        """
        :param file: File contenente una lista di parametri di inizializzazione per il modulo
        """
        self.name = "Goal"
        self.version = "1.0"
        if not(file is None):
            self._readFromFile(file)
            #print('Event: {}\nVersion: {}\nWindow: {}\n'.format(self.name, self.version, self.windowSize))
        self.xDimension = xDimension
        self.yDimension = yDimension

    def recognize(self, data, index):
        """
        Funzione che identifica se la palla è entrata nell'area della porta

        :param data: Dataset compatto con dati posizionali e feature
        :param index: Indice da cui inizia la finestra
        :return: Un dizionario con l'evento riconosciuto, None in caso non sia stato riconosciuto nulla
        """
        minFieldLine, maxFieldLine = self._fieldLimit()
        minGoalLimit, maxGoalLimit = self._goalLimit()
        startBall = data[index].get('ball')
        
        for i in range(int(self.windowSize)) :
            if (index + i) >= len(data) :
                return [None, index]
            ball = data[index + i].get('ball')
            if (minFieldLine < ball.xPosition) and (ball.xPosition < maxFieldLine):
                return [None, index]
            elif (ball.yPosition < minGoalLimit - 1) or (ball.yPosition > maxGoalLimit + 1):
                return [None, index]
            elif (ball.xPosition < minFieldLine - 5) or (ball.xPosition > maxFieldLine + 5):
                return [None, index] 
            i += 1

        output = self._setEvent(startBall, index, startBall)
        if output != None:
            index += i
        return [output, int(index)]
    def _fieldLimit(self):
        """
        Estrae la posizione del fondo campo, da modificare nel caso si decidano sistemi di riferimento diversi ()
        """
        return [0, self.xDimension]
    def _goalLimit(self):
        return [self.yDimension/2 - 3.75, 3.75 + self.yDimension/2]
    def _setEvent(self,data,index,player):
        return [{'event': 'Goal',
                'timestamp': player.timestamp + math.floor(self.windowSize/2)}]
                #'x': player.xPosition,
                #'y': player.yPosition}
    def _initialize(self, list):
        self.windowSize = list[0]
        
# DATA STORING
class XML():
    @staticmethod
    def createEventXML(eventList, filename):
        """
        Crea un file xml a partire da una lista di dizionari contenenti gli eventi

        :param data: Struttura dati da cui creare il file JSON
        :param filename: Stringa con il percorso al file JSON
        :return:
        """
        id = 0
        annotations = ET.Element('annotations')
        for event in eventList:
            track = ET.SubElement(annotations, 'track')
            track.attrib['id'] = str(int(id))
            track.attrib['label'] = event['event']
            
            box = ET.SubElement(track, 'box')
            box.attrib['frame'] = str(int(event['timestamp']))
            box.attrib['keyframe'] = '1'
            box.attrib['occluded'] = '0'
            box.attrib['outside'] = '0'
            box.attrib['xbr'] = '10'
            box.attrib['xtl'] = '100'
            box.attrib['ybr'] = '10'
            box.attrib['ytl'] = '100'
            
            for attributeName in event:
                if ((attributeName != 'event') and (attributeName != 'timestamp')):
                    attribute = ET.SubElement(box, 'attribute')
                    attribute.attrib['name'] = attributeName
                    attribute.text = str(event[attributeName])
            
            id = id + 1
        #tree = ET.ElementTree(annotations)
        xml = DOM.parseString(ET.tostring(annotations))
        with open(filename, 'w') as f:
            f.write(xml.toprettyxml())
        
    @staticmethod
    def getHalfTimeFrame(filename):
        "Estrae il frame di inizio del secondo tempo da Annotations_Atomic_Manual.xml"
        result = 54000000
        tree = ET.parse(filename)
        annotations = tree.getroot()
        if (annotations.tag != 'annotations'):
            raise Exception('No /annotations found in XML')
        else:
            for track in annotations:
                if (track.tag == 'track'):
                    if (track.attrib.get('id') is None):
                        raise Exception('No attribute "id" in /track')
                    elif (int(track.attrib['id']) == 0):
                        if (track.attrib.get('label') is None):
                            raise Exception('No attribute "label" in /track')
                        elif(track.attrib['label'] != 'SecondHalf'):
                            raise Exception('This track has an id = 0 but is not a second half!')
                        else:
                            box = track[0]
                            if (box.tag != 'box'):
                                raise Exception('No /box found in /track')
                            else:
                                if (box.attrib.get('frame') is None):
                                    raise Exception('No attribute "frame" in /box')
                                else:
                                    result = int(box.attrib['frame'])
        return result

    @staticmethod
    def getGoalkeepersId(filename):
        results = []
        tree = ET.parse(filename)
        annotations = tree.getroot()
        if (annotations.tag != 'annotations'):
            raise Exception('No /annotations found in XML')
        else:
            for track in annotations:
                if (track.tag == 'track'):
                    if (track.attrib.get('id') is None):
                        raise Exception('No attribute "id" in /track')
                    elif (int(track.attrib['id']) == -1):
                        if (track.attrib.get('label') is None):
                            raise Exception('No attribute "label" in /track')
                        elif(track.attrib['label'] != 'GoalKeeper'):
                            raise Exception('This track has not goalkeepers!')
                        else:
                            box = track[0]
                            if (box.tag != 'box'):
                                raise Exception('No /box found in /track')
                            else:
                                for attribute in box:
                                    if (attribute.attrib['name'] == 'goalKeeperId'):
                                        results.append(attribute.text)
        return results[0], int(results[1]) + PLAYERVALUE

    @staticmethod
    def getSpecialEvents(filename):
        "Estrae i frame per goal, falli e punizioni da Annotations_Atomic_Manual.xml"
        offsides = []
        fouls = []
        penalties = []
        tree = ET.parse(filename)
        annotations = tree.getroot()
        if (annotations.tag != 'annotations'):
            raise Exception('No /annotations found in XML')
        else:
            for track in annotations:
                if (track.tag == 'track'):
                    if (track.attrib.get('id') is None):
                        raise Exception('No attribute "id" in /track')
                    elif (int(track.attrib['id']) > 0):
                        if (track.attrib.get('label') is None):
                            raise Exception('No attribute "label" in /track')
                        else:
                            actualList = None
                            if(track.attrib['label'] == 'Offside'):
                                actualList = offsides
                            elif(track.attrib['label'] == 'Penalty'):
                                actualList = penalties
                            elif(track.attrib['label'] == 'Foul'):
                                actualList = fouls
                            else:
                                continue
                            box = track[0]
                            if (box.tag != 'box'):
                                raise Exception('No /box found in /track')
                            else:
                                if (box.attrib.get('frame') is None):
                                    raise Exception('No attribute "frame" in /box')
                                else:
                                    if (len(box) <= 0):
                                        raise Exception('No sub attributes in /box')
                                    currentEvent = [int(box.attrib['frame'])]
                                    for attribute in box:
                                        if (attribute.tag != 'attribute') or (attribute.attrib.get('name' is None)):
                                            raise Exception('Malformed sub attributes in /box')
                                        else:
                                            currentEvent.append(attribute.text)
                                    actualList.append(currentEvent)
        return [offsides, fouls, penalties]

    @staticmethod
    def getRefereeEvents(filename):
        "Estrae i frame per goal, falli e punizioni da Annotations_Atomic_Manual.xml"
        goals = []
        fouls = []
        penalties = []
        tree = ET.parse(filename)
        annotations = tree.getroot()
        if (annotations.tag != 'annotations'):
            raise Exception('No /annotations found in XML')
        else:
            for track in annotations:
                if (track.tag == 'track'):
                    if (track.attrib.get('id') is None):
                        raise Exception('No attribute "id" in /track')
                    elif (int(track.attrib['id']) > 0):
                        if (track.attrib.get('label') is None):
                            raise Exception('No attribute "label" in /track')
                        else:
                            actualList = None
                            if(track.attrib['label'] == 'Goal'):
                                actualList = goals
                            elif(track.attrib['label'] == 'Penalty'):
                                actualList = penalties
                            elif(track.attrib['label'] == 'Foul'):
                                actualList = fouls
                            else:
                                continue
                            box = track[0]
                            if (box.tag != 'box'):
                                raise Exception('No /box found in /track')
                            else:
                                if (box.attrib.get('frame') is None):
                                    raise Exception('No attribute "frame" in /box')
                                else:
                                    if (len(box) <= 0):
                                        raise Exception('No sub attributes in /box')
                                    currentEvent = [int(box.attrib['frame'])]
                                    for attribute in box:
                                        if (attribute.tag != 'attribute') or (attribute.attrib.get('name' is None)):
                                            raise Exception('Malformed sub attributes in /box')
                                        else:
                                            currentEvent.append(attribute.text)
                                    actualList.append(currentEvent)
        return [goals, fouls, penalties]
            
#detector
class Detector():
    "Classe che esegue l'event detection"
    def __init__(self, dataPath, eventPath, detectPath, xDimension, yDimension, samplRate, maxSize,
                 isFirstHalf = True, annotationFile = 'annotation.xml', permutation = 0, 
                 featurePath = "feature.json", dataset=[]):
        self.dataPath = dataPath
        self.eventPath = eventPath
        self.xDimension = xDimension
        self.yDimension = yDimension
        self.isFirstHalf = isFirstHalf
        self.samplRate = samplRate
        self.maxSize = maxSize
        self.annotationFile = annotationFile
        self.featurePath = featurePath
        self.halfTimeFrame = XML.getHalfTimeFrame(annotationFile)
        self.specialEvents = XML.getSpecialEvents(annotationFile)
        self.GOALKEEPER0, self.GOALKEEPER1 = XML.getGoalkeepersId(annotationFile)
        self.detectors = [BallDeflectionEvent(detectPath,self.GOALKEEPER0,self.GOALKEEPER1), KickEvent(detectPath),
                          TackleEvent(detectPath), PossessionEvent(detectPath,self.halfTimeFrame,self.GOALKEEPER0,self.GOALKEEPER1)]

        # stampo gli id dei portieri
        print("idGoalkeeper0", self.GOALKEEPER0, "idGoalkeeper1", self.GOALKEEPER1)
        
        # permuta i detector a partire dal valore intero passato, decommentare per attivarla
        #self._permutateFromInteger(permutation)
        self.detectors.insert(0, BallOutEvent(detectPath, xDimension, yDimension, self.specialEvents))
        
        # riconoscimento del goal, non ancora perfetto, decommentare per testare
        #self.detectors.insert(0, GoalEvent(detectPath, xDimension, yDimension))
        self.dataset = dataset
        self.eventList = []
    def startDetection(self):
        "Funzione che esegue l'event detection per un solo tempo della partita"
        pars = LineHalfParser()
        extr = FeatureExtractor(self.samplRate, self.xDimension, self.yDimension, self.isFirstHalf)

        allDataExtracted = False
        index = 0
        while not allDataExtracted:
            print('Cycle {}'.format(index))
            print('Parsing file')
            pars.read(self.dataPath, self.dataset, self.maxSize)
            allDataExtracted = not pars.full

            print('Extracting data')
            extr.extract(self.dataset)
            
            print('Compacting data')
            self.dataset = extr.compact(self.dataset)

            print('Detecting event')
            self._detectEvent()
            
            print('Adding goals and referee events')
            self._sobstituteGoal()
            
            print('Creating XML file')
            XML.createEventXML(self.eventList, self.eventPath)
            
            pars.full = False
            self.dataset.clear()

            if not allDataExtracted :
                print("Processed events until line {}".format(pars.position))
                index += 1
        print("Processing ended")

    def startFullTimeDetection(self):
        "Funzione che esegue l'event detection per un'intera partita"
        pars = LinePandaParser()
        extrFirst = FeatureExtractor(self.samplRate, self.xDimension, self.yDimension, True)
        extrSecond = FeatureExtractor(self.samplRate, self.xDimension, self.yDimension, False)

        print('Starting detecting events')
        allDataExtracted = False
        index = 0
        startAll = time()
        while not allDataExtracted:
            print('Cycle {}'.format(index))
            print('Parsing file')
            start = time()
            halfTimeFrame = XML.getHalfTimeFrame(self.annotationFile)
            self.dataset = pars.read(self.dataPath, self.maxSize, halfTimeFrame)
            allDataExtracted = not pars.full
            elapsed = time() - start
            print('Elapsed {} seconds\n'.format(round(elapsed,1)))

            print('Extracting data')
            start = time()
            if (len(self.dataset[0]) > 0):
                extrFirst.extract(self.dataset[0])
            if (len(self.dataset[1]) > 0):
                extrSecond.extract(self.dataset[1])
            elapsed = time() - start
            print('Elapsed {} seconds\n'.format(round(elapsed,1)))

            print('Compacting data')
            start = time()
            if (len(self.dataset[0]) > 0):
                self.dataset[0] = extrFirst.compact(self.dataset[0])
            if (len(self.dataset[1]) > 0):
                self.dataset[1] = extrFirst.compact(self.dataset[1])
            self.dataset = self.dataset[0]+self.dataset[1]
            elapsed = time() - start
            print('Elapsed {} seconds\n'.format(round(elapsed,1)))
            
            print('Detecting event')
            start = time()
            self._detectEvent()
            elapsed = time() - start
            print('Elapsed {} seconds\n'.format(round(elapsed,1)))

            pars.full = False
            self.dataset.clear()

            if not allDataExtracted :
                print("Processed events until line {}".format(pars.position))
                index += 1
            else:
                print('Creating XML')
                start = time()
                self._sobstituteGoal()
                XML.createEventXML(self.eventList, self.eventPath)
                elapsed = time() - start
                print('Elapsed {} seconds\n'.format(round(elapsed,1)))
        elapsedAll = time() - startAll
        print('Detection processing ended in {} seconds\n'.format(round(elapsedAll,1)))
    
    def startDetectionFromFeature(self):
        "Funzione che esegue l'event detection a partire dalle feature"
        pars = LinePandaParser()
        extrFirst = FeatureExtractor(self.samplRate, self.xDimension, self.yDimension, True)
        extrSecond = FeatureExtractor(self.samplRate, self.xDimension, self.yDimension, False)

        print('Starting detecting events')
        allDataExtracted = False
        index = 0
        startAll = time()
        while not allDataExtracted:
            print('Cycle {}'.format(index))
            print('Parsing file')
            start = time()
            halfTimeFrame = XML.getHalfTimeFrame(self.annotationFile)
            self.dataset = pars.read(self.featurePath, self.maxSize, halfTimeFrame, True)
            allDataExtracted = not pars.full
            elapsed = time() - start
            print('Elapsed {} seconds\n'.format(round(elapsed,1)))

            print('Compacting data')
            start = time()
            if (len(self.dataset[0]) > 0):
                self.dataset[0] = extrFirst.compact(self.dataset[0])
            if (len(self.dataset[1]) > 0):
                self.dataset[1] = extrFirst.compact(self.dataset[1])
            self.dataset = self.dataset[0]+self.dataset[1]
            elapsed = time() - start
            print('Elapsed {} seconds\n'.format(round(elapsed,1)))
            
            print('Detecting event')
            start = time()
            self._detectEvent()
            elapsed = time() - start
            print('Elapsed {} seconds\n'.format(round(elapsed,1)))

            pars.full = False
            self.dataset.clear()

            if not allDataExtracted :
                print("Processed events until line {}".format(pars.position))
                index += 1
            else:
                print('Creating XML')
                start = time()
                # attivare il postprocessing al posto della sostituzione dei goal quando si vuole individuarli con l'event detector
                self._sobstituteGoal()
                #self._postProcessing()
                XML.createEventXML(self.eventList, self.eventPath)
                elapsed = time() - start
                print('Elapsed {} seconds\n'.format(round(elapsed,1)))
        elapsedAll = time() - startAll
        print('Detection processing ended in {} seconds\n'.format(round(elapsedAll,1)))

    def startPreExtraction(self):
        "Funzione che estrae le feature dai dati posizionali e li inserisce in un dataset"
        pars = LinePandaParser()
        extrFirst = FeatureExtractor(self.samplRate, self.xDimension, self.yDimension, True)
        extrSecond = FeatureExtractor(self.samplRate, self.xDimension, self.yDimension, False)
        
        print('Starting pre extracting events')
        allDataExtracted = False
        index = 0
        startAll = time()
        while not allDataExtracted:
            print('Cycle {}'.format(index))
            print('Parsing file')
            start = time()
            halfTimeFrame = XML.getHalfTimeFrame(self.annotationFile)
            self.dataset = pars.read(self.dataPath, self.maxSize, halfTimeFrame,False)
            allDataExtracted = not pars.full
            elapsed = time() - start
            print('Elapsed {} seconds\n'.format(round(elapsed,1)))

            print('Extracting data')
            start = time()
            if (len(self.dataset[0]) > 0):
                extrFirst.extract(self.dataset[0])
            if (len(self.dataset[1]) > 0):
                extrSecond.extract(self.dataset[1])
            self.dataset = self.dataset[0]+self.dataset[1]
            elapsed = time() - start
            print('Elapsed {} seconds\n'.format(round(elapsed,1)))
            
            print('Saving feature data')
            start = time()
            self.createFeatureFile(index < 1)
            elapsed = time() - start
            print('Elapsed {} seconds\n'.format(round(elapsed,1)))

            pars.full = False
            self.dataset.clear()

            if not allDataExtracted :
                print("Processed events until line {}".format(pars.position))
                index += 1
        elapsedAll = time() - startAll
        print('Extraction processing ended in {} seconds\n'.format(round(elapsedAll,1)))

    def extractAndCompact(self):
        "Estrae e compatta il dataset"
        pars = LinePandaParser()
        extrFirst = FeatureExtractor(self.samplRate, self.xDimension, self.yDimension, True)
        extrSecond = FeatureExtractor(self.samplRate, self.xDimension, self.yDimension, False)

        # print('Starting parsing features')
        allDataExtracted = False
        index = 0
        # startAll = time()
        while not allDataExtracted:
            # print('Cycle {}'.format(index))
            # print('Parsing feature')
            # start = time()
            halfTimeFrame = XML.getHalfTimeFrame(self.annotationFile)
            self.dataset = pars.read(self.featurePath, self.maxSize, halfTimeFrame, True)
            allDataExtracted = not pars.full
            # elapsed = time() - start
            # print('Elapsed {} seconds\n'.format(round(elapsed,1)))

            # print('Compacting data')
            # start = time()
            if (len(self.dataset[0]) > 0):
                self.dataset[0] = extrFirst.compact(self.dataset[0])
            if (len(self.dataset[1]) > 0):
                self.dataset[1] = extrSecond.compact(self.dataset[1])
            self.dataset = self.dataset[0]+self.dataset[1]
            # elapsed = time() - start
            # print('Elapsed {} seconds\n'.format(round(elapsed,1)))
            
            pars.full = False

            if not allDataExtracted :
                print("Processed events until line {} PROBLEM".format(pars.position))
                index += 1
            # else:
                # elapsed = time() - start
                # print('Elapsed {} seconds\n'.format(round(elapsed,1)))
        
        # elapsedAll = time() - startAll
        # print('Feature parsing processing ended in {} seconds\n'.format(round(elapsedAll,1)))

    def startPostDetection(self):
        "Funzione che esegue l'event detection a partire da feature già in memoria"
        extrFirst = FeatureExtractor(self.samplRate, self.xDimension, self.yDimension, True)
        extrSecond = FeatureExtractor(self.samplRate, self.xDimension, self.yDimension, False)

        # print('Starting detecting events')
        allDataExtracted = False
        index = 0
        # startAll = time()
        while not allDataExtracted:            
            # print('Detecting event')
            # start = time()
            self._detectEvent()
            # elapsed = time() - start
            # print('Elapsed {} seconds\n'.format(round(elapsed,1)))

            allDataExtracted = True
            #pars.full = False
            #self.dataset.clear()

            if not allDataExtracted :
                print("Processed events until line {}".format(pars.position))
                index += 1
            #else:
                # print('Compacting events')
                # start = time()
                # attivare il postprocessing al posto della sostituzione dei goal quando si vuole individuarli con l'event detector
                self._sobstituteGoal()
                #self._postProcessing()
                # crea l'XML di output, linea da cancellare per risparmiare tempo
                #XML.createEventXML(self.eventList, self.eventPath)
                # elapsed = time() - start
                # print('Elapsed {} seconds\n'.format(round(elapsed,1)))
        
        # elapsedAll = time() - startAll
        # print('Detection processing ended in {} seconds\n'.format(round(elapsedAll,1)))

    def _sobstituteGoal(self):
        "Inserisce i dati arbitrali agli eventi rilevati (goal, falli e punizioni)"
        i,j,q = [0,0,0]
        goals, fouls, penalties = XML.getRefereeEvents(self.annotationFile)
        for k in range(len(self.eventList)+len(goals)+len(fouls)+len(penalties)):
            if(k >= len(self.eventList)):
                # print(k, len(self.eventList), len(goals))
                break
            if(i < len(goals)):
                # print(self.eventList[k]['timestamp'], goals[i][0])
                if (self.eventList[k]['timestamp'] >= goals[i][0]):
                    newGoalEvent = {'event': 'Goal',
                                'timestamp': goals[i][0],
                                'scorer': goals[i][1],
                            'team': goals[i][2]}
                    
                    print(newGoalEvent)

                    if (self.eventList[k]['event'] == 'BallOut'):
                        self.eventList[k] = newGoalEvent
                        n = 1
                        
                        print("IF - Added newGoalEvent to event list")
                    
                    else:
                        self.eventList.insert(k, newGoalEvent)

                        print("ELSE - Added newGoalEvent to event list")

                        n = 0
                    while(self.eventList[k+n]['event'] == 'BallOut'):
                            self.eventList.pop(k+n)
                    i += 1

                elif (k == len(self.eventList) - 1):
                    newGoalEvent = {'event': 'Goal',
                                'timestamp': goals[i][0],
                                'scorer': goals[i][1],
                            'team': goals[i][2]}
                    
                    print(newGoalEvent)
                    self.eventList.insert(k+1, newGoalEvent)
                    print("ELSE - Added newGoalEvent to event list")
                    
                    i += 1


            elif(j < len(fouls)):
                if(self.eventList[k]['timestamp'] >= fouls[j][0]):
                    newFoulEvent = {'event': 'Foul',
                                    'timestamp': fouls[j][0],
                                    'scorerId': fouls[j][1],
                                    'teamId': fouls[j][2]}
                    if (self.eventList[k]['timestamp'] == fouls[j][0]):
                        self.eventList[k] = newFoulEvent
                    else:
                        self.eventList.insert(k-1, newFoulEvent)
                    j += 1
            elif(q < len(penalties)):
                if(self.eventList[k]['timestamp'] >= penalties[q][0]):
                    newPenaltyEvent = {'event': 'Penalty',
                                    'timestamp': penalties[q][0],
                                    'scorerId': penalties[q][1],
                                    'teamId': penalties[q][2]}
                    if (self.eventList[k]['timestamp'] == penalties[q][0]):
                        self.eventList[k] = newPenaltyEvent
                    else:
                        self.eventList.insert(k-1, newPenaltyEvent)
                    q += 1
            else:
                break
        i = 0
        for k in range(len(self.eventList)):
            if(k >= len(self.eventList)):
                break
            if(i < len(goals)):
                if (self.eventList[k]['event'] == 'Goal'):
                    j = 1
                    while(self.eventList[k-j]['event'] == 'BallOut'):
                            self.eventList.pop(k-j)
                            j += 1
                    i += 1
            else:
                break

    def _postProcessing(self):
        "Post processing da usare per individuare i goal"
        for i in range(len(self.eventList)):
            if(i >= len(self.eventList)-1):
                break
            if (self.eventList[i]['event'] == 'BallOut'):
                while(self.eventList[i+1]['event'] == 'BallOut'):
                            self.eventList.pop(i+1)
            elif (self.eventList[i]['event'] == 'Goal'):
                while(self.eventList[i+1]['event'] == 'Goal'):
                            self.eventList.pop(i+1)
        for i in range(len(self.eventList)):
             if(i >= len(self.eventList)-1):
                 break
             if (self.eventList[i]['event'] == 'BallOut'):
                 if (self.eventList[i+1]['event'] == 'Goal'):
                     self.eventList.pop(i+1)
        for i in range(len(self.eventList)):
             if(i >= len(self.eventList)-1):
                 break
             if (self.eventList[i]['event'] == 'Goal'):
                 if (self.eventList[i+1]['event'] == 'BallOut'):
                     self.eventList.pop(i)
             elif (self.eventList[i]['event'] == 'BallOut'):
                 if (self.eventList[i+1]['event'] == 'Ballout'):
                     self.eventList.pop(i+1)

    def _detectEvent(self):
        """
        Funzione per rilevare gli eventi

        :param data: Dataset compatto con dati posizionali e feature
        :param detectors: Lista contenente tutti gli event detector che si vogliono applicare a ciascun istante temporale
        :return: Una lista con tutti gli eventi rilevati
        """
        i = 0
        while (i < len(self.dataset)) :
            for detector in self.detectors:
                event, i = detector.recognize(self.dataset,i)
                if event != None :
                    for e in event:
                        self.eventList.append(e)
                    break
            i += 1
    def _permutateFromInteger(self, integer):
        multiplier = len(self.detectors) - 1
        digits = []
        while (multiplier > 0):
            digits.append(math.floor(integer/math.factorial(multiplier)))
            integer %= math.factorial(multiplier)
            multiplier -= 1
        for digit,i in zip(digits, range(len(self.detectors))):
            self.detectors[i], self.detectors[i+digit] = self.detectors[i+digit], self.detectors[i]
    def createFeatureFile(self, overwrite=False):
        """
        Crea un file con l'elenco degli eventi con le feature estratte
        :param overwrite: Boleano che indica se sovrascrivere il file o meno
        :return:
        """
        if isfile(self.featurePath) and not overwrite:
            fstring = 'a'
        else:
            fstring = 'w'
        with open(self.featurePath, fstring) as f:
            for currentData in self.dataset:
                f.write('{} {} {:.5f} {:.5f} {:.5f} {:.5f} {:.5f} {:.5f} {:.5f} {:.5f} {:.5f} {:.5f} {:.5f} {:.5f}\n'.format(currentData.timestamp, currentData.playerID, 
                                                                                                                             currentData.xPosition, currentData.yPosition, 
                                                                                                                             currentData.direction, currentData.velocity, 
                                                                                                                             currentData.acceleration, currentData.accPeak, 
                                                                                                                             currentData.accPeakReal, currentData.dirChange, 
                                                                                                                             currentData.distToBall, currentData.distToTarget, 
                                                                                                                             currentData.distToGoal, currentData.crossOnTargLine))        

def main():
    datasetPath = "dataset.txt"
    compactedDatasethPath = "extractedDataset.xml"
    
    detectorsPath = "detectors.txt"

    isFirstHalf = False

    windowSize = 2
    threshold1 = 0.5
    threshold2 = 1
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--datasetPath", type=str,  help="Path to the dataset", default="./dataset_Match_2019_08_30_#001")
    parser.add_argument("-m", "--maxSize", type=int, default=4096, help="Maximum space taken by the detector (couldn't eccess maximum RAM size)")
    parser.add_argument("-s", "--samplingRate", type=int, default=100, help="Sampling rate at which the positional data were taken")
    parser.add_argument("-x", "--xDimension", type=int, default=110, help="Horizontal size of the pitch")
    parser.add_argument("-y", "--yDimension", type=int, default=72, help="Vertical size of the pitch")
    parser.add_argument("-f", "--firstHalf", action="store_true", help="Use this flag if the positional data come from the first half of the match")
    parser.add_argument("-mo", "--mode", type=str, default='SINGLE', help="Vertical size of the pitch")
    args = parser.parse_args()
    if not(PATH.isdir(args.datasetPath)):
        raise Exception("No file with such name found!")
    mode = args.mode
    dataPath = args.datasetPath + '//positions.log'
    featurePath = args.datasetPath + '//features.log'
    annotationPath = args.datasetPath + '//Annotations_AtomicEvents_Manual.xml'
    eventStoragePath = args.datasetPath + "//Annotations_AtomicEvents_Detected.xml"
    maxSize = args.maxSize
    samplingRate = args.samplingRate
    xDimension = args.xDimension
    yDimension = args.yDimension
    if args.firstHalf:
        isFirstHalf = True
    
    detector = Detector(dataPath, eventStoragePath, detectorsPath, xDimension, yDimension, samplingRate, maxSize, isFirstHalf, 
                        annotationFile=annotationPath, featurePath=featurePath)
    if (mode == 'SINGLE'):
        detector.startDetection()
    elif (mode == 'FULL'):
        detector.startFullTimeDetection()
    elif (mode == 'FEAT'):
        detector.startDetectionFromFeature()
    elif (mode == 'EXTR'):
        detector.startPreExtraction()
    else:
        raise Exception("Wrong mode")

if __name__ == "__main__":
    main()


