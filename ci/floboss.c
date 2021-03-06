#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <sys/time.h>
#include <errno.h>
#include <stdint.h>

#include <modbus.h>
#include <libmemcached/memcached.h>

#define G_MSEC_PER_SEC 1000

uint32_t gettime_ms(void)
{
    struct timeval tv;
    gettimeofday (&tv, NULL);

    return (uint32_t) tv.tv_sec * 1000 + tv.tv_usec / 1000;
}

enum {
    TCP,
    RTU
};

void gettime_sec_ms(char *str)
{
    char buffer[50];
    struct timeval tv;
    gettimeofday (&tv, NULL);
    	//printf("FUNCTION: sec=%d\t ms_sec=%d \n",tv.tv_sec,tv.tv_usec/1000);
    str[0] = '\0';
    	//printf("str %s buffer %s \n", str, buffer);
    buffer[0] = '\0';
    strcpy(str,"(");
    snprintf(buffer, sizeof(buffer), "%d", tv.tv_sec);
    strcat(str,buffer);
    buffer[0] = '\0';
    strcat(str, ",");
    snprintf(buffer, sizeof(buffer), "%d", tv.tv_usec/1000);
    strcat(str,buffer);
    strcat(str,")\0");
    puts(str);
    	//printf("FUNCTION: out= %s \n",str);
}


/*
uint8_t *get_arr(int value){
    uint8_t array[8];
    //int* array = malloc(sizeof(int) * 8);
    int j;
    printf("get_arr function debug:");
    for (j = 0; j < 8; j++) {
            array[j] = (value >> j) & 1;
            printf("%d",array[j]);
            }
    return array;
}
*/
void printArr(int *array, int len){
     int i=0;
     for (i=0; i<len; i++){
         printf("%d\t", array[i]);
     }
     printf("\n");
}

void arrToStr(uint8_t *array, int len, char *str){
     int i=0;
     char buffer[33];
     str[0] = '\0';
     strcpy(str,"(");
     for (i=0;i<len;i++){
        //itoa (array[i],buffer,10);
        snprintf (buffer, sizeof(buffer), "%d",array[i]);
        strcat(str,buffer);
        if ((i+1)<len)
            strcat(str,",");
        buffer[0] = '\0';
     }
    strcat(str,")\0");
     puts(str);
}

int memcacheSet(memcached_st *_memc, char *_key, char *_value){
	memcached_return _memrc;
	_memrc = memcached_set(_memc, _key, strlen(_key), _value, strlen(_value), (time_t)0, (uint32_t)0);
	if (_memrc != MEMCACHED_SUCCESS){
    		fprintf(stderr, "Couldn't store key: %s\n", memcached_strerror(_memc, _memrc));
    		return 1;//break;
    		}
	return 0;
}
uint16_t bswap_16(uint16_t x)
{
    return (x >> 8) | (x << 8);
}

