#include <stdio.h>
#include <signal.h>
#include <unistd.h>

#include <alchemy/task.h>

#define NTASKS 3

RT_TASK task[NTASKS];
RTIME sec = 1e9;

// function to be executed by the task
void demo(void *arg) {
  int num = * (int *)arg;
  rt_task_sleep(sec);
  rt_task_set_periodic(NULL, TM_NOW, sec * (num + 1));
  RT_TASK_INFO curtaskinfo;
  rt_task_inquire(NULL,&curtaskinfo);
  while(1)
  {
    rt_printf("Task name: %s\tTask number: %d\tRunning every %d second(s)\n", curtaskinfo.name, num, num+1);
    rt_task_wait_period(NULL);
  }
  
  return;
}

int main(int argc, char* argv[])
{
  char task_name[10];
	
  int index;
  for (index=0; index < NTASKS; index++)
  {
    sprintf(task_name,"Task %d", index);
    rt_task_create(&task[index], task_name, 0, 1, 0);
    rt_task_start(&task[index], &demo, &index);
  }
  
  printf("End program by CTRL-C\n");
  pause();
}
