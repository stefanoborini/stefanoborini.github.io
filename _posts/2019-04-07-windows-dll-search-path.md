---
category: microsoft
---

Written 23 Jan 2015

# Windows DLL search path

On windows, we want applications to be able to start without the need for a path specification, yet we need our DLLs to be found. 
In the past, we relied on PATH for this, but this is going away, for the following reasons:

1. The PATH variable on windows is extremely limited (260 chars) and it runs out fast. on User's machines, it can lead to problems.
2. If two or more versions of an application are installed, one of the two will end up using the libraries of the other, with horrible consequences, depending on which come first in the PATH specification.
3. Using the path doesn't solve the problem that some users encounter, that is, if they have a library in the System32 directory that happens to have the same name, it will override ours and generate strange errors.
 
Windows has a weird lookup strategy for dlls, and it depends on flags and other
circumstances. What [http://msdn.microsoft.com/en-us/library/7d83bc18.aspx
MSDN] says is the following order, in the most simplified approach:

* The directory where the executable module for the current process is located.
* The current directory.
* The Windows system directory. The GetSystemDirectory function retrieves the path of this directory.
* The Windows directory. The GetWindowsDirectory function retrieves the path of this directory.
* The directories listed in the PATH environment variable.

An important thing to note is that "executable module" is not necessarily the
running exe. If exe depends on a library dll1 which in turn depends on another
library dll2, the "executable module" will be dll1. To add to the confusion, we
need to deal with both regular dependencies (e.g. linkage) and with dynamic
opening ("dlopen" like) which is extensively used by python to load "pyd" files
(basically, compiled python modules).

We want to make the last entry irrelevant, that is, we don't want to depend on
the path for library lookup. Excluding the system directories and magic
registry tricks, we are left only with the first option. Which means that we
need to put all stuff in the right place. We also don't want system libraries
to take over or influence our installation.

A temporary solution has been devised, but requires care. Also, the solution
may involve two different strategies for developers and users (deployed
version)

## Developers

For developers, keep relying on %PATH% for lookup, and point this to the
external-libs/build/lib. You may still have weird behaviors if there's another
application installed, another python, or another set of libraries somewhere on the
system. This is an acceptable compromise.

The alternative would be littering external-libs/build/ with copies of dll
files in the right places, near the relevant modules.

## Users

As said above, the right place depends on what entity we are talking about.
There are many possible situations that may occur

- direct dependencies of the executable
- direct dependencies of the python27.dll
- direct dependencies of a dll
- dlopen() dependencies of python (that is, pyd files)
- direct dependencies of the pyd files.

Four possible places where dlls may need to go

- in bin
- in lib
- and somewhere under lib/site-packages/
- in lib/qt-plugins

I present here all cases, together with the proper placement.

* Direct dependency (e.g. link time library) of the executable: in bin. Examples: python27.dll.
* Dynamically loaded ("dlopen") library, typically pyd: in lib or in appropriate lib/site-packages dir. 
  This stuff gets opened dynamically by python using LoadLibrary. The lookup is performed thanks to sys.path.
* Dynamic dependency for qt plugins. under lib/qt-plugins. This is resolved thanks to a QCoreApplication.addLibraryPath() invocation. Qt takes care of the rest.
* Link dependencies (dlls) of pyd files. These may go in two places: either on the side with the pyd (that is, under the lib/site-packages/whatever/ path), or in lib/. 
  The second case is for special libraries that happens to be dependencies. The dll gets loaded at startup and when the python module is loaded, apparently the windows 
  loader finds out that the dependency is already mapped to VM and doesn't complain nor explores alternatives.

_NOTE_: If you have both a direct dependency for an executable, and a direct or dynamic dependency on the same dll somewhere else, you might have to have two copies of the dll in two different places.

# Open Problems

* can't use mkl scalapack dynamically, because the dynamic dll is missing the "pzherk" symbol. We are forced to link it statically.

# Other attempts

Here is a list of alternative strategies we examined to tackle the problem, unsuccessful for some reason or another.

* Using AddDllDirectory can't be done. Windows 8 only
* Using SetDllDirectory doesn't appear to work. It allows only one directory. An experiment on h5py led to it being unable to find another pyd file that was needed and was inside the site-packages/h5py. Putting all .pyd in /lib is not a good idea. It's a game that ends as soon as we have two modules with the same filename.
* Using App Path in the registry, not an option. The lookup is done on the executable name, and the executable name will collide if the user installs two versions of the app. 
* On windows, we can't use the same trick we use on linux and OSX (having a pre-startup script that exports the proper paths), for both point one above, and because it would open a terminal. Workarounds may exist, but in the end the problem is much more complex. If we do this export within the C code, we would have to locate the absolute path of the executable, something that may not be easy. Also, we are still constrained to 260 chars, and we would have troubles anyway for subsequent executables spawned by the app.
* manifests. It's unclear if they would help, but they are complex and require further analysis.

