---
category: other
---
# Design of file formats

I worked with file formats for a while during my career. I also saw a lot of
them, produced by others. It is shocking how many bad decisions people do when
designing file formats, in particular when it comes to a fundamental point

*Whatever you write on the customers' disk, is going to stay, and you will have
to support, forever.*

And with this consideration in mind, it's incredible how poor thinking is done
on file formats, both for input and output. Here are what I believe to be
typical design mistakes of a file format.

    - Putting the creation time and date. This metainformation may be somehow
      useful, but it's already supported by the filesystem. Unless you need to
      keep history information, it makes no sense. In addition, it makes the task of
      testing the output for correctness much harder, because in some cases, a quick
      and dirty md5 does the job. With a "creation date" inside the file, the md5
      changes at every run, unless you can override it.

    - Putting a "creator" information. in some circumstances this is rather
      irrelevant. Say you have a program A creating the file. The file now
      contains "A" as creator. Now you open the file with program B, modify the file
      considerably, and save it. Who is now the creator ? well, technically A, but
      this information is largely irrelevant. A didn't provide all the information
      stored into the file.
    - No version. This is so obvious that when I see no version information
      into a file format I start to wonder if the one who deployed the file
      actually knew how to code.
    - Version as a floating point number. Ok, you decide your file version is
      "1.1", but that does not mean it must be a floating point number. You are
      very likely to extract that value from the file and then check it for equality
      in order to do things. Comparing floats for equality is a no-no, and in any
      case it does not make sense. A floating point number is used to perform math
      operations. A version number is an identification token. Do you really plan to
      do the square root of your file version number anytime soon ?
    - Reinventing the wheel, squared. This is incredible. One of the big
      problems of data is how to lay them out on the disk. A file format will
      most likely contain different kind of data, and may need to be portable across
      different platforms. You may also need some kind of check in order to see if
      the file is somehow corrupted at the basic layer of storage, before opening it.
      Some output files today are zip files, masked as something else. ODP is a zip
      file, and so is JAR. If you store computational data, HDF and NetCDF are good
      choices. This is very convenient, because it solves you the problem of disk
      representation, leaving you only the problem of semantic representation of your
      data.
    - Lack of uniformity, lack of official specification.
    - Lack of an IO layer.
