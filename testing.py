

import re

master= "Now im here to whup your ass"

str2= "im here to whup your ass"
str3= "here to whup your ass"

print(re.search(str2, master, re.IGNORECASE))

print(re.search(str3, master, re.IGNORECASE))


print(re.search(master, master, re.IGNORECASE))