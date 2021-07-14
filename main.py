# My resolution is 1920x950, so naturally I've used that for my game. If you
# need to adjust it to to your resolution - you may change it, it's on line 35.

# Note! Controls and cheat codes are:

# Move left with the left arrow key,
# Move right with the right arrow key,
# Press 'p' to pause,
# Press 'u' to unpause,
# The 'up' arrow key is the bosskey,
# The 'down' arrow key exits the boss key's frame.
# CHEAT CODES:
# 'w' - win level,
# 't' - add ten points,
# 's' - increase speed,
# 'd' - decrease speed.


# I need all these from tkinter in order to utilise the UGI's capabilities.

from tkinter import Tk, Button, IntVar, StringVar, Frame, Canvas, \
    Label, PhotoImage, Entry, BooleanVar

# I need this for measuring elapsed time and the sleep method.

import time

# I need this for randomized values (For example random coordiantes).

from random import randint as rand

root = Tk()
root.geometry('1920x950')  # Change this if needed!

# Decoarational images of dogs throughout the whole game.

MAIN_MENU_DOGGO_LEFT = PhotoImage(file='doggo3.png')
MAIN_MENU_DOGGO_RIGHT = PhotoImage(file='doggo3R.png')
GAME_INFO_DOGGO_LEFT = PhotoImage(file='QL.png')
GAME_INFO_DOGGO_RIGHT = PhotoImage(file='QR.png')
CONTROLS_DOGGO_LEFT = PhotoImage(file='CL.png')
CONTROLS_DOGGO_RIGHT = PhotoImage(file='CR.png')
LEADERBOARD_DOGGO_LEFT = PhotoImage(file='LL.png')
LEADERBOARD_DOGGO_RIGHT = PhotoImage(file='LR.png')
GAME_OVER_DOGGO = PhotoImage(file='G_O.png')
NAME_GETTER_DOGGO_LEFT = PhotoImage(file='NGL.png')
NAME_GETTER_DOGGO_RIGHT = PhotoImage(file='NGR.png')
BETWEEN_LEVEL_DOGGO_LEFT = PhotoImage(file='BLL.png')
BETWEEN_LEVEL_DOGGO_RIGHT = PhotoImage(file='BLR.png')


# I've changed the Button's settings such that it changes colour when a mouse
# hovers over it with a class.

class HoverButton(Button):

    def __init__(self, master, **kw):
        tk.Button.__init__(self, master=master, **kw)
        self.defaultBackground = self['background']
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground


# The boss key is bound to the 'UP' arrow key and it's exit is the 'DOWN' arrow
# key. I've chosen these ones because in the game the player would use the
# 'LEFT' and 'RIGHT' arrow keys, so it's much easier for them to switch
# as quickly as possible.

root.bind('<Up>', lambda event: bossKey())
root.bind('<Down>', lambda event: returnFromBossKey())

# GLOBAL VARIABLES START #

dogFactIndex = IntVar()
dogFactIndex.set(rand(0, 9))  # New dog fact everytime the game is booted up.

currScore = IntVar()
currScore.set(0)

bigScore = IntVar()
bigScore.set(0)

currLevel = IntVar()
currLevel.set(0)

controlLeft = StringVar()
controlLeft.set('<Left>')

controlRight = StringVar()
controlRight.set('<Right>')

controlWinCheatCode = StringVar()
controlWinCheatCode.set('<w>')

controlIncreaseScore = StringVar()
controlIncreaseScore.set('<t>')

controlIncreaseSpeed = StringVar()
controlIncreaseSpeed.set('<s>')

controlDecreaseSpeed = StringVar()
controlDecreaseSpeed.set('<d>')

# I need to save the original keybindings, so I can revert them to their
# default if the player chooses to reset controls.

originalKeybindLeft = StringVar()
originalKeybindLeft.set(controlLeft.get())
originalKeybindRight = StringVar()
originalKeybindRight.set(controlRight.get())
originalKeybindWin = StringVar()
originalKeybindWin.set(controlWinCheatCode.get())
originalKeybindAddTen = StringVar()
originalKeybindAddTen.set(controlIncreaseScore.get())
originalKeybindPlusSpeed = StringVar()
originalKeybindPlusSpeed.set(controlIncreaseSpeed.get())
originalKeybindMinusSpeed = StringVar()
originalKeybindMinusSpeed.set(controlDecreaseSpeed.get())

# I need these for updating the leaderboard.

firstPlayerName = StringVar()
secondPlayerName = StringVar()
thirdPlayerName = StringVar()
fourthPlayerName = StringVar()
fifthPlayerName = StringVar()
sixthPlayerName = StringVar()
firstPlayerScore = IntVar()
secondPlayerScore = IntVar()
thirdPlayerScore = IntVar()
fourthPlayerScore = IntVar()
fifthPlayerScore = IntVar()
sixthPlayerScore = IntVar()

firstPlayerName.set('-')
secondPlayerName.set('-')
thirdPlayerName.set('-')
fourthPlayerName.set('-')
fifthPlayerName.set('-')
sixthPlayerName.set('-')
firstPlayerScore.set(0)
secondPlayerScore.set(0)
thirdPlayerScore.set(0)
fourthPlayerScore.set(0)
fifthPlayerScore.set(0)
sixthPlayerScore.set(0)

playerName = ''

# I need these because the dog needs to be able to turn left and right.

goingLeft = BooleanVar()
goingLeft.set(True)

# I need these because the pause button shouldn't work unless the player is
# playing.

inPLAY = BooleanVar()
inPLAY.set(False)

dogCoordsBeforePause = StringVar()

# I need these because with these global variables I can easily change the
# dog's speed.

global add_XL
global add_XR
add_XL = -10
add_XR = 10


# GLOBAL VARIABLES END #

# FRAME SWITCHER FUNCTIONS START #

def showMAIN_MENU():
    inPLAY.set(False)
    PLAY.grid_forget()
    LEADERBOARD.grid_forget()
    GAME_INFO.grid_forget()
    BETWEEN_LEVEL.grid_forget()
    CONTROLS.grid_forget()
    GAME_OVER.grid_forget()
    NAME_GETTER.grid_forget()
    MAIN_MENU.grid()


def showPLAY():
    MAIN_MENU.grid_forget()
    LEADERBOARD.grid_forget()
    GAME_INFO.grid_forget()
    BETWEEN_LEVEL.grid_forget()
    inPLAY.set(True)
    PLAY.grid()
    dogStartPosition()
    currScore.set(0)
    global add_XL
    global add_XR
    add_XL = -10
    add_XR = 10
    LEVEL_1()  # Actually starts the game.


def showGAME_INFO():
    MAIN_MENU.grid_forget()
    GAME_INFO.grid()


def showLEADERBOARD():
    MAIN_MENU.grid_forget()
    LEADERBOARD.grid()


def showCONTROLS():
    MAIN_MENU.grid_forget()
    leftButtonEntry.delete(0, 'end')
    rightButtonEntry.delete(0, 'end')
    winCheatCodeEntry.delete(0, 'end')
    increaseScoreCheatCodeEntry.delete(0, 'end')
    increaseSpeedCheatCodeEntry.delete(0, 'end')
    decreaseSpeedCheatCodeEntry.delete(0, 'end')
    CONTROLS.grid()


def showNAME_GETTER():
    BETWEEN_LEVEL.grid_forget()
    NAME_GETTER.grid()


def showGAME_OVER():
    currScore.set(0)
    bigScore.set(0)
    inPLAY.set(False)
    PLAY.grid_forget()
    BETWEEN_LEVEL.grid_forget()
    GAME_OVER.grid()


def exitGame():
    exit()


def bossKey(event=None):
    MAIN_MENU.grid_forget()
    inPLAY.set(False)
    PLAY.grid_forget()
    LEADERBOARD.grid_forget()
    GAME_INFO.grid_forget()
    BETWEEN_LEVEL.grid_forget()
    NAME_GETTER.grid_forget()
    GAME_OVER.grid_forget()

    # PAUSE.grid_forget()

    currScore.set(0)  # they have essentially left the game
    bigScore.set(0)
    currLevel.set(0)
    BOSS_KEY.grid()


def returnFromBossKey(event=None):
    BOSS_KEY.grid_forget()

    for i in range(len(goodFoods)):
        try:
            gameZone.delete(goodFoods[i])
        except:
            pass
    goodFoods.clear()

    for i in range(len(badFoods)):
        try:
            gameZone.delete(badFoods[i])
        except:

            pass
    badFoods.clear()

    for i in range(len(trash)):
        try:
            gameZone.delete(trash[i])
        except:

            pass
    trash.clear()

    for i in range(len(treats)):
        try:
            gameZone.delete(treats[i])
        except:

            pass
    treats.clear()

    playerNameEntry.delete(0, 'end')
    playerNameEntry.insert(0, '')
    currScore.set(0)
    bigScore.set(0)
    showMAIN_MENU()


def layoutMenu():
    title = Label(
        MAIN_MENU,
        text='DOGGO.EXE',
        font=('UBUNTU', 100, 'bold'),
        bg='black',
        fg='white',
        width=14,
        height=1,
        )
    title.grid(column=2, row=2, columnspan=2)
    PLAYButton = Button(
        MAIN_MENU,
        text='PLAY',
        font=('Times', 50, 'bold italic'),
        bg='black',
        fg='white',
        activebackground='white',
        width=16,
        height=2,
        command=showPLAY,
        borderwidth=10,
        relief='groove',
        )
    GAME_INFOButton = Button(
        MAIN_MENU,
        text='GAME INFO',
        font=('Times', 50, 'bold italic'),
        bg='black',
        fg='white',
        activebackground='white',
        width=16,
        height=2,
        command=showGAME_INFO,
        borderwidth=10,
        relief='groove',
        )
    LEADERBOARDButton = Button(
        MAIN_MENU,
        text='LEADERBOARD',
        font=('Times', 50, 'bold italic'),
        bg='black',
        fg='white',
        activebackground='white',
        width=16,
        height=2,
        command=showLEADERBOARD,
        borderwidth=10,
        relief='groove',
        )

    LOADButton = Button(
        MAIN_MENU,
        text='LOAD',
        font=('Times', 50, 'bold italic'),
        bg='black',
        fg='white',
        activebackground='white',
        width=16,
        height=2,
        command=loadGame,
        borderwidth=10,
        relief='groove',
        )
    CONTROLSButton = Button(
        MAIN_MENU,
        text='CONTROLS',
        font=('Times', 50, 'bold italic'),
        bg='black',
        fg='white',
        activebackground='white',
        width=16,
        height=2,
        command=showCONTROLS,
        borderwidth=10,
        relief='groove',
        )
    QUITButton = Button(
        MAIN_MENU,
        text='QUIT',
        font=('Times', 50, 'bold italic'),
        bg='black',
        fg='white',
        activebackground='white',
        width=16,
        height=2,
        command=exitGame,
        borderwidth=10,
        relief='groove',
        )

    paddingTop = Label(MAIN_MENU, height=6, bg='black')
    paddingTop.grid(column=2, row=1)

    paddingBetweenTitleAndMenu = Label(
        MAIN_MENU,
        height=2,
        bg='black',
        fg='white',
        text=dogFacts[dogFactIndex.get()],
        anchor='n',
        font=('Times', 30, 'bold italic'),
        )
    paddingBetweenTitleAndMenu.grid(column=2, row=3, columnspan=2)

    paddingBelowMenu = Label(MAIN_MENU, height=3, bg='black')
    paddingBelowMenu.grid(column=2, row=7)

    PLAYButton.grid(column=2, row=4)
    GAME_INFOButton.grid(column=2, row=5)
    LEADERBOARDButton.grid(column=2, row=6)
    LOADButton.grid(column=3, row=4)
    CONTROLSButton.grid(column=3, row=5)
    QUITButton.grid(column=3, row=6)

    leftCanvas = Canvas(MAIN_MENU, height=880, width=380, bg='black',
                        highlightthickness=0)
    leftCanvas.grid(row=1, column=1, rowspan=9)
    leftCanvas.create_image(250, 130, image=MAIN_MENU_DOGGO_RIGHT)

    rightCanvas = Canvas(MAIN_MENU, height=880, width=400, bg='black',
                         highlightthickness=0)
    rightCanvas.grid(row=1, column=4, rowspan=9)
    rightCanvas.create_image(100, 130, image=MAIN_MENU_DOGGO_LEFT)


# FRAME SWITCHER FUNCTIONS END #

# The updateScore() function is used throughout the whole PLAY section of the
# game and can easily increase or decrease the player's score.

def updateScore(points):
    currScore.set(currScore.get() + points)


# The levelSwitcher() function takes one integer arguemnt (current level) and
# switches from the PLAY frame to the BETWEEN_LEVEL frame.

def levelSwitcher(current):
    inPLAY.set(False)
    PLAY.grid_forget()
    BETWEEN_LEVEL.grid()
    toTwo.grid_forget()
    toThree.grid_forget()
    toFour.grid_forget()
    toFive.grid_forget()
    toSix.grid_forget()
    toEndless.grid_forget()
    if current == 1:
        toTwo.grid(row=4, column=2)
    elif current == 2:
        toThree.grid(row=4, column=2)
    elif current == 3:
        toFour.grid(row=4, column=2)
    elif current == 4:
        toFive.grid(row=4, column=2)
    elif current == 5:
        toSix.grid(row=4, column=2)
    elif current == 6:
        toEndless.grid(row=4, column=2)


# I need this global variable so I can keep track when the game is paused.

inPause = BooleanVar()
inPause.set(False)


# The pause() function is bound to the 'p' key and pauses play when pressed.

def pause(event):
    if inPLAY.get():
        PLAY.grid_forget()
        PAUSE.grid()
        coords = str(gameZone.coords(dog))
        dogCoordsBeforePause.set(coords)
        inPause.set(True)


# The breakPause() function is bound to the 'u' key (for 'Unpause') and
# unpauses the game when pressed.

def breakPause(event):
    if inPLAY.get() and inPause.get():
        PAUSE.grid_forget()
        PLAY.grid()
        coords = dogCoordsBeforePause.get()
        coords = coords[1:]
        coords = coords[:-10]
        gameZone.coords(dog, coords, 676)
        inPause.set(False)


# These bind the pause() and breakPause() functions.

root.bind('<p>', pause)  # 'p' for Pause.
root.bind('<u>', breakPause)  # 'u' for Unpause.


# The stopLevel() function is the actual pausing mechanism. It checks if
# inPause is true and acts accordingly.

def stopLevel():
    time.sleep(0.1)
    if inPause.get():
        root.after(300, stopLevel)
    else:
        return


# LEVELS START #

# LEVEL 1 #

def LEVEL_1():
    currLevel.set(1)
    inPLAY.set(True)
    levelLabel = Label(
        scoreBoard,
        font=('Ubuntu', 40),
        width=10,
        bg='black',
        fg='white',
        text='LEVEL: ' + str(currLevel.get()),
        )
    levelLabel.place(x=5, y=10)

# SETTINGS #

    num_goodFoods = 1  # Number of the good apples that will spawn at the same
    # time.

    secondsBeforeNewSpawn = 5  # Seconds counted before a new number of good
    # apples is spawned.

    foodSpeedOfGoodApples = 5  # Speed of good apples.

    maxAmountOfGoodApples = 3  # Maximum amount of good apples that can be
    # on-screen at the same time.

    pointsToWin = 100  # Points necessary to win current level.
    normal_applePoints = 10  # Points awarded when a player gets a good apple.

