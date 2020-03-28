# -*- coding: utf-8 -*-

# Import package(s)
from queue import Queue
from threading import Thread
import multiprocessing, os, logging, time, sys
from dataclasses import dataclass
from dataclasses_json import dataclass_json

# CONST VALUE(s)
POSITIONS_INPUT_FILE = "positions_2.log"
CPU_PARALLELISM_MAX = 12

class Read(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):

        # Get the notebook from the queue
        notebook, lines = self.queue.get()
        
        if lines == len(notebook):
            print("The len of my chunk is: " + str(len(notebook)) + ", in agree with the expected.")
            self.read(notebook, 0, 800000)
        else:
            print("The len of my chunk is: " + str(len(notebook)))
            
        self.queue.task_done()
        sys.exit(0)

    def read(self, notebook, firstTime, secondTime):
        entries = []
        try:
            countNone = 0
            for line in notebook:
                extractedData = self._extractFromLine(line.rstrip('\n'))
                if (extractedData is None):
                    countNone += 1
                else:
                    newEntry = self.PlayerData(*extractedData, *[-1 for i in range(14 - len(extractedData))])
                    entries.append(newEntry)
                    
            
            print("Thread ended. Created: " + str(len(entries)) + " player data classes.")
            if(countNone > 0):
                print(countNone)
        except Exception as e:
            print(e)
            print('Exit process')

    def _extractFromLine(self, line):
        try:
            elements = line.split(" ")
            return [float(element) for element in elements]
        except:
            return None

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
        
def main():

    # Initialize variable(s)
    lines_number = 0
    lines_threshold = 100000
    notebook = []
    bookshelf = Queue()

    # Make use of 11 readers
    # (MASTER-SLAVE Design pattern)
    #
    # EXPLANATION:
    # I am the main thread, and since my pc has 12 logical
    # threads, I can have other 11 slave-threads.
    for x in range(CPU_PARALLELISM_MAX-1):
        reader = Read(bookshelf)
        reader.daemon = True
        reader.start()
    
    # Read the file until the EOF
    start = time.time()
    with open(POSITIONS_INPUT_FILE) as f:
        for line in f:

            # Store the line
            notebook.append(line)

            # Increment counter of lines
            lines_number += 1

            # Check if it reaches the threshold
            if lines_number >= lines_threshold:

                # Put a chunk on a concurrent collection
                bookshelf.put((notebook, lines_number))
                
                # Start to fill a new collection
                notebook = []
                lines_number = 0

    # Check if there is more here
    if (len(notebook)) > 0:
        bookshelf.put((notebook, len(notebook)))

    # Wait the result
    bookshelf.join()
    end = time.time()
    print("The process took: " + str(round(end - start, 2)) + "s.")
    print("Done")

if __name__ == '__main__':
    main()
