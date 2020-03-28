# Import packages and modules
import os, sys, xml.etree.ElementTree as ET
from stat import *
from preprocessing.XML_to_ETALIS    import preprocess
from processing.ETALIS              import process
from postprocessing.ETALIS_to_XML   import postprocess
from evaluating.EVALUATOR           import evaluate
from visualizing.VISUALIZER         import visualize

inputDir = "input/"
outputDir = "output/"
dbDir = "processing/"

# Search for subdir under inputDir
for dir in os.listdir(inputDir):

    # Check if directory
    inputSubDir = os.path.join(inputDir, dir)
    mode = os.stat(inputSubDir)[ST_MODE]
    if S_ISDIR(mode):

        # Avoid hidden folders
        if (dir.startswith('.')):
            continue

        print(dir)

        # Search input file in subdir
        atomicEvents = os.path.join(inputSubDir, "Annotations_AtomicEvents_Detected.xml")
        atomicEvents_Manual = os.path.join(inputSubDir, "Annotations_AtomicEvents_Manual.xml")
        complexEvents = os.path.join(inputSubDir, "Annotations_ComplexEvents.xml")
        dbPath = os.path.join(dbDir, "utils.db")

        # Create outputSubDir and clear the content
        outputSubDir = os.path.join(outputDir, dir)
        if not os.path.exists(outputSubDir):
            os.makedirs(outputSubDir)
        
        for the_file in os.listdir(outputSubDir):
            file_path = os.path.join(outputSubDir, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

        outputComplexEvents = os.path.join(outputSubDir, "Annotations_ComplexEvents.xml")
        if os.path.isfile(atomicEvents) and os.path.isfile(complexEvents):

            atomicEventsStream = os.path.join(outputSubDir, "atomic-events.stream")
            complexEventsStream = os.path.join(outputSubDir, "complex-events.stream")            

            # Preprocess data
            preprocess(atomicEvents_Manual, dbPath, atomicEvents, atomicEventsStream)

            # Detect Complex Events with ETALIS
            process(atomicEventsStream, complexEventsStream)

            # Postprocess data
            postprocess(complexEventsStream, outputComplexEvents)

            # Clean
            os.remove(atomicEventsStream)
            # os.remove(complexEventsStream)
            
        evaluationOutputFilePath = os.path.join(outputSubDir, "evaluation.xml")
        evaluate(complexEvents, outputComplexEvents, evaluationOutputFilePath, "evaluating/complex.header", 10, 20, False)
        print("\r")

# BUILD the FINAL RESULTS plot
precision_means                     = [0,0,0,0,0,0,0,0,0,0,0]
recall_means                        = [0,0,0,0,0,0,0,0,0,0,0]

pass_evaluations                    = [0,0,0]
passThenGoal_evaluations            = [0,0,0]
filteringPass_evaluations           = [0,0,0]
filteringPassThenGoal_evaluations   = [0,0,0]
cross_evaluations                   = [0,0,0]
crossThenGoal_evaluations           = [0,0,0]
tackle_evaluations                  = [0,0,0]
shot_evaluations                    = [0,0,0]
shotOut_evaluations                 = [0,0,0]
shotThenGoal_evaluations            = [0,0,0]
savedShot_evaluations               = [0,0,0]
    
# Iterate over the outputSubDir(s)
for dir in os.listdir(outputDir):

    # Check if dir is directory
    outputSubDir = os.path.join(outputDir, dir)
    mode = os.stat(outputSubDir)[ST_MODE]
    if S_ISDIR(mode):

        # Check if an evaluation file exist
        evaluationFilePath = os.path.join(outputSubDir, "evaluation.xml")
        if (os.path.isfile(evaluationFilePath)):
            
            # Parse and get data
            tree = ET.parse(evaluationFilePath)
            root = tree.getroot()
            overall = root.find("overall")

            # Get Pass data
            p = overall.find("Pass")
            pass_evaluations[0] += int(p.find("TP").text)
            pass_evaluations[1] += int(p.find("FP").text)
            pass_evaluations[2] += int(p.find("FN").text)

            # Get PassThenGoal data
            ptg = overall.find("PassThenGoal")
            passThenGoal_evaluations[0] += int(ptg.find("TP").text)
            passThenGoal_evaluations[1] += int(ptg.find("FP").text)
            passThenGoal_evaluations[2] += int(ptg.find("FN").text)

            # Get FilteringPass data
            fp = overall.find("FilteringPass")
            filteringPass_evaluations[0] += int(fp.find("TP").text)
            filteringPass_evaluations[1] += int(fp.find("FP").text)
            filteringPass_evaluations[2] += int(fp.find("FN").text)

            # Get FilteringPassThenGoal data
            fptg = overall.find("FilteringPassThenGoal")
            filteringPassThenGoal_evaluations[0] += int(fptg.find("TP").text)
            filteringPassThenGoal_evaluations[1] += int(fptg.find("FP").text)
            filteringPassThenGoal_evaluations[2] += int(fptg.find("FN").text)

            # Get Cross data
            c = overall.find("Cross")
            cross_evaluations[0] += int(c.find("TP").text)
            cross_evaluations[1] += int(c.find("FP").text)
            cross_evaluations[2] += int(c.find("FN").text)

            # Get FilteringPassThenGoal data
            ctg = overall.find("CrossThenGoal")
            crossThenGoal_evaluations[0] += int(ctg.find("TP").text)
            crossThenGoal_evaluations[1] += int(ctg.find("FP").text)
            crossThenGoal_evaluations[2] += int(ctg.find("FN").text)

            # Get Tackle data
            t = overall.find("Tackle")
            tackle_evaluations[0] += int(t.find("TP").text)
            tackle_evaluations[1] += int(t.find("FP").text)
            tackle_evaluations[2] += int(t.find("FN").text)

            # Get Shot data
            s = overall.find("Shot")
            shot_evaluations[0] += int(s.find("TP").text)
            shot_evaluations[1] += int(s.find("FP").text)
            shot_evaluations[2] += int(s.find("FN").text)

            # Get ShotOut data
            so = overall.find("ShotOut")
            shotOut_evaluations[0] += int(so.find("TP").text)
            shotOut_evaluations[1] += int(so.find("FP").text)
            shotOut_evaluations[2] += int(so.find("FN").text)

            # Get ShotThenGoal data
            stg = overall.find("ShotThenGoal")
            shotThenGoal_evaluations[0] += int(stg.find("TP").text)
            shotThenGoal_evaluations[1] += int(stg.find("FP").text)
            shotThenGoal_evaluations[2] += int(stg.find("FN").text)

            # Get SavedShot data
            ss = overall.find("SavedShot")
            savedShot_evaluations[0] += int(ss.find("TP").text)
            savedShot_evaluations[1] += int(ss.find("FP").text)
            savedShot_evaluations[2] += int(ss.find("FN").text)

print("Results overview")
print("Pass: " + str(pass_evaluations[0]) + ", " + str(pass_evaluations[1]) + ", " + str(pass_evaluations[2]))
print("PassThenGoal: " + str(passThenGoal_evaluations[0]) + ", " + str(passThenGoal_evaluations[1]) + ", " + str(passThenGoal_evaluations[2]))
print("FilteringPass: " + str(filteringPass_evaluations[0]) + ", " + str(filteringPass_evaluations[1]) + ", " + str(filteringPass_evaluations[2]))
print("FilteringPassThenGoal: " + str(filteringPassThenGoal_evaluations[0]) + ", " + str(filteringPassThenGoal_evaluations[1]) + ", " + str(filteringPassThenGoal_evaluations[2]))
print("Cross: " + str(cross_evaluations[0]) + ", " + str(cross_evaluations[1]) + ", " + str(cross_evaluations[2]))
print("CrossThenGoal: " + str(crossThenGoal_evaluations[0]) + ", " + str(crossThenGoal_evaluations[1]) + ", " + str(crossThenGoal_evaluations[2]))
print("Tackle: " + str(tackle_evaluations[0]) + ", " + str(tackle_evaluations[1]) + ", " + str(tackle_evaluations[2]))
print("Shot: " + str(shot_evaluations[0]) + ", " + str(shot_evaluations[1]) + ", " + str(shot_evaluations[2]))
print("ShotOut: " + str(shotOut_evaluations[0]) + ", " + str(shotOut_evaluations[1]) + ", " + str(shotOut_evaluations[2]))
print("ShotThenGoal: " + str(shotThenGoal_evaluations[0]) + ", " + str(shotThenGoal_evaluations[1]) + ", " + str(shotThenGoal_evaluations[2]))
print("SavedShot: " + str(savedShot_evaluations[0]) + ", " + str(savedShot_evaluations[1]) + ", " + str(savedShot_evaluations[2]))
print("\r")

# Generate PRECISION after parsed all evalutions files
try:
    precision_means[0] = round(pass_evaluations[0] / (pass_evaluations[0] + pass_evaluations[1]), 2) * 100   
except ZeroDivisionError:
    precision_means[0] = 0

try:
    precision_means[1] = round(passThenGoal_evaluations[0] / (passThenGoal_evaluations[0] + passThenGoal_evaluations[1]), 2) * 100   
except ZeroDivisionError:
    precision_means[1] = 0

try:
    precision_means[2] = round(filteringPass_evaluations[0] / (filteringPass_evaluations[0] + filteringPass_evaluations[1]), 2) * 100   
except ZeroDivisionError:
    precision_means[2] = 0

try:
    precision_means[3] = round(filteringPassThenGoal_evaluations[0] / (filteringPassThenGoal_evaluations[0] + filteringPassThenGoal_evaluations[1]), 2) * 100   
except ZeroDivisionError:
    precision_means[3] = 0

try:
    precision_means[4] = round(cross_evaluations[0] / (cross_evaluations[0] + cross_evaluations[1]), 2) * 100
except ZeroDivisionError:
    precision_means[4] = 0

try:
    precision_means[5] = round(crossThenGoal_evaluations[0] / (crossThenGoal_evaluations[0] + crossThenGoal_evaluations[1]), 2) * 100   
except ZeroDivisionError:
    precision_means[5] = 0

try:
    precision_means[6] = round(tackle_evaluations[0] / (tackle_evaluations[0] + tackle_evaluations[1]), 2) * 100   
except ZeroDivisionError:
    precision_means[6] = 0

try:
    precision_means[7] = round(shot_evaluations[0] / (shot_evaluations[0] + shot_evaluations[1]), 2) * 100
except ZeroDivisionError:
    precision_means[7] = 0

try:
    precision_means[8] = round(shotOut_evaluations[0] / (shotOut_evaluations[0] + shotOut_evaluations[1]), 2) * 100   
except ZeroDivisionError:
    precision_means[8] = 0

try:
    precision_means[9] = round(shotThenGoal_evaluations[0] / (shotThenGoal_evaluations[0] + shotThenGoal_evaluations[1]), 2) * 100
except ZeroDivisionError:
    precision_means[9] = 0

try:
    precision_means[10] = round(savedShot_evaluations[0] / (savedShot_evaluations[0] + savedShot_evaluations[1]), 2) * 100
except ZeroDivisionError:
    precision_means[10] = 0


# Generate RECALL after parsed all evalutions files
try:
    recall_means[0] = round(pass_evaluations[0] / (pass_evaluations[0] + pass_evaluations[2]), 2) * 100   
except ZeroDivisionError:
    recall_means[0] = 0

try:
    recall_means[1] = round(passThenGoal_evaluations[0] / (passThenGoal_evaluations[0] + passThenGoal_evaluations[2]), 2) * 100
except ZeroDivisionError:
    recall_means[1] = 0

try:
    recall_means[2] = round(filteringPass_evaluations[0] / (filteringPass_evaluations[0] + filteringPass_evaluations[2]), 2) * 100
except ZeroDivisionError:
    recall_means[2] = 0

try:
    recall_means[3] = round(filteringPassThenGoal_evaluations[0] / (filteringPassThenGoal_evaluations[0] + filteringPassThenGoal_evaluations[2]), 2) * 100
except ZeroDivisionError:
    recall_means[3] = 0

try:
    recall_means[4] = round(cross_evaluations[0] / (cross_evaluations[0] + cross_evaluations[2]), 2) * 100
except ZeroDivisionError:
    recall_means[4] = 0

try:
    recall_means[5] = round(crossThenGoal_evaluations[0] / (crossThenGoal_evaluations[0] + crossThenGoal_evaluations[2]), 2) * 100   
except ZeroDivisionError:
    recall_means[5] = 0

try:
    recall_means[6] = round(tackle_evaluations[0] / (tackle_evaluations[0] + tackle_evaluations[2]), 2) * 100   
except ZeroDivisionError:
    recall_means[6] = 0

try:
    recall_means[7] = round(shot_evaluations[0] / (shot_evaluations[0] + shot_evaluations[2]), 2) * 100
except ZeroDivisionError:
    recall_means[7] = 0

try:
    recall_means[8] = round(shotOut_evaluations[0] / (shotOut_evaluations[0] + shotOut_evaluations[2]), 2) * 100   
except ZeroDivisionError:
    recall_means[8] = 0

try:
    recall_means[9] = round(shotThenGoal_evaluations[0] / (shotThenGoal_evaluations[0] + shotThenGoal_evaluations[2]), 2) * 100
except ZeroDivisionError:
    recall_means[9] = 0

try:
    recall_means[10] = round(savedShot_evaluations[0] / (savedShot_evaluations[0] + savedShot_evaluations[2]), 2) * 100
except ZeroDivisionError:
    recall_means[10] = 0

# Generate plot
visualize(tuple(precision_means), tuple(recall_means))