#include <stdio.h>
#include <signal.h>
#include <unistd.h>

#include <alchemy/task.h>

#define NTASKS 5

RT_TASK task[NTASKS];

// function to be executed by the task
void demo(void *arg) {
  RT_TASK_INFO curtaskinfo;
  rt_task_inquire(NULL,&curtaskinfo);
  int num = * (int *)arg;
  rt_printf("Task name: %s\tTask number: %d\n", curtaskinfo.name, num);
}

int main(int argc, char* argv[])
{
  char task_name[10];

  int index;
  for (index=0; index < NTASKS; index++)
  {
    sprintf(task_name,"Task %d", index);
    rt_task_create(&task[index], task_name, 0, 1 + index, 0);
    rt_task_start(&task[index], &demo, &index);
  }
}
