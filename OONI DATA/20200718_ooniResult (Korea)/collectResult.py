import numpy as np
import matplotlib.pyplot as plt
import os, csv, time
from datetime import date


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


def generate_csv(category):
	with open("Websites/"+category+".csv", 'r') as file:
		websites = [row[0][12:-1] for row in csv.reader(file, delimiter = ',')]


	with open("Results/"+category+"_results.csv", 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(["","","",""])
		writer.writerow(["Data collected at "+ time.ctime(),"","",""])
		writer.writerow(["","","",""])
		writer.writerow(["TEST RESULT FOR "+ category.upper()+" (HTTP)","","",""])
		writer.writerow(["Site", "Accessible", "CensorType", "URL"])
		for i in websites:
			writer.writerow([i, "", "", "http://www."+i.lower()+"/"])

		writer.writerow(["","","",""])
		writer.writerow(['Accessible','DNS Blocking','HTTP Blocking','TCP/IP Blocking','Unknown'])
		writer.writerow(["","","",""])
		writer.writerow(["","","",""])
		writer.writerow(["TEST RESULT FOR "+ category.upper()+" (HTTPS)","","",""])
		writer.writerow(["Site", "Accessible", "CensorType", "URL"])
		for i in websites:
			writer.writerow([i, "", "", "https://www."+i.lower()+"/"])

		writer.writerow(["","","",""])
		writer.writerow(['Accessible','DNS Blocking','HTTP Blocking','TCP/IP Blocking','Unknown'])
		writer.writerow(["","","",""])

def edit_output(category, sites, status):
	with open("Results/"+category+"_results.csv", 'r', newline = '') as file:
		readData = [row for row in csv.reader(file, delimiter = ',')]

	for i in readData:
		if i[3][:len(sites)] == sites:
			if status == 0: # Accessible
				i[1] = "O"
			elif status == 1: # Not Accesible
				i[1] = "X"
			elif status == 2: # DNS Blocking
				i[2] = "DNS"
			elif status == 3: # HTTP Blocking
				i[2] = "HTTP"
			elif status == 4: # TCP/IP Blocking
				i[2] = "TCP"

			break

	# Writing the updated content
	with open("Results/"+category+"_results.csv", 'w', newline='') as file:
		writer = csv.writer(file)
		for i in readData:
			writer.writerow(i)


def ret_result(category):
	with open("RAW/"+category+"_result.txt", 'r') as f:
		readData = [i for i in f.readlines()]

	status = -1
	# 0 - Accessible Sites (O)
	# 1 - Not Accessible Sites (X)
	# 2 - DNS Blocking
	# 3 - HTTP Blocking
	# 4 - TCP/IP Blocking
	found = False
	sites = False

	i = 0
	while i < len(readData):
		line = readData[i]
		if line[:28] == "Summary for web_connectivity":
			found = True
			i += 2

		elif found:
			if not sites:
				if line[:len("Accessible URLS")] == "Accessible URLS":
					sites = True
					status = 0
					
				elif line[:len("Not accessible URLS")] == "Not accessible URLS":
					sites = True
					status = 1
					
				elif line[:len("URLS possibly blocked due to dns")] == "URLS possibly blocked due to dns": #DNS Blocking
					sites = True
					status = 2
					
				elif line[:len("URLS possibly blocked due to http-diff")] == "URLS possibly blocked due to http-diff": #HTTP Blocking
					sites = True
					status = 3
					
				elif line[:len("URLS possibly blocked due to http-failure")] == "URLS possibly blocked due to http-failure": #TCP/IP Blocking
					sites = True
					status = 4
					
				i += 1

			else:
				if line[0] == "*":
					edit_output(category, line[2:-1], status)
				else:
					sites = False
		i += 1

def colResult(category):
	with open("Results/"+category+"_results.csv", 'r', newline = '') as file:
		readData = [row for row in csv.reader(file, delimiter = ',')]

	i = 5
	out = []
	temp = [0, 0, 0, 0, 0]
	while i < len(readData):
		line = readData[i]
		if i == 57:
			readData[i] = temp
			out.append(temp)
			temp = [0, 0, 0, 0, 0]

		elif i == 113:
			readData[i] = temp
			out.append(temp)

		if line[1] == "O":
			temp[0] += 1
		elif line[1] == "X":
			if line[2] == "DNS":
				temp[1] += 1
			elif line[2] == "HTTP":
				temp[2] += 1
			elif line[2] == "TCP":
				temp[3] += 1
			else: #UNK
				temp[4] += 1
				line[2] = "UNK"
		i += 1


	# Writing the updated content
	with open("Results/"+category+"_results.csv", 'w', newline='') as file:
		writer = csv.writer(file)
		for i in readData:
			writer.writerow(i)

	return out


def accResult(categories):
	out = [[],[]]
	#HTTP, HTTPS
	
	for i in categories:
		generate_csv(i)
		ret_result(i)
	
		temp = colResult(i)
		out[0].append(temp[0])
		out[1].append(temp[1])

	return out


today = date.today()
date = today.strftime("%Y%m%d")

resultType = ['Accessible','DNS Blocking','HTTP Blocking','TCP/IP Blocking','Unknown']
cat = sorted([i[:-11] for i in os.listdir("RAW/")])
result = accResult(cat)
print(result)

survey1(result[0], resultType, cat, date+'_HTTP_category.png')
survey1(result[1], resultType, cat, date+'_HTTPS_category.png')