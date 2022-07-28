import difflib

cases=[('111aaa123', '111aaa130'),
       ('aaa111bbb', 'aaa156bbb'),
       ('123456', '123466'),
       ('1234abc', '1345abc')] 

for a,b in cases:     
    print('{} => {}'.format(a,b))  
    for i,s in enumerate(difflib.ndiff(a, b)):
        if s[0]==' ': continue
        elif s[0]=='-':
            print(u'Delete "{}" from position {}'.format(s[-1],i))
        elif s[0]=='+':
            print(u'Add "{}" to position {}'.format(s[-1],i))    
    print() 