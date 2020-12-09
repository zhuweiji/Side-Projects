import random
import time
import turtle  # main GUI user interacts with
from itertools import cycle  # for cyclical lists
import re  # for regex searches
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer  # for sound
import math

print('loading please wait..')
screen = turtle.Screen()  # initialising the main screen of the GUI
screen.setup(1000, 800)  # size of GUI window probably 800x800
screen.title("Wheel of Fortune")
mixer.init()

freeplay = 0
wheel_state = 0  # explained later
turn_end = 0
letters_used = []

# todo : solve puzzle congrats image

# todo : rules
# todo : spezzaz
# todo : images for all loses (bankrupt, wrong answer, freeplay etc)
# todo : exe.file without command console visible

# todo : fill up sheet
# todo : playtest
# todo : playtest freeplay
# todo : remove all print statements

# todo : option menu w player number


players = {1: 0, 2: 0, 3: 0}  # key = players | value = money, image files are tagged to player numbers
player_pool = cycle(players)  # creating a rotating list of players
current_player = next(player_pool)  # getting the integer value of the first player
current_cash = players[current_player]

f = open(r'misc/wheel_outcomes', 'r')  # the results of spinning the wheel
wheel_outcomes = f.read().split(',')
for i, j in enumerate(wheel_outcomes):  # converting all dollar values to int
    try:
        wheel_outcomes[i] = int(j)
    except ValueError:
        pass

f = open(r'misc/Phrases.txt', 'r')  # the possible puzzle phrases to be guessed
phrase_list = f.read().split('\n')
puzzle_phrase = phrase_list[random.randint(0, len(phrase_list)-1)]


square = u"\U000025A1"
solved_phrase = []  # currently solved letters


for letter in puzzle_phrase:  # to obscure phrase texts to unicode sqaures
    if letter == ' ':
        solved_phrase.append(' ')
    else:
        solved_phrase.append(square)

solved_phrase = ''.join(solved_phrase)

for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    screen.register_shape('misc/puzzle screen/{}.gif'.format(letter))
screen.register_shape('misc/puzzle screen/blank.gif'.format(letter))
text_turtle = turtle.Turtle()
text_turtle.hideturtle()
text_turtle.speed(500)
text_turtle.up()


def splitting_text() -> str:
    foo = solved_phrase.split()
    out = '\n'.join(a for a in foo)
    return out


split_text = splitting_text()


def delay(length=float(3)):
    start = time.time()
    while time.time() - start < length:
        screen.update()


def start_up():  # add wheel of fortune intro
    """ initial screen when game is first started"""
    mixer.music.load('misc/sound/intro.wav')
    mixer.music.play(0)

    screen.clear()
    delay(0.5)
    screen.register_shape('misc/title/title1.gif')
    screen.bgpic('misc/title/title1.gif')
    delay(1.4)
    screen.register_shape('misc/title/title2.gif')
    screen.bgpic('misc/title/title2.gif')
    delay(1.2)
    screen.register_shape('misc/title/title3.gif')
    screen.bgpic('misc/title/title3.gif')

    delay(5)
    avatar = turtle.Turtle()
    avatar.hideturtle()
    screen.register_shape('misc/avatar/person1.gif')
    avatar.shape('misc/avatar/person1.gif')
    avatar.up()
    avatar.speed(500)
    avatar.goto(100, -200)
    avatar.showturtle()

    delay(1.5)
    avatar = turtle.Turtle()
    avatar.speed(500)
    avatar.up()
    avatar.hideturtle()
    screen.register_shape('misc/avatar/person2.gif')
    avatar.shape('misc/avatar/person2.gif')
    avatar.goto(175, -200)
    avatar.showturtle()

    delay(1.3)
    avatar = turtle.Turtle()
    avatar.speed(500)
    avatar.up()
    avatar.hideturtle()
    screen.register_shape('misc/avatar/person3.gif')
    avatar.shape('misc/avatar/person3.gif')
    avatar.goto(250, -200)
    avatar.showturtle()

    delay(3.5)
    mixer.music.fadeout(2)
    screen.update()


def show_player():
    """ shows the player avatar and their money at the bottom right """
    avatar_path = 'misc/avatar/person{}.gif'.format(current_player)
    mixer.music.stop()

    screen.register_shape(avatar_path)
    avatar = turtle.Turtle()
    avatar.hideturtle()
    avatar.shape(avatar_path)
    avatar.up()
    avatar.speed(500)
    avatar.goto(250, -200)
    avatar.showturtle()

    text_turtle.goto(250, -350)
    text_turtle.write("Cash: ${}".format(current_cash), font=('', 25, 'bold'))


