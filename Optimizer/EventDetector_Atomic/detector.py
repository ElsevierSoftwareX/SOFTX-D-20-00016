#No Multithreading
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import math
import os.path as PATH
import threading
import xml.dom.minidom as DOM
import xml.etree.ElementTree as ET
from itertools import chain
from operator import attrgetter
from os.path import isfile
from time import time

import pandas
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class PlayerData:
    #Data structure containing positional data and player features
    timestamp: float
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


# Player ID is ID of player utils to attribute player to a team
# playerID < PLAYERVALUE -> home team
# playerID > PLAYERVALUE -> opposite team
# playerID = PLAYERVALUE -> ball
PLAYERVALUE = 128

def teamPlayerData(playerValue):
    """

    Function that receive ID of player and return a list
    - first item is 0 if the player belongs to home team and 1 otherwise
    - second item represents ID of player excluding PLAYERVALUE
    """
    if (playerValue < PLAYERVALUE):
        return [0, playerValue]
    elif (playerValue > PLAYERVALUE):
        return [1, playerValue - PLAYERVALUE]
    else:
        return [-1, -1]

#Value of the maximum number of positional data and features contained in 1 MB
MBVALUE = 2048

# PARSER
class GenericParser():
    "Base class from which the different parsers derive"
    def __init__(self):
        self.full = False
        self.position = 0

class LineHalfParser(GenericParser):
    """

    Each row represents positional data of a player in a particular frame
    This parser only reads one game time
    """
    def read(self, filename, data, size):
        """

        Reads the data in the file and extracts them in a list in memory

        :param filename: Path for file
        :param data: List of dataset
        :param size: Memory limit of data in MB
        """
        # calculates the number of total lines it can read, so as not to exceed the memory
        totalMemory = MBVALUE * size
        
        # based on last position skip N line
        with open(filename, 'r') as f:
            i = 0
            line = f.readline().rstrip('\n')
            while (i < self.position and line != ""):
                line = f.readline()
                i = i + 1

            while (not self.full and line != ""):
                extractedData = self._extractFromLine(line)
                newEntry = PlayerData(*extractedData, *[-1 for i in range(10)])
                data.append(newEntry)
                line = f.readline().rstrip('\n')
                i = i + 1

                if (i - self.position) >= totalMemory:
                    self.full = True

                    for k in range(len(actualTime)-1,0,-1):
                        element = actualTime.pop(k)
                        i -= 1
                        if(element.playerID == PLAYERVALUE):
                           break 
                    self.position = i
    def _extractFromLine(self, line):

        elements = line.split(" ")
        return [float(element) for element in elements]

class LineParser(GenericParser):

    def read(self, filename, size, halfTimeFrame):
        """
        List composed by two times of match

        :param filename: Path for file
        :param data: List of dataset
        :param size: Memory limit of data in MB



        """
        totalMemory = MBVALUE * size
        firstTime = []
        secondTime = []
        actualTime = firstTime
        data = [firstTime, secondTime]

        with open(filename, 'r') as f:
            i = 0
            line = f.readline().rstrip('\n')
            while (i < self.position and line != ""):
                line = f.readline()
                i = i + 1

            while (not self.full and line != ""):
                extractedData = self._extractFromLine(line)
                newEntry = PlayerData(*extractedData, *[-1 for i in range(14 - len(extractedData))])
                # aggiunge i dati al tempo corrente, se siamo arrivati al secondo tempo li aggiunge al secondo
                if (int(newEntry.timestamp) == halfTimeFrame):
                    actualTime = secondTime
                actualTime.append(newEntry)
                line = f.readline().rstrip('\n')
                i = i + 1
                
                if (i - self.position) >= totalMemory:
                    self.full = True

                   for k in range(len(actualTime)-1,0,-1):
                        element = actualTime.pop(k)
                        i -= 1
                        if(element.playerID == PLAYERVALUE):
                           break  
                    self.position = i
        return data
    def _extractFromLine(self, line):
        elements = line.split(" ")
        return [float(element) for element in elements]

