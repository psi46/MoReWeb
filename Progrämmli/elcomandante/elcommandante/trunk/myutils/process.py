import os
import sys

def create_pid_file():
    name = sys.argv[0].rsplit("/", 1)[-1]
    pid = os.getpid()
    f = open("/var/tmp/" + name + ".pid", "w")
    f.write(str(pid))
    f.close()

def remove_pid_file():
    name = sys.argv[0].rsplit("/", 1)[-1]
    try:
        os.remove("/var/tmp/" + name + ".pid")
    except:
        pass

def get_process_pid(executable_name):
    # Check for a PID file
    pidfile = executable_name + ".pid"
    if not pidfile in os.listdir("/var/tmp"):
        return -1

    # Open the PID file and read the PID
    pid = -1
    try:
        f = open("/var/tmp/" + pidfile)
        pid = int(f.read())
        f.close()
    except:
        return -1
    return pid

def check_process_running(executable_name):
    pid = get_process_pid(executable_name)
    if pid <= 0:
        return False

    # Read the command line of that process
    try:
        f = open("/proc/" + str(pid) + "/cmdline")
        cmdline = f.read()
        f.close()
    except:
        return False

    # See whether it's the program we expect
    if executable_name in cmdline:
        return True

    return False