# Here I populate the list with one apple and I use the list thoughout the
# whole loop.

    for i in range(num_goodFoods):
        random_X0 = rand(100, 1500)
        goodFoods.append(gameZone.create_image(random_X0, 0,
                         image=normal_appleImg))

# I need this to check for elapsed time.

    start = time.time()

# LEVEL LOOP #

    while currScore.get() < pointsToWin - 1 and currScore.get() >= 0:
        if inPause.get():
            stopLevel()

# Loop responsible for the good apples.

        for i in range(len(goodFoods)):
            foodPosition = gameZone.coords(goodFoods[i])
            if foodPosition == []:
                continue
            gameZone.move(goodFoods[i], 0, foodSpeedOfGoodApples)
            if foodPosition[1] > 950:
                random_X0 = rand(100, 1500)
                random_Y0 = rand(-500, -50)
                gameZone.coords(goodFoods[i], random_X0, random_Y0)
                root.update()
                root.update_idletasks()
                continue
            dogPosition = gameZone.coords(dog)
            dogPosition[0] = dogPosition[0] - 190
            dogPosition[1] = dogPosition[1] + 70
            dogPosition.append(dogPosition[0] + 200)  # Adding x1 for dog.
            dogPosition.append(dogPosition[1] + 200)  # Adding y1 for dog.
            foodPosition.append(foodPosition[0] + 100)  # Adding x1 for good
            # apple.
            foodPosition.append(foodPosition[1] + 100)  # Adding y1 for good
            # apple.
            if foodPosition[0] < dogPosition[2] and foodPosition[2] \
            > dogPosition[0] and foodPosition[1] < dogPosition[3] \
            and foodPosition[3] > dogPosition[1]:
                if not goingLeft.get():
                    # Checking in which direction must the dog face.
                    gameZone.itemconfig(dog, image=imgJump)
                    root.update()
                    root.update_idletasks()
                    gameZone.move(dog, 0, -30)
                    root.update()
                    root.update_idletasks()
                    time.sleep(0.05)
                    gameZone.move(dog, 0, 30)
                    root.update()
                    root.update_idletasks()
                    gameZone.itemconfig(dog, image=img)
                else:
                    gameZone.itemconfig(dog, image=imgJump1)
                    root.update()
                    root.update_idletasks()
                    gameZone.move(dog, 0, -30)
                    root.update()
                    root.update_idletasks()
                    time.sleep(0.05)
                    gameZone.move(dog, 0, 30)
                    root.update()
                    root.update_idletasks()
                    gameZone.itemconfig(dog, image=img1)
                random_X0 = rand(100, 1500)
                gameZone.coords(goodFoods[i], random_X0, -50)
                root.update()
                root.update_idletasks()
                updateScore(normal_applePoints)
                root.update()
                root.update_idletasks()

# After a certain amount of time the game will spawn more good apples.

            if time.time() - start > secondsBeforeNewSpawn \
                and len(goodFoods) < maxAmountOfGoodApples:
                start = time.time()
                random_X0 = rand(100, 1500)
                goodFoods.append(gameZone.create_image(random_X0, 0,
                                 image=normal_appleImg))
        time.sleep(0.02)
        root.update()
    bigScore.set(currScore.get() + bigScore.get())

# Before moving to Level 2 I need to make sure there are no leftover apples
# from Level 1.

    for i in range(len(goodFoods)):
        gameZone.delete(goodFoods[i])

    goodFoods.clear()

# The loop has ended, here I check whether it's because the player lost or won
# the level. I need to make sure that the current score is zero, as it would
# otherwise carry to the next level, but I can't nullify it before the check,
# as I need to see what it's value is.
    currScore.set(0)
    if currScore.get() < 0:
        currScore.set(0)
        showGAME_OVER()
    else:
        currScore.set(0)
        levelSwitcher(1)


# LEVEL 2 #

def LEVEL_2():
    currLevel.set(2)
    inPLAY.set(True)
    levelLabel = Label(
        scoreBoard,
        font=('Ubuntu', 40),
        width=10,
        bg='black',
        fg='white',
        text='LEVEL: ' + str(currLevel.get()),
        )
    levelLabel.place(x=5, y=10)
    BETWEEN_LEVEL.grid_forget()
    PLAY.grid()

# SETTINGS #

    dogStartPosition()  # Whenever a new level starts, I need to make sure the
# dog starts in it's default position.

    num_goodFoods = 1  # Number of the good apples that will spawn at the same
    # time.
    num_badFoods = 2  # Number of the bad apples that will spawn at the same
    # time.

    secondsBeforeNewGoodAppleSpawn = 10  # Seconds counted before a new number
    # of good apples is spawned.
    secondsBeforeNewBadAppleSpawn = 8  # Seconds counted before a new number
    # of bad apples is spawned.

    foodSpeedOfGoodApples = 10  # Speed of good apples.
    foodSpeedOfBadApples = 13  # Speed of bad apples.

    maxAmountOfGoodApples = 2  # Maximum amount of good apples that can be
    # on-screen at the same time.
    maxAmountOfBadApples = 6  # Maximum amount of bad apples that can be
    # on-screen at the same time.

    pointsToWin = 100  # Points necessary to win current level.
    normal_applePoints = 10  # Points awarded when a player gets a good apple.
    rotten_applePoints = -15  # Points subtracted when a player gets a
    # bad apple.

# Here I populate the list with one good apple and I use the list thoughout
# the whole loop.

    for i in range(num_goodFoods):
        random_X0 = rand(100, 1500)
        goodFoods.append(gameZone.create_image(random_X0, 0,
                         image=normal_appleImg))

# Here I populate the list with one bad apple and I use the list thoughout
# the whole loop.

    for i in range(num_badFoods):
        random_X0 = rand(100, 1500)
        badFoods.append(gameZone.create_image(random_X0, 0,
                        image=rotten_appleImg))

# I need this to check for elapsed time.

    start = time.time()

# LEVEL LOOP #

    while currScore.get() < pointsToWin - 1 and currScore.get() >= 0:
        if inPause.get():
            stopLevel()

# Loop responsible for the good apples.

        for i in range(len(goodFoods)):
            goodFoodPosition = gameZone.coords(goodFoods[i])
            if goodFoodPosition == []:
                continue
            gameZone.move(goodFoods[i], 0, foodSpeedOfGoodApples)
            if goodFoodPosition[1] > 950:
                random_X0 = rand(100, 1500)
                random_Y0 = rand(-500, -50)
                gameZone.coords(goodFoods[i], random_X0, random_Y0)
                root.update()
                root.update_idletasks()
                continue
            dogPosition = gameZone.coords(dog)
            dogPosition[0] = dogPosition[0] - 190
            dogPosition[1] = dogPosition[1] + 70
            dogPosition.append(dogPosition[0] + 200)  # Adding x1 for dog.
            dogPosition.append(dogPosition[1] + 200)  # Adding y1 for dog.
            goodFoodPosition.append(goodFoodPosition[0] + 100)  # Adding x1 for
            # good apple.
            goodFoodPosition.append(goodFoodPosition[1] + 100)  # Adding y1 for
            # good apple.
            if goodFoodPosition[0] < dogPosition[2] \
                and goodFoodPosition[2] > dogPosition[0] \
                and goodFoodPosition[1] < dogPosition[3] \
                and goodFoodPosition[3] > dogPosition[1]:
                if not goingLeft.get():  # Checking in which direction must the
                # dog face.
                    gameZone.itemconfig(dog, image=imgJump)
                    root.update()
                    root.update_idletasks()
                    gameZone.move(dog, 0, -30)
                    root.update()
                    root.update_idletasks()
                    time.sleep(0.05)
                    gameZone.move(dog, 0, 30)
                    root.update()
                    root.update_idletasks()
                    gameZone.itemconfig(dog, image=img)
                else:
                    gameZone.itemconfig(dog, image=imgJump1)
                    root.update()
                    root.update_idletasks()
                    gameZone.move(dog, 0, -30)
                    root.update()
                    root.update_idletasks()
                    time.sleep(0.05)
                    gameZone.move(dog, 0, 30)
                    root.update()
                    root.update_idletasks()
                    gameZone.itemconfig(dog, image=img1)
                random_X0 = rand(100, 1500)
                gameZone.coords(goodFoods[i], random_X0, -50)
                root.update()
                root.update_idletasks()
                updateScore(normal_applePoints)
                root.update()
                root.update_idletasks()

# After a certain amount of time the game will spawn more good apples.

            if time.time() - start > secondsBeforeNewGoodAppleSpawn \
                and len(goodFoods) < maxAmountOfGoodApples:
                start = time.time()
                random_X0 = rand(100, 1500)
                goodFoods.append(gameZone.create_image(random_X0, 0,
                                 image=normal_appleImg))
        time.sleep(0.02)
        root.update()

# Loop responsible for the bad apples.

        for i in range(len(badFoods)):
            badFoodPosition = gameZone.coords(badFoods[i])
            if badFoodPosition == []:
                continue
            gameZone.move(badFoods[i], 0, foodSpeedOfBadApples)
            if badFoodPosition[1] > 950:
                random_X0 = rand(100, 1500)
                random_Y0 = rand(-500, -50)
                gameZone.coords(badFoods[i], random_X0, random_Y0)
                root.update()
                root.update_idletasks()
                continue
            dogPosition = gameZone.coords(dog)
            dogPosition[0] = dogPosition[0] - 190
            dogPosition[1] = dogPosition[1] + 70
            dogPosition.append(dogPosition[0] + 200)  # Adding x1 for dog.
            dogPosition.append(dogPosition[1] + 200)  # Adding y1 for dog.
            badFoodPosition.append(badFoodPosition[0] + 100)  # Adding x1 for
            # bad apple.
            badFoodPosition.append(badFoodPosition[1] + 100)  # Adding y1 for
            # bad apple.
            if badFoodPosition[0] < dogPosition[2] \
                and badFoodPosition[2] > dogPosition[0] \
                and badFoodPosition[1] < dogPosition[3] \
                and badFoodPosition[3] > dogPosition[1]:
                if not goingLeft.get():  # Checking in which direction must the
                # dog face.
                    gameZone.itemconfig(dog, image=imgJump)
                    root.update()
                    root.update_idletasks()
                    gameZone.move(dog, 0, -30)
                    root.update()
                    root.update_idletasks()
                    time.sleep(0.05)
                    gameZone.move(dog, 0, 30)
                    root.update()
                    root.update_idletasks()
                    gameZone.itemconfig(dog, image=img)
                else:
                    gameZone.itemconfig(dog, image=imgJump1)
                    root.update()
                    root.update_idletasks()
                    gameZone.move(dog, 0, -30)
                    root.update()
                    root.update_idletasks()
                    time.sleep(0.05)
                    gameZone.move(dog, 0, 30)
                    root.update()
                    root.update_idletasks()
                    gameZone.itemconfig(dog, image=img1)
                random_X0 = rand(100, 1500)
                gameZone.coords(badFoods[i], random_X0, -50)
                root.update()
                root.update_idletasks()
                updateScore(rotten_applePoints)
                root.update()
                root.update_idletasks()

# After a certain amount of time the game will spawn more bad apples.

            if time.time() - start > secondsBeforeNewBadAppleSpawn \
                and len(badFoods) < maxAmountOfBadApples:
                start = time.time()
                random_X0 = rand(100, 1500)
                badFoods.append(gameZone.create_image(random_X0, 0,
                                image=rotten_appleImg))
        time.sleep(0.02)
        root.update()
    bigScore.set(currScore.get() + bigScore.get())

# Before moving to Level 3 I need to make sure there are no leftover apples
# from Level 2.

    for i in range(len(goodFoods)):
        gameZone.delete(goodFoods[i])
    for i in range(len(badFoods)):
        gameZone.delete(badFoods[i])

    goodFoods.clear()
    badFoods.clear()

# The loop has ended, here I check whether it's because the player lost or won
# the level. I need to make sure that the current score is zero, as it would
# otherwise carry to the next level, but I can't nullify it before the check,
# as I need to see what it's value is.
    if currScore.get() < 0:
        currScore.set(0)
        showGAME_OVER()
    else:
        currScore.set(0)
        levelSwitcher(2)


# LEVEL 3 #

def LEVEL_3():
    currLevel.set(3)
    inPLAY.set(True)
    levelLabel = Label(
        scoreBoard,
        font=('Ubuntu', 40),
        width=10,
        bg='black',
        fg='white',
        text='LEVEL: ' + str(currLevel.get()),
        )
    levelLabel.place(x=5, y=10)
    BETWEEN_LEVEL.grid_forget()
    PLAY.grid()

# SETTINGS #

    dogStartPosition()  # Whenever a new level starts, I need to make sure the
    # dog starts in it's default position.

    num_goodFoods = 2  # Number of the good apples that will spawn at the
    # same time
    num_badFoods = 3  # Number of the bad apples that will spawn at the
    # same time.   .

    secondsBeforeNewGoodAppleSpawn = 10  # Seconds counted before a new number
    # of good apples is spawned.
    secondsBeforeNewBadAppleSpawn = 5  # Seconds counted before a new number
    # of bad apples is spawned.

    foodSpeedOfGoodApples = 10  # Speed of good apples.
    foodSpeedOfBadApples = 15  # Speed of bad apples.
    foodSpeedOfChoco = 10  # Speed of chocolate.

    maxAmountOfGoodApples = 3  # Maximum amount of good apples that can be
    # on-screen at the same time.
    maxAmountOfBadApples = 7  # Maximum amount of bad apples that can be
    # on-screen at the same time.
    # Maximum amount of chocolates is ensured to be one.

    pointsToWin = 100  # Points necessary to win current level.
    normal_applePoints = 10  # Points awarded when a player gets a good apple.
    rotten_applePoints = -25  # Points subtracted when a player gets a bad
    # apple.
    chocoPoints = -15  # Points subtracted when a player gets a chocolate.

    chocoFlag = False
    neverChocoAgain = False
    dogSpeedIncrease = 40  # The speed with which dog will be faster after
    # eating a chocolate.

# Here I populate the list with one good apple and I use the list thoughout
# the whole loop.

    for i in range(num_goodFoods):
        random_X0 = rand(100, 1500)
        goodFoods.append(gameZone.create_image(random_X0, 0,
                         image=normal_appleImg))

# Here I populate the list with one bad apple and I use the list thoughout
# the whole loop.

    for i in range(num_badFoods):
        random_X0 = rand(100, 1500)
        badFoods.append(gameZone.create_image(random_X0, 0,
                        image=rotten_appleImg))

# Here I create one chocolate that I will use once in the level.

    random_X0 = rand(100, 1500)
    choco = gameZone.create_image(random_X0, -100, image=chocoImg)

# I need this to check for elapsed time.

    start = time.time()

# LEVEL LOOP #

    while currScore.get() < pointsToWin - 1 and currScore.get() >= 0:
        if inPause.get():
            stopLevel()