def show_solved_phrase():
    screen.clear()
    screen.register_shape('misc/puzzle screen/emptypuzzle.gif')
    screen.bgpic('misc/puzzle screen/emptypuzzle.gif')
    mixer.music.load('misc/sound/Puzzle Reveal.wav')
    mixer.music.play(0)
    split_len = [len(word) for word in puzzle_phrase.split()]
    count = 0
    for word in split_len:
        count += int(word)
        count += 1
    count -= 1

    def put_letter(x, y, letter):
        foo = turtle.Turtle()
        foo.speed(200)
        foo.up()
        foo.hideturtle()
        foo.goto(x, y)
        foo.shape('misc/puzzle screen/{}.gif'.format(letter))
        foo.showturtle()

    x_offset, y_offset = 54.3, -66.8

    x_pos, y_pos = -306, 115
    x_check = -306


    final_x = -306
    for word in solved_phrase.split():
        if x_pos > 306:
            y_pos += y_offset
            if y_pos == 115 or y_pos == -83.6 or math.isclose(y_pos,-85,abs_tol=1):
                x_pos = -306
            else:
                x_pos = -359
            final_x = x_pos

        for letter in word:
            final_x += x_offset

        if final_x > 306:
            y_pos += y_offset
            if y_pos == 115 or y_pos == -83.6 or math.isclose(y_pos,-85,abs_tol=1):
                x_pos = -306
            else:
                x_pos = -359

        for letter in word:
            if letter == u"\U000025A1":
                put_letter(x_pos,y_pos,'blank')
                x_pos += x_offset

            if letter.isalpha():
                put_letter(x_pos, y_pos, letter)
                x_pos += x_offset
        x_pos += x_offset
        final_x = x_pos
    delay(2.5)


def solve_puzzle():
    global current_player, split_text, current_cash, solved_phrase
    mixer.music.stop()
    try:
        answer = screen.textinput(' ', 'Enter your answer:').upper()

    except AttributeError:
        solve_puzzle()

    if answer == puzzle_phrase:
        solved_phrase = puzzle_phrase
        show_solved_phrase()
        screen.clear()

        mixer.music.load('misc/sound/win.wav')
        mixer.music.play(0)

        screen.register_shape('misc/win.gif')
        screen.bgpic('misc/win.gif')
        show_player()
        mixer.music.fadeout(2)
        delay(12)
        screen.bye()

    else:
        mixer.music.load('misc/sound/awwt.wav')
        mixer.music.play(0)
        screen.clear()
        show_player()
        screen.register_shape('misc/wrongans.gif')
        screen.bgpic('misc/wrongans.gif')
        delay(3)
        show_solved_phrase()

        current_player = next(player_pool)
        current_cash = players[current_player]
        player_turn()


def show_wheel(spin=0) -> int or str:
    """ shows the wheel at its current state, returns 0
        nested function spins the wheel a random number of times, returns the spin result"""
    screen.clearscreen()
    global wheel_state

    pointer = turtle.Turtle()
    pointer.hideturtle()
    pointer.shapesize(10)
    pointer.up()
    pointer.speed(100)
    pointer.setpos(15, 300)
    pointer.setheading(270)
    pointer.showturtle()
    show_player()

    def spin_wheel():  # add wheel turning music pipipipipipip todo
        SPIN_SPEED = 0.02
        global wheel_state
        spin_strength = random.randint(100, 250)
        show_player()
        mixer.music.load('misc/sound/Bonus Wheel Music.wav')
        mixer.music.play(-1)
        while spin_strength:
            wheel_path = "misc/wheels/{}.gif".format(wheel_state)
            screen.bgpic(wheel_path)

            if spin_strength < 4:
                delay(SPIN_SPEED * 8)
                mixer.Channel(0).play(mixer.Sound('misc/sound/ding.wav'))
            elif spin_strength < 10:
                delay(SPIN_SPEED * 6)
                mixer.Channel(0).play(mixer.Sound('misc/sound/ding.wav'))
            elif spin_strength < 40:
                delay(SPIN_SPEED * 4)
                mixer.Channel(0).play(mixer.Sound('misc/sound/ding.wav'))
            else:
                delay(SPIN_SPEED)
                mixer.Channel(0).play(mixer.Sound('misc/sound/fastding.wav'))
            screen.update()

            wheel_state += 1
            spin_strength -= 1
            if wheel_state == 24:
                wheel_state = 0

        wheel_state = wheel_state - 1 if wheel_state != 0 else 23
        delay(3)  # todo release fix
        mixer.music.fadeout(1)
        return wheel_outcomes[wheel_state]

    if spin == 1:
        return spin_wheel()
    else:
        wheel_path = "misc/wheels/{}.gif".format(wheel_state)
        screen.register_shape(wheel_path)
        screen.bgpic(wheel_path)
        screen.update()

        delay(3)  # todo release fix

        return 0


