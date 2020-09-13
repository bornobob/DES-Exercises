#include <stdio.h>
#include <signal.h>
#include <unistd.h>

#include <alchemy/task.h>
#include <alchemy/timer.h>
#include <alchemy/sem.h>

#define NTASKS 5

RT_TASK task[NTASKS];
RTIME sec = 1e9;

static RT_SEM s1;

void demo(void *arg) {
  RT_TASK_INFO curtaskinfo;
  rt_task_inquire(NULL, &curtaskinfo);
  int num = * (int *)arg;
  rt_sem_p(&s1, sec);
  rt_printf("Task name: %s\tTask number: %d\n", curtaskinfo.name, num);
  rt_sem_v(&s1);
}

int main(int argc, char* argv[])
{
  char task_name[10];

  rt_sem_create(&s1, "semaphore1", 0, S_PRIO);
  int index;
  for (index=0; index < NTASKS; index++)
  {
    sprintf(task_name, "Task %d", index);
    rt_task_create(&task[index], task_name, 0, 1 + index, 0);
    rt_task_start(&task[index], &demo, &index);
  }
  rt_sem_v(&s1); // rt_sem_broadcast(&s1);
}
