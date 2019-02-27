# Pages

- [Test](test.md)

# Posts

<ul>
{% for post in site.posts %}
  <li><a href="{{ post.url }}">{{ post.date | date_to_string }} - {{ post.title }}</a></li>
{% endfor %}
</ul>
