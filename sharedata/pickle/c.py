import pickle
import time

#fp = open("shared.pkl")
#shared = pickle.load(fp)

while (1):
    try:
	fp = open("shared.pkl",'rb')
	shared = pickle.load(fp)
	print shared#,"\r",
	time.sleep(0.25)
    except EOFError:
	pass
    except:
   	print "\nclosed"
    	break
