import os

import argparse
import multiprocessing
import subprocess
import shlex
from Debug import Debug

import threading

from multiprocessing.pool import ThreadPool

lock = threading.Lock()

def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", help="increase output verbosity",
                        action="store_true")
    parser.add_argument("--setup", help="execParalel's setup file", type=str, default="setup.txt")
    args = parser.parse_args()

    return args.verbose, args.setup


class Setup:
    def __init__(self, setup_file, verbose=False):
        self.setup_file = setup_file
        self.verbose = verbose

        self.EXEC_DIR = None
        self.OUTPUT_DIR = None
        self.N_PROC = None
        self.N_CMD = None
        self.N_CMD = None
        self.N_REEXEC = None
        self.MAIL_FLAG = None
        self.OUTPUT_FILE = None
        self.OUTPUT_TYPE = None
        self.cmds = []
        self.load_setup()

    def load_setup(self):

        with open(self.setup_file) as f:
            while True:
                line = f.readline().rstrip('\n')
                # print line

                # check if line is blank
                if line == "":
                    break

                var, val = line.split("=")

                if var == 'EXEC_DIR':
                    self.EXEC_DIR = val
                elif var == 'OUTPUT_DIR':
                    self.OUTPUT_DIR = val
                elif var == 'N_PROC':
                    self.N_PROC = int(val)
                elif var == 'N_CMD':
                    self.N_CMD = int(val)
                elif var == 'N_REEXEC':
                    self.N_REEXEC = int(val)
                elif var == 'MAIL_FLAG':
                    self.MAIL_FLAG = bool(val)
                elif var == 'OUTPUT_FILE':
                    self.OUTPUT_FILE = str(val)
                elif var == 'ONE_OUTPUT_FILE':
                    self.OUTPUT_TYPE = bool(int(val))

            for i in range(self.N_CMD):
                self.cmds.append(f.readline().rstrip('\n'))

    def __str__(self):
        string =   'EXEC_DIR=' + self.EXEC_DIR \
                + '\nOUTPUT_DIR=' + self.OUTPUT_DIR \
                + '\nN_PROC=' + str(self.N_PROC) \
                + '\nN_CMD=' + str(self.N_CMD) \
                + '\nN_REEXEC=' + str(self.N_REEXEC) \
                + '\nMAIL_FLAG=' + str(self.MAIL_FLAG) \
		        + '\nOUTPUT_FILE=' + str(self.OUTPUT_FILE)\
                + '\nOUTPUT_TYPE=' + str(self.OUTPUT_TYPE)

        # for i in self.cmds:
        #     string += "\n" + i

        return string


def call_proc(cmd, setup, execid, debug):
    global  lock
    """ This runs in a separate thread. """
    # subprocess.call(shlex.split(cmd))  # This will block until cmd finishes
    p = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()

    # Write ouput on the file
    # Critical section of code

    with lock:

        nameFile = setup.OUTPUT_DIR + "/"
        if setup.OUTPUT_TYPE:
            nameFile += setup.OUTPUT_FILE
        else:
            nameFile += cmd.split('/')[1].split()[0] + "." + cmd.split()[-1].split('/')[-1] + "." + setup.OUTPUT_FILE

        debug.print_commum("Processor (" + str(execid) + ")  writing file: " + nameFile)

        with open(nameFile, "a") as f:
            f.write("##{}##:\n{}\n {}\n err: {} \n\n###############\n".format(execid, cmd, out, err))

    return cmd, out, err


def start_experiments(setup, debug):
    os.chdir(setup.EXEC_DIR)

    if setup.N_PROC == 0: # use all processors
        setup.N_PROC = multiprocessing.cpu_count()

    debug.print_commum("Number of processors: " + str(setup.N_PROC))

    pool = ThreadPool(setup.N_PROC)


    results = []

    for cmd in setup.cmds:
        for i in range(setup.N_REEXEC):
            results.append(pool.apply_async(call_proc, (cmd, setup, i, debug)))

    # Close the pool and wait for each running task to complete
    pool.close()
    pool.join()

    # os.chdir(setup.OUTPUT_DIR)
    # with open(setup.OUTPUT_FILE, "w") as f:
    #     for result in results:
    #         cmd, out, err = result.get()
    #         f.write("cmd : {}\n out: {}\n err: {}\n\n\n".format(cmd, out, err))


def main():
    verbose, setup_file = read_args()
    setup = Setup(setup_file, verbose)
    debug = Debug(setup)

    debug.print_commum("### Setup ###")
    debug.print_commum(setup)
    debug.print_commum("\n\n")

    start_experiments(setup, debug)


if __name__ == '__main__':
    main()
