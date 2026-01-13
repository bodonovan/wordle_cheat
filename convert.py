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

# python list to convert wordle word list from 
# https://github.com/bigmac12/wordle_helper_py/blob/main/wordle_words.json
# into the plaintext expected by wordle_cheat

import json

DICT_FILE_NAME = 'words.json'
OUT_FILE_NAME = '5words.txt'

dict_file = open(DICT_FILE_NAME, 'r')
dict_file = open(DICT_FILE_NAME, 'r')
dict_str = dict_file.read()
dict = json.loads(dict_str)

out_lines = []
for line in dict.keys():
    line = line.strip().upper() # conert the words to upper case since Wordle uses upper case
    out_lines.append(line+'\n')

out_file = open(OUT_FILE_NAME, 'w')
out_file.writelines(out_lines)
out_file.close()