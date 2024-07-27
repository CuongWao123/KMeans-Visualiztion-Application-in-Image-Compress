import pygame
from random import randint
import math
from sklearn.cluster import KMeans
import numpy
import matplotlib.pyplot as plt

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
BLACK= (0,0,0)
BACKGROUND_PANEL =(249,255,230)
RED = (255,0,0)
GREEN= (0,255,0)
BLUE =(0,0,255)
YELLOW =(147,153,35)
PURPLE = (255,0,255)
SKY = (0,255,255)
ORANGE = (255,125,25)
GRAPE = (100,25,125)
GRASS =( 55,155,65)
K = 0  # number of cluster
errors = 0
points = []
clusters = []
labels = []
COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE, SKY, ORANGE, GRAPE, GRASS]
def distance (p1, p2):
    return math.sqrt((p1[0]-p2[0])*(p1[0]-p2[0]) + (p1[1]-p2[1])*(p1[1]-p2[1]))

def renderTEXT(str , size , color):
    font = pygame.font.SysFont('sans',size)
    return font.render(str,True,color)

def MENU():

    screen.fill((214,214,214))
    mouse_x, mouse_y = pygame.mouse.get_pos()
    global choose

    # visual button
    pygame.draw.rect(screen,'black', (500 ,200,300,100))
    pygame.draw.rect(screen,'white',(505 ,205,290,90))
    screen.blit(renderTEXT('Visualization',40 , 'black'),(510,220))
    # img compress
    pygame.draw.rect(screen, 'black', (500, 400, 300, 100))
    pygame.draw.rect(screen, 'white', (505, 405, 290, 90))
    screen.blit(renderTEXT('Image Compress', 40, 'black'), (510, 420))

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if choose == 0: # button in menu
                if 500 < mouse_x < 800 and 200 < mouse_y < 300:
                    choose = 1
                if 500 < mouse_x < 800 and 400< mouse_y<500:
                    choose=2

