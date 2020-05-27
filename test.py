from ViewControllerClass import *
from DataControllerClass import *
from StrategyControllerClass import *



dataController = DataControllerClass()
df300s = dataController.GetHS300s()
# print(df300s)
# codeName = '格力电器'
# code = dataController.GetCodeFromName(df300s,'格力电器')
# print(code)

# df_sz = dataController.GetSZShares()
# df_sh = dataController.GetSHShares()
# print(df_sz)
# print(df_sh)


df_all = dataController.ShowAllShares()
print(df_all['ts_code'].values)
print('000651.SZ' in df_all['ts_code'].values)
print('000651.SH' in df_all['ts_code'].values)



# code = dataController.GetCodeFromName(df300s,codeName)
# print(code)
totalList = []
profitList = []
lossList = []

for i in df300s.index:
	name = df300s.loc[i]['name']
	code  = df300s.loc[i]['code']
	if code+'.SZ' in df_all['ts_code'].values:
		code = code+'.SZ'
	if code+'.SH' in df_all['ts_code'].values:
		code = code+'.SH'

	print(name+" "+code)

	df_stockload =  dataController.GetQFQData(code)	
	df_stockload  = dataController.GetFullData(df_stockload)

	list_diff = np.sign(df_stockload['Ma20']-df_stockload['Ma60'])	
	list_signal = np.sign(list_diff-list_diff.shift(1))

	#策略--------
	strategyController = StrategyControllerClass()
	total = strategyController.test(df_stockload)
	total = round(total,2)
	totalList.append(total)
	print(total) 
	if total > 0:
		profitList.append(total)
	else:
		lossList.append(total)

print("profit:")
print(len(profitList))
print(sum(profitList))
print("loss:")
print(len(lossList))
print(sum(lossList))

# np.savetxt("save.csv", totalList, delimiter=',')

## 显示折线图--------------------------
# print(df_stockload)
# print(df_stockload['trade_date'])


# viewController = ViewControllerClass()

# viewController.SetShareData(df_stockload)
# viewController.SetTitle(code+"-格力电器")
# viewController.DrawDealPoint(list_signal)
# viewController.ShowChart()