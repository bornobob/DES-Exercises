import subprocess
import time


PYTHON_EXECUTABLE = 'python'
BRICK_1_PY = 'main_main.py'
BRICK_2_PY = 'main_slave.py'


if __name__ == "__main__":
    proc1 = subprocess.Popen([PYTHON_EXECUTABLE, BRICK_1_PY])
    time.sleep(1)
    proc2 = subprocess.Popen([PYTHON_EXECUTABLE, BRICK_2_PY])

    input('Press [enter] to stop the simulation')
    proc2.kill()
    proc1.kill()
