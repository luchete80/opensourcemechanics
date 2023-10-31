# Recorro 
print("Buscando tags...\n");
tagcount = 0;
taglines = 0;
l = 0;
# with open('index.html') as topo_file:
 # for line in topo_file:
file = open('index.html','r')
outfile = open('test.html','w')
lines = file.readlines()
# for line in file.readlines():
main_end = False;

tag_arr = []
while (l < len (lines)):
  # print (line)  # The comma to suppress the extra new line char
  if ("<li class=\"entry\">" in lines[l]):
    end = False;
    while (not end):
      l +=1;
      if ("</li>" in lines[l]):
        end = True;
      if ("#" in lines[l]):
          # tagl=lines[l];
        taglist = (lines[l]).split("#")
        taglines += 1;
        print('found tagline in line %d' %l);
        print('Tags %s\n',lines[l])
                    # print('Tag count %d\n',len(taglist));
        for t in range(0,len(taglist)):
          print('taglist %s\n' %taglist[t]);
          tag_found = False
          for tt in range (0,len(tag_arr)):
            if (tag_arr[tt]==taglist[t]):
              tag_found=True
          if (not tag_found):
            tag_arr.extend([taglist[t]]);
                
  l +=1
  # print("line %d\n" %l);
 # if ('</main>' in lines[l]):
  # main_end = True;
   
print('tag_arr %s',tag_arr)
print('Encontrados %d tags' %taglines)