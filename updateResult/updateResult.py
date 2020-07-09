import csv
import numpy as np
import matplotlib.pyplot as plt

def errorDNS(filename):
	with open(filename, 'r', newline = '') as file:
		readData = [row for row in csv.reader(file, delimiter = ',')]

	cnt = 0
	webcnt = 0
	init = True
	check = False
	cateno = 0
	# http: 0-15 // https: 16-31

	for i in readData:
		if not check:
			if cnt == 4 and init == True:
				check = True
				init = False
				cnt = -1
			if cnt == 5:
				check = True
				cnt = -1
			cnt+=1

		else:
		# Websites

			# Checking 
			url = i[3]
			rurl = i[5]
			domain = i[0]
			wwwx0 = "http://"+domain.lower()
			wwwx1 = "https://"+domain.lower()

			if url[:-1] == rurl[:(len(url)-1)]:
				i[1] = "O"
				i[2] = ""

			# Checkes whether returned URL is http or https version of input URL without www
			if wwwx0 == rurl[:len(wwwx0)] or wwwx1 == rurl[:len(wwwx1)]:
				i[1] = "O"
				i[2] = ""

			# Checks whether returned URL is http or https version of input URL
			if 0<=cateno<16:
				temp = "https"+url[4:]
			else:
				temp = "http"+url[5:]

			if temp[:-1] == rurl[:(len(temp)-1)]:
				i[1] = "O"
				i[2] = ""

			webcnt+=1
			if webcnt == 50:
				check = False
				webcnt = 0
				cateno+=1


	# Writing the updated content
	with open("temp.csv", 'w', newline='') as file:
		writer = csv.writer(file)
		for i in readData:
			writer.writerow(i)
	


def calResult(filename):
	with open(filename, 'r', newline = '') as file:
		readData = [row for row in csv.reader(file, delimiter = ',')]

	cnt = 0
	webcnt = 0
	init = True
	check = False
	cateno = 0
	acc = [0, 0, 0, 0, 0]
    # [accessible, T/O, DNS, CXN, UNK]

	# http: 0-15 // https: 16-31

	for i in readData:
		if not check:
			if cnt == 4 and init:
				check = True
				init = False
				cnt = -1
			elif cnt == 2 and not init:
				i[0] = acc[0]
				i[1] = acc[1]
				i[2] = acc[2]
				i[3] = acc[3]
				i[4] = acc[4]
				# why does i = acc doesn't work?
				# i = acc
			elif cnt == 5:
				check = True
				cnt = -1
				acc = [0, 0, 0, 0, 0]
			cnt+=1

		else:
		# Websites
			if i[1] == "O":
				acc[0]+=1
			else:
				if i[2] == "T/O":
					acc[1]+=1
				elif i[2] == "DNS":
					acc[2]+=1
				elif i[2] == "CXN":
					acc[3]+=1
				elif i[2] == "UNK":
					acc[4]+=1

			webcnt+=1
			if webcnt == 50:
				check = False
				webcnt = 0
				cateno+=1



	# Writing the updated content
	with open("temp.csv", 'w', newline='') as file:
		writer = csv.writer(file)
		for i in readData:
			writer.writerow(i)

def colResult(filename):
	with open(filename, 'r', newline = '') as file:
		readData = [row for row in csv.reader(file, delimiter = ',')]

	cnt = 0
	webcnt = 0
	init = True
	check = False
	cateno = 0
	resultHTTP = []
	resultHTTPS = []
    # [accessible, T/O, DNS, CXN, UNK]

	# http: 0-15 // https: 16-31

	for i in readData:
		if not check:
			if cnt == 4 and init:
				check = True
				init = False
				cnt = -1
			elif cnt == 2 and not init:

				if 0<cateno<=16:
					resultHTTP.append(i)
				elif 16<cateno<=32:
					resultHTTPS.append(i)
				if cateno==32:
					return (resultHTTP, resultHTTPS)
					
			elif cnt == 5:
				check = True
				cnt = -1
			cnt+=1

		else:
		# Websites
			webcnt+=1
			if webcnt == 50:
				check = False
				webcnt = 0
				cateno+=1

def survey1(results, resultType, categories, label):
    plt.clf()
    # print("Results: ", results)
    # print("Result Type: ", resultType)
    # print("Categories: ", categories)

    # plt.figure(figsize=(6.4, 4.8))
    plt.figure(figsize=(10, 7))

    # set width of bar
    barWidth = 0.18

    # set height of bar
    bars1 = [i[0] for i in results]
    bars2 = [i[1] for i in results]
    bars3 = [i[2] for i in results]
    bars4 = [i[3] for i in results]
    bars5 = [i[4] for i in results]

    # Set position of bar on X axis
    r1 = np.arange(len(bars1))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]
    r4 = [x + barWidth for x in r3]
    r5 = [x + barWidth for x in r4]

     
    # Make the plot
    plt.bar(r1, bars1, color='#38EB09', width=barWidth, edgecolor='white', label=resultType[0])
    plt.bar(r2, bars2, color='#EBE83D', width=barWidth, edgecolor='white', label=resultType[1])
    plt.bar(r3, bars3, color='#3235D9', width=barWidth, edgecolor='white', label=resultType[2])
    plt.bar(r4, bars4, color='#EB110E', width=barWidth, edgecolor='white', label=resultType[3])
    plt.bar(r5, bars5, color='#000000', width=barWidth, edgecolor='white', label=resultType[4])     

    # Add xticks on the middle of the group bars
    plt.xlabel('Category', fontweight='bold',fontsize=18)
    plt.xticks([r + 2*barWidth for r in range(len(bars1))], categories)
    plt.xticks(rotation=45, fontsize=15, ha="right", fontweight='normal')

    # Create legend & Show graphic
    plt.legend()
    plt.tight_layout()

    plt.savefig(label)
    return plt

resultType = ['Accessible','TimeOut','DNS Tampering','ConnectionError','Unknown']
categories = ['Adult', 'Arts', 'Business', 'Computers', 'Games', 'Health', 'Home', 'Kids and Teens', 'News', 'Recreation', 'Reference', 'Regional', 'Science', 'Shopping', 'Society', 'Sports']

errorDNS("20200708 _ result.csv")
calResult("temp.csv")
result = colResult("temp.csv")

httpResult = [[int(j) for j in i] for i in result[0]]
httpsResult = [[int(j) for j in i] for i in result[1]]

survey1(httpResult, resultType, categories, 'temp_http.png')
survey1(httpsResult, resultType, categories, 'temp_https.png')
