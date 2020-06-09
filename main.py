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

def SingleTest():
	dataController = DataControllerClass()
	df300s = dataController.GetHS300s()

	codeName = '格力电器'
	codeName = '贵州茅台'
	codeName = '万科'
	codeName = '白云山'
	codeName = '中国平安'
	codeName = '海康威视'
	codeName = '宝钢股份'
	codeName = 'TCL科技'

	df_all = dataController.ShowAllShares()

	code = dataController.GetCodeFromName(df300s,codeName)
	if code+'.SZ' in df_all['ts_code'].values:
		code = code+'.SZ'
	if code+'.SH' in df_all['ts_code'].values:
		code = code+'.SH'
	print(code +'-'+ codeName)
	# code = '002415.SZ'
	
	df_stockload =  dataController.GetQFQData(code,'D','20200301','20200602')
	# df_stockload = dataController.GetQFQDataFromCSV(code)

	df_stockload  = dataController.GetFullData(df_stockload)
	print(df_stockload)
	strategyController = StrategyControllerClass()
	# total = strategyController.Strategy01(df_stockload)
	# total,shortTimes,longTimes,shortDate,daysList= strategyController.Strategy02(df_stockload,True)
	win,loss,tradeDateList = strategyController.Strategy02(df_stockload,False)


	# 可视化 查看亏损原因



def TotalTest(areaType,timeType,startTime,endTime,alpha):
	dataController = DataControllerClass()

	df_all = dataController.ShowAllShares()
	shortCount = 0
	longCount = 0
	shortDateList = []
	keepDaysList = []


	winTotal = 0
	lossTotal = 0 

	existTotal = 0
	dayCover = []

	codeList = []
	nameList = []
	if areaType=='300':
		codeList,nameList = Get300List()
	if areaType=='all':
		codeList,nameList = GetAllList()

	for i in range(len(codeList)):
		print(str(i)+' '+codeList[i]+' '+nameList[i])
		code = codeList[i]

		# 线上获取
		# df_stockload =  dataController.GetQFQData(code,'D','20190101','20200101')	
		# df_stockload =  dataController.GetQFQData(code,'W','20180101','20190101')	
		# 从csv载入 W
		res,df_stockload = dataController.GetQFQDataFromCSV(code,areaType,timeType,startTime,endTime)
		if res:
			if df_stockload is None:
				pass
			else:
				# df_stockload  = dataController.GetFullData(df_stockload)
				strategyController = StrategyControllerClass()
				# total = strategyController.Strategy01(df_stockload)
				# total,shortTimes,longTimes,shortDate,daysList = strategyController.Strategy02(df_stockload,False)
				win,loss,tradeDateList = strategyController.Strategy02(df_stockload,alpha,True)
				dayCover = dayCover + tradeDateList
				# shortDateList = shortDateList+shortDate
				# keepDaysList = keepDaysList+daysList
				winTotal = winTotal + win
				lossTotal = lossTotal + loss
				existTotal = existTotal + 1
		# print(code +'-'+ codeName)
		# print('短线盈亏：'+str(total))
		# print('短线交易次数：',shortTimes)
		# print('长线交易次数：',longTimes)
		# shortCount = shortCount + shortTimes
		# longCount = longCount + longTimes
		print('------------------------------------')
		# time.sleep(0.01) # tushare一分钟200请求限制
	print('有数据股票数：')
	print(existTotal)
	print('计数:')
	# print(shortCount)
	# print(longCount)
	print(winTotal)
	print(lossTotal)
	# print('日期覆盖:')
	# print(len(shortDateList))
	dayCover = list(set(dayCover))
	print('日期覆盖')
	print(len(dayCover))
	# print(dayCover)

	# shortDateList = list(set(shortDateList))
	# print(len(shortDateList))

	# print('持有天数:')
	# testMap = {}
	# for i in range(len(keepDaysList)):
	# 	if keepDaysList[i] in testMap:
	# 		testMap[keepDaysList[i]] = testMap[keepDaysList[i]] +1
	# 	else:
	# 		testMap[keepDaysList[i]] = 1
	# print(testMap)



# 获取1个月前的时间
def PreMonthDate(time2):
	now_time = datetime.datetime.strptime(time2, '%Y%m%d')
	threeDayAgo = (now_time - datetime.timedelta(days =30))
	timeStamp =int(time.mktime(threeDayAgo.timetuple()))
	otherStyleTime = threeDayAgo.strftime("%Y%m%d")
	return otherStyleTime

def PreHalfYearDate(time2):
	now_time = datetime.datetime.strptime(time2, '%Y%m%d')
	threeDayAgo = (now_time - datetime.timedelta(days =180))
	timeStamp =int(time.mktime(threeDayAgo.timetuple()))
	otherStyleTime = threeDayAgo.strftime("%Y%m%d")
	return otherStyleTime

