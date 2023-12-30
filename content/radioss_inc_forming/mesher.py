from math import *

def writeFloatField(number, length, decimals):
  fmt ='%.' + str(decimals) + 'e'
  # print ('format ' + fmt)
  s = fmt % number
  spaces = ''
  for i in range ((int)(length - len(s))):
    spaces = spaces + ' '
  output = spaces + s
  # print (spaces + s)
  return output

def writeIntField(number, length):
  s = '%d' % number
  spaces = ''
  for i in range ((int)(length - len(s))):
    spaces = spaces + ' '
  output = spaces + s
  # print (spaces + s)
  return output

def Norm2(v):
  norm = 0.0
  if isinstance(v, Vector):
    for i in range (len(v.components)):
      norm = norm + v.components[i] * v.components[i]
  return norm

    
class Vector:
  def __init__(self, *components):
      self.components = components
  def __mul__(self, other):
    components = []
    if isinstance(other, Vector):
      # if (len(self.components)!=len(other.components)):
        # print ("Different length size")
      for i in range (len(self.components)):
        components.append(self.components[i] * other.components[i])
    else:
      components = (other * x for x in self.components)
    return Vector(*components)
  # addition is normally a binary operation between self and other object
  # def __add__(self, other):
    # if isinstance(other, Vector):
      # new_vec = Vector()
      # new_vec.X = self.X + other.X
      # new_vec.Y = self.X + other.Y
      # return new_vec
    # else:
      # raise TypeError("value must be a vector.")
  # def __add__(self, other):
    # added =[]
    # for i in range(len(self.components)):
      # #added = tuple( a + b for a, b in zip(self, other) )
      # added.append(self.components[i] + other.components[i])
      # return Vector(*added)
  def __add__(self, other):
    if isinstance(other, Vector):
    # other.args is the correct analog of self.args
      a = [arg1 + arg2 for arg1, arg2 in zip(self.components, other.components)]
    return self.__class__(*a)
  def __sub__(self, other):
    if isinstance(other, Vector):
    # other.args is the correct analog of self.args
      a = [arg1 - arg2 for arg1, arg2 in zip(self.components, other.components)]
    return self.__class__(*a)
  def Norm():
    norm = 0.0
    norm = [norm + arg1 for arg1 in self.components]
    norm = sqrt (norm)
    return norm
    
  def __repr__(self):
      return str(self.components)
      
  # # __repr__ and __str__ must return string
  # def __repr__(self):
    # # return str(self.components)
    # # return f"Vector{self.components}"
    # return str(self.components)

  def __str__(self):
    # return str(self.components)
    return f"Vector{self.components}"
    # return str(self.components)
    
# def __add__(self, other):
  # if isinstance(other, Vector):
    # new_vec = Vector()
    # new_vec.X = self.X + other.X
    # new_vec.Y = self.X + other.Y
    # return new_vec
  # else:
    # raise TypeError("value must be a vector.")

#TODO: CHANGE ALL TO NODE
class Node(Vector):
  def __init__(self, id, *components):
    self.components = components
    self.id = id
    
    
