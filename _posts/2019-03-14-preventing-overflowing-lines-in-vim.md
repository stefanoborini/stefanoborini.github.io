---
category: vim
title: Preventing overflowing lines in vim
---

Good code is properly formatted. One requirement in python encouraged by PEP-8
is to keep the code within the 80 columns. This is a generally good advice,
although some people (including me) find it too restrictive. I prefer to push
the code up to 100 columns. We have big screens and no longer the need to print
on a 80 columns printer. In other languages, such as fortran the column size is
enforced by the compiler, either at 80 or 130, depending on the fortran
version.

In vim, you can use softwrapping to get an automatic return if the line is too
long, but I find it confusing and not always doing what I want, when I want. I
prefer visual hints. Here are two possible solutions.

- Use the following to highlight in grey (tinker as needed) every character past the 100th column
```
    autocmd BufEnter * highlight OverLength ctermbg=darkgrey guibg=darkgrey
    autocmd BufEnter * match OverLength /\%100v.*/
```
- Set a colored column as a visual boundary with

```
set colorcolumn=100
```
