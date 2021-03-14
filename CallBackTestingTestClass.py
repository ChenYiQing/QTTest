from BackTestingClass import *


code = '000651.SZ'
areaType = '300'
timeType = 'D'
startTime = '20100101'
endTime = '20190101'

backTesting =BackTestingClass()
strategy01 = Strategy01Class()
backTesting.SetStrategyIns(strategy01)
# backTesting.RunSingleShare(code,areaType,timeType,startTime,endTime)
backTesting.RunMultiShare(areaType,timeType,startTime,endTime)

