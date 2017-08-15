import pickle, numpy, sys

with open(sys.argv[1], "rb") as pf:
	pd = pickle.load(pf)
	
	numpy.savetxt("comments_window_v.gz", pd)