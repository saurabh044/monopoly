def p(inp):
    print inp
    mx = max(inp)
    y = [True if i == mx and mx != 0 else False for i in inp]
    print y
    
    
p([1,0,0,0])
p([2,1,1,1])
p([0,1,1,1])
p([0,0,0,0])