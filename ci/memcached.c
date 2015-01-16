#include <libmemcached/memcached.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <sys/time.h>


uint32_t gettime_ms(void)
{
    struct timeval tv;
    gettimeofday (&tv, NULL);

    return (uint32_t) tv.tv_sec * 1000 + tv.tv_usec / 1000;
}


int main(int argc, char **argv) {
  //memcached_servers_parse (char *server_strings);
  memcached_server_st *servers = NULL;
  memcached_st *memc;
  memcached_return rc;
  char *key = "keystring";
  char *value = "keyvalue330.330";
  char myval[30];
  int i;
  char *retrieved_value;
  size_t value_length;
  uint32_t flags;
  uint32_t start,end;
  double elapsed,cycle_ms;
  int print_ms=1000;

  memc = memcached_create(NULL);
  servers = memcached_server_list_append(servers, "localhost", 11211, &rc);
  rc = memcached_server_push(memc, servers);

  if (rc == MEMCACHED_SUCCESS)
    fprintf(stderr, "Added server successfully\n");
  else
    fprintf(stderr, "Couldn't add server: %s\n", memcached_strerror(memc, rc));
//for (i=0;i<10;i++){
start = gettime_ms();
i=0;
while (1) {
  i++;
  sprintf(myval,"%d",i);
  //rc = memcached_set(memc, key, strlen(key), myval, strlen(myval), (time_t)0, (uint32_t)0);

  if (rc != MEMCACHED_SUCCESS)
    //fprintf(stderr, "Key stored successfully\n");
    {
    fprintf(stderr, "Couldn't store key: %s\n", memcached_strerror(memc, rc));
    break;
    }

  retrieved_value = memcached_get(memc, key, strlen(key), &value_length, &flags, &rc);
  //printf("Yay!\n");

  if (rc == MEMCACHED_SUCCESS) {
    //fprintf(stderr, "Key retrieved successfully\n");
    if (!(i % print_ms)) {
    end = gettime_ms();
    elapsed = end - start;

    cycle_ms = elapsed/print_ms;
    printf("i=%d The key '%s' = '%s'",i, key, retrieved_value);
    printf("Cycle time: %.3f ms\n",cycle_ms);
    start = gettime_ms();
    }
    free(retrieved_value);
  }
  else {
    fprintf(stderr, "Couldn't retrieve key: %s\n", memcached_strerror(memc, rc));
    break;
   }
}
  return 0;
}


// gcc -o memchached memcached.c -lmemcached
