#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <alchemy/task.h>
#include <alchemy/timer.h>
#include <alchemy/sem.h>
#include <rtdm/gpio.h>

RTIME SEC = 1e9;
RTIME MSEC = 1e6;
RTIME time_rotation;
RT_SEM synchro;

int DEGREE = 352; //Should be modulo 360
int WIDTH = 16; //Should be multiple of 8

int *lights;

char* pins[] = {"/dev/rtdm/pinctrl-bcm2835/gpio2", "/dev/rtdm/pinctrl-bcm2835/gpio3", "/dev/rtdm/pinctrl-bcm2835/gpio4", "/dev/rtdm/pinctrl-bcm2835/gpio17", "/dev/rtdm/pinctrl-bcm2835/gpio27", "/dev/rtdm/pinctrl-bcm2835/gpio22", "/dev/rtdm/pinctrl-bcm2835/gpio10", "/dev/rtdm/pinctrl-bcm2835/gpio9"};

int x_matrix[][8]= {{1, 0, 0, 0, 0, 0, 0, 1},
				  {0, 1, 0, 0, 0, 0, 1, 0},
				  {0, 0, 1, 0, 0, 1, 0, 0},
				  {0, 0, 0, 1, 1, 0, 0, 0},
				  {0, 0, 0, 1, 1, 0, 0, 0},
				  {0, 0, 1, 0, 0, 1, 0, 0},
				  {0, 1, 0, 0, 0, 0, 1, 0},
				  {1, 0, 0, 0, 0, 0, 0, 1}};
				  
void open_lights() {
	printf("Lights open\n");
	int i, fd, ret, value;
	value = 0;
	for (int i = 0; i < 8; i++) {
		fd = open(pins[i], O_WRONLY);
		ret=ioctl(fd, GPIO_RTIOC_DIR_OUT, &value);
		lights[i] = fd;
	}
}
				  
void turn_on_x(int i) {
	int index;
	for (index = 0; index < 8; index++) {
		write(lights[index],&x_matrix[index][i], sizeof(int));
	}
}

void turn_off_x() {
	int index;
	int value = 0;
	for (index = 0; index < 8; index++) {
		write(lights[index],&value, sizeof(int));
	}
}

void light_handler(void *arg) {
	open_lights();
	while(1)
	{
		rt_sem_p(&synchro, TM_INFINITE);
		rt_task_sleep((time_rotation/360)*DEGREE);
		for (int i = 0; i < 8; i++) {
			turn_on_x(i);
			rt_task_sleep((time_rotation/360)*(WIDTH/8));
		}
		turn_off_x();
	}
}

void demo(void *arg) {
    int fd_sensor, value, ret, index, count;
	count = 0;
	RTIME prev_low;
    int xeno_trigger=GPIO_TRIGGER_EDGE_FALLING|GPIO_TRIGGER_EDGE_RISING;
    fd_sensor=open("/dev/rtdm/pinctrl-bcm2835/gpio23",O_RDONLY);
    ret=ioctl(fd_sensor, GPIO_RTIOC_IRQEN, &xeno_trigger);
    while(1)
    {
        ret=read(fd_sensor, &value, sizeof(value));
		RTIME read = rt_timer_read();
		if (value == 0) {
			time_rotation = (read - prev_low);
			prev_low = read;
			if (count > 3) {
				rt_sem_broadcast(&synchro);
			}
			count += 1;
		}
    }
}

int main(int argc, char* argv[])
{
	lights = calloc(8, sizeof(int));
	
	rt_sem_create(&synchro, "sync", 0, S_FIFO);
	
	RT_TASK task, rotation;
	rt_task_create(&rotation, "Rotating lights", 0, 4, 0);
	rt_task_start(&rotation, &light_handler, 0);
    rt_task_create(&task, "Light sensor", 0, 2, 0);
    rt_task_start(&task, &demo, 0);
    printf("End program by CTRL-C\n");
    pause();
}