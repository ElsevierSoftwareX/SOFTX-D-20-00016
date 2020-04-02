# Validator
This is the validator for events recognized by the **Event Detection System**.

It validates the following *Atomic events*:

1. kickingTheBall
2. ballPossession
3. ballDeflection
4. ballOut
5. goal
6. penalty
7. foul
8. tackle

And the following *Complex events*:
1. pass
2. passThenGoal
3. filteringPass
4. filteringPassThenGoal
5. cross
6. crossThenGoal
7. shot
8. shotOut
9. shotThenGoal
10. savedShot
11. Tackle

## Run the system
To run the system you should have a dateset folder with the following files:
 - `Annotations_AtomicEvents.xml`, the dataset events
 - `Annotations_AtomicEvents_Detected.xml`, the detected events
 - `Annotations_AtomicEvents_Manual.xml`, the file containing the frame of the second half and the goalkeepers identifiers

To launch the process, open a terminal on `Optimizer/Validator/` and type

```
python3 validator.py -options datasetPath 
```

where -options could be any of the following:
 - h/help: To check every possible option
 - e/eventFile: Name of the file with the event list to recognize
 - o/outputFile: Name of the output file
 - a/atomic: Use this if you are checking atomic events
 - w/windowSize: Size of the window to check atomic event
 - p/percentage : Percentage to check complex event