# Loop responsible for the good apples.

        for i in range(len(goodFoods)):
            goodFoodPosition = gameZone.coords(goodFoods[i])
            if goodFoodPosition == []:
                continue
            gameZone.move(goodFoods[i], 0, foodSpeedOfGoodApples)
            if goodFoodPosition[1] > 950:
                random_X0 = rand(100, 1500)
                random_Y0 = rand(-500, -50)
                gameZone.coords(goodFoods[i], random_X0, random_Y0)
                root.update()
                root.update_idletasks()
                continue
            dogPosition = gameZone.coords(dog)
            dogPosition[0] = dogPosition[0] - 190
            dogPosition[1] = dogPosition[1] + 70
            dogPosition.append(dogPosition[0] + 200)  # Adding x1 for dog.
            dogPosition.append(dogPosition[1] + 200)  # Adding y1 for dog.
            goodFoodPosition.append(goodFoodPosition[0] + 100)  # Adding x1 for
            # good apple.
            goodFoodPosition.append(goodFoodPosition[1] + 100)  # Adding y1 for
            # good apple.
            if goodFoodPosition[0] < dogPosition[2] \
                and goodFoodPosition[2] > dogPosition[0] \
                and goodFoodPosition[1] < dogPosition[3] \
                and goodFoodPosition[3] > dogPosition[1]:
                if not goingLeft.get():  # Checking in which direction must the
                # dog face.
                    gameZone.itemconfig(dog, image=imgJump)
                    root.update()
                    root.update_idletasks()
                    gameZone.move(dog, 0, -30)
                    root.update()
                    root.update_idletasks()
                    time.sleep(0.05)
                    gameZone.move(dog, 0, 30)
                    root.update()
                    root.update_idletasks()
                    gameZone.itemconfig(dog, image=img)
                else:
                    gameZone.itemconfig(dog, image=imgJump1)
                    root.update()
                    root.update_idletasks()
                    gameZone.move(dog, 0, -30)
                    root.update()
                    root.update_idletasks()
                    time.sleep(0.05)
                    gameZone.move(dog, 0, 30)
                    root.update()
                    root.update_idletasks()
                    gameZone.itemconfig(dog, image=img1)
                random_X0 = rand(100, 1500)
                gameZone.coords(goodFoods[i], random_X0, -50)
                root.update()
                root.update_idletasks()
                updateScore(normal_applePoints)
                root.update()
                root.update_idletasks()

# After a certain amount of time the game will spawn more good apples.

            if time.time() - start > secondsBeforeNewGoodAppleSpawn \
                and len(goodFoods) < maxAmountOfGoodApples:
                start = time.time()
                random_X0 = rand(100, 1500)
                goodFoods.append(gameZone.create_image(random_X0, 0,
                                 image=normal_appleImg))
        time.sleep(0.02)
        root.update()

# Loop responsible for the chocolate.

        if currScore.get() >= 30 and currScore.get() <= 70 or chocoFlag:
            if neverChocoAgain:
                pass
            else:
                chocoPosition = gameZone.coords(choco)
                chocoFlag = True
                gameZone.move(choco, 0, foodSpeedOfChoco)
                if chocoPosition[1] > 950:
                    gameZone.delete(choco)
                    chocoFlag = False
                    neverChocoAgain = True
                dogPosition = gameZone.coords(dog)
                dogPosition[0] = dogPosition[0] - 190
                dogPosition[1] = dogPosition[1] + 70
                dogPosition.append(dogPosition[0] + 200)  # Adding x1 for dog.
                dogPosition.append(dogPosition[1] + 200)  # Adding y1 for dog.
                chocoPosition.append(chocoPosition[0] + 100)  # Adding x1 for
                # chocolate.
                chocoPosition.append(chocoPosition[1] + 100)  # Adding x1 for
                # chocolate.
                if chocoPosition[0] < dogPosition[2] \
                    and chocoPosition[2] > dogPosition[0] \
                    and chocoPosition[1] < dogPosition[3] \
                    and chocoPosition[3] > dogPosition[1]:
                    if not goingLeft.get():  # Checking in which direction must
                    # the dog face.
                        gameZone.itemconfig(dog, image=imgJump)
                        root.update()
                        root.update_idletasks()
                        gameZone.move(dog, 0, -30)
                        root.update()
                        root.update_idletasks()
                        time.sleep(0.05)
                        gameZone.move(dog, 0, 30)
                        root.update()
                        root.update_idletasks()
                        gameZone.itemconfig(dog, image=img)
                    else:
                        gameZone.itemconfig(dog, image=imgJump1)
                        root.update()
                        root.update_idletasks()
                        gameZone.move(dog, 0, -30)
                        root.update()
                        root.update_idletasks()
                        time.sleep(0.05)
                        gameZone.move(dog, 0, 30)
                        root.update()
                        root.update_idletasks()
                        gameZone.itemconfig(dog, image=img1)
                    global add_XL
                    global add_XR
                    add_XL = -dogSpeedIncrease  # Changing the dog speed going
                    # left.
                    add_XR = dogSpeedIncrease  # Changing the dog speed going
                    # right.
                    gameZone.delete(choco)
                    chocoFlag = False
                    neverChocoAgain = True
                    updateScore(chocoPoints)
                    root.update()
                    root.update_idletasks()
        time.sleep(0.03)
        root.update()

# Loop responsible for the bad apples.

        for i in range(len(badFoods)):
            badFoodPosition = gameZone.coords(badFoods[i])
            if badFoodPosition == []:
                continue
            gameZone.move(badFoods[i], 0, foodSpeedOfBadApples)
            if badFoodPosition[1] > 950:
                random_X0 = rand(100, 1500)
                random_Y0 = rand(-500, -50)
                gameZone.coords(badFoods[i], random_X0, random_Y0)
                root.update()
                root.update_idletasks()
                continue
            dogPosition = gameZone.coords(dog)
            dogPosition[0] = dogPosition[0] - 190
            dogPosition[1] = dogPosition[1] + 70
            dogPosition.append(dogPosition[0] + 200)  # Adding x1 for dog.
            dogPosition.append(dogPosition[1] + 200)  # Adding y1 for dog.
            badFoodPosition.append(badFoodPosition[0] + 100)  # Adding x1 for
            # bad apple.
            badFoodPosition.append(badFoodPosition[1] + 100)  # Adding y1 for
            # bad apple.
            if badFoodPosition[0] < dogPosition[2] \
                and badFoodPosition[2] > dogPosition[0] \
                and badFoodPosition[1] < dogPosition[3] \
                and badFoodPosition[3] > dogPosition[1]:
                if not goingLeft.get():  # Checking in which direction must the
                # dog face.
                    gameZone.itemconfig(dog, image=imgJump)
                    root.update()
                    root.update_idletasks()
                    gameZone.move(dog, 0, -30)
                    root.update()
                    root.update_idletasks()
                    time.sleep(0.05)
                    gameZone.move(dog, 0, 30)
                    root.update()
                    root.update_idletasks()
                    gameZone.itemconfig(dog, image=img)
                else:
                    gameZone.itemconfig(dog, image=imgJump1)
                    root.update()
                    root.update_idletasks()
                    gameZone.move(dog, 0, -30)
                    root.update()
                    root.update_idletasks()
                    time.sleep(0.05)
                    gameZone.move(dog, 0, 30)
                    root.update()
                    root.update_idletasks()
                    gameZone.itemconfig(dog, image=img1)
                random_X0 = rand(100, 1500)
                gameZone.coords(badFoods[i], random_X0, -50)
                root.update()
                root.update_idletasks()
                updateScore(rotten_applePoints)
                root.update()
                root.update_idletasks()

# After a certain amount of time the game will spawn more bad apples.

            if time.time() - start > secondsBeforeNewBadAppleSpawn \
                and len(badFoods) < maxAmountOfBadApples:
                start = time.time()
                random_X0 = rand(100, 1500)
                badFoods.append(gameZone.create_image(random_X0, 0,
                                image=rotten_appleImg))
        time.sleep(0.01)
        root.update()
        if time.time() - start > 12:
            start = time.time()
    bigScore.set(currScore.get() + bigScore.get())

# Before moving to Level 4 I need to make sure there are no leftover apples or
# a chocolate from Level 3.

    for i in range(len(goodFoods)):
        gameZone.delete(goodFoods[i])
    for i in range(len(badFoods)):
        gameZone.delete(badFoods[i])
    gameZone.delete(choco)

    goodFoods.clear()
    badFoods.clear()

# Before moving to Level 4 I need to make sure there the dog's speed is
# returned to normal in case the player ate a chocolate in this level.

    add_XL = -10
    add_XR = 10

# The loop has ended, here I check whether it's because the player lost or won
# the level. I need to make sure that the current score is zero, as it would
# otherwise carry to the next level, but I can't nullify it before the check,
# as I need to see what it's value is.

    if currScore.get() < 0:
        currScore.set(0)
        showGAME_OVER()
    else:
        currScore.set(0)
        levelSwitcher(3)


# LEVEL 4 #

def LEVEL_4():
    currLevel.set(4)
    inPLAY.set(True)
    levelLabel = Label(
        scoreBoard,
        font=('Ubuntu', 40),
        width=10,
        bg='black',
        fg='white',
        text='LEVEL: ' + str(currLevel.get()),
        )
    levelLabel.place(x=5, y=10)
    BETWEEN_LEVEL.grid_forget()
    PLAY.grid()

# SETTINGS #

    dogStartPosition()  # Whenever a new level starts, I need to make sure the
    # dog starts in it's default position.

    num_goodFoods = 1  # Number of the good apples that will spawn at the same
    # time.
    num_badFoods = 3  # Number of the bad apples that will spawn at the same
    # time.
    num_trash = 1  # Number of the trash cans that will spawn at the same time.

    secondsBeforeNewGoodAppleSpawn = 10  # Seconds counted before a new number
    # of good apples is spawned.
    secondsBeforeNewBadAppleSpawn = 10  # Seconds counted before a new number
    # of bad apples is spawned.
    secondsBeforeNewTrashSpawn = 10  # Seconds counted before a new number of
    # trash cans is spawned.

    foodSpeedOfGoodApples = 15  # Speed of good apples.
    foodSpeedOfBadApples = 20  # Speed of bad apples.
    foodSpeedOfChoco = 15  # Speed of chocolate.
    foodSpeedOfTrash = 15  # Speed of trash cans.

    maxAmountOfGoodApples = 2  # Maximum amount of good apples that can be
    # on-screen at the same time.
    maxAmountOfBadApples = 8  # Maximum amount of bad apples that can be
    # on-screen at the same time.
    # Maximum amount of chocolates is ensured to be one.

    maxAmountOfTrash = 2  # Maximum amount of trash cans that can be on-screen
    # at the same time.

    pointsToWin = 100  # Points necessary to win current level.
    normal_applePoints = 10  # Points awarded when a player gets a good apple.
    rotten_applePoints = -25  # Points subtracted when a player gets a bad
    # apple.
    chocoPoints = -15  # Points subtracted when a player gets a chocolate.
    trashPoints = -100  # Points subtracted when a player gets a trash
    # can (Game over).

    chocoFlag = False
    neverChocoAgain = False
    dogSpeedIncrease = 40  # The speed with which dog will be faster after
    # eating a chocolate.

# Here I populate the list with one good apple and I use the list thoughout
# the whole loop.

    for i in range(num_goodFoods):
        random_X0 = rand(100, 1500)
        goodFoods.append(gameZone.create_image(random_X0, 0,
                         image=normal_appleImg))

# Here I populate the list with one bad apple and I use the list thoughout
# the whole loop.

    for i in range(num_badFoods):
        random_X0 = rand(100, 1500)
        badFoods.append(gameZone.create_image(random_X0, 0,
                        image=rotten_appleImg))

# Here I create one chocolate that I will use once in the level.

    random_X0 = rand(100, 1500)
    choco = gameZone.create_image(random_X0, -100, image=chocoImg)

# Here I populate the list with one trash can and I use the list thoughout
# the whole loop.

    for i in range(num_trash):
        random_X0 = rand(100, 1500)
        trash.append(gameZone.create_image(random_X0, 0,
                     image=trashImg))

# I need this to check for elapsed time.

    start = time.time()

# LEVEL LOOP #

    while currScore.get() < pointsToWin - 1 and currScore.get() >= 0:
        if inPause.get():
            stopLevel()

# Loop responsible for the good apples.

        for i in range(len(goodFoods)):
            goodFoodPosition = gameZone.coords(goodFoods[i])
            if goodFoodPosition == []:
                continue
            gameZone.move(goodFoods[i], 0, foodSpeedOfGoodApples)
            if goodFoodPosition[1] > 950:
                random_X0 = rand(100, 1500)
                random_Y0 = rand(-500, -50)
                gameZone.coords(goodFoods[i], random_X0, random_Y0)
                root.update()
                root.update_idletasks()
                continue
            dogPosition = gameZone.coords(dog)
            dogPosition[0] = dogPosition[0] - 190
            dogPosition[1] = dogPosition[1] + 70
            dogPosition.append(dogPosition[0] + 200)  # Adding x1 for dog.
            dogPosition.append(dogPosition[1] + 200)  # Adding y1 for dog.
            goodFoodPosition.append(goodFoodPosition[0] + 100)  # Adding x1 for
            # good apple.
            goodFoodPosition.append(goodFoodPosition[1] + 100)  # Adding y1 for
            # good apple.
            if goodFoodPosition[0] < dogPosition[2] \
                and goodFoodPosition[2] > dogPosition[0] \
                and goodFoodPosition[1] < dogPosition[3] \
                and goodFoodPosition[3] > dogPosition[1]:
                if not goingLeft.get():  # Checking in which direction must the
                # dog face.
                    gameZone.itemconfig(dog, image=imgJump)
                    root.update()
                    root.update_idletasks()
                    gameZone.move(dog, 0, -30)
                    root.update()
                    root.update_idletasks()
                    time.sleep(0.05)
                    gameZone.move(dog, 0, 30)
                    root.update()
                    root.update_idletasks()
                    gameZone.itemconfig(dog, image=img)
                else:
                    gameZone.itemconfig(dog, image=imgJump1)
                    root.update()
                    root.update_idletasks()
                    gameZone.move(dog, 0, -30)
                    root.update()
                    root.update_idletasks()
                    time.sleep(0.05)
                    gameZone.move(dog, 0, 30)
                    root.update()
                    root.update_idletasks()
                    gameZone.itemconfig(dog, image=img1)
                random_X0 = rand(100, 1500)
                gameZone.coords(goodFoods[i], random_X0, -50)
                root.update()
                root.update_idletasks()
                updateScore(normal_applePoints)
                root.update()
                root.update_idletasks()

# After a certain amount of time the game will spawn more good apples.

            if time.time() - start > secondsBeforeNewGoodAppleSpawn \
            and len(goodFoods) < maxAmountOfGoodApples:
                start = time.time()
                random_X0 = rand(100, 1500)
                goodFoods.append(gameZone.create_image(random_X0, 0,
                                 image=normal_appleImg))
        time.sleep(0.02)
        root.update()

