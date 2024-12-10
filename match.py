#
#    Copyright 2024 Brian O'Donovan bodonovan@gmail.com
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
# 
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

DICT_FILE_NAME = '5words.txt'
MATCH_LIMIT = 220   # the maximum number of potential matching words to display
WORDS_PER_LINE = 11 # the maximum number of words to display per line before wrappimg

import sys

version = sys.version
if sys.version_info[0]<3 or sys.version_info[1]<12:
    print("*** WARNING *** you are running python version ", sys.version, "this program requires v3.12 of python. Please upgrade")

dict_file = open(DICT_FILE_NAME, 'r')
dict_lines = dict_file.readlines()

# define the global variables to hold the rules
in_letters = {} 
in_letters_hist = []
out_letters = []
out_letters_hist = []
matches = "_____"
matches_hist = []

# reset the rules i.e. start a new attempt
def clear_rules():
    global in_letters
    global in_letters_hist
    global out_letters
    global out_letters_hist
    global matches
    global matches_hist
    in_letters = {} 
    in_letters_hist = []
    out_letters = []
    out_letters_hist = []
    matches = "_____"
    matches_hist = []

# record the current set of rules in arrays (so we can undo)
def add_rules_to_hist ():
    in_letters_hist.append(in_letters.copy())
    out_letters_hist.append(out_letters.copy())
    matches_hist.append(matches)

# add a rule that the specified letter is not in the target word
def add_out_letter (letter):
    if letter not in out_letters:
        out_letters.append(letter)
        add_rules_to_hist()

# add a rule that a specified letter appears in the specified position
def add_match (letter, posn):
    global matches
    p = int(posn)-1
    start_str = matches[0:p]
    end_str = matches[(p+1):]
    matches = start_str+letter[0]+end_str
    add_rules_to_hist()

# add a rule that a letter appears in the target word, but not in the specified position
def add_in_letter(letter, posn):
    posn = int(posn)
    if letter in in_letters:
        # only add the position if it's not already in the list
        if posn not in in_letters[letter]:
            in_letters[letter].append(posn)
        else:
            print("Same letter and position so ignore")
    else:
        in_letters[letter] = [posn]
    add_rules_to_hist()

# test if the specified word could be our target word
def word_match (word):
    for posn in range(5):
        # rule_text += matches[posn]
        if matches[posn] != '_':
            if matches[posn] != word[posn]:
                return False
    for letter in out_letters:
        if letter in word:
            return False
    for letter in in_letters:
        if not letter in word:
            return False
        for posn in in_letters[letter]:
            if word[posn-1] == letter:
                return False
    return True

# function to list all possible matches
def display_matches():
    match_text = "Possible Matches:\n"
    match_count = 0;
    for line in dict_lines:
        line = line.strip().upper()
        if word_match(line):
            match_count += 1
            match_text += line
            if 0 == match_count % WORDS_PER_LINE:
                match_text += "\n"
            else:
                match_text += " "
            if match_count >= MATCH_LIMIT:
                match_text += "..."
                break
    lbl_matches['text'] = match_text

# function to diplay the current rules            
def display_rules():
    rule_text = "Rules"
    rule_text += "\nMatches:     "
    for x in range(5):
        rule_text += matches[x] + ' '
    rule_text += "\nIn Letters:  "
    for letter in in_letters:
        rule_text += letter
        for num in in_letters[letter]:
            rule_text += "~"+str(num)
        rule_text += " "
    rule_text += "\nOut Letters: "
    for letter in out_letters:
        rule_text += letter
    lbl_rules["text"] = rule_text
    

# increment to value of the position field (limited to a max of 5)
def inc_position():
    posn = ent_posn.get()
    try:
        posn = int(posn)
    except:
        posn = 0
    new_posn = posn+1
    if new_posn>5:
        new_posn = 1
    ent_posn.delete(0, tk.END)
    ent_posn.insert(0, str(new_posn))

# respond to a click on the 'match' button
def match_clicked(event):
    # print("match button clicked")
    ltr_text = ent_ltr.get()
    ent_ltr.delete(0,tk.END)
    if len(ltr_text) < 1:
        print("No letter supplied so ignore")
        return
    posn = ent_posn.get()
    try:
        posn = int(posn)
    except:
        print("position field invalid so ignore")
        return
    add_match(ltr_text[0].upper(), posn)
    display_rules()  
    display_matches()
    inc_position()   

