# Klasifikasi dengan fitur time-frequency domain
# author : Angga Maulana P

from pylab import *
import matplotlib.pyplot as plt
from scipy.io import wavfile
import numpy as np


numframe=20
numfreqframe=5
numtime=2*1000



def convertFFT(amplitude,sampF):
	n = len(amplitude) 
	p = fft(amplitude)
	# print n
	# print p
	data=[]
	
	nUniquePts = int(ceil((n+1)/2.0))
	p = p[0:nUniquePts]
	p = abs(p)

	p = p / float(n) # scale by the number of points so that
	                 # the magnitude does not depend on the length 
	                 # of the signal or on its sampling frequency  
	p = p**2  # square it to get the power 

	# multiply by two (see technical document for details)
	# odd nfft excludes Nyquist point
	if n % 2 > 0: # we've got odd number of points fft
	    p[1:len(p)] = p[1:len(p)] * 2
	else:
	    p[1:len(p) -1] = p[1:len(p) - 1] * 2 # we've got even number of points fft

	# print "sample frequency"
	# print sampFreq
	# print "len"
	# print n

	# print p
	frq = arange(0, nUniquePts, 1.0)
	freqArray = frq * (float(sampF) / float(n));

	p = 10*np.where(p > 0.0000000001, np.log10(p), 0)

	lenpower = len(p)
	freqframe = lenpower/numfreqframe
	for i in range(numfreqframe):
		batasawal=(i*freqframe)
		batasakhir=batasawal+freqframe
		if batasakhir > freqframe:
			batasakhir=lenpower
		average=np.mean(p[batasawal:batasakhir])	
		data.append(average)
		
	# print p
	# print freqArray

	# plt.plot(freqArray/1000, p, color='k')
	# plt.xlabel('Frequency (kHz)')
	# plt.ylabel('Power (dB)')
	# plt.show()
	return data



def convertToDomainFreq(file):
	data=[]
	sampFreq, snd = wavfile.read(file)
	# print snd.dtype
	snd = snd/(2.**15)
	# print snd.shape
	totalamplitude = snd.shape[0]
	# print"======================="
	# print "durasi"
	# print snd.shape[0]/float(sampFreq)
	# print "sample rate"
	# print sampFreq
	# print"======================="

	s1=snd[:,0]


	timeArray = arange(0,totalamplitude,1)
	timeArray = timeArray/float(sampFreq)
	timeArray = timeArray*1000

	# plt.plot(timeArray,s1,color='k')
	# plt.ylabel('Amplitude')
	# plt.xlabel('Time(ms)')
	# plt.show()


	frame = totalamplitude/numframe
	for i in range(numframe): 
		batasawal = (i*frame)
		batasakhir = (batasawal+numframe)
		if batasakhir>totalamplitude:
			batasakhir=totalamplitude
		timecut = s1[batasawal:batasakhir]
		data.append(convertFFT(timecut,sampFreq))

	return data


def xls(data):
	xlss=""
	for dt in data:
		for dta in dt:
			xlss+=str(dta)+","
		xlss+="\n"
	xlss+="\n\n\n"
	return xlss

def euclidean(d1,d2):
	nn = d1-d2
	# nn2=np.power(nn,2)
	nn2 = np.absolute(nn)
	return np.sum(nn2)

def kelas(nilai,dtjarak):
	if nilai==dtjarak[0]:
		return "Ayam Jago"
	elif nilai==dtjarak[1]:
		return "Ayam Jago"
	elif nilai==dtjarak[2]:
		return "Kucing"
	elif nilai==dtjarak[3]:
		return "Kucing"
	elif nilai==dtjarak[4]:
		return "Kucing"
	elif nilai==dtjarak[5]:
		return "Sapi"
	elif nilai==dtjarak[6]:
		return "Sapi"



xl="Ayam Jago1,\n"
data1=convertToDomainFreq('Rooster1.wav')
xl+=xls(data1)

xl+="Ayam Jago2,\n"
data2=convertToDomainFreq('Rooster2.wav')
xl+=xls(data2)

xl+="Kucing1,\n"
data3=convertToDomainFreq('Cat1.wav')
xl+=xls(data3)

xl+="Kucing2,\n"
data4=convertToDomainFreq('Cat2.wav')
xl+=xls(data4)

xl+="Kucing3,\n"
data5=convertToDomainFreq('Cat3.wav')
xl+=xls(data5)

xl+="Sapi1,\n"
data6=convertToDomainFreq('Cow1.wav')
xl+=xls(data6)

xl+="Sapi2,\n"
data7=convertToDomainFreq('Cow2.wav')
xl+=xls(data7)

# TESTING
# MULAI KLASIFIKASI INPUT (OPERASI KNN)---
# HITUNG DISTANCE TIAP DATA TRAINING DENGAN INPUT
test = convertToDomainFreq('Cow3.wav')
jarak1=euclidean(np.array(test).flatten(),np.array(data1).flatten())
jarak2=euclidean(np.array(test).flatten(),np.array(data2).flatten())
jarak3=euclidean(np.array(test).flatten(),np.array(data3).flatten())
jarak4=euclidean(np.array(test).flatten(),np.array(data4).flatten())
jarak5=euclidean(np.array(test).flatten(),np.array(data5).flatten())
jarak6=euclidean(np.array(test).flatten(),np.array(data6).flatten())
jarak7=euclidean(np.array(test).flatten(),np.array(data7).flatten())

datajarak=[jarak1,jarak2,jarak3,jarak4,jarak5,jarak6,jarak7]
# print jarak1
# print jarak2
# print jarak3
# print jarak4
# print jarak5
# print jarak6
# print jarak7
#VOTING

# KLASIFIKASI INPUT---
# Lihat jarak terdekat
# print datajarak
print "KNN: jarak telah diurutkan, misal k=3 berarti pilih 3 kelas paling atas dari pilihan dibawah ini"
dtjr=list(datajarak)
datajarak.sort()
print kelas(datajarak[0],dtjr)
print kelas(datajarak[1],dtjr)
print kelas(datajarak[2],dtjr)
print kelas(datajarak[3],dtjr)
print kelas(datajarak[4],dtjr)
print kelas(datajarak[5],dtjr)
print kelas(datajarak[6],dtjr)


file = open('sound.csv','w')
file.write(xl)

print "==============================="
print "data matriks time-domain masing2 terdapat di sound.csv"
print "==============================="

	
	

