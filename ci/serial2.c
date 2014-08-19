#include <stdio.h>   /* Standard input/output definitions */
#include <string.h>  /* String function definitions */
#include <unistd.h>  /* UNIX standard function definitions */
#include <fcntl.h>   /* File control definitions */
#include <errno.h>   /* Error number definitions */
#include <termios.h> /* POSIX terminal control definitions */
void main()
{
  int fd;  // File descriptor
  int n;
  char *str;
  fd = open_port();
  // Read the configureation of the port 
  struct termios options;
  tcgetattr( fd, &options );
  /* SEt Baud Rate */
  cfsetispeed( &options, B115200 );
  cfsetospeed( &options, B115200 );
  //I don't know what this is exactly 
  options.c_cflag |= ( CLOCAL | CREAD );
  // Set parity - No Parity (8ODD1)
  options.c_cflag |= PARENB;
  options.c_cflag |= PARODD;
  options.c_cflag &= ~CSTOPB;
  options.c_cflag &= ~CSIZE;
  options.c_cflag |= CS8;
  // Enable Raw Input
  options.c_lflag &= ~(ICANON | ECHO | ECHOE | ISIG);
  // Disable Software Flow control
  options.c_iflag &= ~(IXON | IXOFF | IXANY);
  // Chose raw (not processed) output
  options.c_oflag &= ~OPOST;

  if ( tcsetattr( fd, TCSANOW, &options ) == -1 )
    printf ("Error with tcsetattr = %s\t", strerror ( errno ) );
  else
    printf ( "%s\t", "tcsetattr succeed" );

  fcntl(fd, F_SETFL, FNDELAY);

  str="\x05\x02\x00\x00\x00\x08\x78\x48";
  n = write(fd, str, 8);
  if (n < 0)
    fputs("write() of 8 bytes failed!\t", stderr);
  else
    printf ("Write succeed n = %i\t", n );
  usleep(10000);

  char *buf;
  n = read( fd, buf, 6 );
  if ( n == -1 )
      printf ( "Error = %s\t", strerror( errno ) );
  printf ( "Number of bytes to be read = %i\t", n );
  printf ( "Buf = %s\t", buf );
  printf ( "Data: %d %d \n",buf[2],buf[3]);
  close( fd );
}

int open_port(void)
{
  int fd; /* File descriptor for the port */

  fd = open("/dev/ttyUSB0", O_RDWR | O_NOCTTY | O_NDELAY);
  if (fd == -1)
    {
      perror("open_port: Unable to open /dev/ttyS0 - ");
    }
  else
    fcntl(fd, F_SETFL, FNDELAY);

 printf ( "In Open port fd = %i\t", fd);

  return (fd);
}

void todothen()
{
  int j;
  for(j=0;j<10;j++)
	{
	    //do smth here
	}
}