choose =0
def VISUAl():

    global K
    global errors
    global points
    global clusters
    global labels
    global COLORS
    global choose
    mouse_x, mouse_y = pygame.mouse.get_pos()
    screen.fill((214,214,214))

    #panel
    pygame.draw.rect(screen, 'black', (50, 50, 700, 500))  # 50 50 diem bat dau , 700 chieu dai , 500 chieu rong
    pygame.draw.rect(screen, (214,214,214), (55, 55, 690, 490))
    # K button +
    pygame.draw.rect(screen, 'black', (850, 50, 50, 50))
    screen.blit(renderTEXT('+',40,'white'), (865, 50))
    # K button -
    pygame.draw.rect(screen, 'black', (950, 50, 50, 50))
    screen.blit(renderTEXT('-',40,'white'), (960, 50))
    # Run button
    pygame.draw.rect(screen, 'black', (850, 150, 150, 50))
    screen.blit(renderTEXT('RUN',40,'white'), (860, 150))
    # Random Button
    pygame.draw.rect(screen, 'black', (850, 250, 200, 50))
    screen.blit(renderTEXT('RANDOM',40,'white'), (860, 250))
    # Algorithm button
    pygame.draw.rect(screen, 'black', (850, 400, 210, 50))
    screen.blit(renderTEXT('ALGORITHM',40,'white'), (860, 400))
    # reset button
    pygame.draw.rect(screen, 'black', (850, 500, 150, 50))
    screen.blit(renderTEXT('RESET',40,'white'), (860, 500))
    # draw K value
    screen.blit(renderTEXT('K = ' + str(K),40,'black'), (1050, 50))
    # draw Error
    screen.blit(renderTEXT("Error = " + str(errors),40,'black'), (850, 325))
    # Home button
    pygame.draw.rect(screen, 'black', (0, 0, 100, 40))
    screen.blit(renderTEXT('Back',40,'white'),(0,0))

    # draw mouse pos
    if 50 < mouse_x < 750 and 50 < mouse_y < 550:
        fonts = pygame.font.SysFont('sans', 20)
        text_mouse = fonts.render('(' + str(mouse_x - 50) + ',' + str(mouse_y - 50) + ')', True, BLACK)
        screen.blit(text_mouse, (mouse_x + 10, mouse_y))
    # end draw UI
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            # draw point
            if 0<mouse_x<100 and 0<mouse_y<40:
                print ('choose')
                choose = 0

            if 50 < mouse_x < 750 and 50 < mouse_y < 550:
                labels = []
                point = [mouse_x - 50, mouse_y - 50]
                points.append(point)
                errors = 0
            # change K button +
            if 850 < mouse_x < 900 and 50 < mouse_y < 100:
                if K > 8:
                    K = 8
                else:
                    K = K + 1
            # change K button -
            if 950 < mouse_x < 1000 and 50 < mouse_y < 100:
                K = K - 1
                if K < 0:
                    K = 0
            # Run button
            if 850 < mouse_x < 850 + 150 and 150 < mouse_y < 200:
                if K == 0 or len(clusters) == 0 or K != len(clusters):
                    continue
                else:
                    err = 0
                    labels.clear()
                    # assign color point to closet cluster
                    for p in points:
                        list_distance = []
                        for c in clusters:
                            dis = distance(p, c)
                            list_distance.append(dis)

                        minDistance = min(list_distance)
                        label = list_distance.index(minDistance)
                        labels.append(label)
                    # update cluster
                    for i in range(K):
                        sum_x = 0
                        sum_y = 0
                        cnt = 0
                        for j in range(len(points)):
                            if labels[j] == i:
                                cnt += 1
                                sum_x += points[j][0]
                                sum_y += points[j][1]
                        if cnt != 0:
                            clusters[i][0] = sum_x / cnt
                            clusters[i][1] = sum_y / cnt
                        # print(clusters[i][0],clusters[i][1])
                    for i in range(K):
                        for j in range(len(points)):
                            if labels[j] == i:
                                dist = distance(points[j], clusters[i])
                                err = err + dist
                    errors=int(err)
            # random button
            if 850 < mouse_x < 850 + 150 and 250 < mouse_y < 300:
                clusters = []
                labels = []
                errors = 0
                for i in range(K):
                    random_points = [randint(0, 700), randint(0, 500)]
                    clusters.append(random_points)
            # algo button
            if 850 < mouse_x < 850 + 150 and 400 < mouse_y < 450:
                # print("alogo")
                try:
                    kmeans = KMeans(n_clusters=K).fit(points)
                    clusters = kmeans.cluster_centers_
                    labels = kmeans.predict(points)
                    err =0
                    for i in range(K):
                        for j in range(len(points)):
                            if labels[j] == i:
                                dist = distance(points[j], clusters[i])
                                err = err + dist
                    errors = int(err)
                except:
                    print("error")
            # reset button
            if 850 < mouse_x < 850 + 150 and 500 < mouse_y < 550:
                K = 0  # number of cluster
                errors = 0
                points = []
                clusters = []
                labels = []
            # back button

    # ve diem
    for i in range(len(points)):
        pygame.draw.circle(screen, BLACK, (points[i][0] + 50, points[i][1] + 50), 6)
        if len(labels) == 0:
            pygame.draw.circle(screen, (255, 255, 255), (points[i][0] + 50, points[i][1] + 50), 5)
        else:
            pygame.draw.circle(screen, COLORS[labels[i]], (points[i][0] + 50, points[i][1] + 50), 5)

    # random cluster
    for i in range(len(clusters)):
        pygame.draw.circle(screen, COLORS[i], (clusters[i][0] + 50, clusters[i][1] + 50), 6)
    # draw label to point
    pygame.display.flip()

def IMG_COMPRESS(stt , k ):

    global choose
    screen.fill((214,214,214))

    img = plt.imread(stt) # shape -> [width , height , (R,G,B)]
    width = img.shape[0]
    height = img.shape[1]

    img =  numpy.reshape(img,(width*height,3)) #  col2 after cols1

    kmeans = KMeans(n_clusters=k).fit(img)
    clusters = kmeans.cluster_centers_
    labels = kmeans.predict(img)

    img2 = numpy.zeros_like(img)

    for i in range(len(img2)):
        img2[i] = clusters[labels[i]]

    img2 = numpy.reshape(img2,(width,height,3))
    plt.imshow(img2)
    plt.show()
    choose = 0

running = True
while running:
    print(choose)
    if choose ==0 :
        MENU()
    if choose ==1 :
        VISUAl()
    if choose == 2:
        IMG_COMPRESS('hai.jpg',3)
    pygame.display.flip()


pygame.quit()