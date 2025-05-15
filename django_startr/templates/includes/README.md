# Template Includes

This directory contains reusable template fragments that can be included in other templates.

## Available Includes

### boomer.html

The Boomer mascot image with configurable styling.

Usage:
```django
{% include "django_startr/includes/boomer.html" %}
```

With custom styling:
```django
{% include "django_startr/includes/boomer.html" with style="--w:50px; --pos:absolute; --bottom:10px; --right:10px" %}
```
