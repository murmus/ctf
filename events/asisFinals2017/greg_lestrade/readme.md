Simple printf vuln.

Note I started writing a writedword function, but stopped. Since I only need to write one qword, I optimized it to write in the order of the smallest halfwords.

Using the halfword trick, normally you would write a halfword at a time, using the rollover to give you the values you want. Since I'm only doing the one, though, I just sorted it by order.

I then just remap strlen->system and call that.
