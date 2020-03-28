# Import packages
import os, subprocess, time

def process(
    input = "atomic-events.stream",
    output = "complex-events.stream"):

    # Start measure time
    start = time.time()

    # 1st STEP: Find events with the consumption policy set as 'recent'
    #               and find only savedShot events
    savedShotEvents = "savedShot-events.stream"
    recentEventRules = "processing/savedShot.rules"

    f = open(savedShotEvents,"w+")
    subprocess.call(
        [   "swipl",
            "-g",
            "open('../results.txt',append,FH), " +
                "['../../src/etalis.P'], " + 
                "set_etalis_flag(store_fired_events,on), " + 
                #"set_etalis_flag(event_consumption_policy,recent), " + 
                "compile_event_file('" + recentEventRules + "'), "+
                "load_database('processing/utils.db'), " +
                "execute_event_stream_file('" + input + "'), " +
                "findall(" +
                    "stored_event(event(pass(X),T)), " +
                    "stored_event(event(pass(X),T)),List), " +
                    "(List = [stored_event(event(pass(1),[datime(_,_,_,_,_,_,_),datime(_,_,_,_,_,_,_)]))] -> write(FH,'where_01\t\t\tpassed\n') ; write(FH,'where_01\t\t\tfailed\n') ),"
                    +"halt."],

        stdout = f,
        stderr = subprocess.DEVNULL)
    f.close()

    # 2st STEP: Find events with the consumption policy set as 'recent'
    recentOutput = "recent-complex-events.stream"
    recentEventRules = "processing/recentEvent.rules"

    f = open(recentOutput,"w+")
    subprocess.call(
        [   "swipl",
            "-g",
            "open('../results.txt',append,FH), " +
                "['../../src/etalis.P'], " + 
                "set_etalis_flag(store_fired_events,on), " + 
                #"set_etalis_flag(event_consumption_policy,recent), " + 
                "compile_event_file('" + recentEventRules + "'), "+
                "load_database('processing/utils.db'), " +
                "execute_event_stream_file('" + input + "'), " +
                "findall(" +
                    "stored_event(event(pass(X),T)), " +
                    "stored_event(event(pass(X),T)),List), " +
                    "(List = [stored_event(event(pass(1),[datime(_,_,_,_,_,_,_),datime(_,_,_,_,_,_,_)]))] -> write(FH,'where_01\t\t\tpassed\n') ; write(FH,'where_01\t\t\tfailed\n') ),"
                    +"halt."],

        stdout = f,
        stderr = subprocess.DEVNULL)
    f.close()

    # 3rd STEP: Find events with the consumption policy set as 'chronological'
    chronologicalOutput = "chronological-complex-events.stream"
    chronologicalEventRules = "processing/chronologicalEvent.rules"

    f = open(chronologicalOutput,"w+")
    subprocess.call(
        [   "swipl",
            "-g",
            "open('../results.txt',append,FH), " +
                "['../../src/etalis.P'], " + 
                "set_etalis_flag(store_fired_events,on), " + 
                "set_etalis_flag(event_consumption_policy,chronological), " + 
                "compile_event_file('" + chronologicalEventRules + "'), "+
                "load_database('processing/utils.db'), " +
                "execute_event_stream_file('" + input + "'), " +
                "findall(" +
                    "stored_event(event(pass(X),T)), " +
                    "stored_event(event(pass(X),T)),List), " +
                    "(List = [stored_event(event(pass(1),[datime(_,_,_,_,_,_,_),datime(_,_,_,_,_,_,_)]))] -> write(FH,'where_01\t\t\tpassed\n') ; write(FH,'where_01\t\t\tfailed\n') ),"
                    +"halt."],

        stdout = f,
        stderr = subprocess.DEVNULL)
    f.close()

    # Merge results
    filenames = [recentOutput, savedShotEvents, chronologicalOutput]
    with open(output, 'w+') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)

    # Clean
    os.remove(recentOutput)
    os.remove(savedShotEvents)
    os.remove(chronologicalOutput)

    # Stop measure time
    end = time.time()

    # Print info
    elapsed = round(end-start, 1)
    print("[ETALIS]\t Processed data in: " + str(elapsed) + "s.")