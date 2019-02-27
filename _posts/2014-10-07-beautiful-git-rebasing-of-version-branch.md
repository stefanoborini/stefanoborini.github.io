Beautiful Git rebasing of version branch
========================================

In this post, I want to share with you a technique I learned recently
from a colleague. It\'s a really great trick to keep your history nice
and clean, while being able to work and push feature branches.

Let\'s start with the workflow and the problem that generates. You have
a master branch that is pushed to a remote, containing the following

``` {.text}
* f2bc01d 2014-10-07 17:57:52 +0200 Stefano Borini (HEAD, origin/master, origin/HEAD, master) - added 5 to foo
* 2ecacd7 2014-10-07 17:57:52 +0200 Stefano Borini - added 4 to foo
* d0f53d8 2014-10-07 17:57:52 +0200 Stefano Borini - added 3 to foo
* d26a4db 2014-10-07 17:57:52 +0200 Stefano Borini - added 2 to foo
* f98ef63 2014-10-07 17:57:52 +0200 Stefano Borini - added 1 to foo
* d817b10 2014-10-07 17:57:04 +0200 Stefano Borini - Added foo
* 5fdec88 2014-10-07 17:50:00 +0200 Stefano Borini - Initial commit
```

You want to work on a feature, so you create a feature branch from the
current master

``` {.console}
sbo@NAS:~/tmp/git-experiment-1$ git checkout -b feature
Switched to a new branch 'feature'
sbo@NAS:~/tmp/git-experiment-1$ git push --set-upstream origin feature
Total 0 (delta 0), reused 0 (delta 0)
To git@github.com:stefanoborini/git-experiment-1.git
 * [new branch]      feature -> feature
```

Master keeps receiving patches from other developers. At the same time,
you keep pushing your feature changes to your remote, because you don\'t
want to risk losing all your work if your hard drive crashes. The
situation ends up like this

``` {.text}
* 453bada 2014-10-07 18:06:36 +0200 Stefano Borini (HEAD, origin/master, origin/HEAD, master) - added 30 to foo
* 1546da7 2014-10-07 18:06:36 +0200 Stefano Borini - added 29 to foo
* cdfa47d 2014-10-07 18:06:36 +0200 Stefano Borini - added 28 to foo
* 00a0051 2014-10-07 18:06:36 +0200 Stefano Borini - added 27 to foo
* 8bc15dd 2014-10-07 18:06:36 +0200 Stefano Borini - added 26 to foo
* a3b542a 2014-10-07 18:06:36 +0200 Stefano Borini - added 25 to foo
... more commits ...
* 4610ec5 2014-10-07 18:06:36 +0200 Stefano Borini - added 11 to foo
* bf30e67 2014-10-07 18:06:36 +0200 Stefano Borini - added 10 to foo
* 2404746 2014-10-07 18:06:36 +0200 Stefano Borini - added 9 to foo
* 0452b5c 2014-10-07 18:06:36 +0200 Stefano Borini - added 8 to foo
* 245864a 2014-10-07 18:06:36 +0200 Stefano Borini - added 7 to foo
* 85a9f39 2014-10-07 18:06:36 +0200 Stefano Borini - added 6 to foo
| * 8f25256 2014-10-07 18:04:42 +0200 Stefano Borini (origin/feature, feature) - added 5 to bar
| * 7f5c34f 2014-10-07 18:04:42 +0200 Stefano Borini - added 4 to bar
| * 4e57707 2014-10-07 18:04:42 +0200 Stefano Borini - added 3 to bar
| * 9c12235 2014-10-07 18:04:42 +0200 Stefano Borini - added 2 to bar
| * a714ec3 2014-10-07 18:04:42 +0200 Stefano Borini - added 1 to bar
|/
* f2bc01d 2014-10-07 17:57:52 +0200 Stefano Borini - added 5 to foo
* 2ecacd7 2014-10-07 17:57:52 +0200 Stefano Borini - added 4 to foo
* d0f53d8 2014-10-07 17:57:52 +0200 Stefano Borini - added 3 to foo
* d26a4db 2014-10-07 17:57:52 +0200 Stefano Borini - added 2 to foo
* f98ef63 2014-10-07 17:57:52 +0200 Stefano Borini - added 1 to foo
* d817b10 2014-10-07 17:57:04 +0200 Stefano Borini - Added foo
* 5fdec88 2014-10-07 17:50:00 +0200 Stefano Borini - Initial commit
```

