---
category: git
---
Git stash size in the command line prompt
=========================================

Too often I get confused with git when it comes to stashes. I tend to
stash often, as I jump from a task to another or from a branch to
another, but it already happened I forgot I stashed something. The stash
grows and I don\'t remember what each patch contains. Fortunately, I
never really end up doing duplicate work, but this is doomed to happen
if I don\'t take appropriate measures.

I concocted this function and bash prompt to present (in proper color no
less) the current amount of stashed items. This way I always know if I
have stashes around

``` {.bash}
function git_stash_size {
 lines=$(git stash list -n 100 2> /dev/null) || return
 if [ "${#lines}" -gt 0 ]
 then 
   count=$(echo "$lines" | wc -l | sed 's/^[ \t]*//') # strip tabs
   echo " ["${count#} "stash] "
 fi
}
# Comment in the above and uncomment this below for a color prompt
PS1='${debian_chroot:+($debian_chroot)}\[\033[04;34m\]\u\[\033[01;00m\]@
\[\033[04;34m\]\h\[\033[00m\]:\[\033[01;34m\]\W\[\033[00m\]\[\033[36m\]
$(__git_ps1 " (%s)")\[\033[00m\]\[\033[01;31m\]$(git_stash_size)\[\033[00m\]\$ '
```

Reformat properly as a single line.
