import os
from pathlib import Path

# Paths
CONSTPATH = CONSTANTSPATH = os.path.dirname(__file__)
ROOTPATH = Path(CONSTANTSPATH).parent
OUTPUTPATH = os.path.join(ROOTPATH, 'outputs')


GREENLIST = ['jpg', 'gif']

