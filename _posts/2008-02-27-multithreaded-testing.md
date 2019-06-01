---
category: python
title: Multithreaded testing
---

Suppose you have to perform tests. Lots of tests. Functional tests,
where each test could take a lot of time. Suppose also that

-   you don\'t want to wait three days until your tests are done
-   you have a massively parallel architecture available
-   you are using python unittest framework
-   you enjoy colors

What would you do?

You install [testoob](http://testoob.sourceforge.net/). This thing is
life-changing, believe me. So, let\'s see an example. Suppose you have
this test:

```python
import unittest
import time
class MyTestCase(unittest.TestCase):
    def testFoo(self):
        time.sleep(3)
        self.assertEqual(0,0)
    def testBar(self): 
        time.sleep(5)
        self.assertEqual(0,0)

if __name__ == '__main__':
    unittest.main()
```

If you run it, the whole testcase will take 8 seconds.

```
..
----------------------------------------------------------------------
Ran 2 tests in 8.000s

OK
```

But if you install testoob, now you have a nice executable

```
stefano$ testoob test.py 
..
----------------------------------------------------------------------
Ran 2 tests in 8.001s
OK
```

Here is the magic: run it with the option \--threads=2 and the result is
served in just 5 seconds:

```
stefano$ testoob --threads=2 test.py 
..
----------------------------------------------------------------------
Ran 2 tests in 5.001s
OK
```

Ok, but what about the colors? Well, I like the testing suites that
print out something green for every successful test. testoob does it, so
it brings way more fun and enjoyment!

Testoob does a lot more. If you feel limited by the current unittest
module, you should definitely consider to take a look at testoob.
