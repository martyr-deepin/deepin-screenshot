# generate locale file 

gen_locale_mo:
	if [ -d tools ];then cd tools && python generate_mo.py; fi
