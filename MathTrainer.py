import customtkinter as s, random, os, ast
from tkinter import *

#APP CREATION (MAIN WINDOW)
app = s.CTk()
app.geometry("350x500+800+300")
app.title("MathTrainer Version 1.4")
app.resizable(FALSE,FALSE)

#ABBREVIATIONS FOR WIDGET CREATION
label = s.CTkLabel
button = s.CTkButton
window = s.CTkInputDialog
new_window = s.CTkToplevel
entry = s.CTkEntry
progressbar = s.CTkProgressBar
menu = s.CTkOptionMenu
segbutton = s.CTkSegmentedButton
switch = s.CTkSwitch
frame = s.CTkFrame

#ICON


#LANGUAGES
english = {
        "app_head_bar": "Mathtrainer Version 1.4 - by Lukacho",
        "app_description": "Mathtrainer Version 1.4 \n\nDesigned for big thinkers!",
        "app_start_button": "Play",
        "app_options_button": "Options",
        "app_exit_button": "Quit Game",

        "game_countdown": "Prepare yourself!",
        "game_question": "What is",
        "game_streak": " in a row!",
        "game_standard_description1": "Solve as many calculations as possible.\n\n You have around ",
        "game_standard_description2": " minutes on the clock.\n\n\n Currently Selected Difficulty: ",
        "game_practice_description": f"Solve as many calculations as you want!\n\n Since Practice Mode is selected, you don't\nhave a time limit here.\n\n\n Currently Selected Difficulty: ",
        "game_onelife_description": f"Solve as many calculations as possible.\n\n You have unlimited time, but if you\nfail a single time, the game is over.\n\n\n Currently Selected Mode: ",
        "game_ready": "Ready?",
        "game_over":  "Game Over!",
        "game_totalcalcs1": f"You have solved ", 
        "game_totalcalcs2": " calculations. Congrats!\n Your total score: ",
        "game_points": " Points",
        "game_stop": "Stop",
        "game_leave": "Exit",
        "game_mode": "Current mode: ",

        "options_appearance": "Appearance",
        "options_difficulty": "Difficulty",
        "options_subtraction": "Subtraction (-)",
        "options_multiplication": "Multiplication (*)",
        "options_game_mode": "Game Modes",
        "options_exit": "Save Changes",

        "practice_mode": "Practice",

        "mode_easy": "Easy",
        "mode_normal": "Normal",
        "mode_hard": "Hard",
        "mode_extreme": "Extreme",

        "record": "New Highscore!"
    }
deutsch = {
        "app_head_bar": "Mathtrainer Version 1.4 - von Lukacho",
        "app_description": "Mathtrainer Version 1.4 \n\nFür große Denker!",
        "app_start_button": "Spielen",
        "app_options_button": "Optionen",
        "app_exit_button": "Spiel verlassen",

        "game_countdown": "Mach dich bereit!",
        "game_question": "Was ergibt",
        "game_streak": " hintereinander!",
        "game_standard_description1": "Löse so viele Rechnungen wie möglich.\n\n Du hast in etwa ",
        "game_standard_description2": " Minuten Zeit.\n\n\n Ausgewählter Schwierigkeitsgrad: ",
        "game_practice_description": f"Löse so viele Rechnungen wie du willst!\n\n Da der Trainingsmodus aktiviert ist, gibt\nes kein Zeitlimit.\n\n\n Ausgewählter Schwierigkeitsgrad: ",
        "game_onelife_description": f"Löse so viele Rechnungen wie möglich.\n\n Du hast unbegrenzte Zeit, aber\nnach einem Fehler ist das Spiel vorbei\n\n\n Ausgewählter Schwierigkeitsgrad: ",
        "game_ready": "Bereit?",
        "game_over":  "Die Zeit ist aus!",
        "game_totalcalcs1": f"Du hast ", 
        "game_totalcalcs2": " Rechnungen gelöst. Glückwunsch!\n Dein Punktestand: ",
        "game_points": " Punkte",
        "game_stop": "Beenden",
        "game_leave": "Verlassen",
        "game_mode": "Aktueller Modus: ",

        "options_appearance": "Erscheinungsbild",
        "options_difficulty": "Schwierigkeit",
        "options_subtraction": "Subtraktion (-)",
        "options_multiplication": "Multiplikation (*)",
        "options_game_mode": "Spielmodi",
        "options_exit": "Änderungen Speichern",

        "practice_mode": "Training",

        "mode_easy": "Einfach",
        "mode_normal": "Normal",
        "mode_hard": "Schwer",
        "mode_extreme": "Extrem",

        "record": "Neuer Rekord!"
    }

