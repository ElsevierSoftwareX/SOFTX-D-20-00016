# EventDetector_Complex
This is the second half of the **Event Detection System**.

It recognizes the following *Complex events*:

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

And takes as input the following *Atomic events*:

1. kickingTheBall
2. ballPossession
3. ballDeflection
4. ballOut
5. goal
6. penalty
7. foul
8. tackle

## Run the system
To run the system follow the instructions:

1. Create a folder containing the input files:
 - `Annotations_AtomicEvents.txt`, the events exported by the EventDetector_Atomic
 - `Annotations_AtomicEvents_Manual.txt`, the file containing the frame of the second half and the goalkeepers identifiers
 - `Annotations_ComplexEvents.txt`, the ground truth of the Complex Events
2. Place the created folder in `EventDetector_Complex/detector/framework/input/`
3. Launch the process.

To launch the process, open a terminal on `EventDetector_Complex/detector/framework/` and type

```
python3 detect.py
```