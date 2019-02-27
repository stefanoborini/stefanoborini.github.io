Naming for conversion routines
==============================

I love code that self-documents and reads naturally, so I strive to name
my routines and variables appropriately. When you are faced with the
implementation of a conversion method, in generally the name is in the
form \"toB\", where B is the result of the conversion, for example

```python
rgb_values = color.toRgb()
```

The inverse, when we want to convert and integrate the conversion into
an object\'s internal state, is generally in the form \"fromB\"

```python
color.fromRgb(rgb_values)
```

When you have a conversion function, things are slightly different:
\"From\" assumes a different weight and meaning. To perform a conversion
color object to rgb you can use either

```python
rgb_values = colorToRgb(color)
```

or

```python
rgb_values = rgbFromColor(color)
```

The second works best because the proximity and order of the terms
resembles the one naturally established by the prepended nature of the
routine call and the order of the two objects. Everything moves from
right to left in the second example, and it reads naturally. The first
solution is clumsier and disorganized. Similarly, the reverse conversion
will be

```python
color = colorFromRgb(rgb_values)
```

The conclusion is that when you write a conversion function, prefer the
\"From\" naming exclusively, while for methods you can use \"To\" and
\"From\" forms for different conversion directions.
