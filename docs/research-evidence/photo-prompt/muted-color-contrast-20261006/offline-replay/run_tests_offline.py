import sys, unittest
from pathlib import Path
from offline_guard import install
install()
sys.path.insert(0,str(Path.cwd()))
suite=unittest.defaultTestLoader.loadTestsFromNames(sys.argv[1:])
result=unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(not result.wasSuccessful())
