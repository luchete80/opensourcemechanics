# Recorro 
print("Buscando tags...\n");
tagcount = 0;
taglines = 0;
l = 0;
# with open('index.html') as topo_file:
	# for line in topo_file:
file = open('index.html','r')
lines = file.readlines()
# for line in file.readlines():
main_end = False;
while (l < len (lines)):
		# print (line)  # The comma to suppress the extra new line char
	if ("<li class=\"entry\">" in lines[l]):
		end = False;
		while (not end):
			l +=1;
			if ("</li>" in lines[l]):
				end = True;
			if ("#" in lines[l]):
				taglines+=1;
				print('found tagline in line %d' %l);
				print('Tags %s\n',lines[l])
	l +=1
	print("line %d\n" %l);
	# if ('</main>' in lines[l]):
		# main_end = True;
			
	
print('Encontrados %d tags' %taglines)