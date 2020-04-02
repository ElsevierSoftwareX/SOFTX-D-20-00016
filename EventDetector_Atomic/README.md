# Optimizer
This is the genetic algorithm to optimize atomic events.

It optimize the following *Atomic events*:

1. kickingTheBall
2. ballPossession
3. ballDeflection
4. tackle

## Run the system
To run the system you should have a dateset folder with a series of subfolder containing following files:
 - `features.log`, the positional data the extracted feature
 - `Annotations_AtomicEvents_Manual.txt`, the file containing the frame of the second half and the goalkeepers identifiers
 - `Annotations_AtomicEvents.xml`, the dataset events to verify

To launch the process, open a terminal on `Optimizer/` and type

```
python3 optimizer.py -options datasetPath 
```

where -options could be any of the following:
 - h/help: To check every possible option
 - m/maxSize: Maximum memory occupation in MB
 - mo/mode: Execution mode, chosen between FEATURE to only extract features, OPTIMIZER to start optimization and TEST to test the dataset against seeds
 - s/samplingRate: Sampling rate of original dataset
 - x/xDimension: Lenght in meters of the soccer field
 - y/yDimension: Width in meters of the soccer field
 - ps/populationSize: Size of the population for SPEA2 algorithm
 - as/archiveSize: Size of the archive for SPEA2 algorithm
 - n/numberOfGeneration: Number of generation for SPEA2 algorithm
 - c/crossoverProbability: Crossover probability for SPEA2 algorithm
 - mu/mutationProbability: Mutation probability for SPEA2 algorithm
 - se/seed: Individuals to use in TEST mode
 - fo/finalOutput: Path to final output file
