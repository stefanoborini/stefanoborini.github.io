---
category: git
title: Git hangs at clone? It could be a Type of Service issue.
---

Today I was trying to download some code via git, and I got into a
strange problem. When I ran git clone, it simply reported cloning into
\'repo\' and was stuck there, until timeout. Same thing for pull. I
could not understand what was happening, and it took me a while to
figure it out but here is the solution, at least to my problem. Add this
to your .ssh/config

``` {.text}
Host *
  IPQoS 0x00
```

What was the problem? Here are the symptoms:

-   git worked on my NAS (Linux, connected to the router via cable), but
    not from my laptop (OSX, connected via WiFi)
-   ssh worked from the laptop. I could ssh to the NAS and to other
    external ssh machines.
-   However, I observed that the interactive ssh behaved strange when I
    ssh\'d to an external machine. For example, if I asked for an ls, it
    kind of got stuck, and I had to press enter every time to get
    further data. It was like acting with a constant \"more\".
-   using `GIT_TRACE`, I found out that ssh negotiation was completely
    successful and it got stuck at invoking git-upload-pack via ssh.

Google didn\'t help. I changed versions of ssh and git, checked my
router for strange setups, but nothing could solve. Until I smelled
something about the way packets were exchanged. Don\'t ask me how I did
it. I don\'t know. I just had the feeling that strange \"enter to get
more stuff\" behavior had something to do with it. The fact that the
laptop had the problem, while the NAS didn\'t, made me think it was
either a OS issue or a NAT configuration issue.

So I started checking something about NAT, adding NAT to the google
query, and [here I found a post of a Dane who had similar
troubles](http://stackoverflow.com/questions/8750930/git-clone-hangs-forever-on-github),
apparently caused by the router messing up due to [Quality of
Service](https://groups.google.com/forum/#!topic/openspaceaarhus/6Z2WEioFIrc).
This sounded just about right. Quality of Service influences how packets
are considered for priority routing. I did more searching until [I found
this other
post](http://stackoverflow.com/questions/2247782/ssh-example-com-hangs-but-ssh-example-com-bash-i-does-not),
where I found the solution given above.

It was a fun hour.
