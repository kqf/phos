#!/usr/bin/python


import json

#Cell and
def cand(aa, bb): return [c for c in aa if c in bb]


#Cell not
def nand(aa, bb): return [c for c in aa if not c in bb]

def main():
	with open('summary.json', 'r') as f: data = json.load(f)
	print data.keys()

	noisy_channels = nand(data['excluded5times'], data['excluded10times'])
	print len(noisy_channels), ' fitA', len(data['fitA']), ' fitB', len(data['fitB']), ' chi', len(data['chi'])

	a = cand(noisy_channels, data['fitA'])
	b = cand(noisy_channels, data['fitB'])
	c = cand(noisy_channels, data['chi'])
	l = cand(noisy_channels, data['eLow'])
	h = cand(noisy_channels, data['eHig'])
	nl = cand(noisy_channels, data['nLow'])
	nh = cand(noisy_channels, data['nHig'])



	print ', '.join(map(str,sorted(noisy_channels)))

	print len(a)
	print len(b)
	print len(c)
	print len(l)
	print len(h)
	print len(nl)
	print len(nh)


	print cand(l, h)

	print sorted(set(a + b + c + l + h + nh))

if __name__ == '__main__':
	main()