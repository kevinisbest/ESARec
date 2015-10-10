import sys

def PassTransferListToString(ll):
	string = ""
	for i in ll:
		string += str(i)
		string += ","
	return string

def PassTransferStringToList(ss):
	ll = []
	curr = 0
	prev = 0
	for i in ss:
		if i == ',':
			sub = ss[prev:curr]
			ll.append(sub)
			prev = curr+1
		curr += 1
	return ll
	
	

ll = ['h', 'i', 12.345]
string = PassTransferListToString(ll)
print string
lll = PassTransferStringToList(string)
print lll



#print lll
