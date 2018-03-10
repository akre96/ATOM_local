from PyQt4 import QtGui  # (the example applies equally well to PySide)
import pyqtgraph as pg



app = QtGui.QApplication([])

pw=pg.plot()

while True:
    graph_data = open('testData.csv','r').read()
    lines = graph_data.split('\n')[1:]
    xs = []
    ys = []
    for line in lines:
        if len(line) > 1:
            z = line.split(',')
            xs.append(int(z[0]))
            ys.append(int(z[1]))
            print z
    pw.plot(xs,ys,clear=True)
    pg.QtGui.QApplication.processEvents()

