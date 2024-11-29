---
layout: teaching
title: "Previous Courses"
permalink: /teaching/previous-courses/
---
## Current Courses
{% for course in site.teaching %}
  {% if course.year and course.year >= 2024 %}
    - [{{ course.title | default: "Untitled Course" }}]({{ course.url | default: "#" }}) ({{ course.year }})
  {% endif %}
{% endfor %}

## Previous Courses
{% for course in site.teaching %}
  {% if course.year and course.year < 2024 %}
    - [{{ course.title | default: "Untitled Course" }}]({{ course.url | default: "#" }}) ({{ course.year }})
  {% endif %}
{% endfor %}


