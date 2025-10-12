---
layout: archive
permalink: /publications/
author_profile: true
---

{% if author.googlescholar %}
  You can also find my articles on <u><a href="{{author.googlescholar}}">my Google Scholar profile</a>.</u>
{% endif %}

{% include base_path %}

<h2>Journals</h2>
<ul class="pub__list">
{% for post in site.publications reversed %}
  {% assign pt = post.pubtype | downcase %}
  {% if pt == 'journals' %}
    {% include publication-line.html %}
  {% endif %}
{% endfor %}
</ul>

<h2>Preprints</h2>
<ul class="pub__list">
{% for post in site.publications reversed %}
  {% assign pt = post.pubtype | downcase %}
  {% if pt == 'preprints' %}
    {% include publication-line.html %}
  {% endif %}
{% endfor %}
</ul>

<h2>Working papers</h2>
<ul class="pub__list">
{% for post in site.publications reversed %}
  {% assign pt = post.pubtype | downcase %}
  {% if pt == 'working' %}
    {% include publication-line.html %}
  {% endif %}
{% endfor %}
</ul>

<a href="/" class="back-button">← Back to Home</a>