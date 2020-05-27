"""
SEE312, Deakin Uni, Kirill Duplyakin
___________

Calculate CRC encoding using bitwise operations for arbitrary binary message and key

"""

D = int('10011011011', base=2) # message int
P = int('11101', base=2) # predetermined divider int, x^4+x^3+x^2+0^1+x^0
E1 = int('010010000000000', base=2) # error pattern from b.
E2 = int('111010000000000', base=2) # error pattern from c.

def crc_encode(D, P):
    k = D.bit_length(); p_len = P.bit_length()
    n = p_len - 1 + k
    r = D << (n-k) # shifted D
    
    for i in range(k):
        # 111000 11 00000 XOR
        # 110011 00 00000 shifted P
        if not r >> (n-(i+1)): continue # should be 1 or 0, skip on 0
        curr_div = P << ((n-p_len)-i)
        r = r ^ curr_div
        if r == 0: break
    return ((D << (n-k)) + r, r) # (T encoded frame, F remainder)

def crc_check(T, P):
    n = T.bit_length(); p_len = P.bit_length()
    k = n - (p_len-1)
    
    for i in range(k):
        if not T >> (n-(i+1)): continue # should be 1 or 0, skip on 0
        curr_div = P << ((n-p_len)-i)
        T = T ^ curr_div
        if T == 0: break
    return (T == 0, T) # (check, F remainder)

T, F = crc_encode(D, P)
print(f"")
TE1 = T ^ E1
TE2 = T ^ E2
print(crc_check(TE1, P))
print(crc_check(TE2, P))
