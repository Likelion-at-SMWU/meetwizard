#https://github.com/bfaure/Python_Algorithms/blob/master/graham_scan/main.py
# -*- coding: utf8 -*-

import matplotlib  # matplotlib로 데이터시각화(그래프)하고, scatter_plot 함수에서 사용될 plt를 임포트함

from matplotlib import pyplot as plt # for plotting (플로팅: 위치표시하기=점찍기, 산재된 데이터 포인트를 2d로 표현)
from random import randint # for sorting and creating data pts(points)
from math import atan2 # for computing polar angle

# Returns a list of (x,y) coordinates of length 'num_points',
# each x and y coordinate is chosen randomly from the range
# 'min' up to 'max'.
# (x,y) 좌표 만드는 함수.
def create_points(ct,min=0,max=50): # 첫인자 ct=count: 각각의 데이터 포인트에 만들어줘야 할 데이터 포인트의 수를 표시함.
    return [[randint(min,max),randint(min,max)] 
			for _ in range(ct)] # x좌표, y좌표는 랜덤하게 나옴. 일단 0에서 50 사이에서 나오는걸로 설정해둠.

# Creates a scatter plot, input is a list of (x,y) coordinates.
# The second input 'convex_hull' is another list of (x,y) coordinates
# consisting of those points in 'coords' which make up the convex hull,
# if not None, the elements of this list will be used to draw the outer
# boundary (the convex hull surrounding the data points).
# 데이터 포인트는 두 개의 리스트로 나옴.
	# 리스트 1은 X좌표, 리스트 2는 Y좌표.

# convex hull 다각형과 점들을 모두 보여주는 함수. 다각형 안에 흩뿌려진 점들이 보임.
def scatter_plot(coords,convex_hull=None): #coords = data point. convex hull 제공되지 않는다면 값이 none이 디폴트트	
	xs,ys=zip(*coords) # unzip into x and y coord lists(two separate lists)
	plt.scatter(xs,ys) # plot the data points  #matplotlib scatter함수에 x,y좌표 리스트를 넘겨주면, 데이터 포인트들이 산재되어있는걸 2d로 돌려줌.

	if convex_hull!=None:
		# plot the convex hull boundary, extra iteration 테두리 주는 부분에 반복문을 만들어준다 그래야 boundling line이 생긴다 이런뜻인듯. 
		# the end so that the bounding line wraps around
		for i in range(1,len(convex_hull)+1):
			if i==len(convex_hull): i=0
			c0=convex_hull[i-1]
			c1=convex_hull[i]
			plt.plot((c0[0],c1[0]),(c0[1],c1[1]),'r') # wrap. for문 끝에 이터레이션 줌
	plt.show()  # show()로 matplotlib가 plot을 유저에게 보여주도록. 
	        	# 예를 들어 이 코드까지 작성된 상태에서 'scatter_plot(create_points(10)) 하면 그래프에 10개 점만 찍히는 식'


# 이 다음 함수들은 헬퍼 함수들로, quicksort(빠른분류) 알고리즘을 위한거라 함.
# quicksort 알고리즘은 그래험 스캔 안에서 점들을 polar angle로 훑으면서 분류할때 쓰임
# ((https://www.youtube.com/watch?v=vPDPE66nhlo) 4분 20초 짤 참조)

# Returns the polar angle (radians) from p0 to p1. (radians는 각의 크기를 의미)
# If p1 is None, defaults to replacing it with the
# global variable 'anchor', normally set in the
# 'graham_scan' function.
def polar_angle(p0,p1=None): #  polar angle을 p0에서 p1까지의 각으로 계산해 return
	if p1==None: p1=anchor   # anchor는 글로벌 변수/ anchor point 또는 point P = lowest y coordinate in the input set
	y_span=p0[1]-p1[1] 		 # p1 값이 설정이 안된다면 anchor와 동일하게 설정하도록 함.
	x_span=p0[0]-p1[0]		 # 모든 점들이 polar angle로 정리/분류되기 때문에 앵커에 관해서는 매번 함수에 넣어 처리할 필요가 없음.
	return atan2(y_span,x_span)  # polar angle 계산하기 위해서, x 길이, y 길이를 역탄젠트함수에 넣음.
								 # arctangent? -> 삼각형 두 변의 길이가 있을 때 각 계산하기에 가장 쉬운 방법이 역탄제ㅔㄴ트쓴느것.

