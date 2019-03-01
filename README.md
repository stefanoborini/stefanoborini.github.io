# Pages

- [Resume](pages/resume.md)

# Opensource

- [PEP-472](https://www.python.org/dev/peps/pep-0472/)

# Ramblings

- [Graph theory](ramblings/graph_theory.md)

# Slides

- [Fortran](slides/fortran/fortran.svg)
- [Do and Don'ts in coding](slides/do_and_donts_in_coding/do_and_donts_in_coding.svg)
- [Limitations of DFT](slides/limitations_of_DFT/limitations_of_DFT.svg)

# Books

- [PhD Thesis](https://github.com/stefanoborini/thesis-PhD/blob/master/thesis-borini.pdf)
- [Master Thesis](https://github.com/stefanoborini/thesis-master/blob/master/borini-master-thesis.pdf)


<div id="archives">
{% for category in site.categories %}
  <div class="archive-group">
    {% capture category_name %}{{ category | first }}{% endcapture %}
    <div id="#{{ category_name | slugize }}"></div>
    <p></p>
    
    <h3 class="category-head">{{ category_name }}</h3>
    <a name="{{ category_name | slugize }}"></a>
    {% for post in site.categories[category_name] %}
    <article class="archive-item">
      <h4><a href="{{ site.baseurl }}{{ post.url }}">{{post.title}}</a></h4>
    </article>
    {% endfor %}
  </div>
{% endfor %}
</div>

# Posts

<ul>
{% for post in site.posts %}
  <li><a href="{{ post.url }}">{{ post.title }}</a></li>
{% endfor %}
</ul>