# Loop responsible for the chocolate.

        if currScore.get() >= 30 and currScore.get() <= 70 or chocoFlag:
            if neverChocoAgain:
                pass
            else:
                chocoPosition = gameZone.coords(choco)
                chocoFlag = True
                gameZone.move(choco, 0, foodSpeedOfChoco)
                if chocoPosition[1] > 950:
                    gameZone.delete(choco)
                    chocoFlag = False
                    neverChocoAgain = True
                dogPosition = gameZone.coords(dog)
                dogPosition[0] = dogPosition[0] - 190
                dogPosition[1] = dogPosition[1] + 70
                dogPosition.append(dogPosition[0] + 200)  # Adding x1 for dog.
                dogPosition.append(dogPosition[1] + 200)  # Adding y1 for dog.
                chocoPosition.append(chocoPosition[0] + 100)  # Adding x1 for
                # chocolate.
                chocoPosition.append(chocoPosition[1] + 100)  # Adding y1 for
                # chocolate.
                if chocoPosition[0] < dogPosition[2] \
                    and chocoPosition[2] > dogPosition[0] \
                    and chocoPosition[1] < dogPosition[3] \
                    and chocoPosition[3] > dogPosition[1]:
                    if not goingLeft.get():  # Checking in which direction must
                    # the dog face.
                        gameZone.itemconfig(dog, image=imgJump)
                        root.update()
                        root.update_idletasks()
                        gameZone.move(dog, 0, -30)
                        root.update()
                        root.update_idletasks()
                        time.sleep(0.05)
                        gameZone.move(dog, 0, 30)
                        root.update()
                        root.update_idletasks()
                        gameZone.itemconfig(dog, image=img)
                    else:
                        gameZone.itemconfig(dog, image=imgJump1)
                        root.update()
                        root.update_idletasks()
                        gameZone.move(dog, 0, -30)
                        root.update()
                        root.update_idletasks()
                        time.sleep(0.05)
                        gameZone.move(dog, 0, 30)
                        root.update()
                        root.update_idletasks()
                        gameZone.itemconfig(dog, image=img1)
                    global add_XL
                    global add_XR
                    add_XL = -dogSpeedIncrease  # Changing the dog speed
                    # going left.
                    add_XR = dogSpeedIncrease  # Changing the dog speed
                    # going right.
                    gameZone.delete(choco)
                    chocoFlag = False
                    neverChocoAgain = True
                    updateScore(chocoPoints)
                    root.update()
                    root.update_idletasks()
        time.sleep(0.03)
        root.update()

# Loop responsible for the trash cans.

        for i in range(len(trash)):
            trashPosition = gameZone.coords(trash[i])
            if trashPosition == []:
                continue
            gameZone.move(trash[i], 0, foodSpeedOfTrash)
            if trashPosition[1] > 950:
                random_X0 = rand(100, 1500)
                random_Y0 = rand(-500, -50)
                gameZone.coords(trash[i], random_X0, random_Y0)
                root.update()
                root.update_idletasks()
                continue
            dogPosition = gameZone.coords(dog)
            dogPosition[0] = dogPosition[0] - 190
            dogPosition[1] = dogPosition[1] + 70
            dogPosition.append(dogPosition[0] + 200)  # Adding x1 dor dog.
            dogPosition.append(dogPosition[1] + 200)  # Adding y1 for dog.
            trashPosition.append(trashPosition[0] + 100)  # Adding x1 dor
            #  trash can.
            trashPosition.append(trashPosition[1] + 100)  # Adding y1 for
            # trash can.
            if trashPosition[0] < dogPosition[2] and trashPosition[2] \
                > dogPosition[0] and trashPosition[1] < dogPosition[3] \
                and trashPosition[3] > dogPosition[1]:
                random_X0 = rand(100, 1500)  # The level will end, so there is
                # no need to check in which direction the dog must face.
                gameZone.coords(trash[i], random_X0, -50)
                root.update()
                root.update_idletasks()
                updateScore(trashPoints)
                root.update()
                root.update_idletasks()

# After a certain amount of time the game will spawn more trash cans.

            if time.time() - start > secondsBeforeNewTrashSpawn \
                and len(trash) < maxAmountOfTrash:
                start = time.time()
                random_X0 = rand(100, 1500)
                trash.append(gameZone.create_image(random_X0, 0,
                             image=trashImg))
        time.sleep(0.02)
        root.update()

# Loop responsible for the bad apples.

        for i in range(len(badFoods)):
            badFoodPosition = gameZone.coords(badFoods[i])
            if badFoodPosition == []:
                continue
            gameZone.move(badFoods[i], 0, foodSpeedOfBadApples)
            if badFoodPosition[1] > 950:
                random_X0 = rand(100, 1500)
                random_Y0 = rand(-500, -50)
                gameZone.coords(badFoods[i], random_X0, random_Y0)
                root.update()
                root.update_idletasks()
                continue
            dogPosition = gameZone.coords(dog)
            dogPosition[0] = dogPosition[0] - 190
            dogPosition[1] = dogPosition[1] + 70
            dogPosition.append(dogPosition[0] + 200)  # Adding x1 for dog.
            dogPosition.append(dogPosition[1] + 200)  # Adding y1 for dog.
            badFoodPosition.append(badFoodPosition[0] + 100)  # Adding x1 for
            # bad apple.
            badFoodPosition.append(badFoodPosition[1] + 100)  # Adding y1 for
            # bad apple.
            if badFoodPosition[0] < dogPosition[2] \
                and badFoodPosition[2] > dogPosition[0] \
                and badFoodPosition[1] < dogPosition[3] \
                and badFoodPosition[3] > dogPosition[1]:
                if not goingLeft.get():  # Checking in which direction must the
                # dog face.
                    gameZone.itemconfig(dog, image=imgJump)
                    root.update()
                    root.update_idletasks()
                    gameZone.move(dog, 0, -30)
                    root.update()
                    root.update_idletasks()
                    time.sleep(0.05)
                    gameZone.move(dog, 0, 30)
                    root.update()
                    root.update_idletasks()
                    gameZone.itemconfig(dog, image=img)
                else:
                    gameZone.itemconfig(dog, image=imgJump1)
                    root.update()
                    root.update_idletasks()
                    gameZone.move(dog, 0, -30)
                    root.update()
                    root.update_idletasks()
                    time.sleep(0.05)
                    gameZone.move(dog, 0, 30)
                    root.update()
                    root.update_idletasks()
                    gameZone.itemconfig(dog, image=img1)
                random_X0 = rand(100, 1500)
                gameZone.coords(badFoods[i], random_X0, -50)
                root.update()
                root.update_idletasks()
                updateScore(rotten_applePoints)
                root.update()
                root.update_idletasks()

# After a certain amount of time the game will spawn more bad apples.

            if time.time() - start > secondsBeforeNewBadAppleSpawn \
                and len(badFoods) < maxAmountOfBadApples:
                start = time.time()
                random_X0 = rand(100, 1500)
                badFoods.append(gameZone.create_image(random_X0, 0,
                                image=rotten_appleImg))
        time.sleep(0.01)
        root.update()
    bigScore.set(currScore.get() + bigScore.get())

# Before moving to Level 5 I need to make sure there are no leftover apples, a
# chocolate or trash cans from Level 4.

    for i in range(len(goodFoods)):
        gameZone.delete(goodFoods[i])
    for i in range(len(badFoods)):
        gameZone.delete(badFoods[i])
    gameZone.delete(choco)
    for i in range(len(trash)):
        gameZone.delete(trash[i])

    goodFoods.clear()
    badFoods.clear()
    trash.clear()

# Before moving to Level 5 I need to make sure there the dog's speed is
# returned to normal in case the player ate a chocolate in this level.

    add_XL = -10
    add_XR = 10

# The loop has ended, here I check whether it's because the player lost or won
# the level. I need to make sure that the current score is zero, as it would
# otherwise carry to the next level, but I can't nullify it before the check,
# as I need to see what it's value is.
    if currScore.get() < 0:
        currScore.set(0)
        showGAME_OVER()
    else:
        currScore.set(0)
        levelSwitcher(4)


# LEVEL 5 #

def LEVEL_5():
    currLevel.set(5)
    inPLAY.set(True)
    levelLabel = Label(
        scoreBoard,
        font=('Ubuntu', 40),
        width=10,
        bg='black',
        fg='white',
        text='LEVEL: ' + str(currLevel.get()),
        )
    levelLabel.place(x=5, y=10)
    BETWEEN_LEVEL.grid_forget()
    PLAY.grid()

# SETTINGS #

    dogStartPosition()  # Whenever a new level starts, I need to make sure the
    # dog starts in it's default position.

    num_goodFoods = 1  # Number of the good apples that will spawn at the same
    # time.
    num_badFoods = 1  # Number of the bad apples that will spawn at the same
    # time.
    num_trash = 1  # Number of the trash cans that will spawn at the same time.
    num_treats = 1  # Number of treats that will spawn at the same time.

    secondsBeforeNewGoodAppleSpawn = 10  # Seconds counted before a new number
    # of good apples is spawned.
    secondsBeforeNewBadAppleSpawn = 5  # Seconds counted before a new number of
    # bad apples is spawned.
    secondsBeforeNewTrashSpawn = 15  # Seconds counted before a new number of
    # trash cans is spawned.
    secondsBeforeNewTreatSpawn = 8  # Seconds counted before a new number of
    # treats is spawned.

    foodSpeedOfGoodApples = 20  # Speed of good apples.
    foodSpeedOfBadApples = 20  # Speed of bad apples.
    foodSpeedOfChoco = 20  # Speed of chocolate.
    foodSpeedOfTrash = 20  # Speed of trash cans.
    foodSpeedOfTreats = 20  # Speed of treats.

    maxAmountOfGoodApples = 2  # Maximum amount of good apples that can be
    # on-screen at the same time.
    maxAmountOfBadApples = 8  # Maximum amount of bad apples that can be
    # on-screen at the same time.
    # Maximum amount of chocolates is ensured to be one.

    maxAmountOfTrash = 3  # Maximum amount of trash cans that can be on-screen
    # at the same time.
    maxAmountOfTreats = 3  # Maximum amount of treats that can be on-screen
    # at the same time.

    pointsToWin = 100  # Points necessary to win current level.
    normal_applePoints = 10  # Points awarded when a player gets a good apple.
    rotten_applePoints = -25  # Points subtracted when a player gets a
    # bad apple.
    chocoPoints = -15  # Points subtracted when a player gets a chocolate.
    trashPoints = -100  # Points subtracted when a player gets a trash
    # can (Game over).
    treatPoints = 10  # Points awarded when a player gets a treat.

    chocoFlag = False
    neverChocoAgain = False
    dogSpeedIncrease = 40  # The speed with which dog will be faster after
    # eating a chocolate.

# Here I populate the list with one good apple and I use the list thoughout
# the whole loop.

    for i in range(num_goodFoods):
        random_X0 = rand(100, 1500)
        goodFoods.append(gameZone.create_image(random_X0, 0,
                         image=normal_appleImg))

# Here I populate the list with one bad apple and I use the list thoughout the
# whole loop.

    for i in range(num_badFoods):
        random_X0 = rand(100, 1500)
        badFoods.append(gameZone.create_image(random_X0, 0,
                        image=rotten_appleImg))

# Here I create one chocolate that I will use once in the level.

    random_X0 = rand(100, 1500)
    choco = gameZone.create_image(random_X0, -100, image=chocoImg)
    start = time.time()

# Here I populate the list with one trash can and I use the list thoughout the
# whole loop.

    for i in range(num_trash):
        random_X0 = rand(100, 1500)
        trash.append(gameZone.create_image(random_X0, 0,
                     image=trashImg))

# Here I populate the list with one treat and I use the list thoughout the
# whole loop.

    for i in range(num_treats):
        random_X0 = rand(100, 1500)
        treats.append(gameZone.create_image(random_X0, 0,
                      image=treatImg))

# I need this to check for elapsed time.

    start = time.time()

# LEVEL LOOP #

    while currScore.get() < pointsToWin - 1 and currScore.get() >= 0:
        if inPause.get():
            stopLevel()

# Loop responsible for the good apples.

        for i in range(len(goodFoods)):
            goodFoodPosition = gameZone.coords(goodFoods[i])
            if goodFoodPosition == []:
                continue
            gameZone.move(goodFoods[i], 0, foodSpeedOfGoodApples)
            if goodFoodPosition[1] > 950:
                random_X0 = rand(100, 1500)
                random_Y0 = rand(-500, -50)
                gameZone.coords(goodFoods[i], random_X0, random_Y0)
                root.update()
                root.update_idletasks()
                continue
            dogPosition = gameZone.coords(dog)
            dogPosition[0] = dogPosition[0] - 190
            dogPosition[1] = dogPosition[1] + 70
            dogPosition.append(dogPosition[0] + 200)  # Adding x1 for dog.
            dogPosition.append(dogPosition[1] + 200)  # Adding y1 for dog.
            goodFoodPosition.append(goodFoodPosition[0] + 100)  # Adding x1 for
            # good apple.
            goodFoodPosition.append(goodFoodPosition[1] + 100)  # Adding y1 for
            # good apple.
            if goodFoodPosition[0] < dogPosition[2] \
                and goodFoodPosition[2] > dogPosition[0] \
                and goodFoodPosition[1] < dogPosition[3] \
                and goodFoodPosition[3] > dogPosition[1]:
                if not goingLeft.get():  # Checking in which direction must the
                # dog face.
                    gameZone.itemconfig(dog, image=imgJump)
                    root.update()
                    root.update_idletasks()
                    gameZone.move(dog, 0, -30)
                    root.update()
                    root.update_idletasks()
                    time.sleep(0.05)
                    gameZone.move(dog, 0, 30)
                    root.update()
                    root.update_idletasks()
                    gameZone.itemconfig(dog, image=img)
                else:
                    gameZone.itemconfig(dog, image=imgJump1)
                    root.update()
                    root.update_idletasks()
                    gameZone.move(dog, 0, -30)
                    root.update()
                    root.update_idletasks()
                    time.sleep(0.05)
                    gameZone.move(dog, 0, 30)
                    root.update()
                    root.update_idletasks()
                    gameZone.itemconfig(dog, image=img1)
                random_X0 = rand(100, 1500)
                gameZone.coords(goodFoods[i], random_X0, -50)
                root.update()
                root.update_idletasks()
                updateScore(normal_applePoints)
                root.update()
                root.update_idletasks()

# After a certain amount of time the game will spawn more good apples.

            if time.time() - start > secondsBeforeNewGoodAppleSpawn \
                and len(goodFoods) < maxAmountOfGoodApples:
                start = time.time()
                random_X0 = rand(100, 1500)
                goodFoods.append(gameZone.create_image(random_X0, 0,
                                 image=normal_appleImg))
        time.sleep(0.03)
        root.update()

# Loop responsible for the chocolate.

        if currScore.get() >= 30 and currScore.get() <= 70 or chocoFlag:
            if neverChocoAgain:
                pass
            else:
                chocoPosition = gameZone.coords(foodSpeedOfChoco)
                chocoFlag = True
                gameZone.move(choco, 0, foodSpeedOfChoco)
                if chocoPosition[1] > 950:
                    gameZone.delete(choco)
                    chocoFlag = False
                    neverChocoAgain = True
                dogPosition = gameZone.coords(dog)
                dogPosition[0] = dogPosition[0] - 190
                dogPosition[1] = dogPosition[1] + 70
                dogPosition.append(dogPosition[0] + 200)  # Adding x1 for dog.
                dogPosition.append(dogPosition[1] + 200)  # Adding y1 for dog.
                chocoPosition.append(chocoPosition[0] + 100)  # Adding x1 for
                # chocolate.
                chocoPosition.append(chocoPosition[1] + 100)  # Adding y1 for
                # chocolate.
                if chocoPosition[0] < dogPosition[2] \
                    and chocoPosition[2] > dogPosition[0] \
                    and chocoPosition[1] < dogPosition[3] \
                    and chocoPosition[3] > dogPosition[1]:
                    if not goingLeft.get():  # Checking in which direction must
                    # the dog face.
                        gameZone.itemconfig(dog, image=imgJump)
                        root.update()
                        root.update_idletasks()
                        gameZone.move(dog, 0, -30)
                        root.update()
                        root.update_idletasks()
                        time.sleep(0.05)
                        gameZone.move(dog, 0, 30)
                        root.update()
                        root.update_idletasks()
                        gameZone.itemconfig(dog, image=img)
                    else:
                        gameZone.itemconfig(dog, image=imgJump1)
                        root.update()
                        root.update_idletasks()
                        gameZone.move(dog, 0, -30)
                        root.update()
                        root.update_idletasks()
                        time.sleep(0.05)
                        gameZone.move(dog, 0, 30)
                        root.update()
                        root.update_idletasks()
                        gameZone.itemconfig(dog, image=img1)
                    global add_XL
                    global add_XR
                    add_XL = -dogSpeedIncrease  # Changing the dog speed going
                    # left.
                    add_XR = dogSpeedIncrease  # Changing the dog speed going
                    # right.
                    gameZone.delete(choco)
                    chocoFlag = False
                    neverChocoAgain = True
                    updateScore(chocoPoints)
                    root.update()
                    root.update_idletasks()
        time.sleep(0.03)
        root.update()