# 2번째 헬퍼 함수: 완전정확한건 아니어도 근사치인 유클리드 거리 (중간지점과 장소들 사이의 거리 계산)
# Returns the euclidean distance(유클리드 거리: a**2 = b**2+c**2 여기에 좌표 대입해서 두 점 사이의 거리계산. from p0 to p1,
# square root(제곱근) is not applied for sake of speed. 우린 그냥 상대적인 값을비교하는 것임.
# If p1 is None, defaults to replacing it with the
# global variable 'anchor', normally set in the
# 'graham_scan' function.
def distance(p0,p1=None):
	if p1==None: p1=anchor # 또 p1에 input값 없으면 글로별변수 anchor로 초깃값 설정
	y_span=p0[1]-p1[1] #x, y 길이
	x_span=p0[0]-p1[0]
	return y_span**2 + x_span**2  # 이번에는 둘다 제곱해서 더함

# 3번째 헬퍼 함수: 플라즈마 함수 - 세 점이 반시계/시계/동일선상으로 도는 모습인지 판단
# Returns the determinant of the 3x3 matrix...
# 	[p1(x) p1(y) 1]
#	[p2(x) p2(y) 1]
# 	[p3(x) p3(y) 1]
# If >0 then counter-clockwise - det 양이면 반시계방향으로 도는 모습
# If <0 then clockwise - det 음이면 시계방향으로 도는 모습
# If =0 then collinear - det 0이면 세 점은 같은선상에있거나 직선에 있음.
def det(p1,p2,p3): # det = 'determinant' = 부호 있는 영역을 찾는 행렬함수
	return   (p2[0]-p1[0])*(p3[1]-p1[1]) \
			-(p2[1]-p1[1])*(p3[0]-p1[0])

# 우리가 이래저래 만든 quicksort 알고리즘 (polar angle로 점들 정리/분류함)
# Sorts in order of increasing polar angle from 'anchor' point.
# 'anchor' variable is assumed to be global, set from within 'graham_scan'.
# For any values with equal polar angles, a second sort is applied to
# ensure increasing distance from the 'anchor' point.
def quicksort(a):
	if len(a)<=1: return a
	smaller,equal,larger=[],[],[]
	piv_ang=polar_angle(a[randint(0,len(a)-1)]) # select random pivot(중심점)
	for pt in a: # 앵커로부터
		pt_ang=polar_angle(pt) # calculate current point angle
		if   pt_ang<piv_ang:  smaller.append(pt)
		elif pt_ang==piv_ang: equal.append(pt)  # 현재 요소의 polar angle을 중심점의 polar angle과비교
		else: larger.append(pt)
	return quicksort(smaller) \
		+sorted(equal,key=distance) \   
		+quicksort(larger)			   	# 세 개의 부분배열(subarray)를 다시 붙일 때
                                        # (equal array) 같은 배열의 요소에 두번째(이차의) sort를 적용함,
										# anchor에서 점점 더 멀리 떨어지면서 나타남

# 드디어 그래험 스캔 함수
# Returns the vertices comprising the boundaries of
# convex hull containing all points in the input set.
# The input 'points' is a list of (x,y) coordinates. 우리가 convex hull만들고자 하는 데이터 포인트(점)들.
# If 'show_progress' is set to True, the progress in  / show_progress가 True값이면
# constructing the hull will be plotted on each iteration. / convex hull 만드는 과정에서 iteration있을 때마다 위치 표시함.
# 다각형에 새로운 데이터 포인트(점)을 추가할 때마다, 다각형에 두번째 인자로서 통과되고 있는 scatter plot 함수를 부르게 됨.
# 그렇게 되면 점이 많으면 많아질수록... 어떻게 발전되는지 보인다.