class LinePandaParser(GenericParser):
    """
    Pandas Library used for the optimization process
    """
    def read(self, filename, size, halfTimeFrame, isFeature = False):

        totalMemory = MBVALUE * size
        firstTime = []
        secondTime = []
        actualTime = firstTime
        data = [firstTime, secondTime]

        if (isFeature):
            names = ['timestamp', 'playerID','xPosition','yPosition', 'direction', 'velocity', 'acceleration', 
                     'accPeak', 'accPeakReal','dirChange','distToBall','distToTarget', 'distToGoal', 'crossOnTargLine']
        else:
            names = ['timestamp', 'playerID','xPosition','yPosition']
        

        parsedData = pandas.read_csv(filename, sep=' ', engine='c', skiprows=int(self.position), nrows=totalMemory, memory_map=True, names=names)
        

        for row in parsedData.itertuples(name=None):
            newEntry = PlayerData(*row[1:], *[-1 for i in range(14 - len(row)+1)])
            if (int(newEntry.timestamp) == halfTimeFrame):
                actualTime = secondTime
            actualTime.append(newEntry)
        if (len(parsedData) >= totalMemory):
            self.full = True
        self.position += len(parsedData)
        if (self.full):
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
    """
       Feature extraction from positional data
    """
    def __init__(self, sampling, xDimension, yDimension,isFirstHalf):
        """
        :param sampling: sampling rate
        :param xDimension of field
        :param yDimension of field
        :param isFirstHalf: first or second time
        """
        self.sampligRate = sampling
        self.xDimension = xDimension
        self.yDimension = yDimension
        self.isFirstHalf = isFirstHalf
        self.xGoal1Position, self.xGoal2Position, self.yGoalPosition = self._goalExtractor()
        self.currentTimestamp = -1
        self.ballIndex = -1
    def extract(self, data):

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
        Create compact version of datas
        """
        newData = []
        homeTeam = []
        awayTeam = []
        ballIndex = -1
        currentTimestamp = data[0].timestamp
        for i,element in enumerate(data):

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
        Extract location of the football goal
        """
        return [0, self.xDimension, self.yDimension/2]
    def _currentPlayerGoal(self, playerID):

        if((playerID < PLAYERVALUE and self.isFirstHalf) or (playerID > PLAYERVALUE and (not self.isFirstHalf))):
            return [self.xGoal1Position, self.xGoal2Position]
        elif ((playerID < PLAYERVALUE and (not self.isFirstHalf)) or (playerID > PLAYERVALUE and  self.isFirstHalf)):
            return [self.xGoal2Position, self.xGoal1Position]
        else:
            return [-1,-1]
    def _findBall(self, data, index):

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
        #Assigns the acceleration peak to the first 23 elements, which are not considered by the extractor cycledata[index].accPeak = data[index].acceleration
        if (math.fabs(data[index].accPeak) > math.fabs(data[index + 23].accPeak)):
            data[index].accPeakReal = data[index].accPeak
        else:
            data[index].accPeakReal = 0

    def _extractDirection(self, data, index):

        data[index - 23].direction = math.atan2(data[index].yPosition - data[index - 23].yPosition ,
                                      data[index].xPosition - data[index - 23].xPosition)
    def _extractVelocity(self, data, index):

        data[index - 23].velocity = self.sampligRate * math.hypot((data[index].yPosition - data[index - 23].yPosition),
                                                                 (data[index].xPosition - data[index - 23].xPosition))
    def _extractAcceleration(self, data, index):

        data[index - 23].acceleration = data[index].velocity - data[index-23].velocity
    def _extractAccPeak(self, data, index):
        if (data[index - 23].acceleration >= 0):
            data[index].accPeak = data[index - 23].acceleration + max(0,data[index].acceleration)
        else:
            data[index].accPeak = data[index - 23].acceleration + min(0, data[index].acceleration)
    def _extractAccPeakReal(self, data, index):
        """
        It extracts the peak of real acceleration, the method follows that described in the paper with the aggregation of two consecutive frames
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
        "Extract the change of direction from the previous one"
        data[index - 23].dirChange = math.fabs(data[index].direction - data[index - 23].direction)
    def _extractDistToBall(self, data, index):
        """
        Extracts the distance of the current player from the ball,
        which is why he tries to figure out what the ball index is for the current timestamp
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
        "Extracts the player's distance from the opponent's goal"
        thisGoalxPosition = self._currentPlayerGoal(data[index-1].playerID)[1]
        if thisGoalxPosition != -1:
            data[index - 1].distToTarget = math.hypot((self.yGoalPosition - data[index - 1].yPosition),
                                                      (thisGoalxPosition - data[index - 1].xPosition))
        else:
            data[index - 1].distToTarget = -1
    def _extractDistToGoal(self, data, index):
        "Extracts the player's distance from his goal"
        thisGoalxPosition = self._currentPlayerGoal(data[index-1].playerID)[0]
        if thisGoalxPosition != -1:
            data[index - 1].distToGoal = math.hypot((self.yGoalPosition - data[index - 1].yPosition),
                                                      (thisGoalxPosition - data[index - 1].xPosition))
        else:
            data[index - 1].distToGoal = -1
    def _extractCrossOnTargLine(self, data, index):
        "Extracts the moment when the object will intersect the goal line going in the same direction"
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


        :param data:
        :param index:
        :return:
        """
        pass
    def _setEvent(self, data, index, player):
        "To be redefined in the daughter classes, create a dictionary that describes the recognized event"
        return None
    def _readFromFile(self, file):
        "To be redefined in the daughter classes, create a dictionary that describes the recognized event"
        if (PATH.isfile(file)):
            with open(file, 'r') as f:
                self._readFromLines(f)
        elif (type(file) is list):
            self._readFromLines(file)
    def _readFromLines(self, lines):
        # For each line in the list check the version of the event, if it matches use that line to initialize the event
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

        pass


class PlayerEvent(GenericEvent):
    "Base class for all events that include at least one player"
    def recognize(self, data, index):
        """
        Basic function that recognizes events by checking the precondition and then iterating the specific condition
        of the event for each moment of the time window

        :param data: Compact dataset with positional data and features
        :param index: Index from which the window starts
        :return: A dictionary with the recognized event, None in case nothing has been recognized
        """

        result, selectedPlayer = self._checkPrecondition(data, index)
        if not result:
            return [None, index]

        self.middlePlayer = None
        for i in range(1, int(self.windowSize)):
            if (i == math.floor(self.windowSize/2)):
                isMiddle = True
            else:
                isMiddle = False
            if (index + i) >= len(data) :
                return [None, index]
            elif not self._checkCondition(data, index + i, selectedPlayer, isMiddle) :
                return [None, index]
        
        if not(self._checkPostcondition(data, index + int(self.windowSize)-1, selectedPlayer)):
            return [None, index]
        output = self._setEvent(data,index, self.middlePlayer)
        if output != None :
            index += math.floor(self.windowSize/self.stride)
        return [output, int(index)]
    def _checkCondition(self, data, index, selectedPlayer, isMiddle):

        pass

    def _checkPrecondition(self, data, index):
        """
       Function function to check the precondition, check that the distance of the player closest to the ball
        is below the default threshold

        :param data: Compact dataset with positional data and features
        :param index: Index of window
        :return: UA list with the condition is verified and the player who verifies it
        List with condition verified and player
        """
        # I find the player with the least distance from the ball
        minimum = 1000
        playerIndex = -1
        for i,player in enumerate(chain(data[index].get('homeTeam'), data[index].get('awayTeam'))):
            if (player.distToBall < minimum):
                minimum = player.distToBall
                playerIndex = i


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

        return True

class KickEvent(PlayerEvent):

    def __init__(self, file):

        self.name = "KickingTheBall"
        self.version = "3.0"
        self.accelerationCheck = False
        if not(file is None):
            self._readFromFile(file)
            #print('Event: {}\nVersion: {}\nWindow: {}\nThreshold 1: {}\n'.format(self.name, self.version, self.windowSize, self.threshold1))
        self.middlePlayer = None
        self.stride = 1
    def _checkPrecondition(self, data, index):
        "Check for acceleration above threshold in previous windowSize / 2 frames"
        for i in range(math.floor(self.windowSize/2)):
            if not(self.accelerationCheck) and ((index - i) >= 0) :
                if (data[index-i].get('ball').acceleration > self.threshold2):
                        self.accelerationCheck = True
        return super()._checkPrecondition(data, index)
    def _checkCondition(self, data, index, selectedPlayer, isMiddle):
        """
       Check that the ball is moving away from the player

        : param data: Compact dataset with positional data and features
        : param index: Index on which to check the condition
        : param selectedPlayer: Player to check the condition on
        : param isMiddle: Boolean indicating whether it is the intermediate frame or not
        : return: A Boolean indicating whether the condition has occurred or not
        """
        condition = False
        for player in chain(data[index].get('homeTeam'), data[index].get('awayTeam')):
            if (player.playerID == selectedPlayer.playerID):
                if (isMiddle):
                    self.middlePlayer = player
                if not (self.accelerationCheck):
                    if (data[index].get('ball').acceleration > self.threshold2):
                        self.accelerationCheck = True

                if (player.distToBall > selectedPlayer.distToBall):
                    condition = True
                    break
        return condition
    def _checkPostcondition(self, data, index, selectedPlayer):
      "Check that the ball is eventually outside the threshold with a high speed"
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
        # distance, speed at the end, acceleration peak
        self.windowSize, self.threshold1, self.threshold2 = list

class PossessionEvent(PlayerEvent):
    "Ball Possession event"
    def __init__(self, file, halfTimeFrame, goalkeeper0, goalkeeper1):
        """
        :param file: File containing a list of initialization parameters for the module
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
        Verify that the ball remains close to the player and is the only player in the largest threshold

        : param data: Compact dataset with positional data and features
        : param index: Index on which to check the condition
        : param selectedPlayer: Player to check the condition on
        : return: A Boolean indicating whether the condition has occurred or not
        """


        minimum = 1000
        condition = True
        minPlayer = None

        for player in chain(data[index].get('homeTeam'), data[index].get('awayTeam')):
            if (player.distToBall < minimum):
                minimum = player.distToBall
                minPlayer = player

        if minPlayer == None :
            return False

        # Verify that it is still the player who should be in control of the ball
        if selectedPlayer.playerID == minPlayer.playerID:
            if (isMiddle):
                self.middlePlayer = minPlayer


            teamString = 'homeTeam'
            if (selectedPlayer.playerID < PLAYERVALUE):
                teamString = 'awayTeam'

            # identify the side on which the opposing team plays
            if ((teamString == 'awayTeam') and (selectedPlayer.timestamp < self.halfTimeFrame)) or ((teamString == 'homeTeam') and (selectedPlayer.timestamp >= self.halfTimeFrame)):
                side = 'right'
            else:
                side = 'left'

            # Verify that there are no opposing players around the player and mark the opposing player closest to his goal
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

            # Check that the ball is not in the lineout (bottom edge)
            # a) the ball speed lower than 0.1
            # b) the position near the edge line
            if data[index].get('ball').velocity < 0.1 and data[index].get('ball').yPosition > -0.5 and data[index].get('ball').yPosition < 0.5:
                return False

            # Check that the ball is not in the throw-in (top edge)
            # a) the ball speed lower than 0.1
            # b) the position near the edge line
            if data[index].get('ball').velocity < 0.1 and data[index].get('ball').yPosition > 71.5 and data[index].get('ball').yPosition < 72.5:
                return False

        else:
            condition = False
        return condition
    def _checkPostcondition(self, data, index, selectedPlayer):
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
        #minimum, maximum distance and speed
        self.windowSize, self.threshold1,self.threshold2, self.threshold3 = list

class TackleEvent(PlayerEvent):
    "Class that defines the event detector for contrast"
    def __init__(self, file):
        """
       : param file: File containing a list of initialization parameters for the module
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
        Verify that the ball remains close to the player and is not the only player in the largest threshold

        : param data: Compact dataset with positional data and features
        : param index: Index on which to check the condition
        : param selectedPlayer: Player to check the condition on
        : return: A Boolean indicating whether the condition has occurred or not
        """


        minimum = 1000
        condition = False
        minPlayer = None

        for player in chain(data[index].get('homeTeam'), data[index].get('awayTeam')):
            if (player.distToBall < minimum):
                minimum = player.distToBall
                minPlayer = player

        # Verify that it is still the player who should be in control of the ball
        if selectedPlayer.playerID == minPlayer.playerID:
            if (isMiddle):
                self.middlePlayer = minPlayer
            #select the opposing team
            teamString = 'homeTeam'
            if selectedPlayer.playerID < PLAYERVALUE:
                teamString = 'awayTeam'

            # Check that there are no opposing players around the player and save the player who makes the contrast
            for player in data[index].get(teamString):
                distance = math.hypot(player.yPosition - minPlayer.yPosition,
                                      player.xPosition - minPlayer.xPosition)
                if distance < self.threshold2:
                    condition = True
                    self.tacklingPlayer = player
                    break
        return condition
    def _checkPostcondition(self, data, index, selectedPlayer):
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
    " Class that defines the event detector for ball deflection "
    def __init__(self, file, goalkeeper0, goalkeeper1):
        """
      : param file: File containing a list of initialization parameters for the module
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
        "Check for acceleration above threshold in previous windowSize / 2 frames"
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
        Check that there has been contact between the goalkeeper and the ball

        : param data: Compact dataset with positional data and features
        : param index: Index on which to check the condition
        : param selectedPlayer: Player to check the condition on
        : return: A Boolean indicating whether the condition has occurred or not
        """
        condition = False

        if not self.accelerationCheck:
            return condition

        # For each player
        for player in chain(data[index].get('homeTeam'), data[index].get('awayTeam')):

            # Check that the player making the detour is a goalkeeper
            if selectedPlayer.playerID != self.GOALKEEPER0 and selectedPlayer.playerID != self.GOALKEEPER1:
                return False

            # Check that the ball is fast
            # if data [index] .get ('ball'). velocity <self.threshold2:
             # return False

            # Storicizzo il portiere, per l'emissione finale
            if (isMiddle):
                self.middlePlayer = selectedPlayer

            # # If player other than goalkeeper
            # if (player.playerID! = selectedPlayer.playerID):

             # # I check that his distance from the ball is greater than that of the goalkeeper
            # if (player.distToBall <selectedPlayer.distToBall):
             # return False
       
        condition = True
        # print("BallkeeperDeflection - Condition passed at frame:" + str(index))
        return condition

    def _checkPostcondition(self, data, index, selectedPlayer):
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
    "Class that defines the event detector for the ball out"
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
       Function that identifies whether the ball left the field during the time window
        In particular, it checks that it has exited either from the baseline, or from the side edges
        and does not consider the football goal and the areas from which the corner kick can take place

        : param data: Compact dataset with positional data and features
        : param index: Index from which the window starts
        : return: A dictionary with the recognized event, None in case nothing has been recognized
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

        # At first the ball must be within the size of the football pitch
        if (minFieldLine < startBall.xPosition) and (startBall.xPosition < maxFieldLine) and (minFieldCorner < startBall.yPosition) and (startBall.yPosition < maxFieldCorner):

            # At the end (of the observation window) the ball must be off the pitch except
            # a) in the area of ​​the two doors
            if (endBall.xPosition < 0 - 0.1 or endBall.xPosition > maxFieldLine + 0.1) and (endBall.yPosition < minGoalLimit or endBall.yPosition > maxGoalLimit):
                emit = True
            elif (endBall.xPosition <-5  or endBall.xPosition > maxFieldLine +5):
                emit = True
            elif (endBall.yPosition < 0 - 0.1 or endBall.yPosition > maxFieldCorner + 0.1):
                emit = True
            else:
                # Check lower left corner
                if (endBall.xPosition < 0 and endBall.xPosition > -2 and endBall.yPosition > -2 and endBall.yPosition < 0):
                    emit = False
                # Check upper left corner
                elif (endBall.xPosition < 0 and endBall.xPosition > -2 and endBall.yPosition < maxFieldCorner+2 and endBall.yPosition > maxFieldCorner):
                    emit = False
                # Check lower right corner
                elif (endBall.xPosition > maxFieldLine and endBall.xPosition < maxFieldLine+2 and endBall.yPosition > -2 and endBall.yPosition < 0):
                    emit = False
                # Check upper right corner
                elif (endBall.xPosition > maxFieldLine and endBall.xPosition < maxFieldLine+2 and endBall.yPosition < maxFieldCorner+2 and endBall.yPosition > maxFieldCorner):
                    emit = False
                
        
        # the ball is off the pitch but at the doors (behind the door mirror)
        elif (startBall.xPosition < 0 or startBall.xPosition > maxFieldLine) and (startBall.yPosition > minGoalLimit and startBall.yPosition < maxGoalLimit):
            if (endBall.xPosition <-5  or endBall.xPosition > maxFieldLine +5):
                emit = True


      
        if emit == True:
            ballOutFrame = int(startBall.timestamp + self.windowSize)
            # print("Emitting BallOut at frame", str(ballOutFrame))

            # Check that the BallOut is not after a special event
            # that is, an offside, a foul, or a penalty

            # For each list of events
            for lst in self.specialEvents:
                for event in lst:

                    #frame BallOut -> 28951
                    #frame Penalty -> 28928

                    # Check that the BallOut moment is after "event"
                    # within a certain range (the observation range)
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

            index += self.stride
            return [output, int(index)]
        else:
            return [None, int(index)]
    def _fieldLimit(self):
        """
        Extracts the headland position, to be modified if different reference systems are decided ()
        """
        return [0, self.xDimension]
    def _fieldCorner(self):
        """
        Extracts the position of the sides of the field, to be modified if different reference systems are decided ()
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
    "Class that defines the event detector for the goal"
    def __init__(self, file, xDimension, yDimension):
        """
        :param file: File containing a list of initialization parameters for the module
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
       Function that identifies whether the ball has entered the goal area

        : param data: Compact dataset with positional data and features
        : param index: Index from which the window starts
        : return: A dictionary with the recognized event, None in case nothing has been recognized
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
        Extracts the headland position, to be modified if different reference systems are decided ()
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
       Create an xml file from a list of dictionaries containing events

        : param data: Data structure from which to create the JSON file
        : param filename: String with the path to the JSON file
        : Return:
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
        "Extract second half start frame from Annotations_Atomic_Manual.xml"
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
        "Extract frames for goals, fouls and punishments from Annotations_Atomic_Manual.xml"
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
    "Class that performs the event detection"
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

        # I print the ids of the goalkeepers
        print("idGoalkeeper0", self.GOALKEEPER0, "idGoalkeeper1", self.GOALKEEPER1)

        # exchange the detectors starting from the past integer value, uncomment to activate it
        # Self._permutateFromInteger (permutation)
        self.detectors.insert(0, BallOutEvent(detectPath, xDimension, yDimension, self.specialEvents))

        # exchange the detectors starting from the past integer value, uncomment to activate it
        # Self._permutateFromInteger (permutation)
        self.dataset = dataset
        self.eventList = []
    def startDetection(self):
        "Function that performs the event detection for a single time of the game"
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
        "Function that performs event detection for an entire game"
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
        "Function that performs event detection for an entire game"
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
                # activate postprocessing instead of replacing goals when you want to identify them with the event detector
                self._sobstituteGoal()
                #self._postProcessing()
                XML.createEventXML(self.eventList, self.eventPath)
                elapsed = time() - start
                print('Elapsed {} seconds\n'.format(round(elapsed,1)))
        elapsedAll = time() - startAll
        print('Detection processing ended in {} seconds\n'.format(round(elapsedAll,1)))

    def startPreExtraction(self):
        "Function that extracts features from positional data and places them in a dataset"
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
        "Extract and compact the dataset"
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
        "Function that performs the event detection starting from features already in memory"
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
                self._sobstituteGoal()
                #self._postProcessing()

                #XML.createEventXML(self.eventList, self.eventPath)
                # elapsed = time() - start
                # print('Elapsed {} seconds\n'.format(round(elapsed,1)))
        
        # elapsedAll = time() - startAll
        # print('Detection processing ended in {} seconds\n'.format(round(elapsedAll,1)))

    def _sobstituteGoal(self):
        "Insert the arbitration data to the detected events (goals, fouls and punishments)"
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
        "Post processing to be used to identify goals"
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
        function to detect events

        : param data: Compact dataset with positional data and features
        : param detectors: List containing all the event detectors that you want to apply at each instant of time
        : return: A list with all detected events
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
       Create a file with the list of events with the features extracted
        : param overwrite: Bolean that indicates whether to overwrite the file or not
        : Return:
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


