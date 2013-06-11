import time, os, sys
from wlib import *
from config import *

_host=None

if len(sys.argv)>1:
    _host = sys.argv[1]
else:
    _host = host

_content='wellcome\n'


def main():
    
    '''
        Testing Wellcome host
        Author: GL
        
        @return: 
            0 - test passed
            1 - ip address of host not valid
            2 - can not get page content by ip
            3 - can not get page content without proxy
            4 - wrong content


    '''
    result = 0
    verdict = 'PASSED'
    
    try:
        print "Test Started"
        print "Testing host: %s" %_host
        
        if not checkIP(_host):
            verdict = "Entered wrong ip address."
            result = 1
            raise Exception(verdict)

        page = getPage(_host)
        if page is None:
            verdict = "Can not receive browser content."
            result = 2
            raise Exception(verdict)
        else:
            print "Page content:\n-----\n%s\n-----" % page

        page = getPageWithoutProxy(_host)
        if page is None :
            verdict = "Can not receive browser content without proxy."
            result = 3
            raise Exception(verdict)
        else:
            print "Page content:\n-----\n%s\n-----" % page

        if page != _content:
            verdict = "Wrong page contant."
            result=4
            raise Exception(verdict)
                
 
    except Exception, e:
        print e
    finally:
        if verdict!='PASSED': verdict="FAILED. " + verdict
        print "Test Finished with result: %s" % verdict
    
    return result

if __name__ == '__main__':
    main()

# EOF


