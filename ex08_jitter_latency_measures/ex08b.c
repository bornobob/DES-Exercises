#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <alchemy/task.h>
#include <alchemy/timer.h>
#include <alchemy/sem.h>
#include <rtdm/gpio.h>

RT_SEM mainblocker;
RTIME msec = 1e6;
RTIME usec = 1e3;
unsigned int NR_SAMPLES = 10000;
unsigned int SKIP_SAMPLES = 100;
RTIME *time_diff;
RTIME *time_write;
RTIME *time_inter;

void generate(void *arg) {
    rt_task_set_periodic(NULL, TM_NOW, msec);
    int fd,value,ret;
    value=0; 
    fd=open("/dev/rtdm/pinctrl-bcm2835/gpio22",O_WRONLY);
    ret=ioctl(fd, GPIO_RTIOC_DIR_OUT, &value);
    int i;
    for (i=0; i<NR_SAMPLES + SKIP_SAMPLES; i++)
    {
        if (value == 1) value = 0;
        else value = 1;
        if (i >= SKIP_SAMPLES) {
            RTIME read = rt_timer_read();
            time_write[i - SKIP_SAMPLES] = read;
        }
        ret=write(fd, &value, sizeof(value));
        rt_task_wait_period(NULL);
    }
}

void doWork(void *arg) {
    printf("Start working \n");
    while (1) {
        rt_task_sleep(200*usec);
        rt_timer_spin(500*usec); 
    }
}

void catch_interrupts(void *arg) {
    int fd, value, ret;
    fd=open("/dev/rtdm/pinctrl-bcm2835/gpio24",O_RDONLY);
    int xeno_trigger=GPIO_TRIGGER_EDGE_RISING|GPIO_TRIGGER_EDGE_FALLING;
    ret=ioctl(fd, GPIO_RTIOC_IRQEN, &xeno_trigger);
    int i;
    for (i=0; i<NR_SAMPLES + SKIP_SAMPLES; i++)
    {
        ret=read(fd, &value, sizeof(value));
        if (i >= SKIP_SAMPLES) {
            RTIME read = rt_timer_read();
            time_inter[i - SKIP_SAMPLES] = read;
        }
    }
    rt_sem_v(&mainblocker);
}

void calc_time_diffs() 
{
    int i;
    for (i=0; i<NR_SAMPLES; i++) {
        time_diff[i] = time_inter[i] - time_write[i];
    }
}

void write_RTIMES(char *filename, unsigned int number_of_values, RTIME *time_values)
{
    unsigned int n=0;
    FILE *file;
    file = fopen(filename,"w");
    while (n<number_of_values) {
        fprintf(file,"%u,%llu\n",n,time_values[n]);
        n++;
    } 
    fclose(file);
}

RTIME calc_average_time(unsigned int nr_values, RTIME *values) 
{
    RTIME sum = 0;
    int i;
    for (i=0; i<nr_values; i++) {
        sum += values[i];
    }
    return sum / nr_values;
}

int main(int argc, char* argv[])
{
    time_write = calloc(NR_SAMPLES, sizeof(RTIME));
    time_inter = calloc(NR_SAMPLES, sizeof(RTIME));
    time_diff = calloc(NR_SAMPLES, sizeof(RTIME));

    rt_sem_create(&mainblocker, "MainBlocker", 0, S_FIFO);

    RT_TASK generator, worker, inter;
    rt_task_create(&generator, "generator", 0, 50, 0);

    rt_task_create(&worker, "worker", 0, 1, 0);
    rt_task_start(&worker, &doWork, 0);

    rt_task_create(&inter, "interrupter", 0, 80, 0);
    rt_task_start(&inter, catch_interrupts, 0);


    rt_task_start(&generator, &generate, 0);

    rt_sem_p(&mainblocker, TM_INFINITE);

    calc_time_diffs();

    write_RTIMES("time_diff_b.csv", NR_SAMPLES, time_diff);
    RTIME average;
    average = calc_average_time(NR_SAMPLES, time_diff);
    printf("average  %llu\n", average);
}
