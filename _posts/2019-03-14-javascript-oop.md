---
category: javascript
---
# Object-oriented programming, the JavaScript way

As you probably know, I'm a python fan. Unfortunately, python does not run in
the most common development platform out there: the browser. To add more to the
trouble, the only language supported by the browser platform is JavaScript.
Much has been said about the disgraces of this language, to the point that
someone considered important to write a book on The Good Parts of JavaScript.
In other words, everything that is not in that book is most likely to be a
horror zombie monster ready to bite you.

I had my amount of struggling with the language, Occasionally, I hated its
apparent lack of logic and alien behavior, but as time passed I decided to stop
fighting it to fit into my mental schema, and I started embracing it as-is.
After that I reached the same conclusion <a href="http://www.crockford.com/">Crockford</a> said: 
that <a href="http://www.crockford.com/javascript/javascript.html">JavaScript is a deeply misunderstood language</a>.

The only difference is that javascript is different from other languages out
there. I tried to develop my own mental schemes to understand how it works.
Here I share what I found out about object oriented programming in javascript,
and in particular how to instantiate an object.

First thing: javascript does not have class-based inheritance. it has
*prototype-based inheritance*. What's the difference? in
class-based inheritance, you have a class that defines a blueprint of your
object, and you have instances of the class that are concrete materializations
of your class. Python is class-based, as many other languages out there (C++,
Java). The idea is that classes can be arranged in hierarchies, and you can
obtain inheritance through subclassing a base class. For example.

```javascript
class Animal(object):
    def __init__(self):
        self._hungry = True
    def feed(self):
        self._hungry = False

class Cat(Animal): pass

kitty = Cat()
kitty.feed()
```

In this case, Cat does not define the method feed, but the fact that Cat
inherits from Animal automatically grants it all the methods of Animal.

The problem with javascript is that you have many ways to create an object, and
many ways to do object oriented programming. Javascript is so generic, dynamic
and liberal in its design that everything is possible. Javascript has a very
flexible vision of objects: an object is a dictionary that binds keys to
something else. The something else can be an integer, a float, a string,
another object, or a function. You have a instance variable by assigning a
value. You have a method by assigning a function.

Javascript does not work this way. Instead, javascript uses another object
instance as a prototype, which is used in a prototype chain.

## How does prototyping work?

The best conceptual picture I was able to devise to make this point
understandable is the following. Suppose you have this code

```javascript
function Person(name) {
    this._name = name;
    this.getName = function() {
        return this._name;
    }
}

me = new Person("Stefano");
alert(me.getName());
```
in javascript, any function is like a factory (a real one), although very few
functions are actually used for their factory behavior.

There are many, many ways of doing object oriented programming in JavaScript.

*When you see <span style="text-decoration: underline;">this</span>, think <span style="text-decoration: underline;">owner</span>.*

*What happens when you "instantiate" ?*

When you use the new operator on a function Foo, you are invoking the function in "constructor mode", which is not a function invocation in the traditional sense. What happens under the hood is the following:

- A new, empty object is created from scratch.
- The new object.__proto__ attribute  referenced by function Foo.prototype (normally an empty object, but can be modified)
- The object just created is assigned to the "this" variable inside the function Foo.
- The constructor function is entered.
- Inside this function you can use the "this" variable to set up the newly created object with variables and methods. These methods will be available only on the object just created.

*Additional Links*

- http://www.codeproject.com/KB/aspnet/JsOOP1.aspx
- http://www.codeproject.com/KB/aspnet/JsOOP2.aspx
- http://www.codeproject.com/KB/aspnet/JsOOP3.aspx
- http://articles.sitepoint.com/article/oriented-programming-1
- http://articles.sitepoint.com/article/oriented-programming-2
- http://mckoss.com/jscript/object.htm
- http://www.webreference.com/js/column79/
- http://www.webreference.com/js/column80/
- http://www.javascriptkit.com/javatutors/oopjs.shtml
- http://www.javascriptkit.com/javatutors/proto.shtml
- http://www.crockford.com/javascript/javascript.html
- https://developer.mozilla.org/en/Introduction_to_Object-Oriented_JavaScript
- http://amix.dk/blog/viewEntry/19038
- http://phrogz.net/js/classes/OOPinJS.html
- http://phrogz.net/js/classes/OOPinJS2.html
- http://www.w3schools.com/js/js_obj_intro.asp
- http://viralpatel.net/blogs/2009/07/object-oriented-programming-with-javascript.html
- http://www.crockford.com/javascript/inheritance.html
- http://www.sitepoint.com/blogs/2006/01/17/javascript-inheritance/
- http://www.ruzee.com/blog/2008/12/javascript-inheritance-via-prototypes-and-closures
- http://javascript.crockford.com/prototypal.html
- http://ajaxpatterns.org/Javascript_Inheritance
- http://www.cs.rit.edu/~atk/JavaScript/manuals/jsobj/
- http://en.wikipedia.org/wiki/Prototype-based_programming
- http://ejohn.org/blog/simple-javascript-inheritance/
- http://msdn.microsoft.com/en-us/scriptjunkie/ff852808.aspx
- http://odetocode.com/Blogs/scott/archive/2010/07/22/prototypes-and-inheritance-in-javascript.aspx
- http://www.bolinfest.com/javascript/inheritance.php
