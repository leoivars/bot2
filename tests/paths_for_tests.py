''' 
add parent dir to path for give access to app code 
'''
import sys
from pathlib import Path
test_dir = Path(__file__).parent
sys.path.append( str(test_dir.parent)     )  
