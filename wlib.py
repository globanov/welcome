import urllib


def checkIP(addr):
    '''
        IP verification
        @param addr: ip address to check
        @return True/False
    '''
    
    parts = addr.split(".")
    if not len(parts) == 4:
        return False
    for part in parts:
        try:
            number = int(part)
        except ValueError:
            return False
        if number > 255:
            return False
    return True

def getPage(addr):
    '''
        Get page content
        @param addr: ip address of host
        @return content of browser or None in case of exception
    '''

    try:
        return urllib.urlopen('http://%s'%addr).read()
    except Exception, e:
        return None

def getPageWithoutProxy(addr):
    '''
        Get page content directly without proxy
        @param addr: ip address of host
        @return content of browser or None in case of exception
        '''
    
    try:
        opener = urllib.FancyURLopener({})
        return opener.open('http://%s'%addr).read()
    except Exception, e:
        return None


if __name__ == '__main__':
    pass
    








