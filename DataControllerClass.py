import tushare as ts
import pandas  as pd
import requests




class DataControllerClass():
	def __init__(self):
		ts.set_token('c44e067e293a18b4b6852036dbaf87979112fa2615bb2a8d1cdb3b63')
		self.pro = ts.pro_api()
		
	# 当前正常上市的公司列表
	def ShowAllShares(self):
		data = self.pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
		return data

	# 获取日K
	def GetDailyShare(self):
		df = self.pro.daily(ts_code='000002.SZ', start_date='20200501', end_date='20200528')
		print(df)
		print(len(df))

	# 沪股通成分股
	def GetSHShares(self):
		df = self.pro.hs_const(hs_type='SH')
		return df

	# 深股通成分股
	def GetSZShares(self):
		df = self.pro.hs_const(hs_type='SZ')
		return df

	# 沪深300
	def GetHS300s(self):
		df = ts.get_hs300s()
		return df


	# 获取代码
	def GetCodeFromName(self,dfHS300s,name):
		code = ''
		line = dfHS300s[dfHS300s['name'].str.contains(name)]
		code = line['code'].values[0]
		return code

	# 获取代码
	def GetCodeInfoFromDFAll(self,df_all,code):
		line = df_all[df_all['symbol'].str.contains(code)]
		code = line['ts_code'].values[0]
		name = line['name'].values[0]
		return code,name


	# 复权
	# - freq: '1MIN' 'D' 'W' 'M'
	def GetQFQData(self,code,dateFreq,startDate,endDate):
		df = ts.pro_bar(ts_code=code, freq=dateFreq,adj='qfq', start_date=startDate, end_date=endDate)
		# df = ts.pro_bar(ts_code='000651.SZ', adj='qfq', start_date='20150413', end_date='20200413')
		if df is None:
			pass
		else:
			df = df.reindex(index=df.index[::-1])
			df.reset_index(drop=True, inplace=True)
		return df

	def GetQFQDataFromCSV(self,code):
		df = pd.read_csv('.//HisData//'+code+'.csv',index_col=0)
		return df

	def GetFullData(self,df):
		df['Ma5'] = df.close.rolling(window=5).mean()
		df['Ma10'] = df.close.rolling(window=10).mean()
		df['Ma15'] = df.close.rolling(window=15).mean()
		df['Ma20'] = df.close.rolling(window=20).mean()
		df['Ma30'] = df.close.rolling(window=30).mean()
		df['Ma60'] = df.close.rolling(window=60).mean()
		return df

	# 获取实时数据
	def GetTodayDateFromSina(self,sinaCode):
		# sz 深圳
		# sh 上海
		# content=requests.get('http://hq.sinajs.cn/?format=json&list=sh600000').text
		httpStr = 'http://hq.sinajs.cn/?format=json&list='+sinaCode
		content=requests.get(httpStr).text
		list = content.split(',')
		open = list[1]
		current = list[3]
		high = list[4]
		low = list[5]
		date = list[-4]
		date = date[0:4]+date[5:7]+date[8:10]
		return open,current,high,low,date





# dataController = DataControllerClass()
# df_stockload = dataController.GetQFQData('000002.SZ','D','20200520','20200529')	
# print(df_stockload.tail())

# dataController.GetTodayDateFromSina()
# https://tushare.pro/document/1?doc_id=108
# qq 米哥