#FUNC FOR LOADING LANGUAGE SETTING AND RECORDS
def loadFile(filename):
    internal_dir = "_internal"
    file_path = os.path.join(internal_dir, filename)
    
    # Ensure the directory exists
    if not os.path.exists(internal_dir):
        os.makedirs(internal_dir)  # Create the directory if it doesn't exist
    
    # Check if the file exists and read it
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            content = file.read()  # Read file content
            if content != '':
                return content
    elif filename == "PrefLanguage.txt":
        return "English"
    else:
        return "[0,0,0,0,0]"

# Example usage
content = loadFile("somefile.txt")
print(content)


#FUNC FOR SAVING LANGUAGE SETTINGS AND RECORDS
def saveFile(data, filename):
    with open(rf"_internal/{filename}", "w") as file:
        file.write(data)

#INITIALIZING RECORDS AND LANGUAGE SETTINGS
record = loadFile("Records.txt")
language_preference = loadFile("PrefLanguage.txt")
highscores = ast.literal_eval(record)
language = english
if language_preference == "Deutsch":
    language = deutsch
else:
    language = english

numbers_easy = [list(range(1,21)), list(range(1,11)),-0.01, 2, 0.02] #[numbers for + and - operations, numbers for * and / operations, progressbar speed, timer, penalty, scores]
numbers_normal = [list(range(21,101)),list(range(10,21)),-0.0075, 3, 0.03]
numbers_hard = [list(range(101,1001)),list(range(20,31)),-0.0050, 4, 0.04]
numbers_extreme = [list(range(1001,10001)),list(range(30,41)),-0.0025, 5, 0.05]
chosen_difficulty = language["mode_easy"]
chosen_operands = []
operand_bonus = 0
chosen_mode = "Standard"
countdown = 5
solved = 0
streak = 0
mode = "dark"



#GAME##############################################################################################
total_score = 0
rank = "F"

