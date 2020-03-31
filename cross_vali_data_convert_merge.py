import numpy as np,numpy
import csv
import glob
import os
import time
window_size = 1000
threshold = 60
slide_size = 200 #less than window_size!!!

def dataimport(path1, path2,oppath1,oppath2):
	xx = np.empty([0,window_size,90],float)
	yy = np.empty([0,8],float)
	###Input data###
	#data import from csv
	input_csv_files = sorted(glob.glob(path1))
	bigstart = time.time()
	for f in input_csv_files:
		print("input_file_name=",f)
		data = [[ float(elm) for elm in v] for v in csv.reader(open(f, "r"))]
		start=time.time()
		tmp1 = np.array(data) #19k,181
		x2 =np.empty([0,window_size,90],float)

		#data import by slide window
		k = 0
		while k <= (len(tmp1) + 1 - 2 * window_size):
			x = np.dstack(tmp1[k:k+window_size, 1:91].T)
			x2 = np.concatenate((x2, x),axis=0)
			k += slide_size
		end =time.time()
		print("secs",end - start)
		xx = np.concatenate((xx,x2),axis=0)

	xx = xx.reshape(len(xx),-1)

	###Annotation data###
	#data import from csv
	annotation_csv_files = sorted(glob.glob(path2))
	for ff in annotation_csv_files:
		print("annotation_file_name=",ff)
		ano_data = [[ str(elm) for elm in v] for v in csv.reader(open(ff,"r"))]
		tmp2 = np.array(ano_data)

		#data import by slide window
		y = np.zeros(((len(tmp2) + 1 - 2 * window_size)//slide_size+1,8))
		k = 0
		while k <= (len(tmp2) + 1 - 2 * window_size):
			y_pre = np.stack(tmp2[k:k+window_size])
			bed = 0
			fall = 0
			walk = 0
			pickup = 0
			run = 0
			sitdown = 0
			standup = 0
			noactivity = 0
			for j in range(window_size):
				if y_pre[j] == "bed":
					bed += 1
				elif y_pre[j] == "fall":
					fall += 1
				elif y_pre[j] == "walk":
					walk += 1
				elif y_pre[j] == "pickup":
					pickup += 1
				elif y_pre[j] == "run":
					run += 1
				elif y_pre[j] == "sitdown":
					sitdown += 1
				elif y_pre[j] == "standup":
					standup += 1
				else:
					noactivity += 1

			if bed > window_size * threshold / 100:
				y[int(k/slide_size),:] = np.array([0,1,0,0,0,0,0,0])
			elif fall > window_size * threshold / 100:
				y[int(k/slide_size),:] = np.array([0,0,1,0,0,0,0,0])
			elif walk > window_size * threshold / 100:
				y[int(k/slide_size),:] = np.array([0,0,0,1,0,0,0,0])
			elif pickup > window_size * threshold / 100:
				y[int(k/slide_size),:] = np.array([0,0,0,0,1,0,0,0])
			elif run > window_size * threshold / 100:
				y[int(k/slide_size),:] = np.array([0,0,0,0,0,1,0,0])
			elif sitdown > window_size * threshold / 100:
				y[int(k/slide_size),:] = np.array([0,0,0,0,0,0,1,0])
			elif standup > window_size * threshold / 100:
				y[int(k/slide_size),:] = np.array([0,0,0,0,0,0,0,1])
			else:
				y[int(k/slide_size),:] = np.array([2,0,0,0,0,0,0,0])
			k += slide_size


		yy = np.concatenate((yy, y),axis=0)

	print(xx.shape,yy.shape)
	# eliminate the NoActivity Data
	rows, cols = np.where(yy>0)
	xx = np.delete(xx, rows[ np.where(cols==0)],0)
	yy = np.delete(yy, rows[ np.where(cols==0)],0)
	print(xx.shape,yy.shape)
	bigend = time.time()
	print("BIGGGG", bigend - bigstart)
	return (xx, yy)


#### Main ####
# if not os.path.exists("input_files/"):
#         os.makedirs("input_files/")

for i, label in enumerate (["bed", "fall", "pickup", "run", "sitdown", "standup", "walk"]):
	filepath1 = "D:\\project\\Wifi\\Dataset\\Data\\input_*_sankalp*" + str(label) + "*.csv"
	filepath2 = "D:\\project\\Wifi\\Dataset\\Data\\annotation_sankalp*" + str(label) + "*.csv"
	filepath3 = "D:\\project\\Wifi\\Dataset\\Data\\input_*_siamak*" + str(label) + "*.csv"
	filepath4 = "D:\\project\\Wifi\\Dataset\\Data\\annotation_siamak*" + str(label) + "*.csv"
	filepath5 = "D:\\project\\Wifi\\Dataset\\Data\\input_" + str(label) + "_1703*.csv"
	filepath6 = "D:\\project\\Wifi\\Dataset\\Data\\annotation_" + str(label) + "_1703*.csv"
	outputfilename1 = "D:\\project\\Wifi\\Wifi_Activity_Recognition\\RedataFull\\xx_" + str(window_size) + "_" + str(threshold) + "_" + label + ".csv"
	outputfilename2 = "D:\\project\\Wifi\\Wifi_Activity_Recognition\\RedataFull\\yy_" + str(window_size) + "_" + str(threshold) + "_" + label + ".csv"

	x, y = dataimport(filepath1, filepath2,outputfilename1,outputfilename2)
	x1, y1 = dataimport(filepath3, filepath4,outputfilename1,outputfilename2)
	x2, y2 = dataimport(filepath5, filepath6,outputfilename1,outputfilename2)
	with open(outputfilename1, "w") as f:
		writer = csv.writer(f, lineterminator="\n")
		writer.writerows(x)
		writer.writerows(x1)
		writer.writerows(x2)
	with open(outputfilename2, "w") as f:
		writer = csv.writer(f, lineterminator="\n")
		writer.writerows(y)
		writer.writerows(y1)
		writer.writerows(y2)
	print(label + "finish!")
