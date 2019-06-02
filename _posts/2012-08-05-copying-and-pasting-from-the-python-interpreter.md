---
category: python
title: Copying and pasting from the python interpreter
---

One very powerful feature of python is the interactive interpreter: it
allows you to test and quickly evaluate snippets of code. Occasionally,
I need to rerun the same code, either during the same or another python
interpreter session. One quick way to achieve would be to copy and paste
the code again, but you quickly realize the prompt makes it hard:

```
>>> for i in xrange(10):
...     print i+10
...     print i-10
...     print i/2
... 
10
-10
and so on
```

if you directy copy and paste the above snippet, it clearly won\'t work
due to the presence of the prompts:

```
>>> >>> for i in xrange(10):
 File "<stdin>", line 1
 >>> for i in xrange(10):
 ^
SyntaxError: invalid syntax
>>> ...     print i+10
```

Frustrated, I decided to solve the problem once and for all: I created a
.pythonrc file where I override the normal \"\>\>\> \" prompt to a
header prompt, and the continuation prompt to the empty string:

```
import sys
sys.ps1='--- [Python] ---\n'
sys.ps2=''
```

Then, I added the PYTHONSTARTUP variable in my .bash\_profile to refer
to this file:

```
export PYTHONSTARTUP=$HOME/.pythonrc
```

Now my interactive session looks like this

```
Python 2.7.1 (r271:86832, Feb 27 2011, 20:04:04) 
[GCC 4.2.1 (Apple Inc. build 5664)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
--- [Python] ---
for i in xrange(2):
        print i

0
1
--- [Python] ---
```

I am now free to copy and paste the above code and replay it in the
interpreter, or later on, directly into a vim session (but I will have
to change tab spacing).
