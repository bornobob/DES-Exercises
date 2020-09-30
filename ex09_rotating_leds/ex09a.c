#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <alchemy/task.h>
#include <alchemy/timer.h>
#include <rtdm/gpio.h>

unsigned int NR_SAMPLES = 100;
unsigned int SKIP_SAMPLES = 3;
RTIME SEC = 1e9;
RTIME MSEC = 1e6;
RTIME *time_sensor;
RTIME *time_rotation;

float calculate_average(RTIME* times) {
	float running_total = 0;
	int index;
	for(index = SKIP_SAMPLES; index < NR_SAMPLES - SKIP_SAMPLES; index++) {
		running_total += times[index] / (float) MSEC;
	}
	return running_total / (NR_SAMPLES/2 - 2*SKIP_SAMPLES);
}

void demo(void *arg) {
    int fd_sensor, value, ret, index;
	RTIME prev_value, prev_low;
	prev_value = 0;
    int xeno_trigger=GPIO_TRIGGER_EDGE_FALLING|GPIO_TRIGGER_EDGE_RISING;
    fd_sensor=open("/dev/rtdm/pinctrl-bcm2835/gpio23",O_RDONLY);
    ret=ioctl(fd_sensor, GPIO_RTIOC_IRQEN, &xeno_trigger);
    for (index = 0; index < NR_SAMPLES*2; index++)
    {
        ret=read(fd_sensor, &value, sizeof(value));
		RTIME read = rt_timer_read();
		if (value == 0) {
			time_sensor[index] = read - prev_value;
			time_rotation[index] = read - prev_low;
			prev_low = read;
		}
		else {
			prev_value = read;
		}
    }
	float average_sensor = calculate_average(time_sensor);
	float average_rotation = calculate_average(time_rotation);
	float rpm = (1000 / average_rotation) * 60;
	average_sensor = average_sensor;
	printf("Average sensor time: %.2f ms\t RPM: %.2f \n", average_sensor, rpm);
}

int main(int argc, char* argv[])
{
	time_sensor = calloc(NR_SAMPLES, sizeof(RTIME));
	time_rotation = calloc(NR_SAMPLES, sizeof(RTIME));
    RT_TASK task;
    rt_task_create(&task, "Light sensor", 0, 2, 0);
    rt_task_start(&task, &demo, 0);
    printf("End program by CTRL-C\n");
    pause();
}