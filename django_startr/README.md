# Django Startr Smart Select + Other Amazing Features

This package enhances Django admin select fields with smart filtering capabilities.

## Features

- Converts all select fields in the Django admin to smart select fields
- Provides real-time filtering as you type
- Maintains all original select field functionality
- Works with all Django admin select fields automatically

## Installation

1. Add `django_startr` to your `INSTALLED_APPS` in settings.py:

```python
INSTALLED_APPS = [
    ...
    'django_startr',
    ...
]
```

2. Import and add the settings from django_startr to your settings.py:

```python
from django_startr.settings import get_django_startr_settings

# Add the settings
settings_dict = get_django_startr_settings()
for key, value in settings_dict.items():
    globals()[key] = value
```

## Usage

Once installed, all select fields in your Django admin will automatically be converted to smart select fields. No additional configuration is needed.

## Customization

The smart select functionality can be customized by modifying the JavaScript in `django_startr/templatetags/smart_select.py`.

## Requirements

- Django 2.0 or higher
- Python 3.6 or higher 