---
category: other
title: Lines of code as a metric of project complexity
---

First, a disclaimer. I just want to play with numbers in this post.
Lines of code (LOC) do not mean anything in terms of productivity. They
can eventually be used as a rough estimate of the complexity of a
project. MacOSX counts more than 80 millions LOC. the Linux kernel a
little more than 5 millions. Openoffice is around 1 million. GIMP is
650.000 LOC. (Values from
[Wikipedia](http://en.wikipedia.org/wiki/Source_lines_of_code)). In
other words, a huge project like an operating system and its environment
goes in the tenths of millions. A large application could still be
around hundreds of thousands.

I tried to evaluate the maximum number of lines of code a human being
could be able to produce in the best case scenario. It turns out: less
than 4000 per day, assuming an average typist ([240 char per
minute](http://imlocation.wordpress.com/2007/12/05/how-fast-do-people-type/)),
lines of 30 characters and 8 hours of work.

We are of course in a very ideal and practically unrealistic case: no
thinking, just typing, eight hours straight, with no breaks. The Linux
kernel could be done by this typist in slightly more than 3.5 years. It
actually took 15, with a huge amount of people involved.

It turns out, however, that the number of lines of code you can actually
write is of course way lower. Unsurprisingly I must say. On a small
project I did recently, I wrote 2000 lines of code (logic+test) in 40
hours of work. This means 50 lines of code per hour, or 400 lines per
day, a factor of 10 lower than the (in)human limit. If you could
actually count the fact that many lines were modified, debugged etc. you
can see how the actual line counting does not reflect productivity. Does
my productivity decrease if I refactor the code, removing clutter, and
therefore reducing the lines of code? Obviously no.

On another longer (and more complex) project I took part on, I wrote
9200 lines of code (logic+test) in 45 days of work, meaning approx 200
lines of code/day. Testing code, by experience, equals the logic code in
terms of amount.

In other words, assuming my cases as a rough guideline, I would expect
to produce an average of 300 lines of code per day. Of these 300, only
150 are logic. The other 150 are testing.

This leads also to these rough estimates for a one-man-army approach:

-   A small project of 1000 lines of (logic) code can be done in one or
    two weeks
-   An average complexity project of 10.000 lines of (logic) code could
    be completed in two or three months.
-   A large project of 100.000 lines of (logic) code requires at least a
    couple of years

Note that 100.000 lines of code is still 1/6th of the GIMP complexity.

Some interesting reading:

-   <http://www.developer.com/java/other/article.php/988641>
-   <http://discuss.joelonsoftware.com/default.asp?joel.3.286106.22>
-   <http://www.codinghorror.com/blog/archives/000365.html>
