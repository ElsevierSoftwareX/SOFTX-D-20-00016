# EventDetector_Atomic
This is the first half of the **Event Detection System**.

It recognizes the following *Atomic events*:

1. kickingTheBall
2. ballPossession
3. ballDeflection
4. ballOut
5. goal
6. penalty
7. foul
8. tackle

## Install requirements
Before to start to run the system make sure to have all the required packages.
To install the packages type the following command:

```
python3 -m pip install -r requirements.txt
```

## Run the system
To run the system you should have a dateset folder with the following files:
 - `positions.log` or `features.log`, the positional data with or without the extracted feature
 - `Annotations_AtomicEvents_Manual.txt`, the file containing the frame of the second half and the goalkeepers identifiers

To launch the process, open a terminal on `Optimizer/EventDetector_Atomic/` and type

```
python3 detector.py -options datasetPath 
```

where -options could be any of the following:
 - h/help: To check every possible option
 - m/maxSize: Maximum memory occupation in MB
 - mo/mode: Execution mode, chosen between SINGLE, FULL, FEAT and EXTR
 - s/samplingRate: Sampling rate of original dataset
 - x/xDimension: Lenght in meters of the soccer field
 - y/yDimension: Width in meters of the soccer field
 - f /firstHalf : If in SINGLE mode and checking first time