###############################################################################
#TODO: DEFINE MESH
class Mesh:
  node_count = (int) (0.0)
  elem_count = (int) (0.0)
  print_segments = False
  nodes = []
  elnod = []
  elcenter = []
  ini_node_id = 1
  ini_elem_id = 1
  id = 0
  # elnod = [(1,2,3,4)]
  def __init__(self, largo, delta):
    elem_xy = largo/delta
    self.node_count = (int)(elem_xy)
      # self.r = realpart
      # self.i = imagpart
  def __init__(self):
    self.data = []
    
  def alloc_nodes(nod_count):
    for i in range (nod_count-1):
      nodes.append((0.,0.,0.))
  
  def printESurfsRadioss(self,f):
    if (self.print_segments):
      for i in range (self.elem_count):
        line = "/SURF/SEG/%d\nSURF_SEG_%d\n" % (i+1,i+1)
        f.write(line)
        line = writeIntField(i+1,10)
        for d in range (4):
          line = line + writeIntField(self.elnod[i][d]+1,10)
        f.write(line + '\n')
  def printRadioss(self,fname):
    f = open(fname,"w+")
    # self.writeFloatField(-100.0,20,6)
    f.write('/NODES\n')
    for i in range (self.node_count):
      line = writeIntField(i+1,10)
      for d in range (3):
        line = line + writeFloatField(self.nodes[i][d],20,6) 
      # f.write("%.6e, %.6e\n" % (self.nodes[i][0],self.nodes[i][1]))
      f.write(line + '\n')
    f.write('/SHELL/' + str(self.id) + '\n')
    for i in range (self.elem_count):
      line = writeIntField(i+1,10)
      for d in range (4):
        line = line + writeIntField(self.elnod[i][d]+1,10)
      f.write(line + '\n')
  
  def printRigidRadioss(self,f): #ALREADY OPENED
    f.write("/RBODY/%d\n"%(100))
    f.write("PART_%d\n"%(self.id))
    f.write("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n");
    f.write("# node_ID    sens_ID	  Skew_ID	   Ispher	               Mass	  grnd_ID	    Ikrem	     ICoG	  surf_ID\n");
    line = writeIntField(self.ini_node_id + self.node_count - 1, 10) + "                                                  " #50 spaces
    line = line + writeIntField(self.id,10) + "\n"
    f.write(line)
    f.write("\n\n\n") # 3 more line needed for RBODY COMMAND
  def writeCenters(self):
    print ("Writing centers ")
    # print ("self nodes size ",len(self.nodes))
    for e in range (self.elem_count):
      center = [0.,0.,0.]
      for n in range (4):
        for dim in range (3):
          # print ("elem ", e, " node ",n, "el node ", self.elnod[e][n])
          center[dim] = center[dim] + self.nodes[self.elnod[e][n]][dim]

      for dim in range (3):
        center[dim] = center[dim] / 4.0
      self.elcenter.append(Vector(center[0], center[1], center[2]))
    # for e in range (self.elem_count):
      # print ("Element centers ", self.elcenter[e])
        # elcenter
  def findNearestElem(self, x,y,z):
    mx = -1
    maxdist = 1000.0
    for e in range (self.elem_count):
      pos = Vector(x,y,z)
      dist = Norm2(pos - self.elcenter[e])
      # print ("dist: ", dist)
      if ( dist < maxdist ):
        maxdist = dist
        mx = e
    return mx

class Plane_Mesh(Mesh):
  ini_node_id = 1 
  ini_elem_id = 1
  nodes = []
  elnod = []
  elcenter = []
  def set_ini_nod_ele (inin, inie):
    ini_node_id = inin 
    ini_elem_id = inie
  def __init__(self, id, largo, delta):
    self.id = id
    elem_xy = (int)(largo/delta)
    nc = (int)(elem_xy+1)
    self.node_count = nc * nc
    self.elem_count = (int)((elem_xy)*(elem_xy))
    print ('Nodes Count: ' + str(self.node_count))
    print ('Elem Count: ' + str(self.node_count))
    y = -largo/2.0
    for j in range (nc):
      x = -largo/2.0
      for i in range (nc):
        self.nodes.append((x,y,0.))
        x = x + delta
      y = y + delta
      
    for ey in range (elem_xy):    
      for ex in range (elem_xy):   
        #THIS IS THE REAL NODE POSITION (FROM ZERO)
        self.elnod.append(((elem_xy+1)*ey+ex,(elem_xy+1)*ey + ex+1,(elem_xy+1)*(ey+1)+ex+1,(elem_xy+1)*(ey+1)+ex))
                    # elem%elnod(i,:)=[(nel(1)+1)*ey + ex+1,(nel(1)+1)*ey + ex+2,(nel(1)+1)*(ey+1)+ex+2,(nel(1)+1)*(ey+1)+ex+1]         
              # print *, "Element ", i , "Elnod", elem%elnod(i,:) 
    # print(self.elnod)
    self.writeCenters()
    
