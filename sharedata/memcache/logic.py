#import memcache
import time
import pylibmc
import traceback
import mytimer

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
    sleep_delay=get_arg(50.0) #gets value in sec for delay
    #shared = memcache.Client(['127.0.0.1:11211'], debug=0)
    shared = pylibmc.Client(["127.0.0.1"], binary=True)
    shared.behaviors = {"tcp_nodelay": True, "ketama": True}
    count=1
    StartT=time.time()
    cycle_s_arr_i=0
    cycle_s_arr=[0,0]*5	#set len of circular array
    d_out = [0,0]*4 	#set array of 8 zeros
    d_in_prev = d_out_prev = [0,0]*4
    shared["logic_sleep_ms"]=sleep_delay*1000
    timer1_start=time.time()
    timer1=0
    p_prev=0
    do_once=0
    l003_prev = 0
    while (1):
        try:
	    #value = shared.get_multi(['d_in', 'cpu'])
	    #get inputs
	    d_in = list(shared["d_in"])			#read inputs and change tuple to list
	    d_in = [int(not(i)) for i in d_in]		#invert all inputs for human understending
	    
	    #do smth 
	    if not do_once:
		t1 = mytimer.TON(d_in[0])
		t2 = mytimer.TOFF(d_in[1])
		t3 = mytimer.TON(0)
		t4 = mytimer.BLINK(0)
		do_once=1

	    # main logic------------------------------------begin-----------------
	    if not t3.do:
	    	d_out[0] = d_in[0]
	    	d_out[1] = d_in[1]
	
	    	d_raise = lambda x,y: 1 if x and not(y) else 0
	    	if (d_raise(d_in[1],d_in_prev[1]) and not(d_in[0])): d_out[2] = 1
	    	if (d_raise(d_in[0],d_in_prev[0])): d_out[2] = 0
            	if d_raise(d_in[0],d_in_prev[0]): d_out[3] = int(not(d_out[3]))
	    
	    	t1.out(d_in[0],3)
	    	d_out[4] = t1.do

	    	t2.out(d_in[1],7)
	    	d_out[5] = t2.do

	    l001 = not(1 in d_in[:7])
	    t3.out(l001,10)
	    l002 = t3.do
	    #print t3.out_str()
	    t4.out(l002,0.005,0.005)
	    l003 = t4.do
	    if mytimer.get_on(l003,l003_prev):
		if t4.count == 1:
		    d_out[0] = 1
		else:
		    d_out_on = d_out.index(1)
		    d_out[d_out_on] = 0
		    d_out_on +=1
		    if d_out_on >= len(d_out): d_out_on = 0
		    d_out[d_out_on] = 1
		    #print d_out_on, d_out
	    l003_prev = l003
	    #print t4.out_str() # debuf msg
	    
	    # main logic--------------------------------end--------------------
	    #write outputs
	    shared["d_out"] = tuple(d_out)		#write current output and change list to tuple
	    d_in_prev = d_in				#save previous values
	    d_out_prev = d_out

            cycle_s_arr[cycle_s_arr_i]=(time.time()-StartT)
	    cycle_s_arr_i+=1
	    if cycle_s_arr_i >= len(cycle_s_arr):
		cycle_s_arr_i=0
		shared["logic_cycle_time"] = round((sum(cycle_s_arr)/float(len(cycle_s_arr)))*1000,2)
	    shared["logic_count"] = count
	    #----add print for debuging------
	    #print d_out[1],d_out_prev[1],timer1,time.time()-timer1_start,"\r"
	    #increase count and wait
	    count+=1
      	    StartT=time.time()
	    time.sleep(shared["logic_sleep_ms"]/1000.0)
        except:	
	    shared.disconnect_all()
	    print "\nclosed"
            print traceback.format_exc()
    	    break

if __name__ == '__main__':
    main()
