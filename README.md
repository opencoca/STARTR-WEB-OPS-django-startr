# Django Startr Code

Django Startr is here to turbocharge your project setup! With just a few commands, it auto-generates everything you need—views, forms, URLs, admin, and templates—for all the models in your `models.py`. Say goodbye to tedious boilerplate and hello to more time for innovation.

Just add one URL pattern to your project's URLconf, and you're off! You’ll have list, detail, create, update, and delete views for every model in your app, ready to go.

If you want more control, you can choose which models to start from and skip the rest. Everything’s plug-and-play, and totally customizable.

---

## Installing

You can either clone the repository and install it manually, or add it as a submodule or use pip:

```bash
pip install django-startr
```

Add `'django_startr'` to `INSTALLED_APPS`.

---

## Usage

Imagine your project is called **TechRocket**, and it has an app `mission`.

```bash
python manage.py startapp mission
```
At this point define your models in the `models.py` file in the `mission` app. Once you have defined your models, you can run the following command to generate the necessary files for all the models in both apps.


```bash
python manage.py startr mission:Rocket,MissionControl
```
This command generates the necessary files for all the models in both apps. If you only want specific models, like `Rocket` and `MissionControl`, you can narrow it down:



To connect everything, add one URL pattern to your project's URLconf:

```bash
(r'^mission/', include('mission.urls')),
```

And voilà, you’ll have a working URL structure like this:

```
/mission/rocket
/mission/missioncontrol
```

If you want shorter URLs:

```python
(r'^rocket/', include('mission.urls.rocket_urls')),
(r'^missioncontrol/', include('mission.urls.missioncontrol_urls')),
```

Now you’ve got:

```
/rocket
/missioncontrol
```

---

## Views

We keep things tidy by creating a `views` directory, where each model gets its own views file (e.g., `rocket_views.py`). There’s also an `__init__.py` file that imports all the views, making it easy to call what you need.

Almost every method you can override in Django’s CBVs (class-based views) is stubbed out for you, so you can quickly jump in and customize as needed. The attributes and methods are laid out in the order they’re called for convenience.

---

### Niceties Included:

- **form_class** is set to a `ModelForm` in your `forms.py`.
- **context_object_name** is a clean, slugified version of your model name (e.g., `rockets` for `DetailView`, or `rockets_list` for `ListView`).
- If your model has a unique slug field, it's automatically set as the `slug_field` and `slug_url_kwarg`.
- **get_success_url** sends users to the object’s `DetailView` after updates or deletes.

---

## Templates

The generated templates are kept minimalist, so you can easily modify them to fit your style. Each extends a model-specific base file (e.g., `rocket_base.html`), which extends your project’s `base.html`.

- The `ListView` template includes links to view, update, and delete items, plus an option to create new ones.
- The `DetailView` shows the object and links to update or delete it.
- The `CreateView` and `UpdateView` display a form and link back to the list view.
- The `DeleteView` has a confirmation button and links back to the list view.

---

## Admin Setup

For each model, Django Startr generates a `ModelAdmin` using a custom mixin that makes setting up your admin interface super simple. By default, Django Startr guesses intelligent options for `list_display`, `list_filter`, and `search_fields` to give you a full-featured admin panel without the hassle.

---

### Some Extras:

- **list_select_related**: Automatically set for all foreign key fields, improving query performance.
- **list_display**: Includes all model fields except the `id` and `ManyToManyFields`.
- **list_filter**: Smart filtering for fields with `choices`, booleans, and foreign keys with fewer than 100 related objects.
- **search_fields**: Automatically set for `CharField` and `TextField`.

---

## The Future of Django Startr

Our top three goals are:

1. Allow models to be regenerated when new ones are added.
2. Automatically generate tests for each app and model.
3. Add tests to Django Startr itself.

Pull requests are always welcome!

---

## License

Copyright 2023-2025 12787326 Canada Inc.

Licensed under the AGPLv3: https://opensource.org/licenses/agpl-3.0

Dual License Notice
This project is dual-licensed under two licenses:

All code and contributions prior to 2023 are licensed under the MIT License
All code and contributions from 2023 onwards are licensed under the GNU Affero General Public License v3.0 (AGPL-3.0)

MIT License (Pre-2023)
Copyright (c) 2015 Kris Fields.
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

GNU Affero General Public License v3.0 (Post-2023)
All contributions made after 2023 are licensed under the GNU Affero General Public License v3.0.
The full text of this license can be found in the AGPL-3.0.txt file or at:
https://www.gnu.org/licenses/agpl-3.0.en.html
Contribution Guidelines

All new contributions must be licensed under AGPL-3.0
Contributors acknowledge and agree that their contributions will be licensed under AGPL-3.0
The MIT license remains in effect for all code committed prior to 2023