import random



# 18-19
# 359
# 108
# 146

## 29-20
# 401
# 121
# 151


price = 1.0

for i in range(151):
	randNum = random.randint(1,467)
	print(randNum)
	if randNum<121:
		price = price*0.99
		print('loss:'+str(price))
	else:
		price = price*1.01
		print('win:'+str(price))


print(price)

























