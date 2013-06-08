import time, os, sys
from test_lib import *


_host=None

if len(sys.argv)>1:
    _host = sys.argv[1]
else:
    _host = '127.0.0.1'


def main():
    
    '''
        Testing Wellcome host
        Author: GL
        
        @return: 0 or 1
    '''
    result = 0
    
    try:
        print "Test Started"
        print "Testing host: %s" %_host
        
        if not checkIP(_host):
            print "Entered wrong ip address"
            raise
        
        
    #print execute('ls')
    
    
    except Exception, e:
        printLastExceptionStackTrace()
    finally:
        print "Test Finished"
    
    return None

if __name__ == '__main__':
    main()

# EOF