# Loop responsible for the trash cans.

        for i in range(len(trash)):
            trashPosition = gameZone.coords(trash[i])
            if trashPosition == []:
                continue
            gameZone.move(trash[i], 0, foodSpeedOfTrash)
            if trashPosition[1] > 950:
                random_X0 = rand(100, 1500)
                random_Y0 = rand(-500, -50)
                gameZone.coords(trash[i], random_X0, random_Y0)
                root.update()
                root.update_idletasks()
                continue
            dogPosition = gameZone.coords(dog)
            dogPosition[0] = dogPosition[0] - 190
            dogPosition[1] = dogPosition[1] + 70
            dogPosition.append(dogPosition[0] + 200)  # Adding x1 for dog.
            dogPosition.append(dogPosition[1] + 200)  # Adding y1 for dog.
            trashPosition.append(trashPosition[0] + 100)  # Adding x1 for
            # trash can.
            trashPosition.append(trashPosition[1] + 100)  # Adding y1 for
            # trash can.
            if trashPosition[0] < dogPosition[2] and trashPosition[2] \
                > dogPosition[0] and trashPosition[1] < dogPosition[3] \
                and trashPosition[3] > dogPosition[1]:
                random_X0 = rand(100, 1500)  # The level will end, so there is
                # no need to check in which direction the dog must face.
                gameZone.coords(trash[i], random_X0, -50)
                root.update()
                root.update_idletasks()
                updateScore(trashPoints)
                root.update()
                root.update_idletasks()

# After a certain amount of time the game will spawn more trash cans.

            if time.time() - start > secondsBeforeNewTrashSpawn \
                and len(trash) < maxAmountOfTrash:
                start = time.time()
                random_X0 = rand(100, 1500)
                trash.append(gameZone.create_image(random_X0, 0,
                             image=trashImg))
        time.sleep(0.02)
        root.update()

# Loop responsible for the treats.

        for i in range(len(treats)):
            treatsPosition = gameZone.coords(treats[i])
            if treatsPosition == []:
                continue
            gameZone.move(treats[i], 0, foodSpeedOfTreats)
            if treatsPosition[1] > 950:
                random_X0 = rand(100, 1500)
                random_Y0 = rand(-500, -50)
                gameZone.coords(treats[i], random_X0, random_Y0)
                root.update()
                root.update_idletasks()
                continue
            dogPosition = gameZone.coords(dog)
            dogPosition[0] = dogPosition[0] - 190
            dogPosition[1] = dogPosition[1] + 70
            dogPosition.append(dogPosition[0] + 200)  # Adding x1 for dog.
            dogPosition.append(dogPosition[1] + 200)  # Adding y1 for dog.
            treatsPosition.append(treatsPosition[0] + 100)  # Adding x1 for
            # treat.
            treatsPosition.append(treatsPosition[1] + 100)  # Adding y1 for
            # treat.
            if treatsPosition[0] < dogPosition[2] and treatsPosition[2] \
                > dogPosition[0] and treatsPosition[1] < dogPosition[3] \
                and treatsPosition[3] > dogPosition[1]:
                if not goingLeft.get():  # Checking in which direction must
                # the dog face.
                    gameZone.itemconfig(dog, image=imgJump)
                    root.update()
                    root.update_idletasks()
                    gameZone.move(dog, 0, -30)
                    root.update()
                    root.update_idletasks()
                    time.sleep(0.05)
                    gameZone.move(dog, 0, 30)
                    root.update()
                    root.update_idletasks()
                    gameZone.itemconfig(dog, image=img)
                else:
                    gameZone.itemconfig(dog, image=imgJump1)
                    root.update()
                    root.update_idletasks()
                    gameZone.move(dog, 0, -30)
                    root.update()
                    root.update_idletasks()
                    time.sleep(0.05)
                    gameZone.move(dog, 0, 30)
                    root.update()
                    root.update_idletasks()
                    gameZone.itemconfig(dog, image=img1)
                random_X0 = rand(100, 1500)
                gameZone.coords(treats[i], random_X0, -50)
                root.update()
                root.update_idletasks()
                updateScore(treatPoints)
                root.update()
                root.update_idletasks()

# After a certain amount of time the game will spawn more treats.

            if time.time() - start > secondsBeforeNewTreatSpawn \
                and len(treats) < maxAmountOfTreats:
                start = time.time()
                random_X0 = rand(100, 1500)
                treats.append(gameZone.create_image(random_X0, 0,
                              image=treatImg))
        time.sleep(0.02)
        root.update()

# Loop responsible for the bad apples.

        for i in range(len(badFoods)):
            badFoodPosition = gameZone.coords(badFoods[i])
            if badFoodPosition == []:
                continue
            gameZone.move(badFoods[i], 0, foodSpeedOfBadApples)
            if badFoodPosition[1] > 950:
                random_X0 = rand(100, 1500)
                random_Y0 = rand(-500, -50)
                gameZone.coords(badFoods[i], random_X0, random_Y0)
                root.update()
                root.update_idletasks()
                continue
            dogPosition = gameZone.coords(dog)
            dogPosition[0] = dogPosition[0] - 190
            dogPosition[1] = dogPosition[1] + 70
            dogPosition.append(dogPosition[0] + 200)  # Adding x1 for dog.
            dogPosition.append(dogPosition[1] + 200)  # Adding y1 for dog.
            badFoodPosition.append(badFoodPosition[0] + 100)  # Adding x1 for
            # bad apple.
            badFoodPosition.append(badFoodPosition[1] + 100)  # Adding y1 for
            # bad apple.
            if badFoodPosition[0] < dogPosition[2] \
                and badFoodPosition[2] > dogPosition[0] \
                and badFoodPosition[1] < dogPosition[3] \
                and badFoodPosition[3] > dogPosition[1]:
                if not goingLeft.get():  # Checking in which direction must
                # the dog face.
                    gameZone.itemconfig(dog, image=imgJump)
                    root.update()
                    root.update_idletasks()
                    gameZone.move(dog, 0, -30)
                    root.update()
                    root.update_idletasks()
                    time.sleep(0.05)
                    gameZone.move(dog, 0, 30)
                    root.update()
                    root.update_idletasks()
                    gameZone.itemconfig(dog, image=img)
                else:
                    gameZone.itemconfig(dog, image=imgJump1)
                    root.update()
                    root.update_idletasks()
                    gameZone.move(dog, 0, -30)
                    root.update()
                    root.update_idletasks()
                    time.sleep(0.05)
                    gameZone.move(dog, 0, 30)
                    root.update()
                    root.update_idletasks()
                    gameZone.itemconfig(dog, image=img1)
                random_X0 = rand(100, 1500)
                gameZone.coords(badFoods[i], random_X0, -50)
                root.update()
                root.update_idletasks()
                updateScore(rotten_applePoints)
                root.update()
                root.update_idletasks()

# After a certain amount of time the game will spawn more bad apples.

            if time.time() - start > secondsBeforeNewBadAppleSpawn \
                and len(badFoods) < maxAmountOfBadApples:
                start = time.time()
                random_X0 = rand(100, 1500)
                badFoods.append(gameZone.create_image(random_X0, 0,
                                image=rotten_appleImg))
        time.sleep(0.01)
        root.update()
    bigScore.set(currScore.get() + bigScore.get())

# Before moving to Level 6 I need to make sure there are no leftover apples, a
# chocolate, trash cans or treats from Level 5.

    for i in range(len(goodFoods)):
        gameZone.delete(goodFoods[i])
    for i in range(len(badFoods)):
        gameZone.delete(badFoods[i])
    gameZone.delete(choco)
    for i in range(len(trash)):
        gameZone.delete(trash[i])
    for i in range(len(treats)):
        gameZone.delete(treats[i])

    goodFoods.clear()
    badFoods.clear()
    trash.clear()
    treats.clear()

# Before moving to Level 5 I need to make sure there the dog's speed is
# returned to normal in case the player ate a chocolate in this level.

    add_XL = -10
    add_XR = 10

# The loop has ended, here I check whether it's because the player lost or won
# the level. I need to make sure that the current score is zero, as it would
# otherwise carry to the next level, but I can't nullify it before the check,
# as I need to see what it's value is.
    if currScore.get() < 0:
        currScore.set(0)
        showGAME_OVER()
    else:

    # I need to make sure that the current score is zero, as it would otherwise
    # carry from the previous level.

        currScore.set(0)
        levelSwitcher(5)


# LEVEL 6 / EDNLESS MODE #
# The game will get proggresively harder, so I need a value with which I can
# increase various values.

global indexFive
indexFive = 5


def LEVEL_6():
    currLevel.set(6)
    inPLAY.set(True)
    levelLabel = Label(
        scoreBoard,
        font=('Ubuntu', 40),
        width=10,
        bg='black',
        fg='white',
        text='ENDLESS',
        )
    levelLabel.place(x=5, y=10)
    BETWEEN_LEVEL.grid_forget()
    PLAY.grid()

# SETTINGS #

    dogStartPosition()  # Whenever a new level starts, I need to make sure the
    # dog starts in it's default position.

    num_goodFoods = 1  # Number of the good apples that will spawn at the same
    # time.
    num_badFoods = 1  # Number of the bad apples that will spawn at the same
    # time.
    num_trash = 1  # Number of the trash cans that will spawn at the same time.
    num_treats = 1  # Number of treats that will spawn at the same time.

    secondsBeforeNewGoodAppleSpawn = 10  # Seconds counted before a new number
    # of good apples is spawned.
    secondsBeforeNewBadAppleSpawn = 5  # Seconds counted before a new number of
    # bad apples is spawned.
    secondsBeforeNewTrashSpawn = 8  # Seconds counted before a new number of
    # trash cans is spawned.
    secondsBeforeNewTreatSpawn = 5  # Seconds counted before a new number of
    # treats is spawned.

    global indexFive  # The game will get proggresively harder, so I need a
    # value with which I can increase various values.
    indexFive += 5
    negIndexFive = -indexFive

    foodSpeedOfGoodApples = 15 + indexFive  # Speed of good apples.
    foodSpeedOfBadApples = 20 + indexFive  # Speed of bad apples.
    foodSpeedOfChoco = 15 + indexFive  # Speed of chocolate.
    foodSpeedOfTrash = 15 + indexFive  # Speed of trash cans.
    foodSpeedOfTreats = 15 + indexFive  # Speed of treats.
    foodSpeedOfHam = 15 + indexFive  # Speed of ham.

    maxAmountOfGoodApples = 1  # Maximum amount of good apples that can be
    # on-screen at the same time.
    maxAmountOfBadApples = 8  # Maximum amount of bad apples that can be
    # on-screen at the same time.
    # Maximum amount of chocolates is ensured to be one.
    maxAmountOfTrash = 3  # Maximum amount of trash cans that can be on-screen
    # at the same time.
    maxAmountOfTreats = 2  # Maximum amount of treats that can be on-screen at
    # the same time.
    # Maximum amount of ham is ensured to be one.

    pointsToWin = 100  # Points necessary to win current level.
    normal_applePoints = 10  # Points awarded when a player gets a good apple.
    rotten_applePoints = -25 + negIndexFive  # Points subtracted when a player
    # gets a bad apple.
    chocoPoints = -15  # Points subtracted when a player gets a chocolate.
    trashPoints = -100  # Points subtracted when a player gets a trash
    # can (Game over).
    treatPoints = 10  # Points awarded when a player gets a treat.
    hamPoints = 100  # Points awarded when a player gets a piece of
    # ham (Game over).

    chocoFlag = False
    neverChocoAgain = False
    dogSpeedIncrease = 40  # The speed with which dog will be faster after
    # eating a chocolate.

    hamFlag = False
    neverHamAgain = False

# Here I populate the list with one good apple and I use the list thoughout
# the whole loop.

    currScore.set(0)
    for i in range(num_goodFoods):
        random_X0 = rand(100, 1500)
        goodFoods.append(gameZone.create_image(random_X0, 0,
                         image=normal_appleImg))

# Here I populate the list with one bad apple and I use the list thoughout
# the whole loop.

    for i in range(num_badFoods):
        random_X0 = rand(100, 1500)
        badFoods.append(gameZone.create_image(random_X0, 0,
                        image=rotten_appleImg))
    random_X0 = rand(100, 1500)

# Here I create one chocolate that I will use once in the level.

    choco = gameZone.create_image(random_X0, -100, image=chocoImg)
    start = time.time()

# Here I populate the list with one trash can and I use the list thoughout
# the whole loop.

    for i in range(num_trash):
        random_X0 = rand(100, 1500)
        trash.append(gameZone.create_image(random_X0, 0,
                     image=trashImg))

# Here I populate the list with one treat and I use the list thoughout the
# whole loop.

    for i in range(num_treats):
        random_X0 = rand(100, 1500)
        treats.append(gameZone.create_image(random_X0, 0,
                      image=treatImg))

# Here I create one piece of ham that I will use once in the level.

    random_X0 = rand(100, 1500)
    ham = gameZone.create_image(random_X0, -100, image=hamImg)

# I need this to check for elapsed time.

    start = time.time()

# LEVEL LOOP #

    while currScore.get() < pointsToWin - 1 and currScore.get() >= 0:
        if inPause.get():
            stopLevel()

# Loop responsible for the good apples.

        for i in range(len(goodFoods)):
            goodFoodPosition = gameZone.coords(goodFoods[i])
            if goodFoodPosition == []:
                continue
            gameZone.move(goodFoods[i], 0, foodSpeedOfGoodApples)
            if goodFoodPosition[1] > 950:
                random_X0 = rand(100, 1500)
                random_Y0 = rand(-500, -50)
                gameZone.coords(goodFoods[i], random_X0, random_Y0)
                root.update()
                root.update_idletasks()
                continue
            dogPosition = gameZone.coords(dog)
            dogPosition[0] = dogPosition[0] - 190
            dogPosition[1] = dogPosition[1] + 70
            dogPosition.append(dogPosition[0] + 200)  # Adding x1 for dog.
            dogPosition.append(dogPosition[1] + 200)  # Adding y1 for dog.
            goodFoodPosition.append(goodFoodPosition[0] + 100)  # Adding x1
            # for good apple.
            goodFoodPosition.append(goodFoodPosition[1] + 100)  # Adding y1
            # for good apple.
            if goodFoodPosition[0] < dogPosition[2] \
                and goodFoodPosition[2] > dogPosition[0] \
                and goodFoodPosition[1] < dogPosition[3] \
                and goodFoodPosition[3] > dogPosition[1]:
                if not goingLeft.get():  # Checking in which direction must
                # the dog face.
                    gameZone.itemconfig(dog, image=imgJump)
                    root.update()
                    root.update_idletasks()
                    gameZone.move(dog, 0, -30)
                    root.update()
                    root.update_idletasks()
                    time.sleep(0.05)
                    gameZone.move(dog, 0, 30)
                    root.update()
                    root.update_idletasks()
                    gameZone.itemconfig(dog, image=img)
                else:
                    gameZone.itemconfig(dog, image=imgJump1)
                    root.update()
                    root.update_idletasks()
                    gameZone.move(dog, 0, -30)
                    root.update()
                    root.update_idletasks()
                    time.sleep(0.05)
                    gameZone.move(dog, 0, 30)
                    root.update()
                    root.update_idletasks()
                    gameZone.itemconfig(dog, image=img1)
                random_X0 = rand(100, 1500)
                gameZone.coords(goodFoods[i], random_X0, -50)
                root.update()
                root.update_idletasks()
                updateScore(normal_applePoints)
                root.update()
                root.update_idletasks()

