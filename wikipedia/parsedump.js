function parse(a){
	ret=""
	first=1
	for(let c of a.children){
		if(first)ret+="{\n\t\t\t\t\t'name': '"+c.textContent+
			"',\n\t\t\t\t\t'examples': [\n"
		else ret+="\t\t\t\t\t\t'"+c.textContent+"',\n"
		first=0
	}
	ret=ret.slice(0,ret.length-2)
	ret+="\n\t\t\t\t\t]\n\t\t\t\t}"
	navigator.clipboard.writeText(ret)
	return ret
}
