import re
import sys

def safe_filename(text, max_length=2048):
    """
    Sanitizes filenames for many operating systems.

    Keyword arguments:
    text -- The unsanitized pending filename.
    """
    #Quickly truncates long filenames.
    truncate = lambda text: text[:max_length].rsplit(' ', 0)[0]

    #Tidy up ugly formatted filenames.
    text = text.replace('_', ' ')
    text = text.replace(':', ' -')

    #NTFS forbids filenames containing characters in range 0-31 (0x00-0x1F)
    ntfs = [chr(i) for i in range(0, 31)]

    #Removing these SHOULD make most filename safe for a wide range
    #of operating systems.
    paranoid = ['\"', '\#', '\$', '\%', '\'', '\*', '\,', '\.', '\/', '\:',
                '\;', '\<', '\>', '\?', '\\', '\^', '\|', '\~', '\\\\']

    blacklist = re.compile('|'.join(ntfs + paranoid), re.UNICODE)
    filename = blacklist.sub('', text)
    return truncate(filename)
    
def update_progress(maxv,cur_progress):
    """
        This methode draw progres bar
    """
    progress = int((float(cur_progress)/float(maxv))*100)
    sys.stdout.write ( '\r{0}% [{1}] {2}KB'.format(progress,'#'*(progress),cur_progress/1024))
    sys.stdout.flush()
    
def normalized_url(url):
    """
        This methode change url ascii code character into real character
    """
    ret_url=""
    iter = 0;
    pass_two = 0
    for c in url:
        if pass_two == 0:
            if c== '%':
                if url[iter]=='u':
                    pass
                else:
                    val = url[(iter+1):(iter+3)]
                    ival = int(val,16)
                    asci = chr(ival)
                    ret_url+=asci
                    pass_two=2
            else:
                ret_url += c
        else:
            pass_two-=1
        iter+=1
    return ret_url

    
