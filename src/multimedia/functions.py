import subprocess
import threading

def exit_process_send_keystroke(process, command):
    """
    Tries to exit a process cleanly by simulating a keypress, then kills the process if it is still exists.

    Parameters
    ----------
    process : Process
        The process to exit.

    Returns
    -------
    True if the process exited successfully, otherwise false.
    """

    # Nothing to do here.
    if process is None:
        return False

    # Try to exit cleanly.
    try:
        send_keytroke_to_process(process, command)
    except Exception:
        pass

    # Terminate process if it is still alive.
    return terminate_process(process)

def popen_and_wait_for_exit(need_stdin, on_exit, on_process_started, popen_arguments):
    """
    Runs the given args in a "subprocess.Popen()" and then calls the function "on_process_started()" when the process is
    started and "on_exit()" when the subprocess exists.

    Parameters
    ----------
    need_stdin : boolean
        Indicates whether the process's standard input is to be used.
    on_exit : object
        A callable object which gets called after the subprocess has been exited.
    on_process_started : object
        A callable object which gets called when the subprocess is started and passed the process as an argument. It
        should not do any computationally intensive tasks. Introduced only to be able to attach a setter method.
    popen_arguments : list of str
        A list or tuple of arguments that will be given to "subprocess.Popen()".
    """

    def run():

        if need_stdin:
            process = subprocess.Popen(
                popen_arguments,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
        else:
            process = subprocess.Popen(popen_arguments)

        on_process_started(process)
        process.wait()
        on_exit()

    thread = threading.Thread(target=run, args=())
    thread.start()

    # Returns immediately after the thread starts.
    return thread

def send_keytroke_to_process(process, command):
    """
    Sends a simple command to the process's standard input.

    Parameters
    ----------
    process : Process
        The process to control.

    Returns
    -------
    True if the keystroke was sent successfully, false in case the process handler is invalid.
    """

    if process is None:
        return False

    process.stdin.write(command.encode())
    process.stdin.flush()

    return True

def terminate_process(process):
    """
    Tries to terminate the given process.

    Parameters
    ----------
    process : Process
        The process to terminate.

    Returns
    -------
    True if the process was terminated successfully, otherwise false.
    """

    try:
        process.terminate()
        process.wait()
    except Exception:
        return False

    return True
