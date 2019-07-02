import turtle, os, math, random

#Initialize window
window = turtle.Screen()
window.setup(width = 1000, height = 1000)
window.bgcolor(0,0,0)
window.title("Thompson_Sokoban")


#Scoring
score = 0

#Draw score
drawScore = turtle.Turtle()
drawScore.color("white")
drawScore.speed(0)
drawScore.penup()
drawScore.setposition(-470, 460)
resultDraw = "Score %s" %score
drawScore.write(resultDraw, False, align="left", font=("Arial", 14, "normal"))
drawScore.hideturtle()


#Define game space
game_edge = turtle.Turtle()
game_edge.speed(0)
game_edge.color("white")
game_edge.pensize(3)
game_edge.penup()
game_edge.setposition(-450, -450)
game_edge.pendown()

'''
#Register shapes to apply images
turtle.register_shape("player.gif")
turtle.register_shape("invader.gif")
'''

for wall in range(4):
    game_edge.forward(900)
    game_edge.left(90)
game_edge.hideturtle()


#Player icon
player = turtle.Turtle()
player.color("white")
player.shape("triangle")
player.setheading(90)
player.shapesize(2.5, 2.5)
player.penup()
player.speed(0)
player.setposition(0, -375)
pSpeed = 15


#Laser graphic
pew = turtle.Turtle()
pew.hideturtle()
pew.color("red")
pew.shape("square")
pew.shapesize(1.875, 0.5)
pew.penup()
pew.setposition(0,-450)
pew.speed(0)
tSpeed = 45

#Laser game states
#Primed: Can be fired
#Fired: Has been fired
laserState = "primed"

#Player controls
#Move icon left
def go_left():

        x = player.xcor()
        x -= pSpeed
        player.setx(x)
        if x < -420:
            player.setx(-420)

#Move icon right
def go_right():

        x = player.xcor()
        x += pSpeed
        player.setx(x)
        if x > 420:
            player.setx(420)

#Fire laser
def fire():
    global laserState
    if laserState == "primed":
        laserState = "fired"
        #Set starting position
        x = player.xcor()
        y = player.ycor()
        pew.setposition(x,y)
        pew.showturtle()

#Laser collision detection
def isHit(turt1, turt2):
    distance = math.sqrt(math.pow(turt1.xcor()-turt2.xcor(), 2) + \
                         math.pow(turt1.ycor()-turt2.ycor(), 2))
    if distance < 30:
        return True
    else:
        return False

#Keybinds
turtle.listen()
turtle.onkeypress(go_left, "Left")
turtle.onkeypress(go_right, "Right")
turtle.onkey(fire, "space")


#Generate invader list
#plus counter to track victory condition
invader_x_pos = -300
invader_y_pos = 460
invader_n = 0

invader_list = [[],[],[],[],[]]

for i in invader_list:
    count = 0
    invader_y_pos -= 70
    invader_x_pos = -300
    while count <= 10:
        i.append(turtle.Turtle())
        count +=1
        invader_n +=1
    for j in i:
        j.hideturtle()
        j.color("green")
        j.shape("triangle")
        j.setheading(270)
        j.shapesize(2.5, 2.5)
        j.penup()
        j.setx(invader_x_pos)
        invader_x_pos += 60
        j.sety(invader_y_pos)
        j.showturtle()

iSpeed = 5.0

#Game logic
inProgress = True

#Is the game still going?
while inProgress == True:

#Victory Screen
    if invader_n < 1:
        drawWin = turtle.Turtle()
        drawWin.color("red")
        drawWin.speed(0)
        drawWin.penup()
        resultDraw = "You Win"
        drawWin.write(resultDraw, False, align="center", font=("Arial", 64, "normal"))
        drawWin.hideturtle()
        inProgress = False
        delay = input("Press any key to exit:" )

    #Laser travel
    if laserState == "fired":
        y = pew.ycor()
        y += tSpeed
        pew.sety(y)

    #Once the laser leaves the game area, it can fire again
    if pew.ycor() > 450:
        pew.hideturtle()
        laserState = "primed"

    #Reverses invader direction and moves them down
    #when they encounter a "wall"
    for i in invader_list:
        for j in i:
            x = j.xcor()
            x += iSpeed
            j.setx(x)

            if j.xcor() > 420:
                iSpeed *= -1
                for k in invader_list:
                    for l in k:
                        y = l.ycor()
                        y -= 40
                        l.sety(y)
            elif j.xcor() < -420:
                iSpeed *= -1
                for k in invader_list:
                    for l in k:
                        y = l.ycor()
                        y -= 40
                        l.sety(y)
            #Failure state
            elif j.ycor() < -435:
                print("Game Over")
                inProgress = False

            #Check laser collision with Invader
            if isHit(pew, j):
                pew.hideturtle()
                pew.sety(-500)
                laserState = "primed"
            #Score update
                #score += 10
            #Invader destruction
                j.reset()
                j.sety(500)
                iSpeed +=1.5 #Speeds up the remaining invaders
                invader_n -=1 #increments counter (0 = victory)

                # Just because people like scores
                score +=15
                resultDraw = "Score: %s" %score
                drawScore.clear()
                drawScore.write(resultDraw, False, align="left", font=("Arial", 14, "normal"))

            #Check Invader/Player collision
            #Failure state
            if isHit(player, j):
                player.hideturtle()
                print("Game Over")
                inProgress = False