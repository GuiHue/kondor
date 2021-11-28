import sys
import csv
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

# Read CSV
#csvFileName = sys.argv[1]
csvFileName = "results/probe-results.ngc"
csvData = []
with open(csvFileName, 'r') as csvFile:
    csvReader = csv.reader(csvFile, delimiter=' ')
    for csvRow in csvReader:
        csvData.append(csvRow)

# Get X, Y, Z
csvData = np.array(csvData)
csvData = csvData.astype(float)
X, Y, Z = csvData[:,0], csvData[:,1], csvData[:,2]
zmin=np.min(Z)
zmax=np.max(Z)
print(zmin)
print(zmax)
print('Delta max:', zmax-zmin)
zavg=np.mean(Z)
# Plot X,Y,Z
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(X, Y, Z-zavg, color='white', edgecolors='grey', alpha=0.5)
ax.scatter(X, Y, Z-zavg, c='red')
plt.show()

#fig2 = plt.figure(figsize =(10, 7))
 
# Creating plot
#plt.boxplot(Z)
 
# show plot
#plt.show(fig2)
