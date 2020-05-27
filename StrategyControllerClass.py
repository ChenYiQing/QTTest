import pandas as pd
import numpy as np
import copy

class StrategyControllerClass():
	def __init__(self):
		pass

	# 根据传入的跳变值获取买卖点
	def GetSellPointAndTotalValue(self,list_signal,df_data,printBoo):
		dealTypeList = []
		dealDateList = []
		dealPriceList = []

		# 买卖点 仓位 
		for i in range(len(list_signal)):
			if list_signal[i]<0:
				if len(dealTypeList) > 0:
					dealTypeList.append('sell')
					dealDateList.append(df_data.loc[i]['trade_date'])
					dealPriceList.append(df_data.loc[i]['close'])
			if list_signal[i]>0:
				dealTypeList.append('buy')
				dealDateList.append(df_data.loc[i]['trade_date'])
				dealPriceList.append(df_data.loc[i]['close'])

		# 打印
		if printBoo:
			for i in range(len(dealTypeList)):
				print(dealTypeList[i]+' '+dealDateList[i]+' '+str(dealPriceList[i]))
				if dealTypeList[i]=='sell':
					if dealPriceList[i] > dealPriceList[i-1]:
						print('盈--> '+str(round(dealPriceList[i] - dealPriceList[i-1],2)))
					else:
						print('亏--> '+str(round(dealPriceList[i] - dealPriceList[i-1],2)))


		# 盈亏
		total = 0
		for i in range(len(dealTypeList)):
			if dealTypeList[i]=='sell':
				total = total + dealPriceList[i]-dealPriceList[i-1]

		return total

	# 策略1 周K ma5>ma10>ma15>ma20
	def Strategy01(self,df_data):
		list_deltaSum = np.sign(df_data['Ma5']-df_data['Ma10'])+np.sign(df_data['Ma10']-df_data['Ma15'])+np.sign(df_data['Ma15']-df_data['Ma20'])
		# 前几行空值补0
		list_deltaSum = list_deltaSum.fillna(0)
		len = df_data.iloc[:,0].size
		data = np.array([2.5]*len)
		list_same = pd.Series(data,index = [i for i in range(0,len)],dtype = float)
		list_diff = np.sign(list_deltaSum-list_same)
		list_signal = np.sign(list_diff-list_diff.shift(1))

		total = self.GetSellPointAndTotalValue(list_signal,df_data,True)
		print(total)

	# 策略2 周K 底分型 下下上上上 买入 盈利0.01止盈 亏损0.01止损
	def Strategy02(self,df_data,printInfo):
		total = 0		
		totalWith30Days = 0
		ShortTradeTimes = 0
		LongTradeTimes = 0
		ShortDateList = []
		daysList = []

		totalWinTimes = 0
		totalLossTimes= 0

		for index in df_data.index:
			if index > 6 and index< df_data.shape[0]-1:
				openValue = df_data.loc[index,'open']
				closeValue = df_data.loc[index,'close']

				H5 = df_data.loc[index,'high']
				L5 = df_data.loc[index,'low']
				H4 = df_data.loc[index-1,'high']
				L4 = df_data.loc[index-1,'low']
				H3 = df_data.loc[index-2,'high']
				L3 = df_data.loc[index-2,'low']
				H2 = df_data.loc[index-3,'high']
				L2 = df_data.loc[index-3,'low']
				H1 = df_data.loc[index-4,'high']
				L1 = df_data.loc[index-4,'low']
				H0 = df_data.loc[index-5,'high']
				L0 = df_data.loc[index-5,'low']
				# 满足下下上上上
				# if closeValue>openValue and H5>H4 and L5>L4 and H4>H3 and L4>L3 and H3>H2 and L3>L2 and H1>H2 and L1>L2 and H0>H1 and L0>L1:
				if H5>H4 and L5>L4 and H4>H3 and L4>L3 and H3>H2 and L3>L2 and H1>H2 and L1>L2 and H0>H1 and L0>L1:

					if printInfo:
						print(str(df_data.loc[index,'trade_date'])+' DDUUU')
						print(str(df_data.loc[index,'close'])+' with buy')
					buyPoint = df_data.loc[index,'close']
					# 盈亏
					cursor = index+1
					winAlpha = 0.01
					lossAlpha = 0.01

					# while abs(df_data.loc[cursor,'high']-buyPoint)/buyPoint < alpha or abs(df_data.loc[cursor,'low']-buyPoint)/buyPoint < alpha:
					# 止盈不止损
					keepDay = 1
					while True:
						# 超过0.01 止盈
						if (df_data.loc[cursor,'high']-buyPoint)/buyPoint > winAlpha:
							# print('win')
							if printInfo:
								print(str(df_data.loc[cursor,'trade_date'])+' for win')

							totalWinTimes = totalWinTimes+1
							break

						# 超过0.05 止损
						if (buyPoint-df_data.loc[cursor,'high'])/buyPoint > lossAlpha:
							# print('loss')
							if printInfo:
								print(str(df_data.loc[cursor,'trade_date'])+' for loss')
							totalLossTimes = totalLossTimes+1
							break

						if df_data.shape[0]-1 >cursor:
							cursor = cursor+1
							keepDay = keepDay+1
						else:
							break

					sellPoint = df_data.loc[cursor,'high']
					if printInfo:
						print(str(df_data.loc[cursor,'trade_date'])+' over alpha')
						print(str(df_data.loc[cursor,'high'])+' to sell')
						print('盈亏：'+str(sellPoint-buyPoint))
						print('持有天数：'+str(keepDay))
						print('---------------------------------------')
					total = total+sellPoint-buyPoint
					daysList.append(keepDay)
					if keepDay<30:

						totalWith30Days = totalWith30Days+sellPoint-buyPoint
						ShortTradeTimes = ShortTradeTimes+1
						ShortDateList.append(df_data.loc[cursor,'trade_date'])
					else:
						LongTradeTimes = LongTradeTimes+1
						print(str(df_data.loc[index,'trade_date'])+' with buy')
						print(str(df_data.loc[cursor,'trade_date'])+' to sell')

		print('win:'+str(totalWinTimes))
		print('loss:'+str(totalLossTimes))

		if printInfo:
			print('累计盈亏：'+str(total))
			print('断线盈亏：'+str(totalWith30Days))
		# return totalWith30Days,ShortTradeTimes,LongTradeTimes,ShortDateList,daysList
		return totalWinTimes,totalLossTimes

	def Strategy02Infer(self,df_data):
		index = df_data.shape[0]-1
		H5 = df_data.loc[index,'high']
		L5 = df_data.loc[index,'low']
		H4 = df_data.loc[index-1,'high']
		L4 = df_data.loc[index-1,'low']
		H3 = df_data.loc[index-2,'high']
		L3 = df_data.loc[index-2,'low']
		H2 = df_data.loc[index-3,'high']
		L2 = df_data.loc[index-3,'low']
		H1 = df_data.loc[index-4,'high']
		L1 = df_data.loc[index-4,'low']
		H0 = df_data.loc[index-5,'high']
		L0 = df_data.loc[index-5,'low']
		# 满足下下上上上
		if H5>H4 and L5>L4 and H4>H3 and L4>L3 and H3>H2 and L3>L2 and H1>H2 and L1>L2 and H0>H1 and L0>L1:
			return True
		else:
			return False



	def test(self,df_data):
		list_diff = np.sign(df_data['Ma20']-df_data['Ma60'])
		print(list_diff)
		list_signal = np.sign(list_diff-list_diff.shift(1))
		print(list_signal)

		dealTypeList = []
		dealDateList = []
		dealPriceList = []

		# 买卖点 仓位 
		for i in range(len(list_signal)):
			if list_signal[i]<0:
				if len(dealTypeList) > 0:
					dealTypeList.append('sell')
					dealDateList.append(df_data.loc[i]['trade_date'])
					dealPriceList.append(df_data.loc[i]['close'])
			if list_signal[i]>0:
				dealTypeList.append('buy')
				dealDateList.append(df_data.loc[i]['trade_date'])
				dealPriceList.append(df_data.loc[i]['close'])

		# 打印
		# for i in range(len(dealTypeList)):
		# 	print(dealTypeList[i]+' '+dealDateList[i]+' '+str(dealPriceList[i]))
		# 	if dealTypeList[i]=='sell':
		# 		if dealPriceList[i] > dealPriceList[i-1]:
		# 			print('盈--> '+str(round(dealPriceList[i] - dealPriceList[i-1],2)))
		# 		else:
		# 			print('亏--> '+str(round(dealPriceList[i] - dealPriceList[i-1],2)))



		# 盈亏
		total = 0
		for i in range(len(dealTypeList)):
			if dealTypeList[i]=='sell':
				total = total + dealPriceList[i]-dealPriceList[i-1]
		# print('累计盈亏：')
		# print(total)

		return total






		


