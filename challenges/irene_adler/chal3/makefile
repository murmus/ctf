CC=gcc

LUALIB=-I../lua-5.3.4/src -L../lua-5.3.4/src
OUTPUT=-o chal3

chal3: chal3.c
	$(CC) $(LUALIB) chal3.c -llua -lm -ldl $(OUTPUT)
