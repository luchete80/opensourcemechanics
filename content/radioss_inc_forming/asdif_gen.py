#https://www.tutorialsteacher.com/python/create-ui-using-tkinter-in-python
from math import *
from mesher import *
import numpy as np

from tkinter import *
from tkinter.ttk import Combobox
window=Tk()
linea_g=10

flog = open("log.txt","w")

#IMPORTANTE - ACA ESTA DEFINIDO TOOL SPEED
#INPUT VARS
#VER COMO ACOMODAR CON ALFA Y BETA ANGULOS
r_i         = 0.01
r_o         = 0.0325    #NO CONFUNDI CON HERRAMENTAS IN Y OOUT
r           = 0.0325
dr          = 5.0e-4    #DESAPARECE DE ACUERDO A LA GEOMETRIA
t_end       = 1.0e-1
dt          = 1.0e-5
#t_ang       = 1.0e-3    #Periodo angular, ANTES ERA CONSTANTE
p_D         = 2.5e-3     #ASDIF RADIAL DISTANCE BETWEEN TOOLS
p_S         = 4.3e-4     #ASDIF HEIGHT DISTANCE BETWEEN TOOLS
tool_speed  = 0.6 / 60.0 * 5000 #600mm/min according to Valoppi
t_ind       = 1.0e-3
thck        = 5.0e-4
tool_rad    = 0.0025

thermal     = False


filelbl = Label(window, text="Archivo", width=15,justify=LEFT)
filelbl.grid(column=1, row=0)	
textField = Entry(window, width=15)
textField.grid(column=2, row=0)
textField.insert(0,"test.txt")

test = [(1,1),(2,2)]
test.append((3,4))
print (test)
print (test[2][0])
#############################################################################################################################################
largo = 0.1
delta = 0.001

shell_elnod = [(1,2,3,4)]


shell_mesh = Plane_Mesh(1,largo,delta)
sph1_mesh = Sphere_Mesh(2, tool_rad,        \
                        r_i, 0.0,tool_rad + thck, \
                                        5) #(id, radius, divisions):

print("Piece Shell node count", len(shell_mesh.nodes))
print("Shell Shell node count", len(sph1_mesh.nodes))

print("Shell node count var", shell_mesh.node_count)
print("Sphere node count var", sph1_mesh.node_count)


# print("Shell node count", len(shell_mesh.elnod))
# print("Shell node count", len(sph1_mesh.elnod))

model = Model()
print ("Model size: ", len(model.part))
shell = Part(1)
shell.AppendMesh(shell_mesh) 


bcpos = largo/2.0 - 2.0 * delta

sph1_pt = Part(2)
sph1_pt.AppendMesh(sph1_mesh) 
sph1_pt.is_rigid = True
sph1_pt.is_moving = True

model.AppendPart(shell) #FIRST PART TO ADD!
model.AddNodeSetOutsideBoxXY(1000,Vector(-bcpos,-bcpos,0.0), Vector(bcpos,bcpos,0.0)) #id, v1, v2):

model.AppendPart(sph1_pt)

model.AppendMat(Material(1))
model.AppendProp(Prop(1))

inter_1 = Interface(2,1)
model.AppendInterface(inter_1)


model.part[0].mesh[0].print_segments = True

if (thermal):
  model.thermal = True

# THERMAL
for e in range (model.part[0].mesh[0].elem_count):
  lf = Function(0.0,.0,0)
  model.AppendLoadFunction (lf)
# sphere_mesh = Sphere_Mesh(2,1.0, 10,1) #(self, id, radius, divisions, ininode):

# shell_mesh.printRadioss("radioss.rad")

# sphere_mesh.printRadioss("radioss.rad")

