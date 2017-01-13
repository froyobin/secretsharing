# from __future__ import division
import argparse
import random
import math
import decimal

p = int(
    "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF",
    16)
g = 2
h = int(
    "3d941d6d9cd4c77719840d6b391a63ca6ded5b5cf6aafeefb9ea530f523039e9c372736a79b7eb022e50029f7f2cb4fb16fd1def75657288eca90d2c880f306be76fe0341b3c8961ae6e61aabbb60e416069d97eeada2f1408f2017449dddcd5ac927f164b1a379727941bd7f2170d02ef12ef3ec801fae585ac7b9d4079f50feced64687128208d46e3e10c5d78eb05832f5322c07a3b4e14c6f595206fde99115e8eea19b5fb13dd434332ec3eccb41a4baa54a14183c3416313678697db8507abdcfc6a97c86099fa5172316d784c6997fc2e74e8e59c7c1bc90426164682f5bfbf6373b13ea90d7e13fbffd65e10c4ad96c38ccbf8e8def28d76746729dc",
    16)


def encode(n):
    x = ord(n)
    if x > 32 and x < 127:
        return x - 33
    else:
        print("we can only handle ASCII")
        return -1


def genRand(m):
    return random.SystemRandom().randint(0, m)


def StringtoInt(s):
    n = len(s)
    f = 0
    for i in range(n):
        # create integer from base 94 string (characters)
        f += encode(s[i]) * (94 ** (n - i - 1))
    return f


def create_params(s, min_party):
    params = [s]

    for i in range(0, min_party):
        params.append(genRand(p))
    return params


def create_secret(s, parties, params):
    secrets = []
    for i in range(1, parties + 1):
        secret = params[0]
        for j in range(1, len(params) - 1):
            secret += (params[j] * (pow(i, j, p))) % p
        secrets.append(secret % p)
    return secrets


# Gives the decomposition of the gcd of a and b.  Returns [x,y,z]
#  such that x = gcd(a,b) and y*a + z*b = x

def gcdD(a, b):

    if (b == 0):
        return [a, 1, 0]
    else:
        n = math.floor(a / b)
        c = a % b
        r = gcdD(b, c)
    return [r[0], r[2], r[1] - r[2] * n]

#As we have choose the prime number to do the modInverse, so we donot need to
#  calculate the gcd. just pow(a,p-2,p)
# Gives the multiplicative inverse of k mod prime.
# In other words (k * modInverse(k)) % prime = 1 for all prime > k >= 1
def  modInverse(k):
    k = k % p
    if k<0:
        r = -gcdD(p, k)[2]
    else:
        r = gcdD(p, k)[2]
    return (p + r) % p

def modInversePrime(k):
    return pow(k, p-2,p)


def construct_secret(secrets, min_party):
    # we choose 1,3,4,5,6 to recover the secret
    # we hard code here to use 3,4,5 to construct the secret
    secret_pos = [3, 4, 5]
    multi_all = 1
    for i in range(0, min_party):
        multi_all *= secret_pos[i]
        if len(secret_pos) % 2 == 0:
            multi_all *= -1
    ret = 0
    for i in range(0, min_party):
        lower = 1
        upper = multi_all / secret_pos[i]
        for j in range(0, min_party):
            if j == i:
                continue
            else:
                lower *= ((secret_pos[i] - secret_pos[j]) % p)
                lower %= p
        ret = ((upper * modInversePrime(lower) * secrets[secret_pos[
                                                          i]-1])+p+ret) %p
    return ret


def main(args):
    s = StringtoInt(args.secret)
    parties = int(args.party)+1
    min_party = int(args.min_party)
    params = create_params(s, min_party)
    secrets = create_secret(s, parties, params)

    secret = construct_secret(secrets, min_party)
    print "The secret you give is "+ str(params[0])+"\n"
    print "The part-secrets send to client are:"
    for each in secrets[1:]:
        print each

    print "\n\n"
    print "The rejoin code is "+ str(secret)
    if params[0] == secret:
        print "rejoin Successfully!!"
    else:
        print "we cannot rejoin the secret"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create secret shares')
    parser.add_argument('secret', metavar='\"secret\"', type=str,
                        help='the secret to share')
    parser.add_argument('party', metavar='\"secret\"', type=str,
                        help='the secret to share')
    parser.add_argument('min_party', metavar='\"secret\"', type=str,
                        help='the secret to share')
    args = parser.parse_args()
    main(args)