#Based on: https://github.com/caosdoar/spheres/blob/master/src/spheres.cpp 
#https://medium.com/@oscarsc/four-ways-to-create-a-mesh-for-a-sphere-d7956b825db4
class Sphere_Mesh(Mesh):
  #NECESSARY TO CREATE SEPARATED NEW LISTS!
  nodes = []
  elnod = [] 
  def __init__(self, id, radius, ox,oy,oz, divisions):
    print ("Creating Sphere mesh")
    self.id = id
    CubeToSphere_origins = [
    #Vector(-1.0, -1.0, -1.0), #ORGIINAL POINT ONE
    Vector(1.0, -1.0, -1.0),
    Vector(1.0, -1.0, -1.0),
    Vector(1.0, -1.0, 1.0),
    Vector(-1.0, -1.0, 1.0),
    Vector(-1.0, 1.0, -1.0),
    Vector(-1.0, -1.0, 1.0)]
    CubeToSphere_rights = [
    Vector(-2.0, 0.0, 0.0),
    Vector(0.0, 0.0, 2.0),
    Vector(-2.0, 0.0, 0.0),
    Vector(0.0, 0.0, -2.0),
    Vector(2.0, 0.0, 0.0),
    Vector(2.0, 0.0, 0.0)]
    CubeToSphere_ups = [
		Vector(0.0, 2.0, 0.0),
		Vector(0.0, 2.0, 0.0),
		Vector(0.0, 2.0, 0.0),
		Vector(0.0, 2.0, 0.0),
		Vector(0.0, 0.0, 2.0),
		Vector(0.0, 0.0, -2.0) ]
    step = 1.0 / divisions
    step3 = Vector(step, step, step)

    test = Vector (0.,0.,0.)
    n = 0
    for face in range (1): #CUBE FACES 
      origin = CubeToSphere_origins[face]
      right = CubeToSphere_rights[face]
      # print (right)
      up = CubeToSphere_ups[face]
      for j in range (divisions+1):
        j3 = Vector(j,j,j)
        for i in range (divisions+1):
          i3 = Vector(i,i,i)
          # print ("i3 j3 ", i3, j3)
          # print (right)
          # print ("origin ")
          # print (origin)
          # print ("right * origin ")

          # test = right * origin  
          # print (test)
          # test = right + up  
          # print (test)
          # const Vector3 p = origin + step3 * (i3 * right + j3 * up);
          p = origin + ( step3 * (i3 * right  + up *j3 )  )
          p2 = p * p
          # rx = sqrt(1.0 - 0.5 * (p2.y + p2.z) + p2.y*p2.z/3.0)
          # ry = sqrt(1.0 - 0.5 * (p2.z + p2.x) + p2.z*p2.x/3.0)
          # rz = sqrt(1.0 - 0.5 * (p2.x + p2.y) + p2.x*p2.y/3.0)
          rx = p.components[0] * sqrt(1.0 - 0.5 * (p2.components[1] + p2.components[2]) + p2.components[1]*p2.components[2]/3.0)
          ry = p.components[1] * sqrt(1.0 - 0.5 * (p2.components[2] + p2.components[0]) + p2.components[2]*p2.components[0]/3.0)
          rz = p.components[2] * sqrt(1.0 - 0.5 * (p2.components[0] + p2.components[1]) + p2.components[0]*p2.components[1]/3.0)
          
          x = rx * radius + ox;           y = ry * radius + oy ;           z = rz * radius + oz;
          print ("z , z corrected ", rz,z)
          #self.nodes.append((rx,ry,rz))
          self.nodes.append((x,y,z))
          
          n = n +1
    
    
    self.nodes.append((ox,oy,oz)) #CENTER AS RIGID PIVOT
    self.node_count = n + 1
    
    # print ("generated: %d", n , " nodes      ")
    # print ("Node vector count: ", len(self.nodes))
    
      # print (origin)
    
    # for i in range (self.node_count):
      # print ("SPHERE Node ", i, self.nodes[i])
    
    e = 0
    for ey in range (divisions):
      for ex in range (divisions):
        # elem%elnod(i,:)=[(nel(1)+1)*ey + ex+1,(nel(1)+1)*ey + ex+2,(nel(1)+1)*(ey+1)+ex+2,(nel(1)+1)*(ey+1)+ex+1]  
        self.elnod.append(((divisions+1)*ey+ex,(divisions+1)*ey + ex+1,(divisions+1)*(ey+1)+ex+1,(divisions+1)*(ey+1)+ex))      
        e = e + 1
    self.elem_count = e
    
import numpy as np

def plane_mesh(length, delta, nodos, elnod, mesh):
  num_nodos = 10
  num_elem_xy = ()
  # nodos = np.empty(num_nodos,dtype=object)
  # y = np.arange(30).reshape((10, 3)) 
  nodos.append((1,1,1))
  # print("\nArray y : ", y) 
  # np.reshape(nodos,(20,num_nodos))
  print (nodos)
  print (nodos[0][2])
  
class NodeGroup:
  nodes = [] # TODO: CHANGE TO LIST
  part = 0
  def __init__ (self, id):
    self.id = id