# After a certain amount of time the game will spawn more good apples.

            if time.time() - start > secondsBeforeNewGoodAppleSpawn \
                and len(goodFoods) < maxAmountOfGoodApples:
                start = time.time()
                random_X0 = rand(100, 1500)
                goodFoods.append(gameZone.create_image(random_X0, 0,
                                 image=normal_appleImg))
        time.sleep(0.03)
        root.update()

# Loop responsible for the chocolate.

        if currScore.get() >= 30 and currScore.get() <= 70 or chocoFlag:
            if neverChocoAgain:
                pass
            else:
                chocoPosition = gameZone.coords(choco)
                chocoFlag = True
                gameZone.move(choco, 0, foodSpeedOfChoco)
                if chocoPosition[1] > 950:
                    gameZone.delete(choco)
                    chocoFlag = False
                    neverChocoAgain = True
                dogPosition = gameZone.coords(dog)
                dogPosition[0] = dogPosition[0] - 190
                dogPosition[1] = dogPosition[1] + 70
                dogPosition.append(dogPosition[0] + 200)  # Adding x1 for dog.
                dogPosition.append(dogPosition[1] + 200)  # Adding y1 for dog.
                chocoPosition.append(chocoPosition[0] + 100)  # Adding x1
                # for chocolate.
                chocoPosition.append(chocoPosition[1] + 100)  # Adding y1
                # for chocolate.
                if chocoPosition[0] < dogPosition[2] \
                    and chocoPosition[2] > dogPosition[0] \
                    and chocoPosition[1] < dogPosition[3] \
                    and chocoPosition[3] > dogPosition[1]:
                    if not goingLeft.get():  # Checking in which direction
                    # must the dog face.
                        gameZone.itemconfig(dog, image=imgJump)
                        root.update()
                        root.update_idletasks()
                        gameZone.move(dog, 0, -30)
                        root.update()
                        root.update_idletasks()
                        time.sleep(0.05)
                        gameZone.move(dog, 0, 30)
                        root.update()
                        root.update_idletasks()
                        gameZone.itemconfig(dog, image=img)
                    else:
                        gameZone.itemconfig(dog, image=imgJump1)
                        root.update()
                        root.update_idletasks()
                        gameZone.move(dog, 0, -30)
                        root.update()
                        root.update_idletasks()
                        time.sleep(0.05)
                        gameZone.move(dog, 0, 30)
                        root.update()
                        root.update_idletasks()
                        gameZone.itemconfig(dog, image=img1)
                    global add_XL
                    global add_XR
                    add_XL = -dogSpeedIncrease  # Changing the dog speed going
                    # left.
                    add_XR = dogSpeedIncrease  # Changing the dog speed going
                    # right.
                    gameZone.delete(choco)
                    chocoFlag = False
                    neverChocoAgain = True
                    updateScore(chocoPoints)
                    root.update()
                    root.update_idletasks()
        time.sleep(0.03)
        root.update()

# Loop responsible for the piece of ham.

        if currScore.get() >= 30 and currScore.get() <= 80 or hamFlag:
            if neverHamAgain:
                pass
            else:
                hamPosition = gameZone.coords(ham)
                hamFlag = True
                gameZone.move(ham, 0, foodSpeedOfHam)
                if hamPosition[1] > 950:
                    gameZone.delete(ham)
                    hamFlag = False
                    neverHamAgain = True
                dogPosition = gameZone.coords(dog)
                dogPosition[0] = dogPosition[0] - 190
                dogPosition[1] = dogPosition[1] + 70
                dogPosition.append(dogPosition[0] + 200)  # Adding x1 for dog.
                dogPosition.append(dogPosition[1] + 200)  # Adding y1 for dog.
                hamPosition.append(hamPosition[0] + 100)  # Adding x1 for the
                # ham.
                hamPosition.append(hamPosition[1] + 100)  # Adding y1 for the
                # ham.
                if hamPosition[0] < dogPosition[2] and hamPosition[2] \
                    > dogPosition[0] and hamPosition[1] \
                    < dogPosition[3] and hamPosition[3] \
                    > dogPosition[1]:
                    gameZone.delete(ham)  # The level will end, so there is no
                    # need to check in which direction the dog must face.
                    hamFlag = False
                    neverhamAgain = True
                    updateScore(hamPoints)
                    root.update()
                    root.update_idletasks()
        time.sleep(0.03)
        root.update()

# Loop responsible for the trash cans.

        for i in range(len(trash)):
            trashPosition = gameZone.coords(trash[i])
            if trashPosition == []:
                continue
            gameZone.move(trash[i], 0, foodSpeedOfTrash)
            if trashPosition[1] > 950:
                random_X0 = rand(100, 1500)
                random_Y0 = rand(-500, -50)
                gameZone.coords(trash[i], random_X0, random_Y0)
                root.update()
                root.update_idletasks()
                continue
            dogPosition = gameZone.coords(dog)
            dogPosition[0] = dogPosition[0] - 190
            dogPosition[1] = dogPosition[1] + 70
            dogPosition.append(dogPosition[0] + 200)  # Adding x1 for dog.
            dogPosition.append(dogPosition[1] + 200)  # Adding y1 for dog.
            trashPosition.append(trashPosition[0] + 100)  # Adding x1 for
            # trash can.
            trashPosition.append(trashPosition[1] + 100)  # Adding y1 for
            # trash can.
            if trashPosition[0] < dogPosition[2] and trashPosition[2] \
                > dogPosition[0] and trashPosition[1] < dogPosition[3] \
                and trashPosition[3] > dogPosition[1]:
                random_X0 = rand(100, 1500)  # The level will end, so there is
                # no need to check in which direction the dog must face.
                gameZone.coords(trash[i], random_X0, -50)
                root.update()
                root.update_idletasks()
                updateScore(trashPoints)
                root.update()
                root.update_idletasks()

# After a certain amount of time the game will spawn more trash cans.

            if time.time() - start > secondsBeforeNewTrashSpawn \
                and len(trash) < maxAmountOfTrash:
                start = time.time()
                random_X0 = rand(100, 1500)
                trash.append(gameZone.create_image(random_X0, 0,
                             image=trashImg))
        time.sleep(0.02)
        root.update()

# Loop responsible for the treats.

        for i in range(len(treats)):
            treatsPosition = gameZone.coords(treats[i])
            if treatsPosition == []:
                continue
            gameZone.move(treats[i], 0, foodSpeedOfTreats)
            if treatsPosition[1] > 950:
                random_X0 = rand(100, 1500)
                random_Y0 = rand(-500, -50)
                gameZone.coords(treats[i], random_X0, random_Y0)
                root.update()
                root.update_idletasks()
                continue
            dogPosition = gameZone.coords(dog)
            dogPosition[0] = dogPosition[0] - 190
            dogPosition[1] = dogPosition[1] + 70
            dogPosition.append(dogPosition[0] + 200)  # Adding x1 for dog.
            dogPosition.append(dogPosition[1] + 200)  # Adding y1 for dog.
            treatsPosition.append(treatsPosition[0] + 100)  # Adding x1 for
            # treat.
            treatsPosition.append(treatsPosition[1] + 100)  # Adding y1 for
            # treat.
            if treatsPosition[0] < dogPosition[2] and treatsPosition[2] \
                > dogPosition[0] and treatsPosition[1] < dogPosition[3] \
                and treatsPosition[3] > dogPosition[1]:
                if not goingLeft.get():  # Checking in which direction must
                # the dog face.
                    gameZone.itemconfig(dog, image=imgJump)
                    root.update()
                    root.update_idletasks()
                    gameZone.move(dog, 0, -30)
                    root.update()
                    root.update_idletasks()
                    time.sleep(0.05)
                    gameZone.move(dog, 0, 30)
                    root.update()
                    root.update_idletasks()
                    gameZone.itemconfig(dog, image=img)
                else:
                    gameZone.itemconfig(dog, image=imgJump1)
                    root.update()
                    root.update_idletasks()
                    gameZone.move(dog, 0, -30)
                    root.update()
                    root.update_idletasks()
                    time.sleep(0.05)
                    gameZone.move(dog, 0, 30)
                    root.update()
                    root.update_idletasks()
                    gameZone.itemconfig(dog, image=img1)
                random_X0 = rand(100, 1500)
                gameZone.coords(treats[i], random_X0, -50)
                root.update()
                root.update_idletasks()
                updateScore(treatPoints)
                root.update()
                root.update_idletasks()

# After a certain amount of time the game will spawn more treats.

            if time.time() - start > secondsBeforeNewTreatSpawn \
                and len(treats) < maxAmountOfTreats:
                start = time.time()
                random_X0 = rand(100, 1500)
                treats.append(gameZone.create_image(random_X0, 0,
                              image=treatImg))
        time.sleep(0.02)
        root.update()

# Loop responsible for the bad apples.

        for i in range(len(badFoods)):
            badFoodPosition = gameZone.coords(badFoods[i])
            if badFoodPosition == []:
                continue
            gameZone.move(badFoods[i], 0, foodSpeedOfBadApples)
            if badFoodPosition[1] > 950:
                random_X0 = rand(100, 1500)
                random_Y0 = rand(-500, -50)
                gameZone.coords(badFoods[i], random_X0, random_Y0)
                root.update()
                root.update_idletasks()
                continue
            dogPosition = gameZone.coords(dog)
            dogPosition[0] = dogPosition[0] - 190
            dogPosition[1] = dogPosition[1] + 70
            dogPosition.append(dogPosition[0] + 200)  # Adding x1 for dog.
            dogPosition.append(dogPosition[1] + 200)  # Adding y1 for dog.
            badFoodPosition.append(badFoodPosition[0] + 100)  # Adding x1 for
            # bad apple.
            badFoodPosition.append(badFoodPosition[1] + 100)  # Adding y1 for
            # bad apple.
            if badFoodPosition[0] < dogPosition[2] \
                and badFoodPosition[2] > dogPosition[0] \
                and badFoodPosition[1] < dogPosition[3] \
                and badFoodPosition[3] > dogPosition[1]:
                if not goingLeft.get():  # Checking in which direction must
                # the dog face.
                    gameZone.itemconfig(dog, image=imgJump)
                    root.update()
                    root.update_idletasks()
                    gameZone.move(dog, 0, -30)
                    root.update()
                    root.update_idletasks()
                    time.sleep(0.05)
                    gameZone.move(dog, 0, 30)
                    root.update()
                    root.update_idletasks()
                    gameZone.itemconfig(dog, image=img)
                else:
                    gameZone.itemconfig(dog, image=imgJump1)
                    root.update()
                    root.update_idletasks()
                    gameZone.move(dog, 0, -30)
                    root.update()
                    root.update_idletasks()
                    time.sleep(0.05)
                    gameZone.move(dog, 0, 30)
                    root.update()
                    root.update_idletasks()
                    gameZone.itemconfig(dog, image=img1)
                random_X0 = rand(100, 1500)
                gameZone.coords(badFoods[i], random_X0, -50)
                root.update()
                root.update_idletasks()
                updateScore(rotten_applePoints)
                root.update()
                root.update_idletasks()

# After a certain amount of time the game will spawn more bad apples.

            if time.time() - start > secondsBeforeNewBadAppleSpawn \
                and len(badFoods) < maxAmountOfBadApples:
                start = time.time()
                random_X0 = rand(100, 1500)
                badFoods.append(gameZone.create_image(random_X0, 0,
                                image=rotten_appleImg))
        time.sleep(0.01)
        root.update()
    bigScore.set(currScore.get() + bigScore.get())

# Before moving to Endless Mode I need to make sure there are no leftover
# apples, a chocolate, trash cans, treats or ham from Level 6.

    for i in range(len(goodFoods)):
        gameZone.delete(goodFoods[i])
    for i in range(len(badFoods)):
        gameZone.delete(badFoods[i])
    gameZone.delete(choco)
    for i in range(len(trash)):
        gameZone.delete(trash[i])
    for i in range(len(treats)):
        gameZone.delete(treats[i])
    gameZone.delete(ham)

    goodFoods.clear()
    badFoods.clear()
    trash.clear()
    treats.clear()

# Before moving to the next level I need to make sure there the dog's speed is
# returned to normal in case the player ate a chocolate in this level.

    add_XL = -10
    add_XR = 10

# The loop has ended, here I check whether it's because the player lost or won
# the level. I need to make sure that the current score is zero, as it would
# otherwise carry to the next level, but I can't nullify it before the check,
# as I need to see what it's value is.
    if currScore.get() < 0:
        currScore.set(0)
        showGAME_OVER()
    else:
        currScore.set(0)
        levelSwitcher(6)


# LEVELS END #

# FUNCTIONS  START #

# The saveGame() saves the player's score and current level to the file
# "savedGame.txt". This way even if the player quits they have their details
# saved in an external file.

def saveGame():
    lvlANDScore = str(currLevel.get()) + str(bigScore.get())
    save = open('savedGame.txt', 'w')
    save.write(lvlANDScore)
    save.close()
    bigScore.set(0)
    currScore.set(0)
    BETWEEN_LEVEL.grid_forget()
    MAIN_MENU.grid()


# The loadGame() loads the player's score and current level from the file
# "savedGame.txt". This way even if the player had quit, they can still
# load their game.

def loadGame():
    saved = open('savedGame.txt', 'r')
    lvlANDScore = saved.readline()
    saved.close()
    lvl = int(lvlANDScore[0])
    if lvl == 6:
        currLevel.set(6)
    else:
        currLevel.set(lvl + 1)
    bigScore.set(int(lvlANDScore[1:]))
    MAIN_MENU.grid_forget()
    LEADERBOARD.grid_forget()
    GAME_INFO.grid_forget()
    BETWEEN_LEVEL.grid_forget()
    PLAY.grid()
    root.bind(controlLeft.get(), left)
    root.bind(controlRight.get(), right)
    root.bind(controlWinCheatCode.get(), win)
    root.bind(controlIncreaseScore.get(), addTen)
    root.bind(controlIncreaseSpeed.get(), increaseSpeed)
    root.bind(controlDecreaseSpeed.get(), decreaseSpeed)

    if currLevel.get() == 2:
        LEVEL_2()
    elif currLevel.get() == 3:
        LEVEL_3()
    elif currLevel.get() == 4:
        LEVEL_4()
    elif currLevel.get() == 5:
        LEVEL_5()
    elif currLevel.get() == 6:
        LEVEL_6()


# The submit() function saves the player's three initials into the
# "scoreboard.txt" file.

