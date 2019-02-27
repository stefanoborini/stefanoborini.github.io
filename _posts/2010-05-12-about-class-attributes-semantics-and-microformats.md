About class attributes, semantics and microformats
==================================================

I just got to [this post by Richard le
Guen](http://richard.jp.leguen.ca/not-blog/a-css-class) via the
referrals to my blog, and I feel it\'s important to clarify my point.

So, let\'s describe the problem. In HTML, you describe the layout of
your information. How the information will look like is \"presentation\"
and is managed via a so called Cascading Style Sheet, or CSS. Change the
CSS, the visual aspect changes.

To bind the entities you describe in HTML with how they will appear, you
use a standardized attribute, the **class**. An example is:

```html
<div class="info">This is a message</div>
```

In this example, the **info** label is the class assigned to the content
of the \<div\> HTML tag. Now you can change its appearance with a CSS
directive like

```css
.info {
   color: blue;
   font-size: 13px;
}
```

if you want the text to appear blue and of a given size. So far so good.

One of the problems in todays\' web is to give semantic meaning to
things, so that a computer can extract the information and do smart
things with it. Unfortunately there\'s no clear way to perform this
(well, there is, but we would get into an argument too complex to be
described here).

Enter [microformats](http://en.wikipedia.org/wiki/Microformat): the
point of microformats is to grant semantics through ad-hoc class names
that are not only used as a representational reference into the css, but
also are assigned to a well-defined meaning. Example:

```html
<div>
  <div>Joe Doe</div>
  <div>The Example Company</div>
  <div>604-555-1234</div>
  <a href="http://example.com/">http://example.com/</a>
</div>
```

can be endowed with semantic meaning if you use the hCard microformat

```html
<div class="vcard">
  <div class="fn">Joe Doe</div>
  <div class="org">The Example Company</div>
  <div class="tel">604-555-1234</div>
  <a class="url" href="http://example.com/">http://example.com/</a>
</div>
```

With this solution, a computer can now understand meaning out of the
class attribute, and do smart things like aggregating data, and allow
searching on it.

Some time ago, on Jeff Atwood blog, [coding
horror](http://www.codinghorror.com/blog/2009/12/microformats-boon-or-bane.html),
a point was made about microformats and their problems. In particular to
the fact that (citing Jeff) \"**the crux of microformats is overloading
CSS classes**\", and I tended to agree, considering technically wrong to
overload CSS classes with meaning.
[Richard](http://richard.jp.leguen.ca/not-blog/a-css-class) objected
that the very definition at the W3 consortium about class attributes is
also \"For general purpose processing by user agents\", which
convincingly includes hCard scrapping tools.

On this, Richard is right, and I\'m torn on my previous stance. The
point is that the class attribute is indeed specified as a general
purpose tool, which specifically and most frequently is used for
stylization purposes. Microformats are, from the formal point of view, a
totally legitimate use of the class attribute. Nevertheless, when you
overload classes with meaning you can incur in [all the problems Jeff
Atwood points
out](http://www.codinghorror.com/blog/2009/12/microformats-boon-or-bane.html),
and you should be very, very careful, or chaos will ensue. Formal
approval for a usage is not always indicative of a safe practice, but in
this case the problem arises from the fact that we tend to think at
class names as something that has a meaning only within our web
application. With microformats, this meaning extends outside the
boundaries of our self-contained world, and this conflictual view can
produce problems.

**Edit** : Another issue worth reporting is namespacing. The fact that
you grant semantic meaning to a given class attribute means that a given
string, say \"vcard\" conveys a specific meaning which is unique. If you
take every possible available string in the world, they belong to a
unique, flat namespace. Now, RDF-based semantics approach uses
namespacing to distinguish different meanings granted to the same string
by using, instead of a trivial string, a URI. In microformats, and in
the approach used by microformats, you don\'t have namespacing, but you
have containment. For example, the class \"tel\" in the vcard
microformat can be distinguished by another \"tel\" (for example,
indicating a table cell on the same webpage) by the fact that the one in
the microformat matches the selector \".vcard .tel\". It\'s sort of
namespacing, although with a different mechanism, and it\'s done and
built through the containment relationships among HTML elements.

It\'s mind bending if you think about it, but once you see how it works,
it\'s kind of smart. It\'s not as complex and demanding as RDF, not as
powerful as OWL-based ontology description, but it can work for simple
to medium complexity semantic data.
