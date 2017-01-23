# Cantorize
Using Cantor pairing function on a set of ciphertexts as an approximation to deniable encryption

---

## What does it do?

The output of standard encyption algorithms like AES have the problem of being susceptible to ** Rubber-hose attack: ** i.e There's no mechanism in place to avoid release of the encrypted material in case of being pressured to reveal the key.

Here, we encrypt two messages (main message and a dummy message) using the standard AES-128 and then encode the resulting ciphertexts into a single string which responds to different passes differently.

## How does it work?

Without loss of generality assume we want to encrypt a plaintext(s). We use standard encryption algorithms like AES (here we used AES-128 CBC mode) to encrypt that text. We encrypt another dummy text as well. Then, we assume the ciphertext is a number in base 256. We change the basis to something larger than 10 but small enough for us to assign alphabets. Here we hexlified those ciphertexts. Now we change them to base 10.

We assume one of the ciphertext is a numerator of a fraction and another ciphertext is the denominator of that fraction. Since both ciphertexts would be integers, the resulting fraction is rational. Since rationals are countably infinite, there exists a bijective map from rationals to natural numbers.

We use such a map, called "Cantor's pairing function". The output of that function, is just a single natural number. We change the base back to 256 and consider it as the ciphertext which is to be transmitted.

To reverse the process, one would evaluate the inverse of Cantor's function by feeding the newly created ciphertext to it. The output is two ciphertexts. If one uses the first password, the second ciphertext won't get deciphered and vice versa.

## Caveats

The double precision floating point backend of Python's Long type which is used for handling of arbitrary large integers will be inaccurate for the outputs of functions whose codomain are the floats for sufficiently large inputs. To do that, we've defined the (de)pairing function in Mathematica and connected the two together.

## Dependencies

1. Python 2.7 (with PyCrypto)
2. Mathematica

## Usage

0. Make sure you have Mathematica installed, as well as Python!
1. Clone the repo and give executable permission to the contents of `Cantorize/src`. i.e. `chmod +x *`
2. To encrypt a message: `src/cantorize --encrypt -m1 FIRST_MESSAGE -p1 FIRST_PASSWORD -m2 SECOND_MESSAGE -p2 SECOND_PASSWORD`.
3. To decrypt the a message, get the output of (2) and: `src/cantorize --decrypt -m0 OUTPUT_OF_TWO -p0 A_PASSWORD`. If you enter any of the two passwords, you'd get the relevant unencrypted text.


## Possible further features

1. The encryption implementation should not be used. It has hard coded salts and ivs etc. and it is just meant to be a showcase. Making it actually usable might be a good idea!
2. The ciphertexts are represented in base 10. This makes them longer. Converting them back to base 256 or alike may be a good idea.
3. The ciphertexts are being passed through terminal. There's a limitation on the number of characters that can be passed this way. Reading and writing to files on disk should be preferred since it removes that limitation.


## Disclaimer

This is a project I submitted to [PennApps XV]("https://devpost.com/software/deniable-cantor"). I spent almost all of the time dealing with Racket for my initial project, but, it wouldn't have been completed on time. This thing was made in less three hours, which means it can be more polished!