def game():
    global total_score, operand_bonus, chosen_difficulty, chosen_language, record
    game_window = new_window(app)
    game_window.title("")
    game_window.geometry("300x400+800+300")
    game_window.resizable(FALSE,FALSE)
    app.withdraw() 

    match chosen_difficulty:
        case "Einfach":
            chosen_difficulty = "Easy"
        case "Schwer":
            chosen_difficulty = "Hard"
        case "Extrem":
            chosen_difficulty = "Extreme"
    
    match chosen_difficulty:
        case "Easy":
            mode_numbers = numbers_easy[0]
            dot_mode_numbers = numbers_easy[1]
            bar_speed = numbers_easy[2]
            gametime = numbers_easy[3]
            penalty = numbers_easy[4]
            score = 10
            chosen_difficulty = language["mode_easy"]
        case "Normal":
            mode_numbers = numbers_normal[0]
            dot_mode_numbers = numbers_normal[1]
            bar_speed = numbers_normal[2]
            gametime = numbers_normal[3]
            penalty = numbers_normal[4]
            score = 100
            chosen_difficulty = language["mode_normal"]
        case "Hard":
            mode_numbers = numbers_hard[0]
            dot_mode_numbers = numbers_hard[1]
            bar_speed = numbers_hard[2]
            gametime = numbers_hard[3]
            penalty = numbers_hard[4]
            score = 300
            chosen_difficulty = language["mode_hard"]
        case "Extreme":
            mode_numbers = numbers_extreme[0]
            dot_mode_numbers = numbers_extreme[1]
            bar_speed = numbers_extreme[2]
            gametime = numbers_extreme[3]
            penalty = numbers_extreme[4]
            score = 500
            chosen_difficulty = language["mode_extreme"]

    operand_bonus = (len(chosen_operands)-1) * 5
    background = label(game_window,text="+-+-+-+-+\n+-+-+-+-+\n+-+-+-+-+\n+-+-+-+-+\n+-+-+-+-+\n+-+-+-+-+\n", font=("Modern",70),text_color="grey")
    background.place(x=0,y=0)
    bar = progressbar(game_window, progress_color="green",fg_color="lightblue",width=300,height=20,corner_radius=0,determinate_speed=bar_speed,border_color="white")
    bar_text = label(game_window, text="",font=("System",15,"bold"),justify="center",text_color="green")
    question = label(game_window,text="",font=("Tekton Pro",20,"bold"),fg_color="grey", corner_radius=10)
    answer_box = entry(game_window,fg_color="transparent",state=DISABLED)

    stats_text = label(game_window, justify="center")
    stats = label(game_window, justify="center", font=("System",30,"bold"),text_color="darkgreen")
    rank_display = label(game_window, text="", justify="center", font=("System",25,"bold"),text_color="blue")
    record_display = label(game_window, text="",font=("Tekton Pro",20,"bold"),text_color="gold")
    
    def resetDisplay():
        background.configure(text_color="grey")
        answer_box.configure(fg_color=("white","black"))
        bar_text.configure(text="")

    def chooseCalc():
        answer_box.delete(0,END)
        operand = random.choice(chosen_operands)
        global solution
        
        if operand == "+":
            number = random.choice(mode_numbers)
            number2 = random.choice(mode_numbers)
            solution = str(number + number2)
        elif operand == "-":
            number = random.choice(mode_numbers)
            number2 = random.choice(mode_numbers)
            solution = str(number - number2)
        elif operand == "*":
            number = random.choice(dot_mode_numbers)
            number2 = random.choice(dot_mode_numbers)
            solution = str(number * number2)
        elif operand == "/":
            number2 = random.choice(dot_mode_numbers)
            multiplier = random.choice(dot_mode_numbers)
            number = number2 * multiplier
            solution = str(round(number / number2))
        question.configure(game_window, text=language["game_question"]+ f"\n{number} {operand} {number2}?")

    def checkAnswer(event= None):
        global solved, streak, total_score
        answer = answer_box.get()
        if answer == solution:
            solved += 1
            streak += 1
            total_score += (score + operand_bonus)
            if streak >= 5:
                bar_text.configure(text=f"{streak}" + language["game_streak"])
                total_score += streak
            background.configure(text_color="green")
            answer_box.configure(fg_color="green")
            bar_value = float(bar.get())
            bar.set(bar_value + 0.0066)
        else:
            background.configure(text_color="red")
            answer_box.configure(fg_color="red")
            streak = 0
            if chosen_mode == "Standard":
                bar_value = float(bar.get())
                bar.set(bar_value- penalty)
            if chosen_mode == "OneLife":
                stopGame()
                game_window.after(700, resetDisplay)
        chooseCalc()
        game_window.after(700, resetDisplay)

    def checkTimeOver():
        if bar.get() >= 0.001:
            if 0.5 >= bar.get() >= 0.1:
                bar.configure(fg_color="#ed895a")
            elif bar.get() <= 0.1:
                bar.configure(fg_color="#ed5a5a")
            game_window.after(10, checkTimeOver)
        else:
            stopGame()

    def timer():
        global countdown
        if chosen_mode != "Standard":
            countdown = 0
        ready_up_button.destroy()
        game_description.destroy()
        bar.pack()
        bar_text.pack()
        bar.set(1)
        question.pack(pady=30)
        answer_box.pack(pady=20)
        bars = ">>>>>"
        bars_inverse = "<<<<<"
        if countdown > 0:
            max_length = countdown
            bars = bars[:max_length]
            bars_inverse = bars_inverse[:max_length]
            game_window.after(1000, timer)
            question.configure(text=language["game_countdown"] + f"\n\n{bars} {countdown} {bars_inverse}\n")
            countdown -= 1
        else:
            chooseCalc()
            if chosen_mode == "Standard":
                checkTimeOver()
                bar.start()
            if chosen_mode == language["practice_mode"]:
                finish_button.pack(anchor="s")
                bar.configure(progress_color="#1f80e0")
            elif chosen_mode == "OneLife":
                bar.configure(progress_color="orange")
            answer_box.configure(state=NORMAL)
            answer_box.focus()
            countdown = 5

    if chosen_mode == "Standard":
        game_description = label(game_window,fg_color="#8f8786", corner_radius=10, text=language["game_standard_description1"] + f"{gametime}" + language["game_standard_description2"] + chosen_difficulty)
    elif chosen_mode == language["practice_mode"]:
        game_description = label(game_window,fg_color="#1f80e0", corner_radius=10, text=language["game_practice_description"] + chosen_difficulty)
    elif chosen_mode == "OneLife":
        game_description = label(game_window,fg_color="#8f8786", corner_radius=10, text=language["game_onelife_description"] + chosen_difficulty)
    ready_up_button = button(game_window, text=language["game_ready"],command=timer,fg_color="grey",hover_color="green")
    
    game_description.pack(pady=50)
    ready_up_button.pack(pady=10)
    answer_box.bind('<Return>', checkAnswer)
    
    def stopGame():
        global solved, rank, total_score, highscores
        color = ""
        if 0 <= total_score < 1000:
            rank = "F"
            color = "darkred"
        elif 1000 <= total_score < 2000:
            rank = "E"
            color = "gray"
        elif 2000 <= total_score < 3000: 
            rank = "D"
            color = ("brown","darkblue")
        elif 3000 <= total_score < 4000:
            rank = "C"
            color = "blue"
        elif 4000 <= total_score < 5500:
            rank = "B"
            color = ("darkblue","lightblue")
        elif 5500 <= total_score < 7000:
            rank = "A"
            color = "bronze"
        elif 7000 <= total_score < 8500:
            rank = "S"
            color = "purple"
        else:
            rank = "SS"
            color = ("orange","gold")


        bar.configure(fg_color="red")
        question.configure(text=language["game_over"],font=("",24,"bold"))
        answer_box.destroy()
        finish_button.destroy()
        stats_text.configure(text=language["game_totalcalcs1"] + f"{solved}" + language["game_totalcalcs2"])
        stats_text.pack(pady=20)
        stats.configure(text=f"{total_score}" + language["game_points"])
        stats.pack()
        if chosen_mode == "Standard":
            rank_display.configure(text=f"||   {rank}   ||",text_color=color)
            rank_display.pack(pady=20)
            if total_score > highscores[0]:
                question.configure(text=language["record"],text_color="gold")
                highscores[4] = highscores[3]
                highscores[3] = highscores[2]
                highscores[2] = highscores[1]
                highscores[1] = highscores[0]
                highscores[0] = total_score
                record_display.place(x=50,y=40)
            elif highscores[0] > total_score > highscores[1]:
                highscores[4] = highscores[3]
                highscores[3] = highscores[2]
                highscores[2] = highscores[1]
                highscores[1] = total_score
            elif highscores[1] > total_score > highscores[2]:
                highscores[4] = highscores[3]
                highscores[3] = highscores[2]
                highscores[2] = total_score
            elif highscores[2] > total_score > highscores[3]:
                highscores[4] = highscores[3]
                highscores[3] = total_score
            elif highscores[3] > total_score > highscores[4]:
                highscores[4] = total_score
            saveFile(str(highscores), "Records.txt")
        bar.stop()


    def cancelGame():
        global countdown, solved, streak, total_score
        highscore_list_items.configure(text=f"{highscores[0]}\n{highscores[1]}\n{highscores[2]}\n{highscores[3]}\n{highscores[4]}")
        countdown = 5
        solved = 0
        streak = 0
        total_score = 0
        bar.stop()
        game_window.destroy()
        game_window.after(500, app.deiconify)

    finish_button = button(game_window, text=language["game_stop"],command=stopGame)
    exit_game_button = button(game_window, text=language["game_leave"],hover_color="red",command=cancelGame)
    current_mode = label(game_window,text=language["game_mode"] + chosen_mode)
    current_mode.place(x=10,y=370)
    exit_game_button.pack(side="bottom",pady=30)
    game_window.protocol("WM_DELETE_WINDOW", cancelGame)
