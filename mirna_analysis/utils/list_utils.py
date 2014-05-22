'''
@jyeung
May 21 2014
'''

def list_to_csv(mylist, sep=','):
    '''
    Given a list, return a CSV string
    '''
    mylist = [str(i) for i in mylist]
    return sep.join(mylist)
