# Tim  		: MI6
# Anggota	: 
#	1. Ferdian Ifkarsyah/13517024
#	2. Paulus Siahaan/13517
#	3. Renita Napitulu/13517

import OpenGL
import OpenGL.GLU
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from copy import copy, deepcopy
import time
import math
import sys
import threading

exit = False
dimensi = 2
bangun = []
maxrange = 500

################################
########## USER FLOW ###########
################################

def get_bangun_2d():	# bangun disini dalam artian bangun = shape
	# I.S : var bangun sembarang
	# F.S : var bangun terisi input user dalam format row matrix
	# Contoh : Jika user menginput (100,100),(250,250),(300,100)
	# maka, bangun == [[100,100],
	#				   [250,250],
	#				   [300,100]]
	jum_titik = int(input("Masukkan jumlah titik : "))
	bangun = []
	print("*ket : Masukan titik dipisah dengan koma!")
	for i in range(jum_titik):
		x, y = input("Masukkan (x,y)  : ").split(',')
		x, y = float(x), float(y)
		bangun.append([x,y])
	return bangun

def start_perintah():
	# I.S 	: bangun terdefinisi
	# Proses: berinteraksi sesuai deskripsi problem tubes
	# F.S 	: program berhenti
	global exit, bangun
	exit = False
	bangun_awal = deepcopy(bangun)
	print("Masukkan perintah : ")
	while not exit:
		cmd = input().split()
		if cmd[0]=="translate":
			dx, dy = [float(i) for i in cmd[1:]]
			bangun = animate_translate2d(bangun,dx,dy)
		elif cmd[0]=="dilate":
			k = float(cmd[1])
			bangun = dilate2d(bangun,k)
		elif cmd[0]=="rotate":
			deg, a, b = [float(i) for i in cmd[1:]]
			bangun = animate_rotate2d(bangun,deg,a,b)
		elif cmd[0]=="reflect":
			param = str(cmd[1])
			bangun = reflect2d(bangun,param)
		elif cmd[0]=="shear":
			param, k = cmd[1], float(cmd[2])
			bangun = shear2d(bangun,param,k)
		elif cmd[0]=="stretch":
			param, k = cmd[1], float(cmd[2])
			bangun = stretch2d(bangun,param,k)
		elif cmd[0]=="custom":
			a,b,c,d = [float(i) for i in cmd[1:]]
			bangun = multiplyMatrix(bangun,[[a,b],[c,d]])	
		elif cmd[0]=="multiple":
			n = int(cmd[1])
			bangun = multiple(bangun,n)
		elif cmd[0]=="reset":
			bangun = deepcopy(bangun_awal)
		elif cmd[0]=="exit":
			exit = True
			print("Sampai jumpa!")
		else:
			print("Perintah yang anda masukkan invalid!")


def user_flow():
	# self_explained
	global dimensi,bangun
	bangun = get_bangun_2d()
	perintah = start_perintah()

###################################
########## WINDOWS FLOW ###########
###################################
def setup_coordinate():
	# menggambar garis koordinat 
	global maxrange
	glColor3f(1,1,1)
	glBegin(GL_LINES)
	glVertex2f(-maxrange,0)
	glVertex2f(maxrange,0)
	glEnd()
	glColor3f(1,1,1)
	glBegin(GL_LINES)
	glVertex2f(0,maxrange)
	glVertex2f(0,-maxrange)
	glEnd()
	glutSwapBuffers()


def draw_bangun():
	gluOrtho2D(-maxrange,maxrange,-maxrange,maxrange)
	glColor3f(0,1,0)
	glBegin(GL_POLYGON)
	for sumbu in bangun:
		glVertex2f(sumbu[0],sumbu[1])
	glEnd()
	glutSwapBuffers()

def draw():
	# menggambar bangun
	global exit, bangun
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glClearColor(0,0,0,1)
	glLoadIdentity()
	setup_coordinate()
	draw_bangun()
	if exit: 
		glutLeaveMainLoop()
	glutSwapBuffers()

def window_flow():
	# alur dari window program
	global maxrange
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
	glutInitWindowSize(500,500)
	glutInitWindowPosition(100,100)
	glutCreateWindow(b"Simulasi Transformasi 2D")
	glutDisplayFunc(draw)
	glutIdleFunc(draw)
	glutMainLoop()

###################################
########## MAIN FLOW ###########
###################################

def main_flow():
	# membagi alur program menjadi 2 buah thread : user dan window
	thread_user = threading.Thread(target = user_flow)
	thread_window = threading.Thread(target = window_flow)
	thread_window.start()
	thread_user.start()
	
main_flow()

##########################################
########## MATRIX MANIPULATION ###########
##########################################
def multiplyMatrix(A,B):
	# Mengembalikasi hasil perkalian matriks A*B
	return  [[sum(a * b for a, b in zip(A_row, B_col))  
                        for B_col in zip(*B)] 
                                for A_row in A] 

