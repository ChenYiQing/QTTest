import random




price = 1.0

for i in range(400):
	randNum = random.randint(1,4)
	if randNum==1:
		price = price*0.99
		print('loss:'+str(price))
	else:
		price = price*1.01
		print('win:'+str(price))


print(price)

























