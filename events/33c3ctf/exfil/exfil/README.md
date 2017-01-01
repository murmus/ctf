See test.py.

Basically:
	* PCAP is a bunch of DNS requests, base32 encoded, with responses.
	* We go through it using dpkt, decode them, and try to rebuild the gpg and "secret.docx" file that is contained.

The script doesn't work 100% on it's own, you'll have to manually clean up gpg.dmp, but otherwise should just about work fine.
