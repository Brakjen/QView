import sys
import os
sys.path.append(os.getcwd())
from orca import OrcaOutput

f = '/Users/abr121/Documents/dev/QViewDesigner/QView/output_parsers/orca_sp_notdone.out'

output = OrcaOutput(f)

print(output.getSCFRuns())