from CyqStrategyInterface import *

# 井字交易法
class Strategy01Class(CyqStrategyInterface):
	def Run(self,df_data):
		# self.simulatorDeal.BuyShare(self,date,price,shareNum)
		# self.simulatorDeal.SellShare(self,date,price,shareNum)

		for i in range(df_data.shape[0]):
			date = str(df_data['trade_date'].values[i])
			closePrice = float(df_data['close'].values[i])
			if self.simulatorDeal.IsKeepShareEmpty():
				self.simulatorDeal.BuyShare(date,closePrice,1)
			else:
				lastSharePrice = self.simulatorDeal.GetLastSharePrice()
				if closePrice - lastSharePrice>1:
					self.simulatorDeal.SellShare(date,closePrice,1)

				if lastSharePrice- closePrice >1:
					self.simulatorDeal.BuyShare(date,closePrice,1)


	def DisPlay(self):
		# self.simulatorDeal.PrintDealInfo()
		self.simulatorDeal.PrintShotInfo()
		
