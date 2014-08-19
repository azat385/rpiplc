#import memcache
import time
import pylibmc

def get_arg(____default_sleep_delay=50.0, argv=None):
    import sys
    if not argv:
        argv = sys.argv
    if len(argv) >= 2 :
        try:
            float(argv[1])
            ____sleep_delay=float(argv[1]) if float(argv[1])>=1.0 else ____default_sleep_delay
        except:
           print "enter proper number!!! the default is loaded"
           ____sleep_delay=____default_sleep_delay
    else:
        ____sleep_delay = ____default_sleep_delay
    print "sleep time delay is",____sleep_delay,"[ms]\nconnecting..."
    return ____sleep_delay/1000

def main():
    sleep_delay=get_arg(55.0) #gets value in sec for delay
    #shared = memcache.Client(['127.0.0.1:11211'], debug=0)
    shared = pylibmc.Client(["127.0.0.1"], binary=True)
    shared.behaviors = {"tcp_nodelay": True, "ketama": True}
    count=1
    StartT=time.time()
    while (1):
        try:
      	    print count,shared.get_multi(['cpu','disk','ram']),"cycle time [ms]:",round((time.time()-StartT)/count*1000,2),"\r",
	    count+=1
	    time.sleep(sleep_delay)
        except:	
	    shared.disconnect_all()
	    print "\nclosed"
    	    break

if __name__ == '__main__':
    main()
