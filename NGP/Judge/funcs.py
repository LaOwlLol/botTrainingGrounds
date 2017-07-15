

def pfft(n):
	return ( (n/47.0)+((n/46.0)*(1-(n/47.0))) )

def pfsd(n, p):
	return ( (n/(47.0-(2*(p-1))))+((n/(46.0-(2*(p-1))))*(1-(n/(47.0-(2*(p-1)))))) )

def ptsd(n, p):
	return (n/(46.0-(2*(p-1))))

def ptft(n):
	return (n/46.0)

def pftt(n, d):
	return (n/47.0) * ((n-t)/46.0)

