#include <stdio.h>
#include <signal.h>
#include <unistd.h>
#include <alchemy/task.h>
#include <alchemy/mutex.h>
#include <alchemy/timer.h>

RT_TASK task_1, task_2, task_3;
RT_MUTEX mysync;

#define EXECTIME   2e8   // execution time in ns
#define SPINTIME   1e7   // spin time in ns

#define HIGH 52 /* high priority */
#define MID 51 /* medium priority */
#define LOW 50  /* low priority */

void taskOne(void *arg) {
    int i;
    
    rt_task_sleep(SPINTIME / 4);
    
    for (i=0; i < 3; i++) {
        rt_mutex_acquire(&mysync, TM_INFINITE);
        printf("Low priority task locks semaphore\n");
        rt_timer_spin(SPINTIME);
        printf("Low priority task unlocks semaphore\n");
        rt_mutex_release(&mysync);
    }
    printf("..........................................Low priority task ends\n");
}

void taskTwo(void *arg) {
    int i;
    
    rt_task_sleep(SPINTIME / 3);
    
    for(i=0;i<12;i++) {
        printf("Medium task running\n");
        rt_timer_spin(SPINTIME);  // spin cpu doing nothing
    }
    printf("------------------------------------------Medium priority task ends\n");
}

void taskThree(void *arg) {    
    int i;
    
    rt_task_sleep(SPINTIME / 2);
    
    for (i=0; i < 3; i++) {
        printf("High priority task tries to lock semaphore\n");
        rt_mutex_acquire(&mysync, TM_INFINITE);
        printf("High priority task locks semaphore\n");
        rt_timer_spin(SPINTIME);
        printf("High priority task unlocks semaphore\n");
        rt_mutex_release(&mysync);
    } 
    printf("..........................................High priority task ends\n");
}

int main(int argc, char* argv[])
{
    rt_mutex_create(&mysync, "MySemaphore");
    
    rt_task_create(&task_1, "Task 1 - prio Low", 0, LOW, 0);
    rt_task_start(&task_1, &taskOne, 0);
    
    rt_task_create(&task_2, "Task 1 - prio Mid", 0, MID, 0);
    rt_task_start(&task_2, &taskTwo, 0);
    
    rt_task_create(&task_3, "Task 1 - prio High", 0, HIGH, 0);
    rt_task_start(&task_3, &taskThree, 0);
    
    printf("End program by CTRL-C\n");
    pause();
}



















