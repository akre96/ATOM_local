import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style


style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
    graph_data = open('testData.csv','r').read()
    lines = graph_data.split('\n')[1:]
    xs = []
    ys = []
    for line in lines:
        if len(line) > 1:
            z = line.split(',')
            xs.append(z[0])
            ys.append(z[1])
    ax1.clear()
    ax1.plot(xs, ys)

ani = animation.FuncAnimation(fig, animate, interval=1)
plt.show()
