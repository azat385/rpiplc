#include <stdio.h>   /* Standard input/output definitions */
#include <string.h>  /* String function definitions */
#include <unistd.h>  /* UNIX standard function definitions */
#include <fcntl.h>   /* File control definitions */
#include <errno.h>   /* Error number definitions */
#include <termios.h> /* POSIX terminal control definitions */

 /*
  * 'open_port()' - Open serial port 1.
  *
  * Returns the file descriptor on success or -1 on error.
  */

 int open_port(void)
 {
   int fd;                                   /* File descriptor for the port */
   printf("open the port\n");
   fd = open("/dev/ttyUSB1", O_RDWR | O_NOCTTY | O_NDELAY);
   //printf("Port ids opened %s",fd);
   if (fd == -1)
   {                                              /* Could not open the port */
     fprintf(stderr, "open_port: Unable to open /dev/ttyUSB0 - %s\n",
             strerror(errno));
   }
   printf("fd=%d\n",fd);
   return (fd);
 }

void main()
{
 int mainfd=0,fd;                                            /* File descriptor */
 char chout;
 struct termios options;

 mainfd = open_port();

 fcntl(mainfd, F_SETFL, FNDELAY);                  /* Configure port reading */
                                     /* Get the current options for the port */
 tcgetattr(mainfd, &options);
 cfsetispeed(&options, B115200);                 /* Set the baud rates to 19200 */
 cfsetospeed(&options, B115200);

                                   /* Enable the receiver and set local mode */
 options.c_cflag |= (CLOCAL | CREAD);
 options.c_cflag |=  PARODD;	 /* Mask the character size to 8 bits, no parity */
 options.c_cflag &= ~CSTOPB;
 options.c_cflag &= ~CSIZE;
 options.c_cflag |=  CS8;                              /* Select 8 data bits */
 options.c_cflag &= ~CRTSCTS;               /* Disable hardware flow control */

                                 /* Enable data to be processed as raw input */
 options.c_lflag &= ~(ICANON | ECHO | ISIG);

                                        /* Set the new options for the port */
 tcsetattr(mainfd, TCSANOW, &options);

 write(fd,"\x05\x02\x00\x00\x00\x08\x78\x48",8);
 printf("\x05\x02\x00\x00\x00\x08\x78\x48");

 usleep(500000);      /* wait for 5 second*/

 read(mainfd, &chout, sizeof(chout));          /* Read character from ABU (Auto buffering Unit) */

   if (chout != 0)
      printf("Got %c.\n", chout);

   chout=0;

                                                    /* Close the serial port */
  close(mainfd);
 }