def graham_scan(points, show_progress=False):
	global anchor # to be set, (x,y) with smallest y value / 글로벌 변수(밖에서도 access가능) 선언!

	# anchor 변수(가장 작은 y 좌표 가진 점임) 의 실제 값을 해결함.
	# 이걸 위해서 데이터 셋의 모든 점들에 iterate함
	# -> 가장 작은 y 좌표 가진 점이 새로 나올때마다 min index 변수가 갱신됨.
	# Find the (x,y) point with the lowest y value,
	# along with its index in the 'points' list. If
	# there are multiple points with the same y value,
	# choose the one with smallest x.
	# 가장 작은 y 좌표 가진 점이 여러개일 때는, x좌표가 가장 작은 녀석을 고른다. (두번째 if문)
	min_idx=None
	for i,(x,y) in enumerate(points):
		if min_idx==None or y<points[min_idx][1]:
			min_idx=i
		if y==points[min_idx][1] and x<points[min_idx][0]:
			min_idx=i

	# set the global variable 'anchor', used by the
	# 'polar_angle' and 'distance' functions
	anchor=points[min_idx]  # 글로벌 변수 anchor를 우리가 방금 찾은 점으로 갱신함

	# 앵커 결정됐으니까 이제 quicksort 함수로 점들을 점점 커지는 polar angle에 따라 정리함.
	# sort the points by polar angle then delete
	# the anchor from the sorted list (hull에 실수로 두번 추가하지 않을 수 있도록)
	sorted_pts=quicksort(points)
	del sorted_pts[sorted_pts.index(anchor)]

	# anchor and point with smallest polar angle will always be on hull
	# 리스트의 첫째 요소 안의 앵커는 convex hull에 항상 들어갈거니까
	# for문에 따로 조건 붙일 필요 없이 지금 넣어라~.
	hull=[anchor,sorted_pts[0]] # 앵커, 리스트 안의 첫째 요소로 다각형 initiate
	# 리스트 내의 나머지 점들에 iterate
	for s in sorted_pts[1:]:
		while det(hull[-2],hull[-1],s)<=0: # 각 점마다 while문에 넣어서 backtrack. 새 점ㅇ ㅣ추가되도 시계방향으로 돌아갈 일이 없어질 때까지!
			del hull[-1] # backtrack(hull에서 시계방향 회전이 나오면 가장 최근에 추가된 요소 지우는거.)
			#if len(hull)<2: break    # 피ㄹ수는 아님. 앵커 실수로 지워지지 말라고 넣은 코드.
		hull.append(s)  # while문 끝나고, current point를 hull list에 새로 추가함.
		if show_progress: scatter_plot(points,hull)  # show_progress=true이면 convex hulll에 점이 표시됨!
	return hull  # 앵커에서 polar angle 증가하는 순서로 hull list return! (점점점)

def benchmark(sizes=[10,100,1000,10000,100000]): # 너는 뭐니.. 작성자가 추가한듯
	for s in sizes:
		tot=0.0
		for _ in range(3):
			pts=create_points(s,0,max(sizes)*10)
			t0=time()
			hull=graham_scan(pts,False)
			tot+=(time()-t0)
		print("size %d time: %0.5f"%(s,tot/3.0))


pts=create_points(10)  # line14에서 정의한 점만드는 함수. 데이터 포인트 10개 만들고 터미널에서 출력
print("Points:",pts)
hull=graham_scan(pts,True)
print("Hull:",hull)  # convex hull 만들고 출력. scatter plot으로 데이터 시각화
scatter_plot(pts,hull)