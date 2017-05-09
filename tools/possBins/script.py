from binaryninja import *
import argparse

def get_callocs(filename):
	bv = BinaryViewType['ELF'].open(filename)
	assert(bv)
	bv.update_analysis_and_wait()

	allocs = []

	if "calloc" in bv.symbols.keys():
		sym = bv.symbols['calloc']
		for call in bv.get_code_refs(sym.address):
			allocs.append(call.address)

	return allocs

def patch_symbol(fin, fout, symbol):
	bv = BinaryViewType['ELF'].open(fin)
	assert(bv)
	bv.update_analysis_and_wait()
	count = 0
	if symbol in bv.symbols.keys():
		sym = bv.symbols[symbol]
		for call in bv.get_code_refs(sym.address):
			callLen = bv.get_instruction_length(call.address)
			bv.write(call.address, bv.arch.convert_to_nop("A"*callLen, 0))
			count += 1

	print "Patched %d calls to %s" % (count, symbol)
	bv.save(fout)

if __name__ == "__main__":
	p = argparse.ArgumentParser(description="Find which freebins are possible in a [ctf] binary")
	p.add_argument('filename', help="the file to proccess")

	args = p.parse_args()

	print "Loading %s in Binary Ninja" % args.filename

	print "Patching alarms"

	patch_symbol(args.filename, "mcore_bin", "alarm")
	patch_symbol("mcore_bin", "mcore_bin", "printf")
	patch_symbol("mcore_bin", "mcore_bin", "puts")
	patch_symbol("mcore_bin", "mcore_bin", "putchar")
	patch_symbol("mcore_bin", "mcore_bin", "fputs")
	patch_symbol("mcore_bin", "mcore_bin", "setbuf")

	callocs = get_callocs(args.filename)

	for calloc in callocs:
		print "python mcore_script.py mcore_bin %d" % (calloc)