###################################################################################################

chosen_operands = ["+"]

#OPTIONS###########################################################################################
def options():
    global chosen_operands
    app.withdraw()
    options_window = new_window(app)
    options_window.geometry("300x450+800+300")
    options_window.title("Settings")
    options_window.resizable(FALSE,FALSE)

    if chosen_operands == []:
        chosen_operands = ["+"]

    def toggleDarkMode():
        global mode
        if mode == "dark":
            s.set_appearance_mode("light")
            appearancemode_button.configure(text="Dark Mode")
            mode = "light"
        elif mode == "light":
            s.set_appearance_mode("dark")
            appearancemode_button.configure(text="Light Mode")
            mode = "dark"

    background = label(options_window,text="+-+--+-+\n+-+--+-+\n+-+--+-+\n+-+--+-+\n+-+--+-+\n+-+--+-+\n+-+--+-+\n+-+--+-+\n", font=("Modern",60),text_color="grey")
    background.place(x=0,y=-7)
    appearancemode_button = button(options_window, text=language["options_appearance"],command=toggleDarkMode,font=("Comic Sans MS",16))
    appearancemode_button.pack(pady=10)
    
    dif_settings_frame = frame(options_window)
    dif_settings = label(dif_settings_frame,text=language["options_difficulty"],font=("Comic Sans MS",16),)
    difficulty_menu = segbutton(dif_settings_frame, values=[language["mode_easy"],language["mode_normal"],language["mode_hard"],language["mode_extreme"]],font=("Comic Sans MS",16),width=250,dynamic_resizing=TRUE)
    plus_switch = switch(dif_settings_frame, text="Addition (+)",font=("Comic Sans MS",16),onvalue="+",offvalue="")
    minus_switch = switch(dif_settings_frame, text=language["options_subtraction"],font=("Comic Sans MS",16),onvalue="-",offvalue="")
    multi_switch = switch(dif_settings_frame, text=language["options_multiplication"],font=("Comic Sans MS",16),onvalue="*",offvalue="")
    div_switch = switch(dif_settings_frame, text="Division (/)",font=("Comic Sans MS",16),onvalue="/",offvalue="")
    difficulty_menu.set(chosen_difficulty)
    dif_settings.pack(anchor="n")
    difficulty_menu.pack()
    plus_switch.pack(anchor="w",padx=20,pady=5)
    minus_switch.pack(anchor="w",padx=20,pady=5)
    multi_switch.pack(anchor="w",padx=20,pady=5)
    div_switch.pack(anchor="w",padx=20,pady=5)
    dif_settings_frame.pack()

    mode_settings = label(options_window,text=language["options_game_mode"],font=("Comic Sans MS",16),)
    mode_menu = segbutton(options_window, values=["Standard",language["practice_mode"],"OneLife"],font=("Comic Sans MS",16))
    language_menu = segbutton(options_window, values=["English","Deutsch"],font=("Comic Sans MS",16),width=250,dynamic_resizing=TRUE)
    mode_settings.pack()
    mode_menu.pack()
    language_menu.pack(pady=10)
    language_menu.set(language_preference)
    mode_menu.set(chosen_mode)

    difficulty_menu.set(chosen_difficulty)
    if "+" in chosen_operands:
        plus_switch.toggle()
    if "-" in chosen_operands:
        minus_switch.toggle()
    if "*" in chosen_operands:
        multi_switch.toggle()
    if "/" in chosen_operands:
        div_switch.toggle()

    def closeOptions():
        global chosen_operands, chosen_difficulty, opened_from_game, chosen_mode, language, language_preference
        chosen_operands = [plus_switch.get(),minus_switch.get(),multi_switch.get(),div_switch.get()]
        chosen_operands = [item for item in chosen_operands if item != '']
        chosen_difficulty = difficulty_menu.get()
        chosen_mode = mode_menu.get()
        options_window.destroy()
        options_window.after(500, app.deiconify)
        lang_select = language_menu.get()
        if lang_select == "Deutsch":
            language = deutsch
            language_preference = "Deutsch"
        else:
            language = english
            language_preference = "English"
        saveFile(language_preference, "PrefLanguage.txt")
        updateUI()


    exit_options_button = button(options_window, text=language["options_exit"],hover_color="green",command=closeOptions,font=("Comic Sans MS",16))
    exit_options_button.pack(side="bottom",pady=30)
    options_window.protocol("WM_DELETE_WINDOW", closeOptions)



