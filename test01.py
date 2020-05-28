from ViewControllerClass import *
from DataControllerClass import *
from StrategyControllerClass import *
import time
import datetime as datetime


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

	df_all = dataController.ShowAllShares()

	code = dataController.GetCodeFromName(df300s,codeName)
	if code+'.SZ' in df_all['ts_code'].values:
		code = code+'.SZ'
	if code+'.SH' in df_all['ts_code'].values:
		code = code+'.SH'
	print(code +'-'+ codeName)
	# code = '002415.SZ'
	
	# df_stockload =  dataController.GetQFQData(code,'D','20150301','20200301')
	df_stockload = dataController.GetQFQDataFromCSV(code)

	df_stockload  = dataController.GetFullData(df_stockload)
	strategyController = StrategyControllerClass()
	# total = strategyController.Strategy01(df_stockload)
	total,shortTimes,longTimes,shortDate,daysList= strategyController.Strategy02(df_stockload,True)


	# 可视化 查看亏损原因



def TotalTest():
	dataController = DataControllerClass()
	df300s = dataController.GetHS300s()


	# print(df300s)

	df_all = dataController.ShowAllShares()
	shortCount = 0
	longCount = 0
	shortDateList = []
	keepDaysList = []


	winTotal = 0
	lossTotal = 0 

	for index in df300s.index:
	# for index in range(10):
		initCode = df300s.loc[index,'code']
		code,codeName = dataController.GetCodeInfoFromDFAll(df_all,initCode)
		print(str(index)+':'+code +'-'+ codeName)
		# 线上获取
		df_stockload =  dataController.GetQFQData(code,'D','20110301','20120301')	
		# 从csv载入
		# df_stockload = dataController.GetQFQDataFromCSV(code)

		if df_stockload is None:
			pass
		else:
			df_stockload  = dataController.GetFullData(df_stockload)
			strategyController = StrategyControllerClass()
			# total = strategyController.Strategy01(df_stockload)
			# total,shortTimes,longTimes,shortDate,daysList = strategyController.Strategy02(df_stockload,False)
			win,loss = strategyController.Strategy02(df_stockload,False)
			# shortDateList = shortDateList+shortDate
			# keepDaysList = keepDaysList+daysList
			winTotal = winTotal + win
			lossTotal = lossTotal + loss
		# print(code +'-'+ codeName)
		# print('短线盈亏：'+str(total))
		# print('短线交易次数：',shortTimes)
		# print('长线交易次数：',longTimes)
		# shortCount = shortCount + shortTimes
		# longCount = longCount + longTimes
		print('------------------------------------')
	print('计数:')
	# print(shortCount)
	# print(longCount)
	print(winTotal)
	print(lossTotal)
	# print('日期覆盖:')
	# print(len(shortDateList))
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

# 实时监控
def Infer():
	dataController = DataControllerClass()
	df300s = dataController.GetHS300s()
	df_all = dataController.ShowAllShares()

	currentTime = time.strftime("%Y%m%d", time.localtime()) 
	preMonth = PreMonthDate(currentTime)


	findList = []
	for index in df300s.index:
	# for index in range(5):
		print(index)
		initCode = df300s.loc[index,'code']
		code,codeName = dataController.GetCodeInfoFromDFAll(df_all,initCode)
		print(code+' '+codeName)

		if 'ST' in codeName:
			pass
		else:
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
			# print(df_stockload)

			if df_stockload is None:
				pass
			else:
				strategyController = StrategyControllerClass()
				res = strategyController.Strategy02Infer(df_stockload)
				print(res)
				if res:
					findList.append(code+' '+codeName)
	print(currentTime)
	print(findList)
	a = input('enter finish...')


# 保存成离线数据
def SaveCsv():
	dataController = DataControllerClass()
	df300s = dataController.GetHS300s()
	df_all = dataController.ShowAllShares()
	for index in df300s.index:
		print(index)
		initCode = df300s.loc[index,'code']
		code,codeName = dataController.GetCodeInfoFromDFAll(df_all,initCode)
		df_stockload =  dataController.GetQFQData(code,'D','20000301','20200301')	
		df_stockload.to_csv('.//HisData//'+code+'.csv')

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

# SingleTest()
# TotalTest()
Infer()
# SaveCsv()
# GetTodayDate()






