---
layout: teaching
title: "Previous Courses"
permalink: /teaching/previous-courses/
---
{% for course in site.teaching %}
  {% if course.path contains "previous-courses" %}
    - [{{ course.title }}]({{ course.url }}) ({{ course.year }})
  {% endif %}
{% endfor %}