Now you have a problem. If you merge feature back into master, you will
get a very long line connecting your last commit on feature back to the
current master. This may seem trivial, but in complex scenarios it can
become unpleasant to browse.

You may think that rebasing is the solution, but unfortunately, you
would introduce a lot of problems if you do so. The Feature branch is
already pushed to remote, and it\'s on all developers\' machines.
Rebasing would mean force a push and rewrite history, with ugly
consequences.

What you would like to do is to \"cherry pick\" all the commits from
feature on top of your current master, but there\'s a more elegant way
of doing it. First of all, checkout your feature branch

``` {.console}
sbo@NAS:~/tmp/git-experiment-1$ git checkout feature
Switched to branch 'feature'
```

Then, create and checkout a local branch from the feature branch

``` {.console}
sbo@NAS:~/tmp/git-experiment-1$ git checkout -b feature_rebaser
Switched to a new branch 'feature_rebaser'
```

Now, rebase this branch against the current master. This migrates all
the patches from feature\_rebaser to master, but only locally.

``` {.console}
sbo@NAS:~/tmp/git-experiment-1$ git rebase master
First, rewinding head to replay your work on top of it...
Applying: added 1 to bar
Applying: added 2 to bar
Applying: added 3 to bar
Applying: added 4 to bar
Applying: added 5 to bar
```

And finally, you can merge onto master. You can use \--no-ff to keep the
patches \"visually separated\" instead of in continuity with the current
master timeline.

``` {.console}
sbo@NAS:~/tmp/git-experiment-1$ git checkout master
Switched to branch 'master'
Your branch is up-to-date with 'origin/master'.
sbo@NAS:~/tmp/git-experiment-1$ git merge --no-ff feature_rebaser 
```

The resulting tree is the following

``` {.text}
*   c15286c 2014-10-07 18:22:53 +0200 Stefano Borini (HEAD, master) - Merge branch 'feature_rebaser'
|\  
| * 166bbe0 2014-10-07 18:19:45 +0200 Stefano Borini (feature_rebaser) - added 5 to bar
| * 49eb2ac 2014-10-07 18:19:45 +0200 Stefano Borini - added 4 to bar
| * a5e36d7 2014-10-07 18:19:44 +0200 Stefano Borini - added 3 to bar
| * a8ca8a2 2014-10-07 18:19:44 +0200 Stefano Borini - added 2 to bar
| * 69d5ad3 2014-10-07 18:19:44 +0200 Stefano Borini - added 1 to bar
|/  
* 453bada 2014-10-07 18:06:36 +0200 Stefano Borini (origin/master, origin/HEAD) - added 30 to foo
* 1546da7 2014-10-07 18:06:36 +0200 Stefano Borini - added 29 to foo
* cdfa47d 2014-10-07 18:06:36 +0200 Stefano Borini - added 28 to foo
... more commits ...
* bf30e67 2014-10-07 18:06:36 +0200 Stefano Borini - added 10 to foo
* 2404746 2014-10-07 18:06:36 +0200 Stefano Borini - added 9 to foo
* 0452b5c 2014-10-07 18:06:36 +0200 Stefano Borini - added 8 to foo
* 245864a 2014-10-07 18:06:36 +0200 Stefano Borini - added 7 to foo
* 85a9f39 2014-10-07 18:06:36 +0200 Stefano Borini - added 6 to foo
| * 8f25256 2014-10-07 18:04:42 +0200 Stefano Borini (origin/feature, feature) - added 5 to bar
| * 7f5c34f 2014-10-07 18:04:42 +0200 Stefano Borini - added 4 to bar
| * 4e57707 2014-10-07 18:04:42 +0200 Stefano Borini - added 3 to bar
| * 9c12235 2014-10-07 18:04:42 +0200 Stefano Borini - added 2 to bar
| * a714ec3 2014-10-07 18:04:42 +0200 Stefano Borini - added 1 to bar
|/  
* f2bc01d 2014-10-07 17:57:52 +0200 Stefano Borini - added 5 to foo
* 2ecacd7 2014-10-07 17:57:52 +0200 Stefano Borini - added 4 to foo
* d0f53d8 2014-10-07 17:57:52 +0200 Stefano Borini - added 3 to foo
* d26a4db 2014-10-07 17:57:52 +0200 Stefano Borini - added 2 to foo
```

