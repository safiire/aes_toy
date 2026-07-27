
## Toy Version of AES-128

I've been doing a lot of Crypto Challenges on Hack The Box recently. The bulk of the challenges are discovering and exploiting the various ways you can screw up writing your own RSA encryption.

But what about AES?  There's sort of fewer AES challenges on there, and most of them are about how you can screw up the different modes of AES, which doesn't exactly teach you how the normal AES block cipher works.

So long story short, I got obsessed with Galois fields, and reimplemented AES in Python.

Actually I reimplemented it twice, the first time I wrote all the Galois GF(2^8) code myself, and did the optimizations, and the second time (this code) I just used Python's galois package.  For no real reason, I also used galois/numpy to represent every operation as matrix and vector math, because linear algebra is cool.

This is funny (to me anyways) because the Galois field with 2^8 elements was definately chosen due to all the optimizations you can get on a computer with 8-bit bytes, which I pretty much removed every aspect of by doing it that way.

This works out great, because nobody should use this program for anything except learning how AES works, and nobody ever will because it is the slowest running program ever.


## Running

Install galois from `requirements.txt`.

To encrypt a file run `./encrypt <mode> <password> <in_file> <out_file>`
To decrypt a file run `./decrypt <password> <in_file> <out_file>`

Rather than provide an 128-bit key, you can provide whatever length password, and it will use PBKDF2 to generate the correct sized key.

For modes I threw in ECB and CBC

Encrypting creates a JSON file with the PBKDF2 salt and IV for CBC, along with the ciphertext, all base64 encoded.

Decrypting takes such a JSON file and a password.
