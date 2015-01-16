#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <sys/time.h>
#include <errno.h>

#include <modbus.h>

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
/* Tests based on PI-MBUS-300 documentation */
int main(int argc, char *argv[])
{
    uint8_t *tab_bit;
    uint16_t *tab_reg;
    modbus_t *ctx;
    int i,j,updown;
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
    int const debug = 0;
    int print_ms=1000;
    n_loop = 10000000;
    regs = 8;

    ctx = modbus_new_rtu("/dev/ttyUSB0", 115200, 'O', 8, 1);
    modbus_set_slave(ctx, 5);

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

    printf("READ BITS\n\n");

    nb_points = regs;
    start = gettime_ms();
    //modbus_write_bit(ctx,3,1);

    for (i=0; i<n_loop; i++) {
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
        rc = modbus_read_bits(ctx, 0, nb_points, tab_bit);
	if (debug){for (j=0;j < rc;j++) {printf("%u ",tab_bit[j]);} printf("\n");}
	//printf("%x \n", tab_bit);
	//printf("number of bits:%u %u \n",tab_bit[0],tab_bit[1]);
        if (rc == -1) {
            fprintf(stderr, "%s\n", modbus_strerror(errno));
            free(tab_bit);
    	    free(tab_reg);
	    modbus_close(ctx);
    	    modbus_free(ctx);
            return -1;
        }
    if (!(i % print_ms)){
	end = gettime_ms();
	elapsed = end - start;
	cycle_ms = elapsed/print_ms;
	printf("i=%d %.3f ms DO: ",i,cycle_ms);
	for (j=0;j < rc;j++) {printf("%u ",tab_bit[j]);} printf("\n");
	start = gettime_ms();
	}
    }
    end = gettime_ms();
    elapsed = end - start;

    cycle_ms = elapsed/n_loop;
    printf("Cycle time: %.3f ms\n",cycle_ms);

    /* Free the memory */
    free(tab_bit);
    free(tab_reg);

    /* Close the connection */
    modbus_close(ctx);
    modbus_free(ctx);

    return 0;
}
/*	To compile

gcc mytest.c -o mytest `pkg-config --libs --cflags libmodbus`

	To run
time ./mytest


*/