class Prop: 
  def __init__(self, pid):
    self.pid = pid
  def printRadioss(self,f):     
    f.write("##--------------------------------------------------------------------------------------------------\n")
    f.write("## Shell Property Set (pid 1)\n")
    f.write("##--------------------------------------------------------------------------------------------------\n")
    f.write("/PROP/SHELL/1\n")
    f.write("SECTION_SHELL:1 TITLE:probe_section  \n")                                                               
    f.write("#Ishell	Ismstr	Ish3n	Idril	 	 	P_thickfail\n")
    f.write("         4         2                         \n")                                   
    f.write("#hm	hf	hr	dm	dn\n")
    f.write("\n")
    f.write("#N	Istrain	Thick	Ashear	 	Ithick	Iplas    \n")                                                                                                
    f.write("         2          5.00000000000000E-04                                       1         1\n")
             
        
         
     
class Material:
  def __init__(self, mid):
    id = mid
  def printRadioss(self,f):
    f.write("/MAT/COWPER/2\n")  
    f.write("MAT_PIECEWISE_LINEAR_PLASTICITY:2 TITLE:mat_probe   \n")                                                  
    f.write("              7850.0\n")  
    f.write("      200000000000.0                0.33\n")  
    f.write("        300000000.0        2000000000.0                 1.0                 0.01.00000000000000E+30\n")  
    f.write("                0.0                 0.0         1         11.00000000000000E+30\n")  
    f.write("1.00000000000000E+211.00000000000000E+302.10000000000000E+30\n")  
    f.write("#/HEAT/MAT/mat_ID/unit_ID\n")
    f.write("/HEAT/MAT/2\n")
    f.write("#                 T0             RHO0_CP                  AS                  BS     IFORM\n")
    f.write("              20.0                 2.5e6               420.0                  0.0        1\n")
    f.write(" \n") #REQUIRED

class Function:
  val_count = 0 
  def __init__(self, id, x,y):
    self.val_count = 1
    self.vals = []
    self.vals.append((x,y))
  def Append (self,x,y):
    self.vals.append((x,y))
    self.val_count = self.val_count + 1
  def getVal(self, i):
    return self.vals[i]
  def getVal_ij(self, i, j):
    return self.vals[i][j]

#ASSUMING EACH PART HAS ONLY 1 MESH
class Part:
  is_rigid = False
  is_moving = False
  id_grn_move = 0 #GROUP NODE FOR MOVING
  def __init__(self, mid):
    self.id = mid
    self.mesh = []
    self.title = "PART_ID_%d\n" %mid
    self.mid = 0
    self.id_grn_move = mid + 100
  def AppendMesh(self,m):
    if (not isinstance(m, Mesh)):
      print ("part is not a mesh")
    else:
      self.mesh.append(m)
  
  def printRadioss(self,f):                          
    f.write('/SHELL/' + str(self.id) + '\n')
    for i in range (self.mesh[0].elem_count):
      line = writeIntField(i + self.mesh[0].ini_elem_id ,10)
      for d in range (4):
        # print (self.mesh[0].ini_node_id, ", ")
        line = line + writeIntField(self.mesh[0].elnod[i][d] + self.mesh[0].ini_node_id,10)
      f.write(line + '\n')   
    
    line = "/PART/%d\n" % self.id
    f.write(line)
    f.write(self.title)                                                                                            
    f.write("#     pid     mid\n")
    f.write("      1         2\n") 
    line = "/GRNOD/PART/%d\n" % self.id    
    line = line + "PART_%d\n" % self.id
    line = line + writeIntField(self.id,10) + "\n"
    f.write(line)
    
    #GRNOD FOR MOVE 
    if (self.is_moving):
      line = "/GRNOD/NODE/%d\n" % self.id_grn_move    
      line = line + "MOVE_%d\n" % self.id
      line = line + writeIntField(self.mesh[0].ini_node_id + self.mesh[0].node_count - 1, 10) + "\n"
      f.write(line)

      line = "/BCS/%d\n" % self.id
      line = line + "BoundSpcSet_1 \n"  
      line = line + "#  Tra rot   skew_ID  grnod_ID\n"
      line = line + "   000 111         0" + writeIntField(100+self.id, 10) + "\n"
      f.write(line)

    
    if (self.mesh[0].print_segments):
      self.mesh[0].printESurfsRadioss(f) 
    if (self.is_rigid):
      self.mesh[0].printRigidRadioss(f) 
      
class Interface:
  id_master = 0
  id_slave = 0
  bc_count = 0
  def __init__(self, master, slave):
    self.id_master = master
    self.id_slave = slave
  
