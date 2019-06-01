---
category: c++
title: C++ stdlib srand/rand are not repeatable across platforms
---

I recently observed that `std::srand/std::rand` are not required to
yield the same pseudorandom sequence across platforms. This code, for
example

```c
#include <cstdlib>
#include <iostream>
#include <ctime>

int main()
{
     std::srand(333);
     int random_variable = std::rand();
     std::cout << "Random value on [0 " << RAND_MAX << "]: " << random_variable << '\n';
     random_variable = std::rand();
     std::cout << "Random value on [0 " << RAND_MAX << "]: " << random_variable << '\n';
     random_variable = std::rand();
     std::cout << "Random value on [0 " << RAND_MAX << "]: " << random_variable << '\n';
}
```

Gives different results on Linux and Mac. On Linux ubuntu 12.04, it
gives

``` 
Random value on [0 2147483647]: 1756860556
Random value on [0 2147483647]: 1141727289
Random value on [0 2147483647]: 551934435
```

On Mac OSX 10.8 gives instead

```
Random value on [0 2147483647]: 5596731
Random value on [0 2147483647]: 1722461096
Random value on [0 2147483647]: 1324078912
```

Keep this into account if you need cross-platform behavior of your PRNG.
