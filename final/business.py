import os
import numpy
import glob
import re
import time
import matplotlib.pyplot as plt
directories=['business2','sport2','lifestyle2','environment2','opinion2','tech2','world2']
toplot=[]
for d in directories:
	path=os.getcwd()+'/'+d+'/'
	count=dict()
	count['Monday']=0
	count['Tuesday']=0
	count['Wednesday']=0
	count['Thursday']=0
	count['Friday']=0
	count['Saturday']=0
	count['Sunday']=0
	p1=re.compile('DateTime::::[\S]*\+',re.IGNORECASE)
	p2=re.compile('DateTime::::[^ \t\n\r\f\v\+]*\n',re.IGNORECASE)
	#print count
	for filename in glob.glob(os.path.join(path, 'article*')):
		f=open(filename,'r')
		text=f.read()
		#print text
		commenttimes=p2.findall(text)
		articletime=p1.findall(text)
		try:
			articletime=time.strptime(articletime[0],"DateTime::::%Y-%m-%dT%H:%M:%S+")
			print articletime
			for commenttime in commenttimes:
				try:
					temp=time.strftime('%A',time.strptime(commenttime,"DateTime::::%Y-%m-%dT%H:%M:%SZ\n"))
					count[temp]=count[temp]+1
				except:pass
		except:pass
	toplot.append(count)
print toplot
width=1/(2.0*len(toplot))
print width
fig, ax = plt.subplots()
rects=[]
ind=numpy.arange(7)
for dic in toplot:
	arr=[dic['Monday'],dic['Tuesday'],dic['Wednesday'],dic['Thursday'],dic['Friday'],dic['Saturday'],dic['Sunday']]
	rects.append(ax.bar(ind, arr, width))
	ind=ind+width
# ax.set_ylabel('Number of articles')
# ax.set_title('Articles per day of the week')
# ax.set_xticks(ind + width)
# ax.set_xticklabels(('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday','Sunday'))

# ax.legend((rects[0][0], rects[1][0],rects[2][0],rects[3][0], rects[4][0],rects[5][0],rects[6][0]), directories)


# def autolabel(rects):
#     # attach some text labels
#     for rect in rects:
#         height = rect.get_height()
#         ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
#                 '%d' % int(height),
#                 ha='center', va='bottom')
plt.show()