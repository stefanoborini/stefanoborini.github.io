How to convert a QString to unicode object in python 2?
=======================================================

I had this problem to solve, and I tried to find the safest way. This
program illustrates the solution

```python
from PyQt4 import QtCore, QtGui                                                                                                                       
import sys                                                                                                                                            

app = QtGui.QApplication(sys.argv)                                                                                                                    
ed = QtGui.QLineEdit()                                                                                                                                

def editingFinished():                                                                                                                                
    # The text() returns a QString, which is unicode-aware                                                                                            
    print type(ed.text())                                                                                                                             
    # This returns a QByteArray, which is the encoded unicode string in the utf-8 encoding.                                                           
    print type(ed.text().toUtf8())                                                                                                                    
    # Since unicode() accepts a sequence of bytes, the safest and fully controlled way of performing                                                  
    # the transformation is to pass the encoded sequence of bytes, and let unicode know it is utf-8 encoded                                           
    print unicode(ed.text().toUtf8(), encoding="UTF-8")                                                                                               

QtCore.QObject.connect(ed, QtCore.SIGNAL("editingFinished()"), editingFinished)                                                                       
ed.show()                                                                                                                                             

app.exec_()
```

So the solution is

```python
unicode(qstring_object.toUtf8(), encoding="UTF-8")
```

Maybe there\'s another, simpler way that it\'s also safe, but for now
this solution is good enough.
