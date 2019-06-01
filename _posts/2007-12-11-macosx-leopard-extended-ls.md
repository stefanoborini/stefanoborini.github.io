---
category: osx
title: MacOSX Leopard extended ls
---

Apparently, something changed in the `ls` command with the release of
Leopard. I don\'t remember seeing this kind of report on Tiger, although
it looks like the features already existed since long time. Now, take
this information with a grain of salt, as I am not a MacOSX expert, just
a (very busy) occasional tinkerer on this OS.

```
drwxr-xr-x   5 stefano  stefano     170  9 Ott 10:11 Programs
drwxr-xr-x+  4 stefano  stefano     136  1 Ago 01:48 Public
-rw-r--r--@  1 stefano  stefano  221814 20 Ott 20:12 executable network.eps
```

This is an extract of an `ls` run in my home directory. As you can see,
the long `-l` option produces an output containing two additional
characters in the file mode field: an \"at symbol\" and a \"plus
symbol\" permission.

According to the manual page, the plus symbol means that the file has
extended security information, meaning ACLs. It is possible to print out
this information with the option `-e` to the `ls` command.

```
stefano:~ stefano$ ls -led Public/
drwxr-xr-x+ 4 stefano  stefano  136  1 Ago 01:48 Public/
 0: group:everyone deny delete
```

Of course, you can also change the ACL information using chmod

```
stefano:~ stefano$ chmod +ai "guest allow write" Public/
stefano:~ stefano$ ls -le Public/
total 0
drwxr-xr-x+ 4 stefano  stefano  136  1 Ago 01:48 Public/
 0: group:everyone deny delete
 1: user:Guest inherited allow add_file
```

And you can remove the ACLs

```
stefano:~ stefano$ chmod -a# 1 Public
stefano:~ stefano$ chmod -a# 0 Public
stefano:~ stefano$ ls -led Public/
drwxr-xr-x  4 stefano  stefano  136  1 Ago 01:48 Public/
```

As you can see, the plus symbol disappears. Ideally, you can do these
changes also from the Finder, Information window. However trying to do
this lead to a crash of the Finder on my machine. Don\'t know if this
behavior is due to my setup or an actual bug.

Then, what about the at symbol? This feature is undocumented, but if you
add the `-@` option to `ls -l` you will obtain the meaning:

```
stefano:~ stefano$ ls -l@ executable\ network.eps
-rw-r--r--@ 1 stefano  stefano  221814 20 Ott 20:12 executable network.eps
    com.apple.FinderInfo    32
    com.apple.ResourceFork 547102
```

So, apparently there are extended attributes, and this is the meaning of
the at symbol. the first entry is the name of the extended attribute,
the second entry is the size of the contents of the attribute.

You can peek into the contents of the attributes with the command
`xattr`:

```
stefano:~ stefano$ xattr -p com.apple.ResourceFork executable\ network.eps >unknown_content
stefano:~ stefano$ file unknown_content
unknown_content: MS Windows icon resource
```

Apparently, the resource fork contains a icon file.
[ResKnife](http://resknife.sourceforge.net/) also confirms it. If I
understood correctly, the old `file/..namedfork/rsrc` resource fork is
mapped to com.apple.ResourceFork attribute, but you are welcome to
correct me in the comments. I think I should read [this
book](http://www.amazon.com/Mac-OS-Internals-Systems-Approach/dp/0321278542)
for a better understanding.

Here some relevant links:

-   [ArsTechnica: about extended
    attributes](http://arstechnica.com/reviews/os/macosx-10-4.ars/7)
-   [ArsTechnica: about
    ACLs](http://arstechnica.com/reviews/os/macosx-10-4.ars/8)
-   [ResKnife, a resource fork editor](http://resknife.sourceforge.net/)
