


class SimulatorDealClass():
	def __init__(self):
		self.dealHisDate = []
		self.dealHisPrice = []
		self.dealOpt = []
		self.currentShareDate = []
		self.currentSharePrice = []
		self.currentShareNum = 0
		self.currentWinLoss = 0.0

	# todo shareNum 不等于 1 的情况
	def BuyShare(self,date,price,shareNum):
		self.currentShareNum = self.currentShareNum+shareNum
		self.currentShareDate.append(date)
		self.currentSharePrice.append(price)
		self.dealOpt.append('buy')
		self.dealHisDate.append(date)
		self.dealHisPrice.append(price)

	# 获取最后的价格
	def GetLastSharePrice(self):
		return self.currentSharePrice[-1]

	# 获取是否空仓
	def IsKeepShareEmpty(self):
		res = True
		if len(self.currentSharePrice)==0:
			res = True
		else:
			res = False
		return res

	def SellShare(self,date,price,shareNum):
		self.currentShareNum = self.currentShareNum-shareNum
		self.dealOpt.append('sell')
		self.dealHisDate.append(date)
		self.dealHisPrice.append(price)
		self.currentShareDate.pop(-1)
		popPrice = self.currentSharePrice.pop(-1)
		self.currentWinLoss = self.currentWinLoss+price-popPrice


	def CountWinOrLossWithKeepShare(self,finalPrice):
		for i in range(len(self.currentSharePrice)):
			self.currentWinLoss = self.currentWinLoss-(float(self.currentSharePrice[i])-finalPrice)



	def PrintDealInfo(self):
		print('*******************************')
		print('-- 当前持仓：'+str(self.currentShareNum))
		print('-- 当前盈亏：'+str(self.currentWinLoss))
		print('-- 持仓信息：')
		for j in range(len(self.currentShareDate)):
			print(self.currentShareDate[j]+" "+str(self.currentSharePrice[j]))
		print('-- 交易记录：')
		for i in range(len(self.dealHisDate)):
			print(self.dealOpt[i]+" "+self.dealHisDate[i]+" "+str(self.dealHisPrice[i]))
		print('*******************************')

	def PrintShotInfo(self):
		print('*******************************')
		print('-- 当前持仓：'+str(self.currentShareNum))
		print('-- 当前盈亏：'+str(self.currentWinLoss))
		print('-- 持仓信息：')
		for j in range(len(self.currentShareDate)):
			print(self.currentShareDate[j]+" "+str(self.currentSharePrice[j]))



	def ClearData(self):
		self.dealHisDate = []
		self.dealHisPrice = []
		self.dealOpt = []
		self.currentShareDate = []
		self.currentSharePrice = []
		self.currentShareNum = 0
		self.currentWinLoss = 0.0

	def RunSimulator(self,df_data):
		openPriceList = df_data['open']
		for i in range(len(openPriceList)):
			if i ==0:
				self.BuyShare(str(df_data['trade_date'][0]),float(df_data['open'][0]),1)
			else:
				if len(self.currentSharePrice)==0:
					self.BuyShare(str(df_data['trade_date'][i]),float(df_data['open'][i]),1)
					# self.PrintDealInfo()
				else:
					currentPrice = float(openPriceList[i])
					lastPrice = self.currentSharePrice[-1]
					if lastPrice - currentPrice > 2:
						self.BuyShare(str(df_data['trade_date'][i]),float(df_data['open'][i]),1)
						# self.PrintDealInfo()
					if currentPrice-lastPrice > 2:
						self.SellShare(str(df_data['trade_date'][i]),float(df_data['open'][i]),1)
						# self.PrintDealInfo()
		# self.PrintDealInfo()
		self.CountWinOrLossWithKeepShare(float(openPriceList[len(openPriceList)-1]))
		# self.PrintShotInfo()
		retShareNum = self.currentShareNum
		retWinOrLost = self.currentWinLoss
		self.ClearData()
		return retShareNum,retWinOrLost



# simulatorDeal = SimulatorDealClass()
# simulatorDeal.PrintDealInfo()
# simulatorDeal.BuyShare('111',58.5,1)
# simulatorDeal.PrintDealInfo()
# simulatorDeal.SellShare('2222',60.5,1)
# simulatorDeal.PrintDealInfo()
