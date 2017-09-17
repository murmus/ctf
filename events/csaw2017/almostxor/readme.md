Uh...
So, to decrypt you change encrypt from adding to subtracting.

To get the flag, I assumed the plaintext was `flag{`, and try to decrypt the stream that way with every possible bitlen. Then, I took the first 6 bytes of that output and plugged it back in as a key.

Turns out, with bitlen 3, that was pretty close to a flag. So I just brute forced the last byte of that.
