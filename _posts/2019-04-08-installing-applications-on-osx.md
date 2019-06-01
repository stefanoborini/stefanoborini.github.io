---
category: osx
title: Installing applications on OSX
---

OSX is a complex environment with a lot of difference compared to Linux or Windows.
Most of the changes described dealt with the intrinsic difference of the system,
its different compiler (llvl clang), and its different default installation
layout (libraries etc.) out of the box.

# On Frameworks

Before going into detail, it's important to understand the concept of
framework, and in general the concept of bundle in OSX. 

A bundle is a directory with a special structure. Depending on the extension
and content, Bundles can contain (among others) applications or frameworks.
An application is contained in a .app bundle (a dir with a name ending in .app
and a special internal layout), while a library is generally contained in
a .framework. A framework is a container that encompasses together the dynamic
library (in linux parlance, the .so, or .dylib in osx parlance) and the
headers.  When linking, the linker uses frameworks, and falls back to the
traditional linux mechanism (.dylib and .h) only later. Frameworks always have priority,
and most of the complexity of our setup depends by the fact that OSX ships with python
and its framework will prevail on our dynamic library anytime. For this reason, we
use frameworks for python.

However, due to how our application is designed, we need _two_ frameworks,
each containing the different dynamic library with our own magic properties. 
Executables know which frameworks to load through complex magic of the linker.
this magic is done mainly through two mechanism: DYLD_FRAMEWORK_PATH (which is like a
linux LD_LIBRARY_PATH, but for frameworks) and a hardcoded path inside the executable
that is manipulated with a magic utility install_name_tool. This path will be used to
search the frameworks and libraries, it can be seen with otool -L, and can contain
"variables" like @executable_dir. The path is hardcoded at linking time,
extracted from the library and stored into the executable. When we relocate
the library (like in case of deployment), we need to change this path in both
the executable and the library/framework with the cunning use of install_name_tool.
The application deployment script makes liberal use of this command.

Note that traditional dynamic libraries are still looked up in a way similar to
linux, but the variable is called DYLD_LIBRARY_PATH instead. DYLD_LIBRARY_PATH
is always resolved after the frameworks.

Install XQuartz to get libpng and libfreetype (macosx does not ship with functional ones), 
mainly for Qt and matplotlib, or compile the libs ourselves.

For python on OSX, the deployment happens in Frameworks.  In general, the
python Framework directory is also the receiver for site-package deployment. To
prevent duplication of the site-package and the python .py standard library, we
use symbolic links. 

# Potential compatibility issues

- Paths can be different, in particular relative to the executable.
- the OSX filesystem is case preserving, but case insensitive, meaning that Foo and FOO are the same file, even if their
  name is different. If we rely on difference in case to see if two files are different, we will get a bad time.
- changing envvars for application startup is not trivial, meaning that changing the license variables can't be dealt with easily.



