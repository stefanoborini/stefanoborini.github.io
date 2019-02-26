# All posts

{% for post in site.posts %}
  <a href="{{ post.url }}">
    <h2>{{ post.title }}</h2>
    <p>{{ post.date | date_to_string }}</p>
  </a>
{% endfor %}


## Old posts

- [Molecular Builder Project, a retrospective of a Waterfall project.](posts/molecular_builder_project.md)

