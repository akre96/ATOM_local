from PyQt4 import QtGui  # (the example applies equally well to PySide)
import pyqtgraph as pg
import plotly.plotly as py
from plotly.graph_objs import Scatter, Layout, Figure
import time
import readadc

username = 'akre96'
apikey='cC6LIzUltGaMR953sVxH'
stream_token = 'a7adx0bmhu'
py.sign_in(username, api_key)

trace1 = Scatter(
    x=[],
    y=[],
    stream=dict(
        token=stream_token,
        maxpoints=200
    )
)

layout = Layout(
    title='Raspberry Pi Streaming Sensor Data'
)

fig = Figure(data=[trace1], layout=layout)

print py.plot(fig, filename='Raspberry Pi Streaming Example Values')

#app = QtGui.QApplication([])
py.sign_in(username, api_key)


stream = py.Stream(stream_token)
stream.open()
##pw=pg.plot()
#
#while True:
#    graph_data = open('testData.csv','r').read()
#    lines = graph_data.split('\n')[1:]
#    xs = []
#    ys = []
#    for line in lines:
#        if len(line) > 1:
#            z = line.split(',')
#            xs.append(int(z[0]))
#            ys.append(int(z[1]))
#    pw.plot(xs,ys,clear=True)
#    pg.QtGui.QApplication.processEvents()
#
