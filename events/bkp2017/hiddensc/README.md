Basically just a binary search. You're able to malloc some number of bytes, so we search down from 1<<64 until we get a success, free it, and keep walking down. after the script gets low enough, we can take the value printed out after restart and jump to it.

You add 0x11000 because of accounting for the malloc overhead stuff.
