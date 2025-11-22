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
{% assign journal_items = site.publications | where: "pubtype", "journals" | sort: "date" | reverse %}
{% for post in journal_items %}
  {% include publication-line.html %}
{% endfor %}
</ul>

<h2>Proceedings</h2>
<ul class="pub__list">
{% assign proceeding_items = site.publications | where: "pubtype", "proceedings" | sort: "date" | reverse %}
{% for post in proceeding_items %}
  {% include publication-line.html %}
{% endfor %}
</ul>

<h2>Preprints</h2>
<ul class="pub__list">
{% assign preprint_items = site.publications | where: "pubtype", "preprints" | sort: "date" | reverse %}
{% for post in preprint_items %}
  {% include publication-line.html %}
{% endfor %}
</ul>

<h2>Working papers</h2>
<ul class="pub__list">
{% assign working_items = site.publications | where: "pubtype", "working" | sort: "date" | reverse %}
{% for post in working_items %}
  {% include publication-line.html %}
{% endfor %}
</ul>

<a href="/" class="back-button">← Back to Home</a>