def submit():
    playerName = playerNameEntry.get()
    playerScore = int(bigScore.get())
    playerName = playerName[0:3]

    board = open('scoreboard.txt', 'r')
    allScores = board.readlines()
    board.close()

    first = allScores[0]
    second = allScores[1]
    third = allScores[2]
    fourth = allScores[3]
    fifth = allScores[4]
    sixth = allScores[5]

    firstName = first[0:3]
    secondName = second[0:3]
    thirdName = third[0:3]
    fourthName = fourth[0:3]
    fifthName = fifth[0:3]
    sixthName = sixth[0:3]

    names = []
    names.append(firstName)
    names.append(secondName)
    names.append(thirdName)
    names.append(fourthName)
    names.append(fifthName)
    names.append(sixthName)

    firstScore = first.replace('\n', '')
    secondScore = second.replace('\n', '')
    thirdScore = third.replace('\n', '')
    fourthScore = fourth.replace('\n', '')
    fifthScore = fifth.replace('\n', '')
    sixthScore = sixth.replace('\n', '')

    scores = []
    scores.append(first[3:len(first) - 1])
    scores.append(second[3:len(second) - 1])
    scores.append(third[3:len(third) - 1])
    scores.append(fourth[3:len(fourth) - 1])
    scores.append(fifth[3:len(fifth) - 1])
    scores.append(sixth[3:len(sixth) - 1])

    if int(scores[5]) > bigScore.get():
        pass
    else:
        for i in range(6):
            currScore = int(scores[i])
            if currScore <= bigScore.get():
                scores.insert(i, bigScore.get())
                names.insert(i, playerName)
                scores.pop(len(scores) - 1)
                names.pop(len(names) - 1)
                break
        board = open('scoreboard.txt', 'w')
        for i in range(6):
            board.write(str(names[i]) + str(scores[i]) + '\n')
        board.close()

    firstPlayerName.set(names[0])
    secondPlayerName.set(names[1])
    thirdPlayerName.set(names[2])
    fourthPlayerName.set(names[3])
    fifthPlayerName.set(names[4])
    sixthPlayerName.set(names[5])

    firstPlayerScore.set(scores[0])
    secondPlayerScore.set(scores[1])
    thirdPlayerScore.set(scores[2])
    fourthPlayerScore.set(scores[3])
    fifthPlayerScore.set(scores[4])
    sixthPlayerScore.set(scores[5])
    exit()


# The startupUpdateLeaderboard() function updates the leaderboard with the
# names from the "scoreboard.txt" file.

def startupUpdateLeaderboard():
    board = open('scoreboard.txt', 'r')
    allScores = board.readlines()
    board.close()

    first = allScores[0]
    second = allScores[1]
    third = allScores[2]
    fourth = allScores[3]
    fifth = allScores[4]
    sixth = allScores[5]

    firstName = first[0:3]
    secondName = second[0:3]
    thirdName = third[0:3]
    fourthName = fourth[0:3]
    fifthName = fifth[0:3]
    sixthName = sixth[0:3]

    names = []
    names.append(firstName)
    names.append(secondName)
    names.append(thirdName)
    names.append(fourthName)
    names.append(fifthName)
    names.append(sixthName)

    firstScore = first.replace('\n', '')
    secondScore = second.replace('\n', '')
    thirdScore = third.replace('\n', '')
    fourthScore = fourth.replace('\n', '')
    fifthScore = fifth.replace('\n', '')
    sixthScore = sixth.replace('\n', '')

    scores = []
    scores.append(first[3:len(first) - 1])
    scores.append(second[3:len(second) - 1])
    scores.append(third[3:len(third) - 1])
    scores.append(fourth[3:len(fourth) - 1])
    scores.append(fifth[3:len(fifth) - 1])
    scores.append(sixth[3:len(sixth) - 1])

    firstPlayerName.set(names[0])
    secondPlayerName.set(names[1])
    thirdPlayerName.set(names[2])
    fourthPlayerName.set(names[3])
    fifthPlayerName.set(names[4])
    sixthPlayerName.set(names[5])

    firstPlayerScore.set(scores[0])
    secondPlayerScore.set(scores[1])
    thirdPlayerScore.set(scores[2])
    fourthPlayerScore.set(scores[3])
    fifthPlayerScore.set(scores[4])
    sixthPlayerScore.set(scores[5])


# The left() function ensures correct movement to the left.

def left(event):
    goingLeft.set(True)
    gameZone.itemconfig(dog, image=img1)
    root.update_idletasks()
    gameZone.move(dog, add_XL, 0)
    currPosition = gameZone.coords(dog)
    if currPosition[0] < 200:  # Blocks Left Wall
        dogStartPosition()


# The right() function ensures correct movement to the right.

def right(event):
    goingLeft.set(False)
    gameZone.itemconfig(dog, image=img)
    root.update_idletasks()
    gameZone.move(dog, add_XR, 0)
    currPosition = gameZone.coords(dog)
    if currPosition[0] > 1590:  # Blocks Right Wall
        gameZone.coords(dog, 1600, 676)


# The win() function codes the behaviour of the Win Cheat Code.
# The player automatically passes the current level.

def win(Event):
    currScore.set(100)


# The addTen() function codes the behaviour of the Add Score Cheat Code.
# The player automatically wins 10 points.

def addTen(Event):
    currScore.set(currScore.get() + 10)


# The increaseSpeed() function codes the behaviour of the Speed Increase Cheat
# Code. The player automatically increases the dog's speed by 10.

def increaseSpeed(Event):
    global add_XL
    global add_XR
    add_XL -= 10
    add_XR += 10


# The decreaseSpeed() function codes the behaviour of the Speed Decrease Cheat
# Code. The player automatically decreases the dog's speed by 10.

def decreaseSpeed(Event):
    global add_XL
    global add_XR
    if add_XL != -10:
        add_XL += 10
    if add_XR != 10:
        add_XR -= 10


# These functions are necessary so the player can change controls without any
# problem.

def submitLeftControl():
    root.unbind(controlLeft.get())
    newControl = leftButtonEntry.get()
    newControl = '<' + newControl + '>'
    controlLeft.set(newControl)
    root.bind(controlLeft.get(), left)


def submitRightControl():
    root.unbind(controlRight.get())
    newControl = rightButtonEntry.get()
    newControl = '<' + newControl + '>'
    controlRight.set(newControl)
    root.bind(controlRight.get(), right)


def submitWin():
    root.unbind(controlWinCheatCode.get())
    newControl = winCheatCodeEntry.get()
    newControl = '<' + newControl + '>'
    controlWinCheatCode.set(newControl)
    root.bind(controlWinCheatCode.get(), win)


def submitAddTen():
    root.unbind(controlIncreaseScore.get())
    newControl = increaseScoreCheatCodeEntry.get()
    newControl = '<' + newControl + '>'
    controlIncreaseScore.set(newControl)
    root.bind(controlIncreaseScore.get(), addTen)


def submitIncreaseSpeed():
    root.unbind(controlIncreaseSpeed.get())
    newControl = increaseSpeedCheatCodeEntry.get()
    newControl = '<' + newControl + '>'
    controlIncreaseSpeed.set(newControl)
    root.bind(controlIncreaseSpeed.get(), increaseSpeed)


def submitDecreaseSpeed():
    root.unbind(controlDecreaseSpeed.get())
    newControl = decreaseSpeedCheatCodeEntry.get()
    newControl = '<' + newControl + '>'
    controlDecreaseSpeed.set(newControl)
    root.bind(controlDecreaseSpeed.get(), decreaseSpeed)


# The resetSettings() function automatically resets the keybinds of
# the controls to their default setting.
def resetSettings():
    root.unbind(controlLeft.get())
    root.unbind(controlRight.get())
    root.unbind(controlWinCheatCode.get())
    root.unbind(controlIncreaseScore.get())
    root.unbind(controlIncreaseSpeed.get())
    root.unbind(controlDecreaseSpeed.get())

    root.bind(originalKeybindLeft.get(), left)
    root.bind(originalKeybindRight.get(), right)
    root.bind(originalKeybindWin.get(), win)
    root.bind(originalKeybindAddTen.get(), addTen)
    root.bind(originalKeybindPlusSpeed.get(), increaseSpeed)
    root.bind(originalKeybindMinusSpeed.get(), decreaseSpeed)


# The dogStartPosition() function returns the dog to its default position.
# This function is necessary so the dog starts at the actual start after each
# level.
def dogStartPosition():
    gameZone.coords(dog, 200, 676)


# FUNCTIONS  END #

# MAIN CODE #

# MAIN_MENU FRAME #

MAIN_MENU = Frame(root, bg='black')

dogFacts = [
    'All dogs are good boys and girls.',
    'Dogs noses are wet to help absorb scent chemicals.',
    'The sense of smell of a Bloodhound\ncan be used as evidence in court.',
    'Three dogs survived the Titanic sinking!',
    'The Beatles song "A Day in the Life"\nhas a frequency only dogs' +
    'can hear.',
    'The tallest dog in the world is 44 inches tall.',
    'Thirty percent of Dalmatians are deaf in one ear.',
    'Dogs have three eyelids.',
    'Puppies are blind, deaf and toothless when born.',
    'In Bulgaria, if a dog curls up in a ball\nit means it is going to rain.',
    ]

layoutMenu()

# PLAY FRAME #

PLAY = Frame(root)
root.bind(controlLeft.get(), left)  # I've put these here so the dog can't
# move unless the user is looking at the PLAY screen.
root.bind(controlRight.get(), right)
root.bind(controlWinCheatCode.get(), win)
root.bind(controlIncreaseScore.get(), addTen)
root.bind(controlIncreaseSpeed.get(), increaseSpeed)
root.bind(controlDecreaseSpeed.get(), decreaseSpeed)
goodFoods = []
badFoods = []
trash = []
treats = []

gameZone = Canvas(PLAY, width=1600, height=883, bg='black')
gameZone.grid(row=0, column=0)

scoreBoard = Canvas(PLAY, width=315, height=883, bg='black')
scoreBoard.grid(row=0, column=1)

currScoreLabel = Label(
    scoreBoard,
    font=('Ubuntu', 90),
    width=4,
    bg='black',
    fg='white',
    textvariable=currScore,
    )
currScoreLabel.place(x=1, y=60)

bigScoreLabel = Label(
    scoreBoard,
    font=('Ubuntu', 45),
    width=4,
    bg='black',
    fg='grey',
    textvariable=bigScore,
    )
bigScoreLabel.place(x=140, y=180)

bg = PhotoImage(file='bg.png')
background = gameZone.create_image(820, 440, image=bg)

img = PhotoImage(file='doggo3.png')
img1 = PhotoImage(file='doggo3R.png')

imgJump = PhotoImage(file='doggo3Jump.png')
imgJump1 = PhotoImage(file='doggo3RJump.png')
x = 200
y = 660
dog = gameZone.create_image(x, y, anchor='ne', image=img)

# Actual items as images in tkinter.

normal_appleImg = PhotoImage(file='normal_apple.png')
rotten_appleImg = PhotoImage(file='rotten_apple.png')
chocoImg = PhotoImage(file='choco.png')
trashImg = PhotoImage(file='trash.png')
treatImg = PhotoImage(file='treat.png')
hamImg = PhotoImage(file='ham.png')

# LEADERBOARD FRAME #

LEADERBOARD = Frame(root, bg='black')

Button(
    LEADERBOARD,
    text='Main Menu',
    font=('Times', 50, 'bold italic'),
    bg='black',
    fg='white',
    activebackground='white',
    width=16,
    height=1,
    borderwidth=10,
    relief='groove',
    command=showMAIN_MENU,
    ).grid(row=4, column=2)

leftCanvas = Canvas(LEADERBOARD, height=880, width=400, bg='black',
                    highlightthickness=0)
leftCanvas.grid(row=0, column=1, rowspan=5)
leftCanvas.create_image(250, 130, image=LEADERBOARD_DOGGO_LEFT)

rightCanvas = Canvas(LEADERBOARD, height=880, width=400, bg='black',
                     highlightthickness=0)
rightCanvas.grid(row=0, column=3, rowspan=5)
rightCanvas.create_image(100, 130, image=LEADERBOARD_DOGGO_RIGHT)

paddingTop = Label(LEADERBOARD, height=4, background='black')
paddingTop.grid(row=0, column=2)

startupUpdateLeaderboard()
leaderBoardTitleLabel = Label(
    LEADERBOARD,
    text='LEADERBOARD',
    font=('Times', 90, 'bold italic'),
    width=18,
    bg='black',
    fg='white',
    anchor='n',
    )
leaderBoardTitleLabel.grid(row=1, column=2)

firstPlayerNameString = firstPlayerName.get()
firstPlayerScoreString = str(firstPlayerScore.get())

secondPlayerNameString = secondPlayerName.get()
secondPlayerScoreString = str(secondPlayerScore.get())

thirdPlayerNameString = thirdPlayerName.get()
thirdPlayerScoreString = str(thirdPlayerScore.get())

fourthPlayerNameString = fourthPlayerName.get()
fourthPlayerScoreString = str(fourthPlayerScore.get())

fifthPlayerNameString = fifthPlayerName.get()
fifthPlayerScoreString = str(fifthPlayerScore.get())

sixthPlayerNameString = sixthPlayerName.get()
sixthPlayerScoreString = str(sixthPlayerScore.get())

leaderBoardPlayersLabel = Label(
    LEADERBOARD,
    text='\n1. ' + firstPlayerNameString + ' - '
        + firstPlayerScoreString + '\n2. ' + secondPlayerNameString
        + ' - ' + secondPlayerScoreString + '\n3. '
        + thirdPlayerNameString + ' - ' + thirdPlayerScoreString
        + '\n4. ' + fourthPlayerNameString + ' - '
        + fourthPlayerScoreString + '\n5. ' + fifthPlayerNameString
        + ' - ' + fifthPlayerScoreString + '\n6. '
        + sixthPlayerNameString + ' - ' + sixthPlayerScoreString,
    font=('Times', 45, 'bold italic'),
    width=20,
    height=8,
    bg='black',
    fg='white',
    anchor='n',
    borderwidth=8,
    relief='ridge',
    )
leaderBoardPlayersLabel.grid(row=2, column=2)
paddingBetweenScoresAndButton = Label(LEADERBOARD, height=1,
        background='black')
paddingBetweenScoresAndButton.grid(row=3, column=2)
paddingRight = Label(LEADERBOARD, width=120, height=100,
                     background='black')
paddingRight.grid(row=5, column=4)

# GAME_INFO FRAME #

GAME_INFO = Frame(root, bg='black')
Button(GAME_INFO, text='Go To Main Menu',
       command=showMAIN_MENU).grid(row=2, column=2)

leftCanvas = Canvas(GAME_INFO, height=900, width=550, bg='black',
                    highlightthickness=0)
leftCanvas.grid(row=0, column=1, rowspan=11)
leftCanvas.create_image(190, 130, image=GAME_INFO_DOGGO_LEFT)

rightCanvas = Canvas(GAME_INFO, height=900, width=500, bg='black',
                     highlightthickness=0)
rightCanvas.grid(row=0, column=6, rowspan=11)
rightCanvas.create_image(300, 130, image=GAME_INFO_DOGGO_RIGHT)

paddingTop = Label(GAME_INFO, height=3, width=35, background='black')
paddingTop.grid(row=1, column=2)
paddingQuestionAndAsnwers = Label(GAME_INFO, height=1, width=35,
                                  background='black')
paddingQuestionAndAsnwers.grid(row=3, column=2)
paddingBottomRight = Label(GAME_INFO, height=50, width=200,
                           background='black')
paddingBottomRight.grid(row=15, column=15)
paddingBottom = Label(GAME_INFO, height=2, width=1, background='black')
paddingBottom.grid(row=10, column=2)

question = Label(
    GAME_INFO,
    text='Game Information',
    font=('Times', 70, 'bold italic'),
    fg='white',
    height=1,
    width=20,
    background='black',
    ).grid(row=2, column=2)

