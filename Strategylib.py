from ViewControllerClass import *
from DataControllerClass import *
from StrategyControllerClass import *
import time
import datetime as datetime


def Get300List():
	dataController = DataControllerClass()
	df300s = dataController.GetHS300s()
	df_all = dataController.ShowAllShares()

	codeList = []
	nameList = []
	for index in df300s.index:
	# for index in range(10):
		initCode = df300s.loc[index,'code']
		code,codeName = dataController.GetCodeInfoFromDFAll(df_all,initCode)
		codeList.append(code)
		nameList.append(codeName)
	return codeList,nameList


def GetAllList():
	dataController = DataControllerClass()
	df_all = dataController.ShowAllShares()
	codeList = []
	nameList = []
	for index in df_all.index:
		code = df_all.loc[index,'ts_code']
		codeName = df_all.loc[index,'name']
		codeList.append(code)
		nameList.append(codeName)
	return codeList,nameList



# 获取顶分型和底分型
def CallPrintTopAndButtom(areaType,timeType,startTime,endTime):
	dataController = DataControllerClass()
	strategyController = StrategyControllerClass()

	if areaType=='300':
		codeList,nameList = Get300List()
	if areaType=='all':
		codeList,nameList = GetAllList()

	# for i in range(len(codeList)):
	for i in range(10):
		print(str(i)+' '+codeList[i]+' '+nameList[i])
		code = codeList[i]

		res,df_stockload = dataController.GetQFQDataFromCSV(code,areaType,timeType,startTime,endTime)
		if res:
			if df_stockload is None:
				pass
			else:
				strategyController.PrintTopAndButtom(df_stockload)


# 统计一个K线 三个结果
def StatisticsOneKLine(areaType,timeType,startTime,endTime):
	dataController = DataControllerClass()
	totalA = 0
	totalB = 0
	totalC = 0
	totalD = 0

	# df_all = dataController.ShowAllShares()
	if areaType=='300':
		codeList,nameList = Get300List()
	if areaType=='all':
		codeList,nameList = GetAllList()

	for i in range(len(codeList)):
		print(str(i)+' '+codeList[i]+' '+nameList[i])
		code = codeList[i]

		res,df_stockload = dataController.GetQFQDataFromCSV(code,areaType,timeType,startTime,endTime)
		if res:
			if df_stockload is None:
				pass
			else:
				strategyController = StrategyControllerClass()
				typeA,typeB,typeC,typeD = strategyController.StategyCount2K(df_stockload)
				totalA = totalA + typeA
				totalB = totalB + typeB
				totalC = totalC + typeC
				totalD = totalD + typeD
	print(totalA/(totalA+totalB+totalC+totalD))
	print(totalB/(totalA+totalB+totalC+totalD))
	print(totalC/(totalA+totalB+totalC+totalD))
	print(totalD/(totalA+totalB+totalC+totalD))