def closeGame():
    app.destroy()

#MENU##############################################################################################
loadFile("Records.txt")
background = label(app,text="+-+--+-+\n+-+--+-+\n+-+--+-+\n+-+--+-+\n+@+--+@+\n+-+--+-+\n", font=("Modern",70),text_color="grey")
background.place(x=2,y=20)
introduction = label(app,font=("Courier",16,"bold"), text=language["app_description"])
start_button = button(app, text=language["app_start_button"],command=game,font=("Comic Sans MS",18))
options_button = button(app ,text=language["app_options_button"],command=options,font=("Comic Sans MS",18))
quit_button = button(app, text=language["app_exit_button"],hover_color="red",command=closeGame,font=("Comic Sans MS",18))
scoreboard = frame(app,height=160,width=130)
scoreboard.pack_propagate(FALSE)
scores_list = label(scoreboard, text="Highscores",font=("System",22),text_color=("purple","gold"))
highscore_list = label(scoreboard, text=f"1.\n2.\n3.\n4.\n5.",font=("System",14))
highscore_list_items = label(scoreboard, text=f"{highscores[0]}\n{highscores[1]}\n{highscores[2]}\n{highscores[3]}\n{highscores[4]}",font=("System",14))

scoreboard.place(x=200,y=160)
scores_list.pack()
highscore_list.place(x=20,y=80,anchor="w")
highscore_list_items.place(x=80,y=80,anchor="e")
introduction.pack(pady=50)
start_button.pack(pady=15,padx=30,anchor="w")
options_button.pack(pady=15,padx=30,anchor="w")
quit_button.pack(pady=15,padx=30,anchor="w")

head_bar = label(app,text=language["app_head_bar"],bg_color="blue",text_color="white",height=30,width=1000,justify="left",font=("System",14,"bold"))
posx = -500
def placeHeadbar():
    global posx
    head_bar.place(x=posx,y=0)
    posx += 0.35
    if posx > 0:
        posx = -600
    app.after(10, placeHeadbar)
app.after(10, placeHeadbar)
###################################################################################################
def updateUI():
    introduction.configure(text=language["app_description"])
    start_button.configure(text=language["app_start_button"])
    options_button.configure(text=language["app_options_button"])
    quit_button.configure(text=language["app_exit_button"])
    head_bar.configure(text=language["app_head_bar"])


app.mainloop()