def consonant_vowel(x, y):
    global current_cash, solved_phrase, turn_end, current_player, letters_used, freeplay
    count = 0
    consonant = 1 if x < 0 else 0
    choice = screen.textinput(' ', 'Enter a {}'.format('consonant' if consonant else 'vowel'))
    mixer.music.stop()

    if choice is None:
        consonant_vowel(x, y)

    try:
        choice = choice.upper()

        if len(choice) != 1:  # add error message todo
            screen.clear()
            show_player()
            text_turtle.goto(-200, 0)
            text_turtle.write("That's more than one character !", font=('', 40, 'bold'))

            delay(3)
            raise TypeError

        if consonant:  # making sure that letter is a vowel
            if 'BCDFGHJKLMNPQRSTVXYZ'.find(choice) == -1:
                screen.clear()
                show_player()
                text_turtle.goto(-200, 0)
                text_turtle.write('Please enter a consonant', font=('', 40, 'bold'))
                text_turtle.goto(-200, -100)
                text_turtle.write('BCDFGHJKLMNPQRSTVXYZ', font=('', 20, 'bold'))

                delay(3)
                raise TypeError

            if choice in letters_used:  # check if letter has been used yet
                screen.clear()

                screen.register_shape('misc/alreadychosen.gif')
                screen.bgpic('misc/alreadychosen.gif')
                mixer.music.load('misc/sound/awwt.wav')
                mixer.music.play(0)

                delay(3)
                show_solved_phrase()
                current_player = next(player_pool)
                current_cash = players[current_player]
                player_turn()

        if not consonant:  # making sure that user entry is a vowel

            if 'AEIOU'.find(choice) == -1:
                screen.clear()
                show_player()
                text_turtle.goto(-200, 0)
                text_turtle.write('Please enter a vowel', font=('', 40, 'bold'))
                text_turtle.goto(-200, -100)
                text_turtle.write('AEIOU', font=('', 20, 'bold'))
                delay(3)

            if choice in letters_used:  # checking that letter has not been used yet
                screen.clear()
                screen.register_shape('misc/alreadychosen.gif')
                screen.bgpic('misc/alreadychosen.gif')
                mixer.music.load('misc/sound/awwt.wav')
                mixer.music.play(0)

                delay()

                show_solved_phrase()

                current_player = next(player_pool)
                current_cash = players[current_player]
                player_turn()

    except TypeError:
        print('TypeError ignored')
        consonant_vowel(x, y)

    except AttributeError:
        pass

    letters_used.append(choice)

    if consonant:  # user chose consonant
        for i, letters in enumerate(puzzle_phrase):  # checking for correct letter
            if letters == choice:
                solved_phrase = solved_phrase[:i] + letters + solved_phrase[i+1:] # fill consonant into phrase
                count += 1

        if count:  # correct guess
            if not freeplay:
                current_cash += count * wheel_outcomes[wheel_state]  # add wheel result + wheel result * number of cons
            count = 0  # can take out if function is called from the start

            screen.clear()
            mixer.music.load('misc/sound/Puzzle solve.wav')
            mixer.music.play(1)
            screen.register_shape('misc/lettercorrect.gif')
            screen.bgpic('misc/lettercorrect.gif')
            delay(3)

            show_solved_phrase()

            freeplay = 0
            screen.clear()

            show_player()
            text_turtle.goto(-300, -100)
            text_turtle.write('Spin the wheel again\n\n\n'  
                              'Buy a vowel\n\n\n'
                              'Solve the puzzle', font=('', 37, 'bold'))
            mixer.music.load('misc/sound/Countdown.wav')
            mixer.music.play(0)
            screen.onclick(win_consonant)

            delay(10)
            # lambda xpos,ypos : player_turn() if x<0
            # player has another spin or can buy vowel or solve puzzle todo

        else:  # incorrect guess
            screen.clear()
            screen.register_shape('misc/wrongans.gif')
            screen.bgpic('misc/wrongans.gif')
            mixer.music.load('misc/sound/awwt.wav')
            mixer.music.play(0)
            delay(3)
            show_solved_phrase()

            if freeplay:
                screen.clear()

                show_player()
                text_turtle.goto(-300, -100)
                text_turtle.write('Spin the wheel again\n\n\n'
                                  'Buy a vowel\n\n\n'
                                  'Solve the puzzle', font=('', 37, 'bold'))  # todo: add pic and music
                mixer.music.load('misc/sound/Countdown.wav')
                mixer.music.play(0)
                freeplay = 0
                screen.onclick(win_consonant)
                delay(10)

            turn_end = 1
            current_player = next(player_pool)
            current_cash = players[current_player]
            player_turn()

    if not consonant:  # vowel
        if current_cash >= 250 or freeplay:
            if not freeplay:
                current_cash -= 250

            for i, letters in enumerate(puzzle_phrase):
                if letters == choice:
                    count += 1
                    solved_phrase = solved_phrase[:i] + letters + solved_phrase[i+1:]  # fill vowel into phrase

            if count != 0:  # vowel sucess
                freeplay = 0
                count = 0
                screen.clear()
                screen.register_shape('misc/lettercorrect.gif')
                screen.bgpic('misc/lettercorrect.gif')
                mixer.music.load('misc/sound/Puzzle solve.wav')
                mixer.music.play(1)
                delay(3)

                show_solved_phrase()
                screen.clear()

                show_player()
                text_turtle.goto(-300, -100)
                text_turtle.write('Buy a vowel\n\n\n\n\n\n'
                                  'Solve the puzzle', font=('', 37, 'bold'))  # todo make nice
                text_turtle.goto(-300, -250)
                text_turtle.write('Vowels cost $250', font=('', 25, 'bold'))

                mixer.music.load('misc/sound/Countdown.wav')
                mixer.music.play(0)
                screen.onclick(win_vowel)

                delay(10)
            else:
                freeplay = 0
                screen.clear()
                text_turtle.goto(-200, 300)
                text_turtle.write('Wrong Guess', font=('', 40, 'bold')) # todo: make nice
                mixer.music.load('misc/sound/awwt.wav')
                mixer.music.play(0)

                show_solved_phrase()
                delay(3)
                turn_end = 1
                current_player = next(player_pool)
                current_cash = players[current_player]
                player_turn()

        else:  # not enough money
            screen.clear()
            screen.register_shape('misc/notenough.gif')
            screen.bgpic('misc/notenough.gif')

            mixer.music.load('misc/sound/awwt.wav')
            mixer.music.play(0)

            delay(3)
            player_turn()


