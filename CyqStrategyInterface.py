from abc import ABCMeta,abstractmethod
from SimulatorDealClass import *
				

class CyqStrategyInterface(object):
	def __init__(self):
		self.testParam = 1
		self.simulatorDeal = SimulatorDealClass()

	def Run(self,df_data):
		print(df_data)

	def DisPlay(self):
		print('CyqStrategyInterface DisPlay')


	def SimluatorClear(self):
		self.simulatorDeal.ClearData()


class testClass(CyqStrategyInterface):
	def Run(self,df_data):
		pass

	def DisPlay(self):
		print('DisPlay')
		print(self.testParam)			




		