import subprocess
import time
# This script does the whole conversion pipeline

# 1) Conversion_to_PositionsLog: "annotation.xml"           -> "positions_onscreen.log"
# 2) positionsLog2dTo3d:         "positions_onscreen.log"   -> "positions_onthepitch.log"
# 3) coordinates_mapper          "positions_onthepitch.log" -> "positions_final_partial.log"
# 4) data_filler                 "positions_partial.log"    -> "positions.log"

input_file = "anotation.xml"
output_file = "positions.log"

stage_1_filename = "conversion_to_PositionsLog.py"
stage_2_filename = "positionsLog2dTo3d.py"
stage_3_filename = "coordinates_mapper.py"
stage_4_filename = "data_filler.py"

whole_start_time = time.time()
print("[do_pipeline.py] started...\n")

start_time = time.time()
print("[{0}] started...".format(stage_1_filename))
subprocess.call("python " + stage_1_filename)
print("[{0}] ended in {1:.2f} seconds.\n".format(stage_1_filename, time.time() - start_time))

start_time = time.time()
print("[{0}] started...".format(stage_2_filename))
subprocess.call("python " + stage_2_filename)
print("[{0}] ended in {1:.2f} seconds.\n".format(stage_2_filename, time.time() - start_time, ))

start_time = time.time()
print("[{0}] started...".format(stage_3_filename))
subprocess.call("python " + stage_3_filename)
print("[{0}] ended in {1:.2f} seconds.\n".format(stage_3_filename, time.time() - start_time))

start_time = time.time()
print("[{0}] started...".format(stage_4_filename))
subprocess.call("python " + stage_4_filename)
print("[{0}] ended in {1:.2f} seconds.\n".format(stage_4_filename, time.time() - start_time))

print("\n[do_pipeline.py] ended in {0:.2f} seconds.".format(time.time() - whole_start_time))