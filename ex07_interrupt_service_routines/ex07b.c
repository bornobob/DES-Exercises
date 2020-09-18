#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <alchemy/task.h>
#include <alchemy/timer.h>
#include <rtdm/gpio.h>

RTIME halfsec = 5e8;

void demo(void *arg) {
    rt_task_set_periodic(NULL, TM_NOW, halfsec);
    int fd,value,ret;
    value=1; 
    fd=open("/dev/rtdm/pinctrl-bcm2835/gpio22",O_WRONLY);
    ret=ioctl(fd, GPIO_RTIOC_DIR_OUT, &value);

    while(1)
    {
        if (value == 1) value = 0;
        else value = 1;
        ret=write(fd, &value, sizeof(value));
        rt_task_wait_period(NULL);
    }
}

void interrupts(void *arg) {
    int fd, value, count, ret;
    count = 0;
    fd=open("/dev/rtdm/pinctrl-bcm2835/gpio24",O_RDONLY);
    int xeno_trigger=GPIO_TRIGGER_EDGE_FALLING|GPIO_TRIGGER_EDGE_RISING;
    ret=ioctl(fd, GPIO_RTIOC_IRQEN, &xeno_trigger);

    while(1)
    {
        ret=read(fd, &value, sizeof(value));
        count += 1;
        printf("Number of interrupts: %d\n", count);
    }
}

int main(int argc, char* argv[])
{
    RT_TASK task, counting_task;
    rt_task_create(&task, "Blinky light", 0, 2, 0);
    rt_task_start(&task, &demo, 0);

    rt_task_create(&counting_task, "County count", 0, 1, 0);
    rt_task_start(&counting_task, &interrupts, 0);

    printf("End program by CTRL-C\n");
    pause();
}