Note how the feature branch is now \"brought to present day\" and
inserts nice and easy. The feature branch can then be left dangling and
deleted at your best convenience.

Coudn\'t we just rebase feature, instead of creating a new branch?
Unfortunately no. I created the same situation with a new branch
\"feature2\", pushed it to remote, and rebased feature2. Checking out
master and then back to feature2 I get

``` {.console}
sbo@NAS:~/tmp/git-experiment-1$ git checkout feature2
Switched to branch 'feature2'
Your branch and 'origin/feature2' have diverged,
and have 15 and 5 different commits each, respectively.
  (use "git pull" to merge the remote branch into yours)
```

oops\... I changed history on my local machine, and this differs from
the situation that is on the remote server. If you pull now, you will
apply the same patches twice

``` {.console}
sbo@NAS:~/tmp/git-experiment-1$ git pull
Merge made by the 'recursive' strategy.
```

with the following tree

``` {.text}
*   a037791 2014-10-07 18:37:03 +0200 Stefano Borini (HEAD, origin/feature2, feature2) - Merge branch 'feature2' of github.com:stefanoborini/git-experiment-1 into fea
|\  
| * 6c9e82a 2014-10-07 18:30:45 +0200 Stefano Borini - added 10 to bar
| * 4bcfced 2014-10-07 18:30:45 +0200 Stefano Borini - added 9 to bar
| * 469517d 2014-10-07 18:30:45 +0200 Stefano Borini - added 8 to bar
| * a28a360 2014-10-07 18:30:45 +0200 Stefano Borini - added 7 to bar
| * 894b24c 2014-10-07 18:30:45 +0200 Stefano Borini - added 6 to bar
* | a2b14a4 2014-10-07 18:31:44 +0200 Stefano Borini (origin/master, origin/HEAD, master) - added 10 to bar
* | acefda0 2014-10-07 18:31:44 +0200 Stefano Borini - added 9 to bar
* | 2be9bef 2014-10-07 18:31:44 +0200 Stefano Borini - added 8 to bar
* | 5d528cb 2014-10-07 18:31:44 +0200 Stefano Borini - added 7 to bar
* | a6ec80f 2014-10-07 18:31:44 +0200 Stefano Borini - added 6 to bar
* | d1dc5d2 2014-10-07 18:31:17 +0200 Stefano Borini - added 40 to foo
* | bdafcce 2014-10-07 18:31:17 +0200 Stefano Borini - added 39 to foo
* | 2dd4415 2014-10-07 18:31:17 +0200 Stefano Borini - added 38 to foo
* | 11a8f22 2014-10-07 18:31:17 +0200 Stefano Borini - added 37 to foo
* | f208658 2014-10-07 18:31:17 +0200 Stefano Borini - added 36 to foo
* | ef1e319 2014-10-07 18:31:17 +0200 Stefano Borini - added 35 to foo
```

Git is unable to recognize the patches\' duplication, because rebasing
changes the SHA. In this case, it went smooth, but in a real-case
scenario, you would get plenty of conflicts.