appleTreat = Label(
    GAME_INFO,
    height=4,
    width=70,
    fg='white',
    font=('Times', 20, 'bold italic'),
    background='black',
    text='Eating an apple or treat gives you points!' +
    'You need 100 to pass to the next level.',
    anchor='w',
    )
appleTreat.grid(row=4, column=2)
choco = Label(
    GAME_INFO,
    height=4,
    width=70,
    fg='white',
    font=('Times', 20, 'bold italic'),
    background='black',
    text="Eating chocolate increases your speed but decreases you points" +
    "because it isn't good for you.",
    anchor='w',
    )
choco.grid(row=5, column=2)
trashL = Label(
    GAME_INFO,
    height=4,
    width=70,
    fg='white',
    font=('Times', 20, 'bold italic'),
    background='black',
    text='Eating trash is, as is in most cases - deadly.',
    anchor='w',
    )
trashL.grid(row=6, column=2)
rot = Label(
    GAME_INFO,
    height=4,
    width=70,
    fg='white',
    font=('Times', 20, 'bold italic'),
    background='black',
    text="Eating rotten apples won't kill you, but it will hurt your score.",
    anchor='w',
    )
rot.grid(row=7, column=2)
ham = Label(
    GAME_INFO,
    height=4,
    width=70,
    fg='white',
    font=('Times', 20, 'bold italic'),
    background='black',
    text='Eating the ham will advance you to the next level automatically!',
    anchor='w',
    )
ham.grid(row=8, column=2)

Button(
    GAME_INFO,
    text='Main Menu',
    font=('Times', 50, 'bold italic'),
    bg='black',
    fg='white',
    activebackground='white',
    width=16,
    height=1,
    borderwidth=10,
    relief='groove',
    command=showMAIN_MENU,
    ).grid(row=9, column=2)

leftCanvas.create_image(500, 220, image=normal_appleImg)
leftCanvas.create_image(390, 220, image=treatImg)
leftCanvas.create_image(500, 340, image=chocoImg)
leftCanvas.create_image(500, 460, image=trashImg)
leftCanvas.create_image(500, 580, image=rotten_appleImg)
leftCanvas.create_image(500, 700, image=hamImg)

# BETWEEN_LEVEL FRAME #

BETWEEN_LEVEL = Frame(root, bg='black')

leftCanvas = Canvas(BETWEEN_LEVEL, height=800, width=600, bg='black',
                    highlightthickness=0)
leftCanvas.grid(row=0, column=1, rowspan=7)
leftCanvas.create_image(420, 130, image=BETWEEN_LEVEL_DOGGO_LEFT)

rightCanvas = Canvas(BETWEEN_LEVEL, height=800, width=600, bg='black',
                     highlightthickness=0)
rightCanvas.grid(row=0, column=6, rowspan=7)
rightCanvas.create_image(190, 130, image=BETWEEN_LEVEL_DOGGO_RIGHT)

paddingTop = Label(BETWEEN_LEVEL, height=5, width=35, background='black'
                   )
paddingTop.grid(row=1, column=2)
paddingQuestionAndAsnwers = Label(BETWEEN_LEVEL, height=3, width=35,
                                  background='black')
paddingQuestionAndAsnwers.grid(row=3, column=2)
paddingBottomRight = Label(BETWEEN_LEVEL, height=50, width=200,
                           background='black')
paddingBottomRight.grid(row=10, column=10)

question = Label(
    BETWEEN_LEVEL,
    text='Woof! Congratulations!\nNow what?',
    font=('Times', 50, 'bold italic'),
    fg='white',
    height=2,
    width=20,
    background='black',
    )
question.grid(row=2, column=2)

saveScoreAndQuit = Button(
    BETWEEN_LEVEL,
    text='Quit and Save Score',
    width=20,
    height=2,
    command=showNAME_GETTER,
    font=('Times', 50, 'bold italic'),
    bg='black',
    fg='white',
    activebackground='white',
    borderwidth=10,
    relief='groove',
    ).grid(row=5, column=2)

saveGameAndQuit = Button(
    BETWEEN_LEVEL,
    text='Quit and Save Game',
    height=2,
    width=20,
    command=saveGame,
    font=('Times', 50, 'bold italic'),
    bg='black',
    fg='white',
    activebackground='white',
    borderwidth=10,
    relief='groove',
    ).grid(row=6, column=2)

toTwo = Button(
    BETWEEN_LEVEL,
    text='Level 2',
    command=LEVEL_2,
    width=20,
    height=2,
    font=('Times', 50, 'bold italic'),
    bg='black',
    fg='white',
    activebackground='white',
    borderwidth=10,
    relief='groove',
    )
toThree = Button(
    BETWEEN_LEVEL,
    text='Level 3',
    command=LEVEL_3,
    width=20,
    height=2,
    font=('Times', 50, 'bold italic'),
    bg='black',
    fg='white',
    activebackground='white',
    borderwidth=10,
    relief='groove',
    )
toFour = Button(
    BETWEEN_LEVEL,
    text='Level 4',
    command=LEVEL_4,
    width=20,
    height=2,
    font=('Times', 50, 'bold italic'),
    bg='black',
    fg='white',
    activebackground='white',
    borderwidth=10,
    relief='groove',
    )
toFive = Button(
    BETWEEN_LEVEL,
    text='Level 5',
    command=LEVEL_5,
    width=20,
    height=2,
    font=('Times', 50, 'bold italic'),
    bg='black',
    fg='white',
    activebackground='white',
    borderwidth=10,
    relief='groove',
    )
toSix = Button(
    BETWEEN_LEVEL,
    text='Go To Endless Mode?',
    command=LEVEL_6,
    width=20,
    height=2,
    font=('Times', 50, 'bold italic'),
    bg='black',
    fg='white',
    activebackground='white',
    borderwidth=10,
    relief='groove',
    )
toEndless = Button(
    BETWEEN_LEVEL,
    text='Stay in Endless Mode?',
    command=LEVEL_6,
    width=20,
    height=2,
    font=('Times', 50, 'bold italic'),
    bg='black',
    fg='white',
    activebackground='white',
    borderwidth=10,
    relief='groove',
    )

# NAME_GETTER FRAME #

NAME_GETTER = Frame(root, bg='black')

leftCanvas = Canvas(NAME_GETTER, height=880, width=500, bg='black',
                    highlightthickness=0)
leftCanvas.grid(row=0, column=0, rowspan=6)
leftCanvas.create_image(320, 130, image=NAME_GETTER_DOGGO_LEFT)

rightCanvas = Canvas(NAME_GETTER, height=880, width=600, bg='black',
                     highlightthickness=0)
rightCanvas.grid(row=0, column=3, rowspan=6)
rightCanvas.create_image(180, 130, image=NAME_GETTER_DOGGO_RIGHT)

playerNameEntry = Entry(NAME_GETTER, font=('Times', 90, 'bold'),
                        width=5)
playerNameEntry.grid(row=3, column=1)

paddingBottomRight = Label(NAME_GETTER, height=100, width=200,
                           background='black')
paddingBottomRight.grid(row=10, column=10)
paddingBetweenQuestionAndEntry = Label(NAME_GETTER, height=10, width=1,
        background='black').grid(row=2, column=1)
paddingBetweenEntryAndSubmit = Label(NAME_GETTER, height=2, width=1,
        background='black').grid(row=4, column=1)

question = Label(NAME_GETTER,
                 text="""A good dog knows when to stop chasing its tail.
Please input your 3 initials!
(If you don't input just 3 characters,
we will take the first three and give the rest to the dog.)""",
                 font=('Times', 30, 'bold'), bg='black', fg='white'
                 ).grid(row=1, column=1)

sub_btn = Button(
    NAME_GETTER,
    text='Submit and Exit',
    command=submit,
    width=20,
    height=2,
    font=('Times', 50, 'bold italic'),
    bg='black',
    fg='white',
    activebackground='white',
    borderwidth=10,
    relief='groove',
    ).grid(row=5, column=1)

# GAME_OVER FRAME #

GAME_OVER = Frame(root, bg='black')

leftCanvas = Canvas(GAME_OVER, height=880, width=700, bg='black',
                    highlightthickness=0)
leftCanvas.grid(row=0, column=1, rowspan=6)

rightCanvas = Canvas(GAME_OVER, height=880, width=700, bg='black',
                     highlightthickness=0)
rightCanvas.grid(row=0, column=3, rowspan=6)

paddingBetweenMessageAndButton = Canvas(GAME_OVER, height=400,
        width=400, bg='black', highlightthickness=0)
paddingBetweenMessageAndButton.grid(row=3, column=2)
paddingBetweenMessageAndButton.create_image(200, 200,
        image=GAME_OVER_DOGGO)

Label(
    GAME_OVER,
    text='Sad woof...\nAll dogs go to heaven.',
    font=('Times', 50, 'bold italic'),
    fg='white',
    height=2,
    width=20,
    background='black',
    ).grid(row=2, column=2)

Button(
    GAME_OVER,
    text='Main Menu',
    font=('Times', 50, 'bold italic'),
    bg='black',
    fg='white',
    width=17,
    height=2,
    command=showMAIN_MENU,
    activebackground='white',
    borderwidth=10,
    relief='groove',
    ).grid(row=4, column=2)

# BOSS_KEY FRAME #

BOSS_KEY = Frame(root)
bossCanvas = Canvas(BOSS_KEY, width=1800, height=900)
bossCanvas.grid(row=0, column=0)
bossKeyImg = PhotoImage(file='bossKey.png')
bossCanvas.create_image(1050, 465, image=bossKeyImg)

# PAUSE FRAME #

PAUSE = Frame(root, bg='black')
paddingLeftAndTop = Label(PAUSE, height=5, width=20, background='black'
                          ).grid(row=0, column=0)
message = Label(
    PAUSE,
    text="Tea time!\nThe game is paused, press 'u' to unpause!",
    fg='white',
    bg='black',
    font=('Ubuntu', 60, 'bold'),
    height=5,
    width=35,
    ).grid(row=1, column=1)
paddingLeftAndTop = Label(PAUSE, height=80, width=35, background='black'
                          ).grid(row=10, column=10)

# CONTROLS Frame #

CONTROLS = Frame(root, bg='black')

leftCanvas = Canvas(CONTROLS, height=890, width=360, bg='black',
                    highlightthickness=0)
leftCanvas.grid(row=0, column=0, rowspan=11)
leftCanvas.create_image(220, 130, image=CONTROLS_DOGGO_LEFT)

rightCanvas = Canvas(CONTROLS, height=890, width=400, bg='black',
                     highlightthickness=0)
rightCanvas.grid(row=0, column=6, rowspan=11)
rightCanvas.create_image(150, 130, image=CONTROLS_DOGGO_RIGHT)

leftButtonEntry = Entry(CONTROLS, width=2)
leftButtonEntry.grid(row=3, column=3, sticky='e')

rightButtonEntry = Entry(CONTROLS, width=2)
rightButtonEntry.grid(row=4, column=3, sticky='e')

winCheatCodeEntry = Entry(CONTROLS, width=2)
winCheatCodeEntry.grid(row=5, column=3, sticky='e')

increaseScoreCheatCodeEntry = Entry(CONTROLS, width=2)
increaseScoreCheatCodeEntry.grid(row=6, column=3, sticky='e')

increaseSpeedCheatCodeEntry = Entry(CONTROLS, width=2)
increaseSpeedCheatCodeEntry.grid(row=7, column=3, sticky='e')

decreaseSpeedCheatCodeEntry = Entry(CONTROLS, width=2)
decreaseSpeedCheatCodeEntry.grid(row=8, column=3, sticky='e')

paddingTop = Label(CONTROLS, height=1, width=45, background='black')
paddingTop.grid(row=0, column=1)

question = Label(
    CONTROLS,
    height=2,
    width=25,
    text='     Would you like to change\n     the controls?',
    fg='white',
    background='black',
    font=('Times', 60, 'bold'),
    )
question.grid(row=1, column=1, columnspan=4)

leftQuestion = Label(
    CONTROLS,
    height=1,
    width=53,
    text='Pressing this button causes the dog to move to the left:',
    fg='white',
    font=('Times', 25, 'bold'),
    background='black',
    anchor='w',
    )
leftQuestion.grid(row=3, column=1, columnspan=2)

rightQuestion = Label(
    CONTROLS,
    height=1,
    width=53,
    text='Pressing this button causes the dog to move to the right:',
    fg='white',
    font=('Times', 25, 'bold'),
    background='black',
    anchor='w',
    )
rightQuestion.grid(row=4, column=1, columnspan=2)

winCheatCodeQuestion = Label(
    CONTROLS,
    height=1,
    width=53,
    text='Pressing this button causes the player to pass to the next level: ',
    fg='white',
    font=('Times', 25, 'bold'),
    background='black',
    anchor='w',
    )
winCheatCodeQuestion.grid(row=5, column=1, columnspan=2)

increaseScoreCheatCodeQuestion = Label(
    CONTROLS,
    height=1,
    width=53,
    text='Pressing this button increases the current score by 10:',
    fg='white',
    font=('Times', 25, 'bold'),
    background='black',
    anchor='w',
    )
increaseScoreCheatCodeQuestion.grid(row=6, column=1, columnspan=2)

increaseSpeedCheatCodeQuestion = Label(
    CONTROLS,
    height=1,
    width=53,
    text="Pressing this button increases the dog's speed: ",
    fg='white',
    font=('Times', 25, 'bold'),
    background='black',
    anchor='w',
    )
increaseSpeedCheatCodeQuestion.grid(row=7, column=1, columnspan=2)

decreaseSpeedCheatCodeQuestion = Label(
    CONTROLS,
    height=1,
    width=53,
    text="Pressing this button decreases the dog's speed: ",
    fg='white',
    font=('Times', 25, 'bold'),
    background='black',
    anchor='w',
    )
decreaseSpeedCheatCodeQuestion.grid(row=8, column=1, columnspan=2)

leftSubmit = Button(CONTROLS, text='Submit',
                    command=submitLeftControl).grid(row=3, column=5,
        sticky='w')
rightSubmit = Button(CONTROLS, text='Submit',
                     command=submitRightControl).grid(row=4, column=5,
        sticky='w')
winCheatCodeSubmit = Button(CONTROLS, text='Submit',
                            command=submitWin).grid(row=5, column=5,
        sticky='w')
increaseScoreCheatCodeSubmit = Button(CONTROLS, text='Submit',
        command=submitAddTen).grid(row=6, column=5, sticky='w')
increaseSpeedCheatCodeSubmit = Button(CONTROLS, text='Submit',
        command=submitIncreaseSpeed).grid(row=7, column=5, sticky='w')
decreaseSpeedCheatCodeSubmit = Button(CONTROLS, text='Submit',
        command=submitDecreaseSpeed).grid(row=8, column=5, sticky='w')

Button(
    CONTROLS,
    text='Main Menu',
    font=('Times', 50, 'bold italic'),
    bg='black',
    fg='white',
    width=17,
    height=2,
    command=showMAIN_MENU,
    activebackground='white',
    borderwidth=10,
    relief='groove',
    ).grid(row=10, column=2, columnspan=4, sticky='w')

Button(
    CONTROLS,
    text='Reset Settings',
    font=('Times', 50, 'bold italic'),
    bg='black',
    fg='white',
    width=17,
    height=2,
    command=resetSettings,
    activebackground='white',
    borderwidth=10,
    relief='groove',
    ).grid(row=10, column=1, sticky='w')

MAIN_MENU.grid()
root.mainloop()
