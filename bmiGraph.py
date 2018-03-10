from PyQt4 import QtGui  # (the example applies equally well to PySide)
import pyqtgraph as pg



app = QtGui.QApplication([])

pw=pg.plot()

while True:
    graph_data = open('testData.csv','r').read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    for line in lines:
        if len(line) > 1:
            z = line.split(',')
            xs.append(z[0])
            ys.append(z[1])
    pw.plot(xs,ys,clear=True)
    pg.QtGui.QApplication.processEvents()

