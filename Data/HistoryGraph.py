from PyQt5.QtWidgets import QDialog, QSizePolicy
from QtDesign.HistoryGraph_ui import Ui_HistoryGraph
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as pyplot
from matplotlib import ticker
from matplotlib import dates
from mpl_finance import candlestick_ohlc
import pandas


class HistoryGraph(QDialog, Ui_HistoryGraph):

    def __init__(self, stock_data: pandas.DataFrame):
        super().__init__()
        self.setupUi(self)
        canvas = GraphCanvas(self, width=5, height=4)
        canvas.move(0, 0)
        canvas.plot(stock_data)


class GraphCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plot(self, stock_data: pandas.DataFrame):
        trimmed_data = pandas.DataFrame()
        trimmed_data['date'] = pandas.to_datetime(stock_data['date'], format="%Y-%m-%d")
        trimmed_data['date'] = dates.date2num(trimmed_data['date'])
        trimmed_data['open'] = stock_data['open']
        trimmed_data['high'] = stock_data['high']
        trimmed_data['low'] = stock_data['low']
        trimmed_data['close'] = stock_data['close']
        ax1 = pyplot.subplot2grid((6, 4), (1, 0), rowspan=4, colspan=4)
        candlestick_ohlc(ax1, trimmed_data.values, width=.6, colorup='#ff1717', colordown='#53c156')
        ax1.grid(True, color='w')
        ax1.xaxis.set_major_locator(ticker.MaxNLocator(10))
        ax1.xaxis.set_major_formatter(dates.DateFormatter('%Y-%m-%d'))
        ax1.yaxis.label.set_color("w")
        ax1.spines['bottom'].set_color("#5998ff")
        ax1.spines['top'].set_color("#5998ff")
        ax1.spines['left'].set_color("#5998ff")
        ax1.spines['right'].set_color("#5998ff")
        ax1.tick_params(axis='y', colors='w')
        pyplot.gca().yaxis.set_major_locator(ticker.MaxNLocator(prune='upper'))
        ax1.tick_params(axis='x', colors='w')
        ax1.plot()
        self.draw()