#IMPORTANTE: LA VELOCIDAD SE ASUME PARA RADIO CONSTANTE EN CADA VUELTAS
#CON LO CUAL EN LA REALIDAD DISMINUYE UN POCO
def save(lin):
# f= open(textField.get(),"w+")
  # LA HERRAMIENTA INTERNA ESTA EN EL TOP, LA EXTERNA EN EL BOTTOM
  # PERO TOP Y BOTTOM CONFUNDE POR LAS INDENTACIONES
  fi_x = open("movi_x.csv","w")
  fi_y = open("movi_y.csv","w")
  fi_z = open("movi_z.csv","w")
  fo_x = open("movo_x.csv","w")
  fo_y = open("movo_y.csv","w")
  fo_z = open("movo_z.csv","w")
  
  t = 0.0
  r = r_i
  turn = 1
  
  z  = 0.0 
  zo = -thck #ESTA HERRAMIENTA NO DESCIENDE (PARA EVITAR DEFORMACIONES IRREGULARES)
  zi =  thck 
  vz = (thck + p_S) / t_ind # EN PRINCIPIO S EDESPLAZA SOLO LA INTERIOR 
  
  #####################INDENTACION ######################### 
  xi = r - p_D/2.0
  xo = r + p_D/2.0
  
  while (t < t_ind):    
    zi -= vz * dt
    #HAY QUE VER SI ES NECESARIO ESCRIBIR X E Y PARA TODOS LOS TIEMPOS
    fi_x.write("%.6e, %.6e\n" % (t,xi))
    fi_y.write("%.6e, %.6e\n" % (t,0.0))
    fi_z.write("%.6e, %.6e\n" % (t,zi))

    fo_x.write("%.6e, %.6e\n" % (t,xo))
    fo_y.write("%.6e, %.6e\n" % (t,0.0))
    fo_z.write("%.6e, %.6e\n" % (t,zo))  
    t +=dt 
 
  print("Final zi %.3e , zo %.3e \n" %(zi,zo))
  
  ######################## VUELTAS ##############################
  while (t < t_end):
    t_ang = 2.0 * pi * r / tool_speed #Tiempo (incremento) de cada vuelta (ASUMIENDO RADIO CONSTANTE)
    print("Turn %d Turn Time %.3e Time %.3e Radius %.3e\n" %(turn, t_ang,t,r))
    t_vuelta = t + t_ang  #Tiempo de final de vuelta (TOTAL)
    t_0 = t               #Tiempo de comienzo de vuelta
    t_inc = 0.0           # t - t_0
    dz = dr               #CAMBIAR SEGUN GEOMETRIA
    vz = dz / t_ang
    while (t < t_vuelta): #VUELTAS  
      # print ("t_inc %.3e t_ang %.3e"%(t_inc,t_ang))
      xi = (r - p_D/2.0 + dr * t_inc/t_ang) *cos(2.0*pi*t_inc/t_ang)
      yi = (r - p_D/2.0 + dr * t_inc/t_ang) *sin(2.0*pi*t_inc/t_ang)
      zi -= vz * dt

      xo = (r + p_D/2.0 + dr * t_inc/t_ang) *cos(2.0*pi*t_inc/t_ang)
      yo = (r + p_D/2.0 + dr * t_inc/t_ang) *sin(2.0*pi*t_inc/t_ang)      
      zo -= vz * dt #CAMBIAR A DZ
      
      # print("zi %.3e , zo %.3e \n" %(zi,zo))
      # z -= t_inc/t_ang * dr # CAMBIAR A dz
      
      fi_x.write("%.6e, %.6e\n" % (t,xi))
      fi_y.write("%.6e, %.6e\n" % (t,yi))
      fi_z.write("%.6e, %.6e\n" % (t,zi))

      fo_x.write("%.6e, %.6e\n" % (t,xo))
      fo_y.write("%.6e, %.6e\n" % (t,yo))
      fo_z.write("%.6e, %.6e\n" % (t,zo))
      
      t_inc +=dt
      t += dt

      # if (thermal):
        # e = model.part[0].mesh[0].findNearestElem(xi,yi,zi)
        # flog.write ("TIME %f, pos: %.6e %.6e, Found %d\n" % (t, xi, yi, e ))
        # coord = str (model.part[0].mesh[0].elcenter[e].components)
        # flog.write ("baricenter: %s\n" %(coord))  
        # model.load_fnc[e].Append(t,1.0e6)
      
    r +=dr
    turn += 1    
    
  for e in range (model.part[0].mesh[0].elem_count):  
    model.load_fnc[e].Append(1.0e3,0.0)
  
  #SPRINGBACK
  fi_x.close;fi_y.close;fi_z.close
  fo_x.close;fo_y.close;fo_z.close


  # for e in range (10):
    # # for f in range (len(load_function[e])):
    # for f in range (model.load_fnc[e].val_count):
      # print ("Load Fnction ", e, model.load_fnc[e].getVal(f))
    
  model.printRadioss("test_0000.rad")


#Si no se coloca lambda no funciona
b = Button(window, text="Generar", width=10, command=lambda:save(linea_g))
b.grid(column=3, row=10)
#b.pack()

window.title('Incremental Forming PATH Script')
window.geometry("400x200+10+10")
window.mainloop()