uint32_t bswap_32(uint32_t x)
{
    return (bswap_16(x & 0xffff) << 16) | (bswap_16(x >> 16));
}
/* Get a float from 4 bytes in Modbus format (ABCD) */
float modbus_get_float_cdab(const uint16_t *src)
{
    float f;
    uint32_t i;

    i = (((uint32_t)src[0]) << 16) + src[1];
    memcpy(&f, &i, sizeof(float));

    return f;
}
/* Tests based on PI-MBUS-300 documentation */
int main(int argc, char *argv[])
{
  // memcached variables
  memcached_server_st *servers = NULL;
  memcached_st *memc;
  memcached_return memrc;
  char * key = (char *) malloc(100);
  //char *value;
  char * value = (char *) malloc(100);
  char *retrieved_value;
  size_t value_length;
  uint32_t flags;
    // libmodbus and etc
    uint8_t *tab_bit;
    //uint16_t *tab_reg;
    modbus_t *ctx;
    int i,j,updown,changed;
    int nb_points;
    double elapsed;
    double cycle_ms;
    uint32_t start;
    uint32_t end;
    uint32_t bytes;
    uint32_t rate;
    int rc;
    int n_loop;
    int use_backend;
    int regs;
    struct timeval response_timeout;
    uint8_t *set_coil;//[8];// = {1,0,1,0,1,1,0,1};
    set_coil = malloc(sizeof(uint8_t) * 8);
    int set_coil_value = 0b00000001;
    int const debug = 1;
    int print_ms=1000;
    n_loop = 3;//1E9;
    regs = 8;
    uint8_t di[8]={0},di_prev[8]={0},doo[8]={0},doo_prev[8]={0};
    char timeStr[50];
    //char *arrStr;
    char * arrStr = (char *) malloc(100);

  // set up connection to MEMCACHED
  memc = memcached_create(NULL);
  servers = memcached_server_list_append(servers, "localhost", 11211, &memrc);
  memrc = memcached_server_push(memc, servers);
  if (memrc == MEMCACHED_SUCCESS)
    fprintf(stderr, "Added server successfully\n");
  else
    fprintf(stderr, "Couldn't add server: %s\n", memcached_strerror(memc, memrc));

  // check up the arguments
  if (argc > 1) {
        if (strcmp(argv[1], "fl1") == 0) {
            use_backend = TCP;
        } else if (strcmp(argv[1], "fl2") == 0) {
            use_backend = RTU;
        } else {
            printf("Usage:\n  %s [fl1|fl2] - Modbus client to measure data bandwith\n\n", argv[0]);
            exit(1);
        }
    } else {
        /* By default */
	printf("Usage:\n  %s [tcp|rtu] - Modbus client to measure data bandwith\n\n", argv[0]);
	exit(1);
    }

    if (use_backend == TCP) {
        ctx = modbus_new_tcp("192.168.1.1", 502);
	modbus_set_slave(ctx, 1);
    } else {
        ctx = modbus_new_tcp("192.168.1.2", 502);
        modbus_set_slave(ctx, 1);
    }

    if (modbus_connect(ctx) == -1) {
        fprintf(stderr, "Connexion failed: %s\n",
                modbus_strerror(errno));
        modbus_free(ctx);
        return -1;
    }
    response_timeout.tv_sec = 1;
    response_timeout.tv_usec = 0;
    modbus_set_response_timeout(ctx, &response_timeout);
    /* Allocate and initialize the memory to store the status */
    tab_bit = (uint8_t *) malloc(regs * sizeof(uint8_t));
    memset(tab_bit, 0, regs * sizeof(uint8_t));

    uint16_t tab_reg[128];
    int regs_data[4][2]={
	{7000,42},
	{7126,6},
	{7160,14},
	{7232,16}
	};
    int regs_start;
    int regs_number;
    int k;

    printf("READ BITS\n\n");
    start = gettime_ms();

// main cycle
for (i=1; i<n_loop; i++) {
    for (k=0;k<4;k++) {
	regs_start = regs_data[k][0];
	regs_number = regs_data[k][1];

	rc = modbus_read_registers(ctx, regs_start, regs_number, tab_reg);
	//if (debug){for (j=0;j < rc;j++) {printf("%u ",tab_bit[j]);} printf("\n");}
	//printf("number of bits:%u %u \n",tab_bit[0],tab_bit[1]);
        if (rc == -1) {
            fprintf(stderr, "Reading Error: %s\n", modbus_strerror(errno));
            free(tab_bit);
	    modbus_close(ctx);
    	    modbus_free(ctx);
            return -1;
	    break;
            }
	//printf("%d\t",i);print_arr("tab_bit =",tab_bit,8);
	//gettime_sec_ms();
	//sleep(1);

	//for (j=0; j < rc; j++)
	//	printf("reg[%d]=%d (0x%X)\n", j, tab_reg[j], tab_reg[j]);
	printf("\nrequest number %d\n", k);
	for (j=0; j < (rc+1)/2; j++) {
		printf("float%02d=%14.3f\t\t", regs_start+2*j, modbus_get_float_cdab(&tab_reg[2*j]));
		if (!((j+1) % 4))
			printf("\n");
		}
    }//k loop
	for (j=0; j<8; j++){
		di[j] = tab_bit[j];
		doo[j] = !di[j];
		}
	//print_arr("DI",doo,8);print_arr("DO",doo,8);
	changed = 0;
	for (j=0; j<8; j++){
		if (doo[j]!=doo_prev[j]) {
			changed = 1;
			printf("changed\n");
			break;
			}
		}
	//print_arr("DO",doo,8);print_arr("DO_prev",doo_prev,8);
	if (memcmp(di_prev,di,sizeof(di))!=0) {
		gettime_sec_ms(timeStr);	// get time in STR
		//printf("MAIN: timeStr= %s \n",timeStr);
		arrToStr(tab_bit, 8, arrStr);	// get arra in STR
		//printf("MAIN: arrStr= %s \n", arrStr);
		if (use_backend == TCP)
			strcpy(key, "tcp");
		else
			strcpy(key, "rtu");
		strcat(key, "_di"); puts(key);
		//printf("MAIN: prepare to set to memcache: %s \t %s\n", key, arrStr);
		value = NULL;
		value=(char *)malloc(100*sizeof(char));
		strcpy(value, arrStr); puts(value);
		printf("MAIN: set to memcache: %s \t %s\n", key, value);
		memrc = memcached_set(memc, key, strlen(key), value, strlen(value), (time_t)0, (uint32_t)0);
                if (memrc != MEMCACHED_SUCCESS) {
                        fprintf(stderr, "Couldn't store key: %s\n", memcached_strerror(memc, memrc));
                        break;
                }
		strcat(key,"_arc");
		strcpy(value,timeStr);	strcat(value,arrStr);	puts(value);
                printf("MAIN: append to memcache: %s=%s\n",key, value);
		memrc = memcached_append(memc, key, strlen(key), value, strlen(value), (time_t)0, (uint32_t)0);
		if (memrc != MEMCACHED_SUCCESS){
			if (strcmp(memcached_strerror(memc, memrc), "NOT STORED")==0) {
				printf("we gonna create it first\n");
				memrc = memcached_set(memc, key, strlen(key), value, strlen(value), (time_t)0, (uint32_t)0);
			}
			else {
    			fprintf(stderr, "Couldn't store key: %s\n", memcached_strerror(memc, memrc));
    			break;
			}
    		}
		//di_prev = di;
		memcpy(di_prev,di,sizeof(di));
	}
	if (changed==1) {
		rc = modbus_write_bits(ctx,0,8,doo);
		printf("change DOs\n");
	     	for (j=0; j<8; j++){doo_prev[j] = doo[j];}
		if (rc == -1) {
            		fprintf(stderr, "%s\n", modbus_strerror(errno));
            		modbus_close(ctx);
            		modbus_free(ctx);
            		return -1;
            		break;
	   		}
		}


/*
    //set_coil = get_arr(set_coil_value);
	for (j = 0; j < 8; j++) {
            set_coil[j] = (set_coil_value >> j) & 1;
            if (debug){printf("%d",set_coil[j]);}
	    }

	if (debug){printf("main: set_coil_value = %d ", set_coil_value);
	printf("main: set_coil = ");}
	//for (j=0;j<8;j++){printf("%u ",set_coil[j]);}printf("DO feadback");
	rc = modbus_write_bits(ctx,0,8,set_coil);
	    if (rc == -1) {fprintf(stderr, "%s\n", modbus_strerror(errno));}
	if (set_coil_value==1) updown=1;
	if (set_coil_value==128) updown=0;
    	set_coil_value = updown ? set_coil_value<<1 : set_coil_value>>1;
*/
    if (!(i % print_ms)){

        if (use_backend == TCP)
        	strcpy(key, "tcp");
        else
                strcpy(key, "rtu");
        strcat(key, "_cycle"); puts(key);
	value = NULL;
	value=(char *)malloc(100*sizeof(char));
	sprintf (value, "%ld", i);
	//strcat(value,"0\0");
	puts(value);
	memrc = memcached_set(memc, key, strlen(key), value, strlen(value), (time_t)0, (uint32_t)0);
                if (memrc != MEMCACHED_SUCCESS) {
                        fprintf(stderr, "Couldn't store key: %s\n", memcached_strerror(memc, memrc));
                        break;
                }

	end = gettime_ms();
	elapsed = end - start;
	cycle_ms = elapsed/print_ms;
	printf("i=%d %.3f ms DI: ",i,cycle_ms);
	for (j=0;j < rc;j++) {printf("%u ",tab_bit[j]);} printf("\n");
	start = gettime_ms();
	}
    if (!(i % (5*print_ms))) {
	if (use_backend == TCP)
                strcpy(key, "tcp");
        else
              	strcpy(key, "rtu");
        strcat(key, "_di_arc"); puts(key);

	printf("ADDITIONAL: reset to memcache: %s \t %s\n", key, "reset");
        memrc = memcached_set(memc, key, strlen(key), "reset", strlen("reset"), (time_t)0, (uint32_t)0);
        if (memrc != MEMCACHED_SUCCESS) {
        	fprintf(stderr, "Couldn't store key: %s\n", memcached_strerror(memc, memrc));
                break;
                }
	}
}
    end = gettime_ms();
    elapsed = end - start;

    cycle_ms = elapsed/n_loop;
    printf("Cycle time: %.3f ms\n",cycle_ms);

    /* Free the memory */
    free(tab_bit);
    //free(tab_reg);

    /* Close the connection */
    modbus_close(ctx);
    modbus_free(ctx);

    return 0;
}
/*	To compile

gcc mambas.c -o mambas -lmemcached `pkg-config --libs --cflags libmodbus`

	To run
time ./mambas


*/
