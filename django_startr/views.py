# core/views.py

from django.conf import settings
from django.apps import apps
from django.http import HttpResponseNotFound, HttpResponseForbidden
from django.urls import get_resolver, URLPattern, URLResolver
from django.template.loader import render_to_string
import re
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms

# Registration form with additional fields
class UserRegistrationForm(UserCreationForm):
    """Form for user registration."""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

def register_view(request):
    """View for registering a new user"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
        
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Your account has been created successfully! You can now log in.")
            return redirect('login')
    else:
        form = UserRegistrationForm()
        
    return render(request, 'registration/register.html', {'form': form})

def debug_index(request, exception=None):
    """
    A custom debug view to replace Django's default 404 debug page.
    It examines the current URL, finds the URL node that matched,
    then lists the direct sub-URLs (grouped by app and sorted).
    """
    # Only show this in DEBUG mode
    if not settings.DEBUG:
        return HttpResponseNotFound("<h1>404 – Not Found</h1>")
    
    current_path = request.path  # e.g. "/foo/bar/unknown/"
    # Ensure the path ends with a slash (as most URL patterns do)
    base_path = current_path if current_path.endswith('/') else current_path + '/'

    # Get the root URL resolver and start with the top-level patterns
    resolver = get_resolver()
    patterns = resolver.url_patterns

    # Break the current path into segments (ignoring empty segments)
    segments = [seg for seg in base_path.strip("/").split("/") if seg]
    matched_patterns = patterns
    prefix_matched_count = 0

    # Walk through the URL segments, descending into includes as needed.
    for i, seg in enumerate(segments):
        found = False
        for pattern in matched_patterns:
            if isinstance(pattern, URLResolver):
                # Check if this include's prefix (as a regex or route) matches the segment.
                regex = getattr(pattern.pattern, "regex", None)
                if regex and regex.match(seg + "/"):
                    matched_patterns = pattern.url_patterns
                    prefix_matched_count = i + 1
                    found = True
                    break
            elif isinstance(pattern, URLPattern):
                regex = getattr(pattern.pattern, "regex", None)
                if regex and regex.match(seg + "/"):
                    prefix_matched_count = i + 1
                    # If this pattern is a final view and there are still segments left,
                    # then we've reached a dead end.
                    if i < len(segments) - 1:
                        found = False
                    else:
                        matched_patterns = []  # no further patterns under a final view
                        found = True
                    break
        if not found:
            break

    # Reconstruct the base prefix (the portion of the URL that was successfully matched)
    base_prefix_segments = segments[:prefix_matched_count]
    base_prefix = "/" + "/".join(base_prefix_segments) + ("/" if base_prefix_segments else "")

    # At this point, `matched_patterns` is the list of URL patterns at the level
    # where the requested URL did not match any further.
    subpatterns = matched_patterns

    # Collect direct child URL fragments
    sub_urls = []
    for pat in subpatterns:
        if isinstance(pat, URLResolver):
            # For an include, the pattern string is the prefix (e.g. "blog/").
            fragment = str(pat.pattern)
        elif isinstance(pat, URLPattern):
            fragment = str(pat.pattern)
        else:
            continue
        # Remove regex anchors if present
        fragment = fragment.lstrip("^").rstrip("$")
        # Only consider direct children (i.e. no additional '/')
        if "/" not in fragment.strip("/"):
            sub_urls.append((pat, fragment))

    # Group sub-URLs by the app they belong to.
    grouped = {}
    for pat, fragment in sub_urls:
        if isinstance(pat, URLPattern):
            view_func = pat.callback
            module_name = view_func.__module__  # e.g. "myapp.views"
        else:  # URLResolver
            urlconf = pat.urlconf_module
            if isinstance(urlconf, list):
                # If urlconf_module is a list, use a default/fallback name.
                module_name = "Included URLConf (list)"
            else:
                module_name = getattr(urlconf, '__name__', "unknown")
        # Try to match the module name to an installed app.
        app_label = None
        for app in apps.get_app_configs():
            if module_name.startswith(app.name):
                app_label = app.verbose_name or app.label
                break
        if app_label is None:
            app_label = "Other"
        grouped.setdefault(app_label, []).append(fragment)

    # Sort groups and URLs alphabetically.
    sorted_grouped = {
        app: sorted(urls) for app, urls in sorted(grouped.items(), key=lambda x: x[0].lower())
    }

    # Render our custom technical 404 template.
    context = {
        "request_path": current_path,
        "base_path": base_prefix,
        "grouped_urls": sorted_grouped,
    }
    html = render_to_string("technical_404.html", context, request=request)
    return HttpResponseNotFound(html)

def debug_permission_denied(request, exception=None):
    """
    A custom debug view to replace Django's default 403 debug page.
    Provides a more user-friendly permission denied message with helpful actions.
    """
    # Only show this in DEBUG mode
    if not settings.DEBUG:
        return HttpResponseForbidden("<h1>403 – Permission Denied</h1>")
    
    # Render our custom technical 403 template
    html = render_to_string("technical_403.html", {}, request=request)
    return HttpResponseForbidden(html)
