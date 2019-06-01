---
category: semantic web
title: XML Namespace URL (updated)
---

I am attending the [EMBRACE workshop in SOAP
clients](http://www.cbs.dtu.dk/courses/embrace/2008-02-06/). A very
interesting workshop I would say, and I\'ll wrote more about it when
finished. During the workshop, it has been pointed out the usual issue
of XML namespaces: the attribute value looks like a URL but it is not
referring to anything in particular. An example from a SOAP envelope

```xml
<?xml version="1.0"?>
<soap:Envelope xmlns:soap="http://www.w3.org/2001/12/soap-envelope"
soap:encodingStyle="http://www.w3.org/2001/12/soap-encoding">
</soap:Envelope>
```

Technically, the attribute value is a string that represents the
namespace. The choice to use a URL stems by the fact that the DNS system
guarantees uniqueness and authoritativeness, so if you define a new
namespace, using your own domain guarantees (sort of) to be unique.
However, there is no consensus about what this URL should resolve to. In
some cases, it refers to the XML schema. In others to a DTD, or to a
stylesheet, or more frequently to nothing. You can have a picture of the
situation from these articles
[1](http://www.oreillynet.com/pub/a/oreilly/xml/news/xmlnut2_0201.html),
[2](http://www.xml.com/pub/a/2001/02/28/rddl.html), and
[3](http://www.rpbourret.com/xml/NamespacesFAQ.htm#uris_5). The first
two articles, in particular, advocate the use of RDDL to solve the
problem. Basically in the ambiguity of what to put, the answer with RDDL
is: none of them. Instead, provide a RDDL document that says where to
find each of them (if provided). Not a bad idea.

Waiting for the community to decide what to put at that address, my
personal choice went toward a still standard but not deliberately
confusing choice. I put a uuid URN.

```xml
xmlns:foo="urn:uuid:212e2ac7-dc35-4112-ae86-cefd26abb856"
```

which is valid according to standard (you can put any URN), it is unique
and at least it does not pretend to look like it\'s referencing to
something. You can generate one with `uuidgen`.

An objection to this approach is that a uuid is not easy to remember,
and so you have to copy and paste it every time. Well, the URL approach
has more or less the same issue. Namespacing does not work correctly if
you don\'t specify the URL namespace exactly, so you end up copying and
pasting it anyway.

**Update**: Just today, the W3C released an [interesting
plea](http://www.w3.org/blog/systeam/2008/02/08/w3c_s_excessive_dtd_traffic)
to developers in order to limit the traffic at w3.org. Apparently, they
get an insane amount of traffic, due to the attempts by various
softwares around the net to get the documents referred by the addresses
in DTD and namespace. This is another indication that you should be very
careful in putting an URL, in particular if your format becomes very
popular and you don\'t have big pipes to hold the traffic.