class Model:
  tot_nod_count = 0
  tot_ele_count = 0
  thermal = False
  node_group_count = 0
  def __init__(self):
    self.part_count = 0
    self.part = []
    self.mat = []
    self.prop = []
    self.load_fnc = []
    self.inter = []
    self.node_group = []
    
  
  def AppendPart(self, p):
    if (not isinstance(p, Part)):
      print ("ERROR: added object is not a part ")
    else:
      self.part.append(p)
      self.part_count = self.part_count + 1
      print ("part count ", self.part_count)
      if (self.part_count > 1):
        self.tot_nod_count = self.tot_nod_count + self.part[self.part_count-2].mesh[0].node_count
        self.part[self.part_count-1].mesh[0].ini_node_id = self.tot_nod_count + 1
        
        self.tot_ele_count = self.tot_ele_count + self.part[self.part_count-2].mesh[0].elem_count
        self.part[self.part_count-1].mesh[0].ini_elem_id = self.tot_ele_count + 1
        
    print ("Part ", self.part_count, " initial node: ", self.tot_nod_count + 1)
  
  def AppendInterface(self, i):
    if (not isinstance(i, Interface)):
      print ("ERROR: added object is not a interface ")
    else:
      self.inter.append(i)
      
  def AppendMat(self, m):
    if (not isinstance(m, Material)):
      print ("ERROR: added object is not a part ")
    else:
      self.mat.append(m)

  def AppendLoadFunction(self, lf):
    self.load_fnc.append(lf)
    
  def AppendProp(self, p):
    if (not isinstance(p, Prop)):
      print ("ERROR: added object is not a part ")
    else:
      self.mat.append(p)
      
  def printInterfaces(self,f):
    f.write("#-  9. INTERFACES:\n")  
    for i in range (len(self.inter)):
      f.write("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
      f.write("/INTER/TYPE7/%d\n" % (1))
      f.write("INTERFACE %d\n" % (1))
      f.write("#  Slav_id   Mast_id      Istf      Ithe      Igap                Ibag      Idel     Icurv      Iadm\n")
      line = writeIntField(self.inter[i].id_slave,10) + writeIntField(self.inter[i].id_master,10) 
      f.write(line)
      # WITHOUT ENDLINE
      f.write("         0         0         0                   0         0         0         0\n")
      f.write("#          Fscalegap             GAP_MAX             Fpenmax\n")
      f.write("                   0                   0                   0\n")
      f.write("#              Stmin               Stmax          %mesh_size               dtmin  Irem_gap\n")
      f.write("                   0                   0                   0                   0         0\n")
      f.write("#              Stfac                Fric              Gapmin              Tstart               Tstop\n")
      f.write("#                  1                  0.                  .0                   0                   0\n")
      f.write("                   1                 .0           0.0000                       0                   0\n")
      f.write("#      IBC                        Inacti                VisS                VisF              Bumult\n")
      f.write("       000                             0                   1                   1                   0\n")
      f.write("#    Ifric    Ifiltr               Xfreq     Iform   sens_ID\n")
      f.write("         0         0                   0         0         0\n")
  
  # def printMovingPart(self,id,fid,f):
  def printMovingParts(self,f):
    for p in range(self.part_count):
      if (self.part[p].is_moving):
        f.write("/IMPDISP/1\n")
        f.write("NUM3HS1D00_fixvel_1\n")
        f.write("#funct_IDT       Dir   skew_ID sensor_ID  grnod_ID  frame_ID     Icoor\n")
        f.write("         1         X         0         0       102         0         0\n")
        f.write("#           Ascale_x            Fscale_Y              Tstart               Tstop\n")
        f.write("                   1                   1                   0               11000  \n")                  
        f.write("/IMPDISP/2\n")
        f.write("NUM3HS1D00_fixvel_1\n")
        f.write("#funct_IDT       Dir   skew_ID sensor_ID  grnod_ID  frame_ID     Icoor\n")
        f.write("         2         Y         0         0       102         0         0\n")
        f.write("#           Ascale_x            Fscale_Y              Tstart               Tstop\n")
        f.write("                   1                   1                   0               11000 \n")
        f.write("/IMPDISP/3\n")
        f.write("NUM3HS1D00_fixvel_1\n")
        f.write("#funct_IDT       Dir   skew_ID sensor_ID  grnod_ID  frame_ID     Icoor\n")
        f.write("         3         Z         0         0       102         0         0\n")
        f.write("#           Ascale_x            Fscale_Y              Tstart               Tstop\n")
        f.write("                   1                   1                   0               11000 \n")
  
  def AddNodeSetOutsideBoxXY (self, id, v1, v2):
    self.node_group.append(NodeGroup(id))
    nc = 0
    for p in range (self.part_count):
      # print ("ini node id ",self.part[p].mesh[0].ini_node_id )
      for n in range (self.part[p].mesh[0].node_count):
        inc = False
        for d in range (2):
          if (self.part[p].mesh[0].nodes[n][d] < v1.components[d] or self.part[p].mesh[0].nodes[n][d] > v2.components[d]):
            inc = True
            # print ("comp, bound", self.part[p].mesh[0].nodes[n][d], v1.components[d],v2.components[d])
        if (inc): 
          self.node_group[self.node_group_count].nodes.append(self.part[p].mesh[0].ini_node_id + n)   
          nc = nc +1
    self.node_group_count =   self.node_group_count + 1
    print ("Outside Box Set Node count: ", nc)
        

  def printFixNodeGroups(self,f):
    for g in range (self.node_group_count):
      # print ("Writing set of count: ", len (self.node_group[g].nodes))
      f.write("/GRNOD/NODE/%d\n" % self.node_group[g].id)
      f.write("FIX_%d\n" % self.node_group[g].id)
      ff = 0;
      line = ""
      for i in range (len (self.node_group[g].nodes)):
        # print ("i ",i, "id ", self.node_group[g].nodes[i], "line ", line  )
        line = line + writeIntField(self.node_group[g].nodes[i],10)
        ff = ff + 1
        if (ff ==10):
          ff = 0
          f.write(line + "\n")
          line = ""
      if (ff>0):
        f.write(line + "\n")    
      f.write("/BCS/%d\n" % self.node_group[g].id)
      f.write("BoundSpcSet_1\n")     
      f.write("#  Tra rot   skew_ID  grnod_ID\n")      
      f.write("   111 111         0" + writeIntField(self.node_group[g].id,10) + "\n")         

  
  def printRadioss(self,fname):
    f = open(fname,"w+")
    f.write("#RADIOSS STARTER\n")
    f.write("/BEGIN\n")
    f.write("test                                                        \n")                   
    f.write("      2019         0 \n")
    f.write("                  kg                   m                   s\n")
    f.write("                  kg                   m                   s\n")
    f.write("#include functions.inc\n")
    f.write('/NODE\n')
    for p in range (self.part_count):
      # print ("part node count ", self.part[p].mesh[0].node_count)
      for i in range (self.part[p].mesh[0].node_count):
        print ("Node ", self.part[p].mesh[0].nodes[i])
        line = writeIntField(i + self.part[p].mesh[0].ini_node_id,10)
        for d in range (3):
          line = line + writeFloatField(self.part[p].mesh[0].nodes[i][d],20,6) 
        f.write(line + '\n')

    # Print element connectivity
    for p in range (self.part_count):
      self.part[p].printRadioss(f)
    
    print ("printing materials: ", len(self.mat))
    for m in range (len(self.mat)):
      self.mat[m].printRadioss(f)
    
    
    if (self.thermal):
      # f.write("#include thermal.inc\n")  
      print ("Load function count: ", len(self.load_fnc))
      ### LOAD FNC
      for lf in range (len(self.load_fnc)):
        # print ("fn ", self.load_fnc[lf][0], "\n")
        line = "/FUNCT/%d\n" % (lf+1)
        line = line + "F_ELEM_%d\n" % (lf+1)
        for val in range (self.load_fnc[lf].val_count):
          line = line + writeFloatField(self.load_fnc[lf].getVal(val)[0],20,6) + \
                        writeFloatField(self.load_fnc[lf].getVal(val)[1],20,6) + "\n"
        f.write(line)

      f.write("################################### ELEMENT FLUXES #####################################\n")
      for lf in range (len(self.load_fnc)):
        # print ("fn ", self.load_fnc[lf][0], "\n")
        line = "/IMPFLUX/%d\nFLUX_ELEM%d\n" % (lf+1,lf+1)
        line = line + writeIntField(lf+1,10)+ writeIntField(lf+1,10) + "\n"
        line = line + "       1.0       1.0\n"
        f.write(line)
      
    for p in range(len(self.prop)):
      self.mat[p].printRadioss(f)
      
    self.printInterfaces(f)
    
    self.printFixNodeGroups(f)
    self.printMovingParts(f)
      
    f.write('/END\n')