# 实时监控
def Infer(areaType,timeType):
	dataController = DataControllerClass()
	df300s = dataController.GetHS300s()
	df_all = dataController.ShowAllShares()

	currentTime = time.strftime("%Y%m%d", time.localtime()) 
	preMonth = PreMonthDate(currentTime)
	preHalfYear = PreHalfYearDate(currentTime)

	findList = []


	codeList = []
	nameList = []
	if areaType=='300':
		codeList,nameList = Get300List()
	if areaType=='all':
		codeList,nameList = GetAllList()

	for i in range(len(codeList)):
		code = codeList[i]
		codeName = nameList[i]
		# if i<1400:
		# 	continue
		print(str(i)+' '+code+' '+codeName)
		if 'ST' in codeName:
			pass
		else:
			if timeType =='D':
				df_stockload =  dataController.GetQFQData(code,'D',preMonth,currentTime)	
				# 补充当天盘中数据
				sinaCode = ''
				if 'SZ' in code:
					sinaCode = 'sz'+code[0:6]
				if 'SH' in code:
					sinaCode = 'sh'+code[0:6]
				open,current,high,low,date = dataController.GetTodayDateFromSina(sinaCode)
				# print(open+' '+current+' '+high+' '+low)
				id = df_stockload.shape[0]
				if df_stockload.loc[id-1,'trade_date']==date:
					pass
				else:
					df_stockload.loc[id]=[code,date,float(open),float(high),float(low),float(current),'','','','','']

			if timeType == 'W':
				df_stockload =  dataController.GetQFQData(code,'W',preHalfYear,currentTime)
				apiCode = ''
				if 'SZ' in code:
					apiCode = 'sz'+code[0:6]
				if 'SH' in code:
					apiCode = 'sh'+code[0:6]
				res,open,close,high,low,date = dataController.GetDataFromTencent(apiCode)
				if res:
					print(open+' '+close+' '+high+' '+low+' '+date)
					id = df_stockload.shape[0]
					if len(df_stockload.index)<10:
						pass
					else: 
						if df_stockload.loc[id-1,'trade_date']==date:
							pass
						else:
							df_stockload.loc[id]=[code,date,float(close),float(open),float(high),float(low),'','','','','']
			if df_stockload is None or len(df_stockload.index)<10:
				pass
			else:
				strategyController = StrategyControllerClass()
				res = strategyController.Strategy02Infer(df_stockload)
				print(res)
				if res:
					findList.append(code+' '+codeName)
				print(findList)
	print(currentTime)
	print(findList)
	a = input('enter finish...')


# 保存成离线数据
def SaveCsv(timeType,areaType,startDate,endDate):
	dataController = DataControllerClass()
	df300s = dataController.GetHS300s()
	df_all = dataController.ShowAllShares()

	if areaType=='300':
		for index in df300s.index:
			print(index)
			initCode = df300s.loc[index,'code']
			code,codeName = dataController.GetCodeInfoFromDFAll(df_all,initCode)
			df_stockload =  dataController.GetQFQData(code,timeType,startDate,endDate)
			if df_stockload is None:
				pass
			else:
				df_stockload.to_csv('.//HisData//300//'+timeType+'//'+code+'.csv')
		time.sleep(0.1)

	if areaType=='all':
		for index in df_all.index:
			print(index)
			code = df_all.loc[index,'ts_code']
			codeName = df_all.loc[index,'name']
			df_stockload =  dataController.GetQFQData(code,timeType,startDate,endDate)
			if df_stockload is None:
				pass
			else:
				df_stockload.to_csv('.//HisData//all//'+timeType+'//'+code+'.csv')
		time.sleep(0.1)


# 载入数据
def LoadCsv():
	df = pd.read_csv('.//HisData//000001.SZ.csv',index_col=0)
	print(df)



# 获取今日股价
def GetTodayDate():
	dataController = DataControllerClass()
	df300s = dataController.GetHS300s()
	df_all = dataController.ShowAllShares()
	for index in df300s.index:
		initCode = df300s.loc[index,'code']
		code,codeName = dataController.GetCodeInfoFromDFAll(df_all,initCode)
		# print(code)
		sinaCode = ''
		if 'SZ' in code:
			sinaCode = 'sz'+code[0:6]
		if 'SH' in code:
			sinaCode = 'sh'+code[0:6]
		# print(sinaCode)
		open,current,high,low,date = dataController.GetTodayDateFromSina(sinaCode)
		print(open+' '+current+' '+high+' '+low)



# 显示折线图
def ShowChart():
	dataController = DataControllerClass()
	code = '000651.sz'
	df_stockload =  dataController.GetQFQData(code,'D','20190101','20200101')

	print(df_stockload)
	print(df_stockload['trade_date'])
	df_stockload  = dataController.GetFullData(df_stockload)

	list_diff = np.sign(df_stockload['Ma20']-df_stockload['Ma60'])	
	list_signal = np.sign(list_diff-list_diff.shift(1))


	viewController = ViewControllerClass()

	viewController.SetShareData(df_stockload)
	viewController.SetTitle(code+"-格力电器")
	viewController.DrawDealPoint(list_signal)
	viewController.ShowChart()


def main():
	# SingleTest()
	areaType = 'all'
	timeType = 'W'
	startTime = '20190101'
	endTime = '20200101'
	alpha = 0.01
	# TotalTest(areaType,timeType,startTime,endTime,alpha)
	Infer(areaType,timeType)
	# ShowChart()


if __name__ == '__main__':
	main()




