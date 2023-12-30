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

DICT_FILE_NAME = 'words'
OUT_FILE_NAME = '5words.txt'

dict_file = open(DICT_FILE_NAME, 'r')
dict_lines = dict_file.readlines()

out_lines = []
for line in dict_lines:
    line = line.strip().upper() # conert the words to upper case since Wordle uses upper case
    if 5==len(line): # only copy words with length 5
        print(line)
        out_lines.append(line+'\n')
    elif 4==len(line): # mpost words in English take a 'S' suffix so take 4 letter words wit a suffix of 'S'
        line += "S"
        print(line)
        out_lines.append(line+'\n')

out_file = open(OUT_FILE_NAME, 'w')
out_file.writelines(out_lines)
out_file.close()

