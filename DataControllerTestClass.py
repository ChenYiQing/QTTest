from DataControllerClass import *



class DataControllerTestClass(object):
	def __init__(self):
		self.dataController = DataControllerClass()

	def TestShowAllShares(self):
		data = self.dataController.ShowAllShares()
		print(data['name'].values)

		for item in data['name'].values:
			print(item)

	def TestGetHS300s(self):
		df = self.dataController.GetHS300s()
		for i in range(df.shape[0]):
			if i%10==0:
				print('*************************')
			print(df['name'].values[i]+' '+str(df['weight'].values[i]))

		print("========= 300s权重大于1的股票 ========")
		for i in range(df.shape[0]):
			if df['weight'].values[i]>1:
				print(df['name'].values[i]+' '+str(df['weight'].values[i]))

	# tushare接口获取前复权数据
	def TestGetQFQData(self):
		code = '000651.SZ'
		df = self.dataController.GetQFQData(code,'D','20200301','20200602')
		print(df)

	# 从CSV获取前复权数据
	def TestGetQFQDataFromCSV(self):
		code = '000651.SZ'
		areaType = '300'
		timeType = 'D'
		startTime = '20190301'
		endTime = '20190601'
		res,df = self.dataController.GetQFQDataFromCSV(code,areaType,timeType,startTime,endTime)
		print(res)
		print(df)





dataControllerTest = DataControllerTestClass()
dataControllerTest.TestGetQFQDataFromCSV()