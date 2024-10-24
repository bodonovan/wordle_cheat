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
MATCH_LIMIT = 200   # the maximum number of potential matching words to display
WORDS_PER_LINE = 10 # the maximum number of words to display per line before wrappimg

import sys

version = sys.version
if sys.version_info[0]<3 or sys.version_info[1]<12:
    print("*** WARNING *** you are running python version ", sys.version, "this program requires v3.12 of python. Please upgrade")

dict_file = open(DICT_FILE_NAME, 'r')
dict_lines = dict_file.readlines()

in_letters = {} 
out_letters = []
matches = {}

def clear_rules():
    global in_letters
    global out_letters
    global matches
    in_letters = {}
    out_letters = []
    matches = {}

def add_out_letter (letter):
    if letter not in out_letters:
        out_letters.append(letter)

def add_match (letter, posn):
    matches[letter] = posn

def add_in_letter (letter, posn):
    if letter in in_letters:
        in_letters[letter].append(posn)
    else:
        in_letters[letter] = [posn]

def word_match (word):
    for letter in matches:
        posn = matches.get(letter)
        posn -= 1
        if not letter == word[posn]:
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
    for letter in matches:
        rule_text += letter + "("
        rule_text += str(matches[letter])
        rule_text +=") "
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


def clear_clicked(event):
    # print("clear button clicked")
    ent_ltr.delete(0, tk.END)
    ent_posn.delete(0, tk.END)
    ent_posn.insert(0, "1")
    clear_rules()
    display_rules()  
    display_matches()
      

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
btn_clear = tk.Button(master=frm_form, text="Clear")
btn_clear.grid(row=0, column=7)
btn_clear.bind("<Button-1>", clear_clicked)

frm_matches = tk.Frame(relief=tk.SUNKEN, borderwidth=3)
frm_matches.pack(anchor="w")
lbl_matches = tk.Label(master=frm_matches, text="Possible matches:", anchor="w", justify="left", font=("Courier", 12) )
lbl_matches.grid(row=0, column=0, sticky="e")
display_matches()

window.mainloop()
