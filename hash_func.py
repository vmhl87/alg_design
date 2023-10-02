import random
import string

alg=0
ln=100

def hash_string(str):
	if alg==0: return hash_0(str)
	if alg==1: return hash_1(str)
	if alg==2: return hash_2(str)
	return hash_0(str)

def hash_2(str):
	opt,max,cur=1,len(str),1
	for i in range(7):
		if cur*(len(str)-i)>max:
			max=cur*(len(str)-i)
			opt=i
		cur*=2
		# max = pow(2,i)*(len(str)-i)
	out,bin=[],[]
	for i in range(7):out.append(0)
	for i in range(opt):bin.append(0)
	cur=0
	for c in str:
		bin[0]+=1
		a=0
		while a<opt and bin[a]>1:
			bin[a]=0
			a+=1
			if a<opt:bin[a]+=1
		for i in range(opt):
			if bin[i]:out[i]+=ord(c)-ord('a')
		out[opt+cur%(7-opt)]+=ord(c)-ord('a')
		cur+=1
	ret=0
	for i in range(7):ret=10*ret+out[i]%10
	return ret

def hash_1(str):
	ret=0
	for c in str:ret+=ord(c)-ord('a')
	return ret%10000000

def hash_0(str):
	last=ord('a')
	out,ret=0,0
	for c in str:
		diff=ord(c)-last
		last=ord(c)
		out=23*out+diff%23
		if out>10000000:
			ret+=out%10000000
			out=int(out/10000000)
	ret+=out
	return ret%10000000

print("alg "+str(alg))
print("len "+str(ln))
vals=[]
for i in range(10000000):vals.append(0)
print("array init")
for i in range(100000):vals[hash_string(''.join(random.choices(string.ascii_lowercase,k=ln)))]+=1
print("hashes calc")
collisions,unique=0,0
for i in vals:
	if i>1:
		collisions+=i-1
		unique+=1
print("Total collisions: "+str(collisions))
if unique>0: collisions=str(1+collisions/unique)
print("Average keys per colliding cell: "+collisions)
while True:
	n=input(">>> ")
	if n=="exit":break
	print(hash_string(n))
