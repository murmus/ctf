a = "\xd6\xc9\xc2\xce\x47\xde\xda\x70\x85\xb4\xd2\x9e\x4b\x62\x1e\xc3\x7f\x37\x7c\xc8\x4f\xec\xf2\x45\x18\x61\x17\x1a\x29\x11\xc7\x75\x02\x48\x26\x93\x83\x8a\x42\x79\x81\x10\x50\x44\xc4\x6d\x84\xa0\xb1\x72\x96\x76\xad\x23\xb0\x2f\xb2\xa7\x35\x57\x5e\x92\x07\xc0\xbc\x36\x99\xaf\xae\xdb\xef\x15\xe7\x8e\x63\x06\x9c\x56\x9a\x31\xe6\x64\xb5\x58\x95\x49\x04\xee\xdf\x7e\x0b\x8c\xff\xf9\xed\x7a\x65\x5a\x1f\x4e\xf6\xf8\x86\x30\xf0\x4c\xb7\xca\xe5\x89\x2a\x1d\xe4\x16\xf5\x3a\x27\x28\x8d\x40\x09\x03\x6f\x94\xa5\x4a\x46\x67\x78\xb9\xa6\x59\xea\x22\xf1\xa2\x71\x12\xcb\x88\xd1\xe8\xac\xc6\xd5\x34\xfa\x69\x97\x9f\x25\x3d\xf3\x5b\x0d\xa1\x6b\xeb\xbe\x6e\x55\x87\x8f\xbf\xfc\xb3\x91\xe9\x77\x66\x19\xd7\x24\x20\x51\xcc\x52\x7d\x82\xd8\x38\x60\xfb\x1c\xd9\xe3\x41\x5f\xd0\xcf\x1b\xbd\x0f\xcd\x90\x9b\xa9\x13\x01\x73\x5d\x68\xc1\xaa\xfe\x08\x3e\x3f\xc5\x8b\x00\xd3\xfd\xb6\x43\xbb\xd4\x80\xe2\x0c\x33\x74\xa8\x2b\x54\x4d\x2d\xa4\xdc\x6c\x3b\x21\x2e\xab\x32\x5c\x7b\xe0\x9d\x6a\x39\x14\x3c\xb8\x0a\x53\xf7\xdd\xf4\x2c\x98\xba\x05\xe1\x0e\xa3"

b = "95eeaf95ef94234999582f722f492f72b19a7aaf72e6e776b57aee722fe77ab5ad9aaeb156729676ae7a236d99b1df4a"

o = ""
while b:
	t = int(b[:2], 16)
	b = b[2:]

	o += chr(a.index(chr(t)))

print o
