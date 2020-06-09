import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec#分割子图
import mpl_finance as mpf #替换 import matplotlib.finance as mpf
import pandas as pd
import pandas_datareader.data as web
import datetime
import talib
import tushare as ts

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号



class ViewControllerClass():
	def __init__(self):
		self.fig = plt.figure(figsize=(8,6), dpi=100,facecolor="white")#创建fig对象
		self.gs = gridspec.GridSpec(4, 1, left=0.05, bottom=0.2, right=0.96, top=0.96, wspace=None, hspace=0, height_ratios=[3.5,1,1,1])
		self.graph_KAV = self.fig.add_subplot(self.gs[0,:])
		self.graph_VOL = self.fig.add_subplot(self.gs[1,:])
		self.graph_MACD = self.fig.add_subplot(self.gs[2,:])
		self.graph_KDJ = self.fig.add_subplot(self.gs[3,:])


	# 设置数据矩阵
	def SetShareData(self,df_stock):
		self.df = df_stock
		self.numt = np.arange(0, len(self.df.index))

	# 设置标题
	def SetTitle(self,title):
		# self.graph_KAV.set_title(u"600797 浙大网新-日K线")
		self.graph_KAV.set_title(title)


	# 绘制均线
	def DrawKLine(self):
		ohlc = []
		ohlc = list(zip(np.arange(0,len(self.df.index)),self.df.open,self.df.close,self.df.high,self.df.low))
		mpf.candlestick_ochl(self.graph_KAV, ohlc, width=0.2, colorup='r', colordown='g', alpha=1.0)
		self.graph_KAV.plot(self.numt, self.df['Ma20'],'black', label='M20',lw=1.0)
		self.graph_KAV.plot(self.numt, self.df['Ma30'],'green',label='M30', lw=1.0)
		self.graph_KAV.plot(self.numt, self.df['Ma60'],'blue',label='M60', lw=1.0)
		self.graph_KAV.legend(loc='best')
		self.graph_KAV.set_ylabel(u"价格")
		self.graph_KAV.set_xlim(0,len(self.df.index))
		self.graph_KAV.set_xticks(range(0,len(self.df.index),15))
		self.graph_KAV.grid(True,color='k')

	# 绘制交易量
	def DrawVol(self):
		self.graph_VOL.bar(self.numt, self.df.vol,color=['g' if self.df.open[x] > self.df.close[x] else 'r' for x in range(0,len(self.df.index))])
		self.graph_VOL.set_ylabel(u"成交量")
		self.graph_VOL.set_xlim(0,len(self.df.index))
		self.graph_VOL.set_xticks(range(0,len(self.df.index),15))


	# 绘制MACD
	def DrawMACD(self):
		macd_dif, macd_dea, macd_bar = talib.MACD(self.df['close'].values, fastperiod=12, slowperiod=26, signalperiod=9)
		self.graph_MACD.plot(np.arange(0, len(self.df.index)), macd_dif, 'red', label='macd dif')    
		self.graph_MACD.plot(np.arange(0, len(self.df.index)), macd_dea, 'blue', label='macd dea') 
		#绘制BAR>0 柱状图
		bar_red = np.where(macd_bar>0, 2*macd_bar, 0)
		#绘制BAR<0 柱状图
		bar_green = np.where(macd_bar<0, 2*macd_bar, 0)        
		self.graph_MACD.bar(np.arange(0, len(self.df.index)), bar_red, facecolor='red')
		self.graph_MACD.bar(np.arange(0, len(self.df.index)), bar_green, facecolor='green')
		self.graph_MACD.legend(loc='best',shadow=True, fontsize ='10')

		self.graph_MACD.set_ylabel(u"MACD")
		#graph_MACD.set_xlabel("日期")
		self.graph_MACD.set_xlim(0,len(self.df.index)) 
		self.graph_MACD.set_xticks(range(0,len(self.df.index),15))

	# 绘制KDJ
	def DrawKDJ(self):
		xd = 9-1
		date = self.df.index.to_series()
		RSV = pd.Series(np.zeros(len(date)-xd),index=date.index[xd:])
		Kvalue = pd.Series(0.0,index=RSV.index)
		Dvalue = pd.Series(0.0,index=RSV.index)
		Kvalue[0],Dvalue[0] = 50,50

		for day_ind in range(xd, len(self.df.index)):
			RSV[date[day_ind]] = (self.df.close[day_ind] - self.df.low[day_ind-xd:day_ind+1].min())/(self.df.high[day_ind-xd:day_ind+1].max()-self.df.low[day_ind-xd:day_ind+1].min())*100
			if day_ind > xd:
				index = day_ind-xd
				Kvalue[index] = 2.0/3*Kvalue[index-1]+RSV[date[day_ind]]/3
				Dvalue[index] = 2.0/3*Dvalue[index-1]+Kvalue[index]/3
		self.df['RSV'] = RSV
		self.df['K'] = Kvalue
		self.df['D'] = Dvalue
		self.df['J'] = 3*Kvalue-2*Dvalue   
		 
		self.graph_KDJ.plot(np.arange(0, len(self.df.index)), self.df['K'], 'blue', label='K')   
		self.graph_KDJ.plot(np.arange(0, len(self.df.index)), self.df['D'], 'g--', label='D')
		self.graph_KDJ.plot(np.arange(0, len(self.df.index)), self.df['J'], 'r-', label='J')        
		self.graph_KDJ.legend(loc='best',shadow=True, fontsize ='10')

		self.graph_KDJ.set_ylabel(u"KDJ")
		self.graph_KDJ.set_xlabel("日期")
		self.graph_KDJ.set_xlim(0,len(self.df.index))
		self.graph_KDJ.set_xticks(range(0,len(self.df.index),15))
		# self.graph_KDJ.set_xticklabels([self.df.index.strftime('%Y-%m-%d')[index] for index in self.graph_KDJ.get_xticks()])
		self.graph_KDJ.set_xticklabels([self.df.trade_date[index] for index in self.graph_KDJ.get_xticks()])

	# 显示横坐标
	def DrawXAxis(self):
		for label in self.graph_KAV.xaxis.get_ticklabels():   
			label.set_visible(False)

		for label in self.graph_VOL.xaxis.get_ticklabels():   
			label.set_visible(False)

		for label in self.graph_MACD.xaxis.get_ticklabels():   
			label.set_visible(False)
				
		for label in self.graph_KDJ.xaxis.get_ticklabels():   
			label.set_rotation(45)
			label.set_fontsize(10)


	# 显示买卖点
	def DrawDealPoint(self,list_signal):
		for i in range(len(list_signal)):
			if list_signal[i] < 0:
				self.graph_KAV.annotate(u"卖", xy=(i, self.df['Ma20'][i]), xytext=(i, self.df['Ma20'][i]+1.5),arrowprops=dict(facecolor='green', shrink=0.2))
				# print(self.df.iloc[i])
			if list_signal[i] > 0:
				self.graph_KAV.annotate(u"买", xy=(i, self.df['Ma20'][i]), xytext=(i, self.df['Ma20'][i]-1.5),arrowprops=dict(facecolor='red', shrink=0.2))
				# print(self.df.iloc[i])

	# 显示图表		
	def ShowChart(self):
		self.DrawKLine()
		self.DrawVol()
		self.DrawMACD()
		self.DrawKDJ()
		self.DrawXAxis()
		plt.show()



