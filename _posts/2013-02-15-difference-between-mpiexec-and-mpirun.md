---
category: other
title: Difference between mpiexec and mpirun
---

A few days ago I started playing with MPI, and I started wondering:
\"what\'s the difference between mpiexec and mpirun?\" It turns out that
the distinction is [mostly
historical](http://www.open-mpi.org/community/lists/users/2006/03/0733.php).
In the first MPI specifications, there was nothing defining how the
executables should run. Implementors of the specifications created an
mpirun executable, but each implementation had different switches and
different behavior. The MPI2 standard filled this gap, but it was not
possible to merge the different implementor-dependent behaviors that
became established in the meantime. The solution was to standardize the
utility name as mpiexec. As a consequence, MPI2 compliant
implementations will generally have both: mpiexec to honor the standard,
and mpirun to honor compatibility with their previous implementation.