def transpose(matrix):
	# self_explained
	return  [[matrix[j][i] for j in range(len(matrix))] 
							for i in range(len(matrix[0]))] 		

def translate2d(matrix,dx,dy):
	# menggeser matrix sejauh [dx dy]
	for vertex in matrix:
		vertex[0] += dx
		vertex[1] += dy
	return matrix		


def dilate2d(matrix,k):
	# mendilatasi matrix dengan konstanta k
	for vertex in matrix:
		vertex[0] *= k
		vertex[1] *= k
	return matrix

def rotate2d(matrix,deg,a,b):
	# merotasi matrix sebanyak deg dengan pusat p(a,b)
	rad = math.radians(deg)
	transMat = [[math.cos(rad), -math.sin(rad)],
			 	[math.sin(rad), math.cos(rad)]]
	matrix = translate2d(matrix,-a,-b)
	matrix = multiplyMatrix(transMat,transpose(matrix))
	matrix = translate2d(matrix,a,b)
	matrix = transpose(matrix)
	return matrix



def reflect2d(matrix,param):
	# mengembalikan hasil refleksi matrix terhadap garis
	if param=="y=x":
		transMat = [[0,1],
					[1,0]]
	elif param=="y=-x":
		transMat = [[0,-1],
					[-1,0]]
	elif param=="x": 
		transMat = [[1,0],
					[0,-1]]
	elif param=="y": 
		transMat = [[-1,0],
					[0,1]]
	matrix = multiplyMatrix(transMat,transpose(matrix))
	matrix = transpose(matrix)
	return matrix


def shear2d(matrix,param,k):
	# mengembalikan hasil shear matrix terhadap garis
	if param=="x":
		transMat =[[1,k],
				   [0,1]]
	else:
		transMat =[[1,0],
				   [k,1]]
	matrix = multiplyMatrix(transMat,transpose(matrix))
	return transpose(matrix)

def stretch2d(matrix,param,k):
	# mengembalikan hasil stretch matrix terhadap garis
	if param=="x":
		transMat =[[k,0],
				   [0,1]]
	else:
		transMat =[[1,0],
				   [0,k]]
	matrix = multiplyMatrix(transMat,transpose(matrix))
	return transpose(matrix)

def multiple(bangun,n):
	for i in range(n):
		print("Masukkan perintah : ")
		cmd = input().split()
		if cmd[0]=="translate":
			dx, dy = [float(i) for i in cmd[1:]]
			bangun = translate2d(bangun,dx,dy)
		elif cmd[0]=="dilate":
			k = float(cmd[1])
			bangun = dilate2d(bangun,k)
		elif cmd[0]=="rotate":
			deg, a, b = [float(i) for i in cmd[1:]]
			bangun = rotate2d(bangun,deg,a,b)
		elif cmd[0]=="reflect":
			param = str(cmd[1])
			bangun = reflect2d(bangun,param)
		elif cmd[0]=="shear":
			param, k = cmd[1], float(cmd[2])
			bangun = shear2d(bangun,param,k)
		elif cmd[0]=="stretch":
			param, k = cmd[1], float(cmd[2])
			bangun = stretch2d(bangun,param,k)
		elif cmd[0]=="custom":
			a,b,c,d = [float(i) for i in cmd[1:]]
			bangun = multiplyMatrix(bangun,[[a,b],[c,d]])

##########################################
########## ANIMASI #######################
##########################################
def animate_translate2d(matrix,dx,dy):
	stepx = dx/maxrange
	stepy = dy/maxrange
	s = abs(1/maxrange)
	for i in range(maxrange-100):
		time.sleep(s)
		matrix = translate2d(matrix,stepx,stepy)
	return matrix

def animate_dilate2d(matrix,k):
	stepk = k/maxrange
	s = abs(1/maxrange)
	for i in range(maxrange):
		time.sleep(s)
		matrix = dilate2d(matrix,k)
	return matrix

def animate_rotate2d(matrix,deg,a,b):
	step = deg/maxrange
	s = abs(1/maxrange)
	for i in range(maxrange):
		time.sleep(s)
		matrix = rotate2d(matrix,step,a,b)				
	return matrix

def animate_shear2d(matrix,param,k):
	stepk = k/maxrange
	s = abs(1/maxrange)
	for i in range(maxrange):
		time.sleep(s)
		matrix = shear2d(matrix,param,stepk)	
	return matrix		

def animate_stretch2d(matrix,param,k):
	stepk = k/maxrange
	s = abs(1/maxrange)
	for i in range(maxrange):
		time.sleep(s)
		matrix = stretch2d(matrix,param,stepk)		
	return matrix