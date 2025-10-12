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
  {% assign venue = post.venue | default: post.booktitle %}
  {% assign pt = post.pubtype | downcase %}
  {% assign is_preprint = venue contains 'arXiv' or venue contains 'bioRxiv' %}
  {% if pt == 'journals' or (pt == '' and venue and is_preprint == false) %}
    {% include publication-line.html %}
  {% endif %}
{% endfor %}
</ul>

<h2>Preprints</h2>
<ul class="pub__list">
{% for post in site.publications reversed %}
  {% assign venue = post.venue | default: post.booktitle %}
  {% assign pt = post.pubtype | downcase %}
  {% assign is_preprint = venue contains 'arXiv' or venue contains 'bioRxiv' %}
  {% if pt == 'preprints' or (pt == '' and is_preprint) %}
    {% include publication-line.html %}
  {% endif %}
{% endfor %}
</ul>

<h2>Working papers</h2>
<ul class="pub__list">
{% for post in site.publications reversed %}
  {% assign venue = post.venue | default: post.booktitle %}
  {% assign pt = post.pubtype | downcase %}
  {% assign is_preprint = venue contains 'arXiv' or venue contains 'bioRxiv' %}
  {% if pt == 'working' or (pt == '' and venue == nil and is_preprint == false) %}
    {% include publication-line.html %}
  {% endif %}
{% endfor %}
</ul>

<a href="/" class="back-button">← Back to Home</a>