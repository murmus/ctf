from manticore import Manticore
import argparse

fastbins = []

def mcore_calloc(filename, call, seed = None):

	#FASTBINS 

        m = Manticore(filename)
	if seed:
		m.concrete_data = seed

        @m.hook(0x555555554000+call)
        def fastbin_hook(state):
                cpu = state.cpu
                state.add(cpu.RDI * cpu.RSI <= 0x80)

                rdi = state.solve_one(cpu.read_register("RDI"))
                rsi = state.solve_one(cpu.read_register("RSI"))

                print "Fastbin with calloc(%d, %d)" % (rdi, rsi)
                fastbins.append(call)
                m.terminate()

	#m.verbosity = 2
	m.workers = 8
        m.run()


	#SMALL BINS

        m = Manticore(filename)
	if seed:
		m.concrete_data = seed

        @m.hook(0x555555554000+call)
        def fastbin_hook(state):
                cpu = state.cpu
                state.add(cpu.RSI >= 0x80)
                state.add(cpu.RSI <= 0x400)

                rdi = state.solve_one(cpu.read_register("RDI"))
                rsi = state.solve_one(cpu.read_register("RSI"))

                print "Smallbins with calloc(%d, %d)" % (rdi, rsi)
                fastbins.append(call)
                m.terminate()

	m.verbosity = 2
	m.workers = 8
        m.run()

	exit(1)

	#LARGE BINS
        m = Manticore(filename)
	if seed:
		m.concrete_data = seed

        @m.hook(0x555555554000+call)
        def fastbin_hook(state):
                cpu = state.cpu
                state.add(cpu.RSI >= 0x400)
                state.add(cpu.RSI <= 0x4000)

                rdi = state.solve_one(cpu.read_register("RDI"))
                rsi = state.solve_one(cpu.read_register("RSI"))

                print "Largebins with calloc(%d, %d)" % (rdi, rsi)
                fastbins.append(call)
                m.terminate()

	#m.verbosity = 2
	m.workers = 8
        m.run()

	#LARGE BINS
        m = Manticore(filename)
	if seed:
		m.concrete_data = seed

        @m.hook(0x555555554000+call)
        def fastbin_hook(state):
                cpu = state.cpu
                state.add(cpu.RDI * cpu.RSI >= 0x400)
                state.add(cpu.RDI * cpu.RSI <= 0x4000)

                rdi = state.solve_one(cpu.read_register("RDI"))
                rsi = state.solve_one(cpu.read_register("RSI"))

                print "MMAPbins with calloc(%d, %d)" % (rdi, rsi)
                fastbins.append(call)
                m.terminate()

	#m.verbosity = 2
	m.workers = 8
        m.run()

if __name__ == "__main__":
	p = argparse.ArgumentParser(description="Find which freebins are possible in a [ctf] binary")
        p.add_argument('filename', help="the file to proccess")
	p.add_argument("calloc", type=int, help="address of calloc")
	p.add_argument("seedfile", default=None, help="seed file for stdin")

        args = p.parse_args()

	if args.seedfile:
		print "Seeding with %s" % (args.seedfile)
		mcore_calloc(args.filename, args.calloc, open(args.seedfile).read())
	else:
		mcore_calloc(args.filename, args.calloc)
