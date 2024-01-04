import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import fmds0809

building = fmds0809.Building('./src/test_data.json')

print(building.main())