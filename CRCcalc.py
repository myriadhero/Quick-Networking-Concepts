"""
Calculate CRC encoding using bitwise operations for arbitrary message and key

To optimise:
1. No need to shift data or return multiple outputs when checking instead of calculating
2. Getting lengths and for loop feel not quite pythonic...
"""

D = int('1010001101', base=2) # message int
P = int('110101', base=2) # predetermined key int

def CRCremainder(D, P):
    k = len(bin(D)[2:])
    p_len = len(bin(P)[2:])
    n = p_len - 1 + k
    r = D << (n-k) # shifted D
    
    for i in range(k):
        # 111000 11 00000 XOR
        # 110011 00 00000 shifted P
        if not r >> (n-(i+1)): continue # should be 1 or 0, skip on 0
        curr_div = P << ((n-p_len)-i)
        r = r ^ curr_div
        if r == 0: break
    return (r, (D << (n-k)) + r)
    
F, T = CRCremainder(D,P)
print(f"{bin(T)[2:]:>{n}}")
check,_ = CRCremainder(T,P)
print(check == 0)
