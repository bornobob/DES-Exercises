#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <alchemy/task.h>
#include <alchemy/timer.h>
#include <alchemy/sem.h>

RT_SEM mainblocker;
RTIME WAIT_TIME = 1e5;
unsigned int NR_SAMPLES = 10000;
unsigned int SKIP_SAMPLES = 100;
RTIME *time_diff;
RTIME *time_reads;

void demo(void *arg) 
{
    rt_task_set_periodic(NULL, TM_NOW, WAIT_TIME);
    
    int i;
    for (i=0; i<NR_SAMPLES + SKIP_SAMPLES; i++)
    {
        if (i >= SKIP_SAMPLES - 1) {
            RTIME read = rt_timer_read();
            time_reads[i - SKIP_SAMPLES + 1] = read;
        }
        rt_task_wait_period(NULL);
    }
    
    rt_sem_v(&mainblocker);
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

void calc_time_diffs() 
{
    RTIME prev = time_reads[0];
    int i;
    for (i=0; i<NR_SAMPLES; i++) { 
        time_diff[i] = time_reads[i+1] - prev;
        prev = time_reads[i+1];
    }
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
    time_reads = calloc(NR_SAMPLES + 1, sizeof(RTIME));
    time_diff = calloc(NR_SAMPLES, sizeof(RTIME));
    
    rt_sem_create(&mainblocker, "MainBlocker", 0, S_FIFO);
    
    RT_TASK task;
    rt_task_create(&task, "Demo", 0, 1, 0);
    rt_task_start(&task, &demo, 0);

    rt_sem_p(&mainblocker, TM_INFINITE);
    
    calc_time_diffs();
    
    write_RTIMES("time_diff.csv", NR_SAMPLES, time_diff);
    RTIME average;
    average = calc_average_time(NR_SAMPLES, time_diff);
    printf("average  %llu\n", average);
}
