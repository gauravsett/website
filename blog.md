---
title: Blog
permalink: /blog.html
layout: default
last_modified_at: 2023-08-18
---

# My Blog

### Posts
{% for post in site.posts %}
- [{{ post.title }}]({{ post.url }}) [{{ post.date | date: "%Y-%m-%d" }}]
{% endfor %}