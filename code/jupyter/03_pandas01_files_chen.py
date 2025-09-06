import pandas as pd
import os
import os.path as path
# print (os.path.expanduser('~'))
HOME = (os.path.expanduser('~'))    ### give us ~, the home directory
print("HOMMMMMMMMMMM", HOME)

data_path = HOME + '/workspace/class/jupyter/data'
print("WWWWWWWWWWWWW", data_path)

# ##### option 1: ##### works in macOS/Windows/Jupyter
# df = pd.read_csv(data_path+"/data.csv")


# ##### option 2: with open ##### works in macOS/Windows/Jupyter
# with open(data_path+"/data.csv") as f:
#     df = pd.read_csv(f)


# ##### option 3: path.join ##### works in mac/Windows/Jupyter
# data = path.join(data_path, "data.csv")
# with open(data) as f:
#     df = pd.read_csv(f)


##### option 4: change dir ##### works in Windows 11/macOS/Jupyter
os.chdir(data_path)
df = pd.read_csv("data.csv")

# ##### output
print(df.describe())

