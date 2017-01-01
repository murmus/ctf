```
[*] '/home/sam/ctf/events/33c3ctf/babyfengshui/babyfengshui'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE
```

Pretty classic pwnable style: You have user objects you can add, remove, update, and display. Each user has both a name and description, and the struct looks like:

```
struct __attribute__((aligned(4))) user
{
  char *desc;
  BYTE name[124];
};
```

The interesting part is the "l33t defenses" to make sure you don't overflow the desc field. When updating a user, you send a length of the field, then it checks to make sure there is room in the description for that many bytes.

Because of how the allocations are done, if no users are removed the code works right. They check to make sure the last byte you would write into description has a lower address than the first byte of the user struct.

The short version of the exploit here:

* Create 2 users, plus a third user with name and description of `/bin/sh` for triggering our exploit.
* Remove the first user.
* Create a new users with a long description.
  * We use a length of 120 bytes for the description, which makes it take up most of the space left from the freed user.
  * We're then able to put a ton of bytes into the description field, since the user struct ends up way at the end of the heap.
  * In this case, we are going to bash the description pointer in the following object to point into the record for free in the got.

* Pull out the current value in the got, use pwntools to calculate our slide
* Update the users[1] description to write a new pointer into the got
* Free our users[2] object to pop a shell
