---
category: qt
title: PyQt Gotchas
---

PyQt and Qt have a fundamental conflict: memory management. Python frees stuff
when references go out of scope, while Qt, being based on C++, has no such
automatic mechanism for free storage data (that is, stuff allocated with new).
Qt obviates to this problem by using a hierarchy: when the parent is deleted,
the children are deleted in cascade.  Unfortunately, this can create a lot of
hard-to-debug chaos in two cases:

* if the Qt mechanism (which knows nothing about python) deletes a C++ object while we are holding a python object pointing to that C++ one.

* if python deletes a python object because it goes out of scope, and that object is still referenced and used by Qt at the C++ level.

Both cases will lead to access to freed memory, leading to undefined behavior. Let's see some examples to make things clear.

## Gotcha #1: Using WA_DeleteOnClose

Never use WA_DeleteOnClose.

```
  import sys
  from PyQt4 import QtGui, QtCore
  
  class Main(QtGui.QPushButton):
      def __init__(self, parent=None):
          QtGui.QPushButton.__init__(self, parent)
          self._label = QtGui.QLabel("hello")
          self._label.setAttribute(QtCore.Qt.WA_DeleteOnClose)   # Gotcha
          self.clicked.connect(self.showLabel)
  
      def showLabel(self, *args):
          self._label.show()
  
  if __name__ == "__main__":
      app = QtGui.QApplication(sys.argv)
      widget = Main()
      widget.show()
      sys.exit(app.exec_())
```

Launch the example, and press the button. A label will be shown. Close the
label, and press the button again. The following error occurs: "RuntimeError:
wrapped C/C++ object of type QLabel has been deleted". The reason is that when
the label is closed, the C++ object is deleted, but we are still holding a
reference to it via the self._label python object. Any attempt to use the
self._label object will involve a deleted backend, with bad consequences.

## Gotcha #2: Using a parent that has local scope for a child that has broader scope 

Launch the example, and press the button twice.

```
  import sys
  from PyQt4 import QtGui, QtCore
  
  class Main(QtGui.QPushButton):
       def __init__(self, parent=None):
          QtGui.QPushButton.__init__(self, parent)
          self._counter = 0
          self.clicked.connect(self.doThing)
  
      def doThing(self, *args):
          if self._counter == 0:
              widget = QtGui.QWidget()                          # Gotcha
              self._label = QtGui.QLabel("hello", widget)       # Gotcha
              self._label.show()
          elif self._counter == 1:
              self._label.setText("whatever")
  
          self._counter += 1
  
  if __name__ == "__main__":
       app = QtGui.QApplication(sys.argv)
  
      widget = Main()
      widget.show()
  
      sys.exit(app.exec_())
```

What happens here is that the parent of the label (widget) is local in scope, and its child is kept around as self._label.
When widget goes out of scope in python, it is freed. This triggers a C++ delete of the children. However, we are still holding
a reference to the python object representing one of the children (self._label), which is now referring to freed memory.

## Gotcha #3: Using deleteLater

Launch the example, and press the button three times.

```
  import sys
  from PyQt4 import QtGui, QtCore
  
  class Main(QtGui.QPushButton):
      def __init__(self, parent=None):
          QtGui.QPushButton.__init__(self, parent)
          self._counter = 0
          self.clicked.connect(self.doThing)
  
      def doThing(self, *args):
          if self._counter == 0:
              self._label = QtGui.QLabel("hello")
              self._label.show()
          elif self._counter == 1:
              self._label.setText("whatever")
          elif self._counter == 2:
              self._label.deleteLater()
          elif self._counter > 2:
              self._label.setText("whatever")
  
          self._counter += 1
  
  if __name__ == "__main__":
      app = QtGui.QApplication(sys.argv)
  
      widget = Main()
      widget.show()
  
      sys.exit(app.exec_())
```

The problem here is due to deleteLater(). This routine schedules a deletion of a widget for later, but in doing so, only the C++ object is freed. The python object stays alive and again references freed memory.

## Non-Gotcha: using local scope for child widgets

In this example, 2 subwidgets are added to the layout of a main widget. Access to the widgets are provided only by using the C++ API of Qt, ie. without setting a Python
'self' reference.

```
  import sys
  from PyQt4 import QtGui
  
  class A(QtGui.QLabel):
      def __init__(self, parent=None):
          QtGui.QLabel.__init__(self, parent)
  
  class B(QtGui.QLabel):
      def __init__(self, parent=None):
          QtGui.QLabel.__init__(self, parent)
  
  class Widget(QtGui.QWidget):
      def __init__(self):
          QtGui.QWidget.__init__(self)
  
          # Base layout
          layout = QtGui.QVBoxLayout(self)
  
          # Add widgets
          a = A(self)                          # Here
          b = B(self)                          # Here
  
          layout.addWidget(a)
          layout.addWidget(b)
   
      def a(self):
          return self.layout().itemAt(0).widget()
   
      def b(self):
          return self.layout().itemAt(1).widget()
    
  if __name__ == "__main__":
       app = QtGui.QApplication(sys.argv)
  
      widget = Widget()
      widget.show()
      print widget.a()
      print widget.b()
  
      sys.exit(app.exec_())
```

This is not a problem, because PyQt is clever enough to increment the pythonn
reference count of the objects a and b. In this case, when the a and b objects
go out of scope, the underlying C++ is not deleted as a cascade effect of the
python decrement reference count.

