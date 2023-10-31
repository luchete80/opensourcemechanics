# Removing spaces from a string
# replace() , split() & join() , translate() , regex, reduce() , regex. findall() , 
# map() & lambda() , for loop & join() , itertools. filterfalse() , and isspace() functions.
# https://sparkbyexamples.com/python/python-remove-spaces-from-string/#:~:text=You%20can%20remove%20spaces%20from,()%20%2C%20and%20isspace()%20functions.

# Recorro 
print("Buscando tags...\n");
tagcount = 0;

l = 0;
# with open('index.html') as topo_file:
 # for line in topo_file:
file = open('index.html','r')
outfile = 'test.html'
lines = file.readlines()
# for line in file.readlines():
main_end = False;

def remove_endl_spaces(string):
  string.replace(" ", "")
  string.replace("\t", "")
  string.replace("\n", "")
  return string
  
tag_arr = []
tag_arr_count = []
inside_main = True
while (l < len (lines) and inside_main):
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
        # Always remove first element which is an space: 
        # IMPORTANT! Assumes first contains only spaces!
        del taglist[0]; 
        print('found tagline in line %d' %l);
        print('Tags %s\n',lines[l])
                    # print('Tag count %d\n',len(taglist));
        for t in range(0,len(taglist)): 
          cadena = taglist[t].replace(" ","")
          cadena = cadena.replace("\n","")
          print('->taglist %s<-\n' %cadena)
          tag_found = False
          for tt in range (0,len(tag_arr)):
            if (tag_arr[tt]==cadena):
              tag_found=True
              tag_arr_count[tt] +=1
          if (not tag_found):
            tagcount +=1
            tag_arr.extend([cadena])
            tag_arr_count.extend([1])
  # print("line %d %s\n" %(l,lines[l]))
  if ( "</main>" in lines[l] ):
    inside_main = False
  l +=1

 # if ('</main>' in lines[l]):
  # main_end = True;
   
print('tag_arr %s',tag_arr)
print('tag_arr count %d',tag_arr_count)
print('Encontrados %d tags' %tagcount)

# FIRST: HAVE TO SEARCH <ul class ="cloud"
with open(outfile, 'w') as f:
  f.write ('test\n')
  # sys.stdout = f
  for t in range (0, len(tag_arr)):
    # print ('<li><a data-weight="%d"\n' ,tag_arr_count[t])
    f.write('<li><a data-weight="' + str(tag_arr_count[t]) + 
    '" href="#" onclick="javascript:search_by_string(' +tag_arr[t] + '#C++\');return false;">C++</a></li>\n')
    
  # sys.stdout = original_stdout