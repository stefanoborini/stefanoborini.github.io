# Pages

- [Resume](pages/resume.md)

# Opensource

- [PEP-472](https://www.python.org/dev/peps/pep-0472/)

# Slides and presentations

- [Model View Controller](slides/model-view-controller/index.html)
- [Do and Don'ts in coding](slides/do_and_donts_in_coding/do_and_donts_in_coding.svg)
- [Fortran notes](slides/fortran/fortran.svg)
- [Limitations of DFT](slides/limitations_of_DFT/limitations_of_DFT.svg)
- [Testing analysis](slides/testing-analysis/testing-analysis.svg)
- [EuroSciPy 2017 - Simphony-remote - Accessing containerized desktop and web applications with a web browser (video)](https://www.youtube.com/watch?v=QK2ydXN8yv4)

# Books

- [Computing for Comparative Microbial Genomics: Bioinformatics for Microbiologists](https://www.amazon.co.uk/Computing-Comparative-Microbial-Genomics-Microbiologists/dp/1848002548)
- [Understanding Model-View-Controller](book-modelviewcontroller)
- [PhD Thesis](https://github.com/stefanoborini/thesis-PhD/blob/master/thesis-borini.pdf)
- [Master Thesis](https://github.com/stefanoborini/thesis-master/blob/master/borini-master-thesis.pdf)

# Posts

<div id="archives">
{% assign sorted_cats = site.categories | sort %}
{% for category in sorted_cats %}
  <div class="archive-group">
    {% capture category_name %}{{ category | first }}{% endcapture %}
    <div id="#{{ category_name | slugize }}"></div>
    <p></p>
    
    <h3 class="category-head">{{ category_name | capitalize }}</h3>
    <a name="{{ category_name | slugize }}"></a>
    <ul>
    {% assign sorted_posts = category[1] | sort:"title" %}
    {% for post in sorted_posts %}
        <li><article class="archive-item"><a href="{{ site.baseurl }}{{ post.url }}">{{post.title}}</a></article></li>
    {% endfor %}
    </ul>
  </div>
{% endfor %}
</div>

