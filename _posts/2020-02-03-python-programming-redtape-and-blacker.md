---
category: python
title: Python programming is drowning in red tape. My experience with forking black (in progress)
---

A few weeks ago, I got really angry at the state of things with black. Everybody uses this
autoformatter that breaks pep8, and nothing annoys me more like breaking pep8.

Why? Because the whole Python community and even beyond that has been extremely
annoying in the past years every time some code was created and not complying
with pep8. It was bikeshedding at its worst, and even myself has been slapped
in the face with childish cries of non-pep8 compliance for code that was supposed
to wrap non-pep8 compliant APIs. Not that I care, but it gives you an idea
of the situation.

Now, somehow, since the PSF has endorsed this autoformatter, we all have to
move to a new cargo cult of black, disregarding the advantages of pep8, and
specifically one I care a lot about: visual cues.

Python has made a fortune by providing code that looks *nice*. And nice means
being friendly to the eye. Indentation, PEP8, the attention to detail for the
syntax, made python great. In particular, this part really annoys me to no end

```
# in:

def very_important_function(template: str, *variables, file: os.PathLike, engine: str, header: bool = True, debug: bool = False):
    """Applies `variables` to the `template` and writes to `file`."""
    with open(file, 'w') as f:
        ...

# out:

def very_important_function(
    template: str,
    *variables,
    file: os.PathLike,
    engine: str,
    header: bool = True,
    debug: bool = False,
):
    """Applies `variables` to the `template` and writes to `file`."""
    with open(file, "w") as f:
```

My problem with the above formatting is that the list of arguments and the body of the function
are now at the same indentation level. This both removes a visual cue, and breaks folding
editors that rely on indentation to fold the content, especially when the closing parenthesis
is at indentation level zero. PEP8 recommends:

```
# Add 4 spaces (an extra level of indentation) to distinguish arguments from the rest.
def long_function_name(
        var_one, var_two, var_three,
        var_four):
    print(var_one)
```

My point is that the proper way to indent the above code is


```
def very_important_function(
        template: str,
        *variables,
        file: os.PathLike,
        engine: str,
        header: bool = True,
        debug: bool = False,
        ):
    """Applies `variables` to the `template` and writes to `file`."""
    with open(file, "w") as f:
```

So [after arguing about this topic on the black issue reporting](https://github.com/psf/black/issues/1178), 
seeing that people kept not reading what was the core of the issue, and seeing
that [more people are really angry at this autoformatter](https://www.reddit.com/r/Python/comments/exrtgn/my_unpopular_opinion_about_black_code_formatter/), 
I decided to do the unthinkable: fork it. Mostly because I am bored.

# The horror

I don't know if you ever saw the code of black. It's a single, massive 3000
lines python module that chokes pycharm. There's no organisation whatsover
in the routines. It hurts my eyes to see it. They might have a justification but I don't
care. If the justification forces people to write code like this, something really has
gone wrong in the python world.

But this is just the beginning. The amount of red tape one has to do today to code in
python is astounding. Remove all the fluff, and the code would be easily be half.
It seems like a package that has been developed by someone who wanted to add _everything_
of the latest toys available, and they went all in. The result is that a lot of
stuff is generated on the fly on the build machine, and by using a reformatter
there's no guarantee that the code you see is the code that is actually tested
on the build machine.

So, in the next few days, I am going to:

1. Remove the "for humans" garbage. Pipenv is absolute trash and I plan to
   eliminate it as soon as possible. I am going to use poetry.
2. repartition the code that belongs together into smaller modules.


# Piles and piles of red tape

As I adventured in this petty task, I discovered that today, starting a python project that 
complies with the sensitivities of the opensource community you must have so much stuff setup
that setting it up is a project in itself. You need:

- isort: because be damned if your imports are in the wrong order.
- pre-commit: whatever this thing does
- setup.cfg. Wait, no. setup.py. Wait, no. pyproject.toml: to describe your project, and all the tools that you need, all shoved in.
- all the github templates, because of course we need to setup github as well. 
- travis, because of course we want travis.
- poetry, because we need to setup our work environment. But wait, maybe pipenv. Or maybe virtualenv but I don't know because I use pycharm.
- editorconfig, because I am too lazy to setup the editor.
- bumpversion, because I am too lazy to put a single file with a version number, and sphinx is too hard to setup to fetch this version number.
- setuptools\_scm, because our versions must change at every new commit.
- flake8: yeah, because we need that help. Seriously. Flake8 is a miracle.
- mypy, because we can never have enough Generic[T] in our code, that used to
  read nice and sleek, and now it feels like listening to a speech from a guy
  with a hiccup.
- a CODE\_OF\_CONDUCT, because we assume preemptively that you are a racist
  homophobic asshole, and we have to cover our bases.
- nose. No wait, pytest. No wait, pytest with a bunch of plugins. No wait, ward. Eh, screw it, I'll use unittest.
- As ✨ many ✨ stars ✨ as ✨ possible

Can I start writing code now? of course not! You forgot appveyor!


