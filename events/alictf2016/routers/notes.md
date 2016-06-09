RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      FILE
[32mFull RELRO   [m   [32mCanary found   [m   [32mNX enabled [m   [32mPIE enabled  [m   [32mNo RPATH [m  [32mNo RUNPATH [m  routers

Two object types, routers and terminals. Can abuse linking of routers together to be able to both get arbitrary reads and a null byte write into heap structures.

Got as far as reading arbitrary memory, didn't have time to turn the write into code xecution.
