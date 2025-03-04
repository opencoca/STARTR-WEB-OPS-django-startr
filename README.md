# Django Startr Code

Django Startr is here to turbocharge your project setup! With just a few commands, it auto-generates everything you need. Django Startr is a powerful tool that eliminates boilerplate code by automatically generating complete CRUD functionality for your Django models. With a single command, it creates:

- Class-based views (List, Detail, Create, Update, Delete)
- Forms for your models
- URL configurations
- Admin interfaces
- Templates with a clean, customizable design

## ⚡ Quick Start

### Installation

Choose one of these installation methods:

```bash
# Using pip
pip install django-startr

# Using git submodule (recommended for customization)
git submodule add https://github.com/Startr/STARTR-django-code.git our_submodules/STARTR-django-code
ln -s our_submodules/STARTR-django-code/django_startr django_startr
```

Add to your `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'django_startr',
    # ...
]
```

### Basic Usage

1. Create your Django app and define your models:

```bash
python manage.py startapp store
```

2. Define your models in `store/models.py`:

```python
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
```

3. Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

4. Generate CRUD functionality:

```bash
python manage.py startr store
```

5. Add to your project's `urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    # ...
    path('store/', include('store.urls')),
    # ...
]
```

That's it! You now have a fully functional admin interface and CRUD views for your models!

## 🔍 Detailed Usage

### Selective Generation

You can specify which models to generate for:

```bash
# Generate for specific models only
python manage.py startr store:Product,Category

# Generate for multiple apps
python manage.py startr store:Product inventory:Item,Warehouse
```

### URL Structure

Django Startr creates intuitive URL patterns:

```
# List view
/store/product/
# Detail view
/store/product/1/
# Create view
/store/product/create/
# Update view
/store/product/1/update/
# Delete view
/store/product/1/delete/
```

For shorter URLs, you can import specific URL modules:

```python
# In your project's urls.py
path('products/', include('store.urls.product_urls')),
```

This gives you cleaner URLs like `/products/` instead of `/store/product/`.

## 🛠️ Customization

### Views

Django Startr creates views in a `views` directory, with a separate file for each model:

```
store/
├── views/
│   ├── __init__.py
│   ├── product_views.py
│   └── category_views.py
```

Each view file contains class-based views with all common methods stubbed out for easy overriding:

```python
# Example of a generated ProductListView
class ProductListView(ListView):
    model = Product
    template_name = "store/product_list.html"
    paginate_by = 20
    context_object_name = "product_list"
    
    def get_queryset(self):
        # Override this method to customize your queryset
        return super().get_queryset()
        
    def get_context_data(self, **kwargs):
        # Override this method to add extra context
        return super().get_context_data(**kwargs)
```

### Templates

Generated templates extend a model-specific base template, which in turn extends your project's `base.html`:

```
templates/
├── base.html                  # Your project's base template
└── store/
    ├── product_base.html      # Base template for product
    ├── product_list.html
    ├── product_detail.html
    ├── product_form.html
    └── product_confirm_delete.html
```

This hierarchical approach makes it easy to customize templates at different levels.

### Admin Interface

Django Startr creates an intelligent ModelAdmin for each model with:

- Sensible defaults for `list_display` based on your model fields
- Smart `list_filter` setup for appropriate field types
- Automatic `search_fields` for text fields
- Performance optimizations with `list_select_related`

Example generated admin:

```python
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')
    search_fields = ('name', 'description')
    list_filter = ('price',)
```

## 📋 Best Practices

### Project Structure

For large projects, consider organizing your code as follows:

```
myproject/
├── apps/                      # Your Django apps
│   ├── store/
│   └── inventory/
├── our_submodules/            # Git submodules
│   └── STARTR-django-code/
├── django_startr -> our_submodules/STARTR-django-code/django_startr
├── templates/                 # Project-wide templates
│   └── base.html
└── manage.py
```

### Customization Flow

1. Generate the initial code
2. Customize views for specific business logic
3. Enhance templates with your design
4. Extend the admin interface for advanced features

### Regeneration

When adding new models, you can safely regenerate code:

1. Back up any customized files
2. Run `python manage.py startr your_app:NewModel`
3. Merge your customizations back in

## 🚀 Planned Features

1. **Change Detection**: Automatically detect model changes and update generated code while preserving customizations
2. **Test Generation**: Create basic unit and integration tests for models and views
3. **API Integration**: Generate Django REST Framework serializers and viewsets
4. **Documentation**: Generate Swagger/OpenAPI documentation for your models
5. **Form Enhancement**: Add support for crispy-forms and more advanced form layouts
6. **Theming System**: Provide multiple template themes with easy switching
7. **Admin Customization**: More advanced admin features like filters, actions, and inline forms
8. **Internationalization**: Better i18n support in generated templates

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch: `git checkout -b new-feature`
3. Commit your changes: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin new-feature`
5. Submit a pull request

## 📜 License

Copyright 2023-2025 12787326 Canada Inc.

Django Startr is dual-licensed:
- Pre-2023 code: MIT License
- Post-2023 code: AGPLv3

See [LICENSE.md](LICENSE.md) for full details.

