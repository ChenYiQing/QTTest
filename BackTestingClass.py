from enum import Enum
from CyqStrategyInterface import *
from Strategy01Class import *
from DataControllerClass import *
from Strategylib import *


class StrategyType(Enum):
	StrategyDefault = 0
	Strategy01 = 1
	Strategy02 = 2



class BackTestingClass(object):
	def __init__(self):
		self.strategyType = StrategyType.StrategyDefault
		self.strategyInterface = CyqStrategyInterface()
		# 支持的方法名带描述
		self.strategyDict = {}
		self.strategyDict[StrategyType.StrategyDefault] = '缺省策略'
		self.strategyDict[StrategyType.Strategy01] = '策略01的描述'
		self.PrintStategys()

		self.dataController = DataControllerClass()

	def SetStrategyIns(self,strategy):
		self.strategyInterface = strategy
		

	# 批量执行
	def RunMultiShare(self,areaType,timeType,startTime,endTime):
		if areaType=='300':
			codeList,nameList = Get300List()
			for i in range(len(codeList)):
				print(str(i)+' '+codeList[i]+' '+nameList[i])
				code = codeList[i]
				res,df_stockload = self.dataController.GetQFQDataFromCSV(code,areaType,timeType,startTime,endTime)
				if res:
					self.RunSingleShare(code,areaType,timeType,startTime,endTime)
				self.strategyInterface.SimluatorClear()

		

	# 单一执行
	def RunSingleShare(self,code,areaType,timeType,startTime,endTime):
		res,df_data = self.dataController.GetQFQDataFromCSV(code,areaType,timeType,startTime,endTime)
		self.strategyInterface.Run(df_data)
		self.strategyInterface.DisPlay()

	# 打印支持的策略
	def PrintStategys(self):
		for item in self.strategyDict.keys():
			print(str(item)+':')
			print(str(self.strategyDict[item]))




