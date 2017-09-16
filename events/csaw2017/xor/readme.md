So, it's a lot easier to show than explain
but I assumed the flag{ had to start either the key or plaintext
and since that gave me A qua as the start of the ciphertext, I shifted that through the md5 to see if either could be xor'd with the md5
only A q could be, as the last 3 bytes of it
which meant that the key had to be 67 bytes long, making the plaintext 38 bytes(edited)

from there, it's a matter of assuming A qua is the start of the key, which means xor(buf[38:], "A qua") would give me more of the key
