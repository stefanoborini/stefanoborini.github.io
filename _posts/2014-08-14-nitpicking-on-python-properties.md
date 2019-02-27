Nitpicking on python properties
===============================

I like python properties, I really do. Properties allow you to convert
explicit setters and getters into lean code while keeping control of
your operation. Instead of this

```python
state.setMode(EditorMode.INSERT)
current_mode = state.mode()
```

with properties you can write a much more pleasant

```python
state.mode = EditorMode.INSERT
current_mode = state.mode
```

In both cases, if it weren\'t for the magic of properties, you would get
direct access to a member, but if you create your class like this

```python
class State(object):
    def __init__(self):
        self._mode = EditorMode.COMMAND

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        self._mode = value
```

the two decorated methods are called automatically. This gives you a
chance for validating the passed value, for example, or using smart
tricks like caching if getting the value is slow, basically the same
tricks you would obtain by traditional accessor methods, but with a
better syntax and without violating encapsulation.

That said, I noticed a few minor things with properties that are good to
point out.

1. Refactoring
--------------

Imagine that you find \"mode\" too poor as a name. and you decide to use
editor\_mode instead. If you had an accessor method, you would refactor
setMode() to setEditorMode(). If any part of your code still calls
setMode(), you get an exception.

With a property, the same refactoring implies a change from state.mode
to state.editor\_mode. However, if other parts of your code still use
state.mode = something, you will not get an exception. In fact, it\'s
trivially correct. This could produce hard-to-find bugs.

2. No callbacks
---------------

While you can store or pass around state.setEditorMode as a callback,
you can\'t achieve the same effect with a property, not trivially at
least. No, you can\'t use a lambda, because assignment is forbidden in a
lambda.

3. Mocking
----------

You can certainly [mock a
property](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.PropertyMock),
but requires a bit more care. Nothing impossible, but if you learn the
mock module, you have to go on that extra bit if you want to cover
properties.

4. Soft-returning a set operation details
-----------------------------------------

Sometimes you might want your setter to return state information about
the set operation. One trivial example may be True or False, depending
if the operation was successful or not. You can certainly throw an
exception for this specific case, but your mileage may vary depending on
the specifics of your problem and what \"looks better\" for your design.
A property does not give you flexibility to return a value during set.

5. Only one value at a time
---------------------------

If your setters are connected to some notification system, you might
want to set multiple values at once to trigger a single notification.
Once again, it\'s a minor problem: you can use a special property
accepting a tuple. For example, if you have values v1 and v2, on class
Foo, you could have something like

```python
class Foo(object): 
    def __init__(self): 
        self._v1 = None 
        self._v2 = None 
    @property 
    def v1(self): 
        return self._v1 
    @v1.setter 
    def v1(self, value): 
        self._v1 = v1 
        # notify listeners 
    @property 
    def v2(self): 
        return self._v2 
    @v2.setter 
    def v2(self, value): 
        self._v2 = v2 
        # notify listeners 
    @property 
    def values(self): 
        return (self._v1, self._v2) 
    @values.setter 
    def values(self, value_tuple): 
        self._v1, self._v2 = value_tuple 
        # notify listeners 

f=Foo() 
f.values = (1,2)
```

6. Magic!
---------

There\'s some kind of magic behind properties that you can\'t perceive
to be there when you read client code. For example, code like this

```python
myobj.my_foo = 5
```

generally makes you think of a simple assignment taking place, but this
is not the case if my\_foo is a property. Maybe naming convention could
disambiguate? I am not a fan of the strict PEP-8 requirements on naming
of methods, so one could potentially decide for

```python
myobj.myMethod()
myobj.myProperty = 5
myobj.my_member_var = 3
```

I am thinking out loud here, and I don\'t have a strong opinion on this
issue. That said, properties are definitely cool and will make your
interfaces much more pleasant, so I definitely recommend their use, if
no other constraints prevent you to do so.
