import os, subprocess, shutil, traceback, sys#, paramiko
from stat import *
from os.path import join as pjoin


import socket

def checkIP(addr):
    '''
        IP verification
        
        @return True/False
    '''

    try:
        socket.inet_aton(addr)
        print "T"
        return True
    except socket.error:
        print "F"
        return False

def printLastExceptionStackTrace():
    """
    Prints to stdout stack trace of the last exception occurred in the system. It is very useful to call this method on script failure.
    There is a strict rule: util.printLastExceptionStackTrace() should be called only from except blocks or from the points where it is 100% confidence
    that there was some exception before.
    """
    print >> sys.stderr, "\n" + traceback.format_exc() + "\n"
    sys.stderr.flush()


def checkExists(file_or_fold):
    """
    Check that file or folder exists

    @param file_or_fold: path to file or folder
    """
    if not os.path.exists(file_or_fold):
        raise Exception("Couldn't find this file or folder '%s'" % file_or_fold)


def execute(cmd, cd = None, safe = True, print_output = True, env = None):
    """
    Execute command in OS

    @param cmd: command line
    @param cd (optional): change directory to "cd" before executing the "cmd". Return back at the end of the function.
    @param safe (optional): raise Exception if exception occured
    @param print_output (optional): print stdout and err from program in standard stdout
    @param env(optional): passed to subprocess.Popen

    @return (stdout, stderr) 
    """
    program_name = cmd.split()[0].split(os.sep)[-1]
    if print_output:
        print '--- executing %s [%s] ---' % (program_name, cmd)

    out = []
    err = []

    if cd:
        curdir = os.curdir
        os.chdir(cd)

    e = None
    rc = None
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell = True, env = env)

        outReadLine = proc.stdout.readline
        while True:
            l = outReadLine()
            if l:
                out.append(l.strip())
                if print_output:
                    print l.strip()
            else:
                break

        errReadLine = proc.stderr.readline
        while True:
            l = errReadLine()
            if l:
                err.append(l.strip())
                if print_output:
                    print l.strip()
            else:
                break

        rc = proc.wait()
        if rc != 0:
            print >> sys.stderr, "Return code of [%s] is not 0, but %d" % (cmd, rc)

    except Exception, e:
        printLastExceptionStackTrace()
        if not safe:
            raise
    finally:
        if cd:
            os.chdir(curdir)

        if (err or e or rc) and not safe:
            if err:
                raise Exception(err)
            elif e:
                raise e
            else:
                raise Exception("Return code of [%s] is not 0, but %d" % (cmd, rc))
        return out, err


def p4Sync(folder, force = True):
    """
    Sync code with p4

    @param folder: full path to folder (accept any format that p4 accept)
    @param force (optional): to force sync or not

    @return (stdout, stderr) 
    """
    out, err = execute("p4 sync%s %s%s..." % (' -f' if force else '', folder, '/' if not folder.endswith('/') else ''), safe = True)
    if err:
        exc = [l.strip() for l in err if l.strip().rfind('file(s) up-to-date') == -1]
        if exc:
            raise Exception(exc)
    return out, err


def grantAllPermissions(file):
    """
    Make file available for all operations for anyone. Same as "chmod 777" on *nix systems
    
    @param file: path to file
    """
    os.chmod(file, S_IXUSR + S_IXGRP + S_IXOTH + S_IWUSR + S_IWOTH + S_IWGRP + S_IRUSR + S_IRGRP + S_IROTH)


def cp(src, dst):
    """
    Copy files and folders

    @param src: source
    @param dst: destination

    @return: list of copied files
    """
    copied_files = []
    if os.path.isdir(src):
        if not os.path.exists(dst):
            os.makedirs(dst)
        for name in os.listdir(src):
            copied_files += cp(pjoin(src, name), pjoin(dst, name))
    else:
        if not os.path.exists(dst): 
            d = os.path.dirname(dst)
            if not os.path.exists(d):
                os.makedirs(d)
        else:
            grantAllPermissions(dst)
        print 'copy %s -> %s' % (src, dst)
        shutil.copy2(src, dst)
        grantAllPermissions(dst)
        copied_files.append(dst)
    shutil.copystat(src, dst)
    return copied_files


def checkFolderContent(folder, list_of_files):
    """
    Check that folder consist only files from passed list

    @param folder: folder to check in
    @param list_of_files: list of files to check

    @return: list of unexpected files
    """
    wrong_files = []
    for path, dirs, files in os.walk(folder):
        if path[0].islower():
            path = path[0].upper() + path[1:]
        for _file in files:
            f = pjoin(path, _file)
            if not f in list_of_files:
                wrong_files.append(f)
    return wrong_files


def removePythonCompiledFiles(folder):
    """
    Remove python compiled files in folder

    @param folder: path to folder
    """
    print "cleaning %s" % (folder,)
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(('.pyc', '.pyo')):
                f = os.path.abspath(root + os.sep + file)
                os.remove(f)
                print "Cleaned: %s" % f
    print 'done'


def runSshCommand(host, username, password, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command(command)
    except Exception, e:
        raise Exception, "Command '%s' on remote server '%s' FAILED: %s" % (command, host, e)
    finally:
        errors = stderr.readlines()
        output = stdout.readlines()
        ssh.close()
        if errors:
            print "Error occured: %s" % errors
        if output:
            return output


if __name__ == '__main__':
    try:
        print checkExists('c:\windows')
    except Exception, e:
        print e
    try:
        print checkExists('/home/five9inf')
    except Exception, e:
        print e

    try:
        p4Sync('//tools/automation/automation_tools/prepare_setup/log/')
    except Exception, e:
        print e
    try:
        p4Sync('asdadsas')
    except Exception, e:
        print e

    print execute('cd')
    








