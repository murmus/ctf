This exploit is super rough. It worked locally, but remote I couldn't get the buffering working right.

The short explanation: there is a bug in swappnig items/pokemon moves. You set up a swap by picking an item, which sets the swap_idx global variable, and then use the tm01 item. After giving strength to pokemon, you then drop into the pokemon context menu without setting the swap_idx global variable back to -1.

I then swap an attack with the pokemon's name, and which has been set up to leak out a got entry when printing out the attack name. The attack function is set to be a call to get_bytes, which reads in new data into the struct.

We use that once, replace the data with "/bin/sh;#" + stuff + system(), and pop a shell.

As you can see, I kind of expected everything to just work. When I tried to throw it, with network latency, I almost always ended up +/- coordinate off where I expected to be. The technique is sound, my game botting just wasn't stronk enough to actually land on the game boxes.