def win_consonant(x, y):
    if y > 190:
        player_turn()
    elif 190 >= y >= 0:
        consonant_vowel(5, 0)
    elif 0 > y:
        solve_puzzle()


def win_vowel(x, y):
    if y > 0:
        consonant_vowel(5, 0)
    else:
        solve_puzzle()


def player_turn():
    global current_player, current_cash, freeplay, turn_end  # all calling from the same player dictionary in main scope
    screen.clearscreen()

    turn_end = 0
    mixer.music.stop()
    text_turtle = turtle.Turtle()  # text writing turtle in this function
    text_turtle.hideturtle()
    text_turtle.speed(500)
    text_turtle.up()

    def announce_player():
        text_turtle.goto(-400, 150)
        text_turtle.write("Player {}'s turn".format(current_player), font=('', 70, 'bold'))
        show_player()

    def show_result():
        screen.clearscreen()
        show_player()
        screen.register_shape('misc/spinresult.gif')
        screen.bgpic('misc/spinresult.gif')

        mixer.music.load('misc/sound/Toss Up Solve.wav')
        mixer.music.play(1)

        text_turtle.color("white")
        text_turtle.goto(50, 170)
        text_turtle.write(wheel_result, font=('', 75, 'bold'))
        delay(3)

    def select_screen():
        screen.clearscreen()

        mixer.music.load('misc/sound/Countdown.wav')
        mixer.music.play(1)

        screen.register_shape('misc/select1.gif')
        screen.bgpic('misc/select1.gif')

        screen.onclick(consonant_vowel)

        start = time.time()
        while not turn_end:
            screen.update()
            if time.time() - start >= 10.5:
                return

    announce_player()

    delay(2)  # todo release fix
    screen.clear()

    show_player()
    wheel_result = show_wheel(1)  # todo release fixspins the wheel and saves the result

    if wheel_result == 'Free Play':
        freeplay = 1
        screen.clear()
        screen.register_shape('misc/freeplay.gif')
        screen.bgpic('misc/freeplay.gif')
        delay(2)

    if wheel_result == 'Lose Turn' or wheel_result == 'Bankrupt':
        screen.clear()
        mixer.music.load('misc/sound/bankrupt.wav') # todo: change sound
        mixer.music.play(0)

        if wheel_result == 'Bankrupt':
            current_cash = 0
            screen.register_shape('misc/bankrupt.gif')
            screen.bgpic('misc/bankrupt.gif')

        if wheel_result == 'Lose Turn':
            screen.register_shape('misc/loseturn.gif')
            screen.bgpic('misc/loseturn.gif')

        delay(3)
        current_player = next(player_pool)
        current_cash = players[current_player]
        player_turn()

    show_result()
    show_solved_phrase()
    select_screen()

    current_player = next(player_pool)
    current_cash = players[current_player]
    player_turn()
    delay(3)


def game_loop():
    # check exit
    start_up()
    player_turn()


def prod_loop():
        player_turn()

print('loading complete!')
game_loop()
print(puzzle_phrase)
#solve_puzzle()
#prod_loop()
#show_solved_phrase()
#consonant_vowel(-1,2)
turtle.done()



