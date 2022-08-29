import matplotlib.pyplot as plt

l1 = []
l2 = []
l3 = []

fig = plt.figure()
ax = plt.axes(projection ='3d')

with open('points.pts', 'r') as f:
    for line in f:
        p = line.strip().split()
    
        l1.append(float(p[0]))
        l2.append(float(p[1]))
        l3.append(float(p[2]))

ax.scatter(l1, l2, l3,)
plt.show()