# respond to the 'in' button being clicked
def in_clicked(event):
    # print("in button clicked")
    ltr_text = ent_ltr.get()
    ent_ltr.delete(0,tk.END)
    if len(ltr_text) < 1:
        print("No letter supplied so ignore")
        return
    posn = ent_posn.get()
    try:
        posn = int(posn)
    except:
        print("position field invalid so ignore")
        return
    add_in_letter(ltr_text[0].upper(), posn)
    display_rules()  
    display_matches()
    inc_position()   

# respond to the 'out' button being clicked
def out_clicked(event):
    # print("out button clicked")
    ltr_text = ent_ltr.get()
    ent_ltr.delete(0,tk.END)
    if len(ltr_text) < 1:
        print("No letter supplied so ignore")
        return
    add_out_letter(ltr_text[0].upper())
    display_rules()  
    display_matches()
    inc_position()   

# change ent_posn - set it to 1 less than current value
def decrement_posn():
    posn = ent_posn.get()
    # print('Existing posn =', posn)
    ent_posn.delete(0, tk.END)
    try:
        posn = int(posn)
        # print('Existing posn int =', posn)
        if posn>1:
            posn = (posn-1) % 5
            # print('Posn updated to =', posn)
        ent_posn.insert(0, str(posn))
    except:
        print("position field invalid so set to 1")
        ent_posn.insert(0, str("1"))

# respond to the 'undo' button being clicked
def undo_clicked(event):
    # print("undo button clicked")
 
    global out_letters_hist
    global out_letters
    global in_letters_hist
    global in_letters
    global matches_hist
    global matches

    if len(out_letters_hist)<2:
        # print("only one history entry so just clear")
        clear_clicked({})
        return
 
    decrement_posn()
    ent_ltr.delete(0, tk.END) # blank the letter input

    out_letters = out_letters_hist[-2]
    # print("out_letters", out_letters)
    out_letters_hist = out_letters_hist[0:-1]
    # print("out_letters_hist", out_letters_hist)

    in_letters = in_letters_hist[-2]
    # print("in_letters", in_letters)
    in_letters_hist = in_letters_hist[0:-1]
    # print("in_letters_hist", in_letters_hist)

    matches = matches_hist[-2]
    # print("matches", matches)
    matches_hist = matches_hist[0:-1]
    # print("matches_hist", matches_hist)

    display_rules()  
    display_matches()

# respond to the 'clear' button being clicked
def clear_clicked(event):
    print("clearing rules")
    ent_ltr.delete(0, tk.END)
    ent_posn.delete(0, tk.END)
    ent_posn.insert(0, "1")
    clear_rules()
    display_rules()  
    display_matches()

# define the UI
import tkinter as tk
window = tk.Tk()
window.title("Wordle Cheat")

frm_form = tk.Frame(relief=tk.SUNKEN, borderwidth=3)
frm_form.pack(anchor="w")

lbl_posn = tk.Label(master=frm_form, text="Position:")
ent_posn = tk.Entry(master=frm_form, width=1)
ent_posn.insert(0, "1")
lbl_posn.grid(row=0, column=0, sticky="e")
ent_posn.grid(row=0, column=1)

lbl_rules = tk.Label(master=window, justify="left", font=("Courier", 12))
display_rules()
lbl_rules.pack(anchor="w")

lbl_ltr = tk.Label(master=frm_form, text="Letter:")
ent_ltr = tk.Entry(master=frm_form, width=1)
lbl_ltr.grid(row=0, column=2, sticky="e")
ent_ltr.grid(row=0, column=3)

btn_match = tk.Button(master=frm_form, text="Match")
btn_match.grid(row=0, column=4)
btn_match.bind("<Button-1>", match_clicked)
btn_in = tk.Button(master=frm_form, text="In")
btn_in.grid(row=0, column=5)
btn_in.bind("<Button-1>", in_clicked)
btn_out = tk.Button(master=frm_form, text="Out")
btn_out.grid(row=0, column=6)
btn_out.bind("<Button-1>", out_clicked)
btn_undo = tk.Button(master=frm_form, text="UnDo")
btn_undo.grid(row=0, column=7)
btn_undo.bind("<Button-1>", undo_clicked)
btn_clear = tk.Button(master=frm_form, text="Clear")
btn_clear.grid(row=0, column=8)
btn_clear.bind("<Button-1>", clear_clicked)

frm_matches = tk.Frame(relief=tk.SUNKEN, borderwidth=3)
frm_matches.pack(anchor="w")
lbl_matches = tk.Label(master=frm_matches, text="Possible matches:", anchor="w", justify="left", font=("Courier", 12) )
lbl_matches.grid(row=0, column=0, sticky="e")
display_matches()

window.mainloop()
