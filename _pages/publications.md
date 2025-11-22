---
layout: archive
permalink: /publications/
author_profile: true
---

{% if author.googlescholar %}
  You can also find my articles on <u><a href="{{author.googlescholar}}">my Google Scholar profile</a>.</u>
{% endif %}

{% include base_path %}

<h2>Published</h2>
<ul class="pub__list">
{% assign journal_items = site.publications | where: "pubtype", "journals" %}
{% assign proceeding_items = site.publications | where: "pubtype", "proceedings" %}
{% assign published_items = journal_items | concat: proceeding_items | sort: "date" | reverse %}
{% for post in published_items %}
  {% include publication-line.html %}
{% endfor %}
</ul>

<h2>Working Papers & Preprints</h2>
<ul class="pub__list">
{% assign preprint_items = site.publications | where: "pubtype", "preprints" %}
{% assign working_items = site.publications | where: "pubtype", "working" %}
{% assign unpublished_items = preprint_items | concat: working_items | sort: "date" | reverse %}
{% for post in unpublished_items %}
  {% include publication-line.html %}
{% endfor %}
</ul>

<a href="/" class="back-button">← Back to Home</a>