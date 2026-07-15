import numpy as np
import scipy.stats as sps
import scipy.optimize as spo
import matplotlib.pyplot as plt

import importlib.util; import sys; spec = importlib.util.spec_from_file_location("monkey_patch", r'/home/codespace/.vscode-remote/extensions/ofirbartal.sciviewer-0.2.1/out/assets/monkey_patch.py'); module = importlib.util.module_from_spec(spec); sys.modules["monkey_patch"] = module; spec.loader.exec_module(module)

time, x = np.loadtxt('Raw_Data.csv', usecols=(0,1), skiprows=1, delimiter=',', unpack=True)
print(time, x)

plt.plot(time, x)
plt.show()

