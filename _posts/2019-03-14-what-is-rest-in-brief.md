---
category: web
title: What is REST, in brief (incomplete)
---
# What is REST, in brief (incomplete)

What exactly IS a REST API. What makes it RESTful? What is an average use case
for this in a program?  My knowledge of APIs is... Well, not that good, but a
lot of stuff I've seen talks about REST and I don't really understand it.

Not really relevant to python, but here is the thing.  The idea behind REST is
that everything is a resource or can be represented as a resource, and must be
presented to the outside world as such. Each resource is represented by one URL
(actually, a URI which also happens to be a URL), which contains a unique ID
(either a numeric value, or a uuid, are generally used). You can create, read,
update, or delete these resources using the standard http verbs. You create
with POST, you read with GET, you update with PUT (or POST) and you delete with
DELETE. When you create the object with POST, you also deliver a payload, in
whatever format you want, that describes the content. The most trivial example
would be a collection of users, you create a new user like this, supposing the
payload is in xml. You send this to the webserver

```
POST /users/
<user><name>John Doe</name></user>
```

The response generally contains the new id, suppose it's 2453. now you have a
resource at http://example.com/users/2453/ and if you GET it, you obtain back
your xml, or another representation, if you want

```
GET /users/2453/
<user><name>John Doe</name</user>
```

The idea is that you always create resources, and all operations are changes in
the state of these resources. You never perform actions on these resources on
the webserver, meaning that some patterns that rely on "remote procedure call"
like behavior, such as when you call stuff like
http://example.com/?action=changeName&id=2453&newName=John%20Deer
is a no-no in REST. Instead, you would do

```
PUT /users/2453/
<user><name>John Deer</name</user>
```

And you would delete with

```
DELETE /users/2453/
```

Most of the difficulty of using REST is to convert your problem as being
representable as a resource. For example, one problem I had was to create a
queuing system. In that case, you have a queue, and create a resource for a new
submission. This submission payload contains the relevant information to start
the job. When you query the resource, it contains the info plus a flag that
says if it's submitted, errored, in the queue, or running, meaning that the
webserver does not necessarily act just as a repository of info you stuff in.
It can also add new info.  If you want to understand more, the best resource is
definitely Roy Fielding's thesis (not all of it, just the relevant parts), and
the o'Reilly book RESTful web services. It's rather short, but clean and
concise.

Edit:
A rather challenging part of REST is to perform transactions. Suppose you have
to perform multiple operations to keep the resource set consistent. How do you
do it, considering that you are operating on one resource at a time? In that
case, you first create a transaction resource, e.g. in /transactions/. Then,
you perform the operations on the individual resources, and inside the payload
you specify the transaction id you got. GET operations on the resources while
you are performing the transaction return the old payload. When you are done,
you PUT the transaction with a payload flag "state: committed" and the
resources are synchronized.  Alternatively, you can create the transaction with
the payload describing the operations to perform and on which resources, and
then the webserver applies atomically all the changes. It's mostly a matter of
taste, but the point is that, as I said, everything is seen as a resource, even
transactions.



