import argparse
import shamir_secret_sharing
from Crypto.Util import number

#To make it simple, we give the f(X)=5+3x+8x^2 as params. It is easy to do
# the test and write the code.


p = int(
    "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF",
    16)
g = 2
h = int(
    "3d941d6d9cd4c77719840d6b391a63ca6ded5b5cf6aafeefb9ea530f523039e9c372736a79b7eb022e50029f7f2cb4fb16fd1def75657288eca90d2c880f306be76fe0341b3c8961ae6e61aabbb60e416069d97eeada2f1408f2017449dddcd5ac927f164b1a379727941bd7f2170d02ef12ef3ec801fae585ac7b9d4079f50feced64687128208d46e3e10c5d78eb05832f5322c07a3b4e14c6f595206fde99115e8eea19b5fb13dd434332ec3eccb41a4baa54a14183c3416313678697db8507abdcfc6a97c86099fa5172316d784c6997fc2e74e8e59c7c1bc90426164682f5bfbf6373b13ea90d7e13fbffd65e10c4ad96c38ccbf8e8def28d76746729dc",
    16)


def create_verifies(params, p, g):
    verifies = []
    for each in params:
        verifies.append(pow(g, each, p))
    return verifies


def verify_each(i, verifies, len_pamras):
    left_value = 1
    for j in range(0, len_pamras):
        upper = pow(i, j, p)
        left_value *= pow(verifies[j], upper, p)


def calculate_left(verfies, i, t, p, g):
    powerall = [1]
    for each_t in range(1, t):
        powerall.append(pow(i, each_t))
    left_val = 1
    for j in range(0, len(verfies)):
        c = pow(verfies[j], powerall[j], p)
        left_val *= c
        left_val %= p
    return left_val % p


def verifies_shares(secrets, verifies, params,p,g):
    for i in range(0, len(secrets)):
        left_value = calculate_left(verifies, i+1, len(params), p,g)
        right_value = pow(g, (secrets[i])%p, p)
        if left_value == right_value:
            print "checking %d Successfully!!" % i
        else:
            print "secret  %d has been modified!!" % i



def test_prime():


    n_length = 2048


    q= (p-1)%2
    print q
    print number.isPrime((p-1)/2)

    primeNum1 = number.getPrime(n_length)
    # primeNum2 = number.getStrongPrime(n_length, primeNum1)
    i=2
    while True:
        pl = p-1
        print i
        if pl%i == 0:
            if number.isPrime(pl / i):
                print "############"
                print i
                print "############"
                break

        i += 1
        if i==10000:
            break
    print "found!!"

    print "############################"
    print primeNum1
    print "############################"


def main(args):

    parties = 7
    min_party = 3
    params = [5, 3, 8]
    secrets = shamir_secret_sharing.create_secret(parties, params, p)

    secret = shamir_secret_sharing.construct_secret(secrets, min_party, p)
    verifies = create_verifies(params, p, g)
    verifies_shares(secrets, verifies, params, p, g)
    print "The secret you give is " + str(params[0]) + "\n"

    print "The rejoin code is " + str(secret)
    if params[0] == secret:
        print "rejoin Successfully!!"
    else:
        print "done"
        # print "we cannot rejoin the secret"


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
