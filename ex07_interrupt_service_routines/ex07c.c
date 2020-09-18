#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <alchemy/task.h>
#include <alchemy/timer.h>
#include <rtdm/gpio.h>

void demo(void *arg) {
    int fd_button, fd_light, value, ret, light_on, count;
    light_on=1;
    count=0;
    fd_light=open("/dev/rtdm/pinctrl-bcm2835/gpio22",O_WRONLY);
    ret=ioctl(fd_light, GPIO_RTIOC_DIR_OUT, &light_on);

    int xeno_trigger=GPIO_TRIGGER_EDGE_FALLING|GPIO_TRIGGER_EDGE_RISING;
    fd_button=open("/dev/rtdm/pinctrl-bcm2835/gpio23",O_RDONLY);
    ret=ioctl(fd_button, GPIO_RTIOC_IRQEN, &xeno_trigger);

    while(1)
    {
        ret=read(fd_button, &value, sizeof(value));
        if (light_on == 1) light_on = 0;
        else light_on = 1;
        ret=write(fd_light, &light_on, sizeof(light_on));
        count += 1;
        printf("Number of interrupts: %d\n", count);		
    }
}

int main(int argc, char* argv[])
{
    RT_TASK task;
    rt_task_create(&task, "Blinky light", 0, 2, 0);
    rt_task_start(&task, &demo, 0);
    printf("End program by CTRL-C\n");
    pause();
}