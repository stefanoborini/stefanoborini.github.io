Unraveling Unicode problems in WikkaWiki
========================================

author

:   Stefano

category

:   Unicode

While I was setting up the wiki, I realized some problems with
non-English letters, such as ö. Therefore I had to find out more details
about Unicode and encoding (a task that does not happen frequently if
you program in languages such as Fortran, where you normally have other
class of problems to handle). I found this [very interesting page on
JoelOnSoftware](http://www.joelonsoftware.com/articles/Unicode.html),
and another [FAQ for
Unix/Linux](http://www.cl.cam.ac.uk/~mgk25/unicode.html).

Basically, if I understood correctly, everything can be summed up to the
following:

-   Unicode is a standard that define how to handle all the conceivable
    symbols (roman letters, numbers, Japanese and Chinese ideograms,
    arabic letters etc\...). Actually, there is both ISO 10646 and
    Unicode, and they are not the same: Unicode does a lot more. So
    Unicode is a superset of ISO 10646, but for our discussion we will
    talk about Unicode even if talking about ISO 10646 would suffice
    just because is easier to type.
-   Unicode assigns to every symbol a given number, the **code point**.
    For example, the letter A is assigned to code point 0x41, and 食
    (taberu), which is the japanese character for the verb \"to eat\",
    has code point 0x98DF. The code point set can be eventually expanded
    to include any symbol, even those from invented languages (although
    unofficially, [Tolkien\'s
    Tengwar](http://www.evertype.com/standards/csur/tengwar.html) and
    [Klingon](http://www.evertype.com/standards/csur/klingon.html) are
    included).
-   The code point specifies an abstract symbol, not a way to draw that
    symbol. How this symbol is drawn is a task involving the font, which
    is used to produce a concrete glyph representation for each code
    point it covers.
-   To write code points into files or in memory, you have to use an
    encoding, basically a technique to represent the code point value in
    practice. There is an insane amount of encodings, but they can be
    classified in two rough categories: **fixed length encodings** and
    **variable length encodings**.
-   In fixed length encodings, every symbol require a fixed number of
    bytes, say 4. This is the approach
    [UTF-32](http://en.wikipedia.org/wiki/UTF-32) uses: every code point
    requires four bytes to be written, always. This solution increases
    the space occupation four-fold even if you are only using plain
    English characters. Moreover, it is not backward compatible, so you
    cannot read a pure English text encoded in UTF-32 with `cat`. The
    advantage of this solution is that you know how much you have to
    skip to jump to the next or previous character, four bytes, and you
    know very easily how many characters you have: the occupied size
    divided by four.
-   In variable length encodings, whose major representative is
    [UTF-8](http://en.wikipedia.org/wiki/UTF-8), the number of bytes
    needed to encode a code point depends on the code point itself. For
    code points in the interval 0x0-0x7F, UTF-8 uses just one byte. Code
    points between 0x80--0x7FF will need two bytes, code points between
    0x800--0xD7FF will require three bytes and so on. With this
    approach, simple English text will continue to be small and backward
    compatible, because each code point will be represented with a
    single byte, and this code point is mapped as in ASCII. Another
    important advantage is that the space occupation is of course more
    efficient. The disadvantage is that it is more difficult to go
    forward or backward one symbol: in C, buf++ will not work, because
    you could instead jump in the middle of a two-byte encoded
    character. With a fixed length encoding you know how many bytes you
    have to skip. With UTF-8 you have to parse the code point
    representation, and then determine how many bytes to move. Normally,
    however, proper API is provided to take care of these issues once
    and for all.

The problems I had with the ö letter arised from a wrong encoding
WikkaWiki was assuming: it specified the document as
[iso-8859-1](http://en.wikipedia.org/wiki/ISO_8859-1) encoded.
ISO-8859-1 (also known as Latin-1) is basically a single-byte encoding
like ASCII, where values from 0x80 to 0xFF map to most European symbols.
However, the data I wrote was UTF-8 encoded, and this introduced a
mismatch between the data and the decoding performed by the browser (in
ISO-8859-1, as specified in the HTML). Since ö has code point U+00F6
(binary 11110110), this resulted in a two-byte UTF-8 encoding of the
type 110yyyyy 10zzzzzz: 11000011 10110110, or 0xC3 0xB6. Each of these
two bytes was interpreted as a single-byte ISO-8859-1 value, leading to
a weird Ã¶ (capital A tilde and [pilcrow end
paragraph](http://en.wikipedia.org/wiki/Pilcrow)) instead of an ö (o
with umlaut).

To solve, I basically changed the default meta tag content in WikkaWiki,
from

``` {.html}
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
```

to

``` {.html}
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
```

and now it works correctly.

Other references:

-   <http://unicode.org/faq/unicode_iso.html>
-   <http://en.wikipedia.org/wiki/Comparison_of_Unicode_encodings>
