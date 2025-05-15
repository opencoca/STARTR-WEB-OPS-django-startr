from django.http import HttpResponse, JsonResponse
from django.contrib.admin.sites import site
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import user_passes_test
from django.template.response import TemplateResponse
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
import json

@csrf_protect
@user_passes_test(lambda u: u.is_staff)
def load_lazy_inline(request, app_label, model_name, object_id):
    """
    View to handle AJAX requests for loading inline content dynamically.
    
    This view renders just the inline part of the admin form and returns it
    as an HTML response that can be inserted into the DOM.
    """
    import logging
    logger = logging.getLogger('django')
    
    logger.debug(f"Lazy inline request for {app_label}.{model_name} (object_id: {object_id})")
    
    if request.method != 'POST':
        logger.warning(f"Non-POST request to lazy_inline: {request.method}")
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    
    # Get the model class and admin instance
    try:
        model_class = apps.get_model(app_label, model_name)
        admin_instance = site._registry.get(model_class)
        
        if not admin_instance:
            logger.error(f"No admin registered for {app_label}.{model_name}")
            return JsonResponse({'error': f'No admin registered for {app_label}.{model_name}'}, status=404)
    except LookupError:
        logger.error(f"Model {app_label}.{model_name} not found")
        return JsonResponse({'error': f'Model {app_label}.{model_name} not found'}, status=404)
    
    # Log some info about what we found
    logger.debug(f"Found model: {model_class.__name__}, admin: {admin_instance.__class__.__name__}")
    
    # Get the parent object
    try:
        parent_obj = get_object_or_404(model_class, pk=object_id)
        logger.debug(f"Found parent object: {parent_obj}")
    except Exception as e:
        logger.error(f"Error getting parent object: {str(e)}")
        return JsonResponse({'error': f'Error getting parent object: {str(e)}'}, status=404)
    
    # Check permissions
    if not admin_instance.has_change_permission(request, parent_obj):
        logger.warning(f"Permission denied for user {request.user} on {parent_obj}")
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    # Get the inline type from the request
    inline_type = request.POST.get('inline_type')
    logger.debug(f"Requested inline type: {inline_type}")
    
    # Find the correct inline instance
    inline_instance = None
    for inline in admin_instance.get_inline_instances(request, parent_obj):
        # Use a safe comparison with class_name or get class name directly
        inline_class_name = getattr(inline, 'class_name', inline.__class__.__name__)
        if inline_class_name.lower() == inline_type.lower():
            inline_instance = inline
            logger.debug(f"Found inline instance: {inline_instance}")
            break
    
    if not inline_instance:
        logger.error(f"Inline {inline_type} not found")
        return JsonResponse({'error': f'Inline {inline_type} not found'}, status=404)
    
    # Create a context that mimics the admin change form context
    admin_form = admin_instance.get_form(request, parent_obj)(instance=parent_obj)
    
    # Get a formset factory for just this inline
    formset_factory = inline_instance.get_formset(request, parent_obj)
    
    # Create the formset instance
    inline_formset = formset_factory(instance=parent_obj, prefix=inline_instance.get_formset_kwargs(request)['prefix'])
    
    # Create the context for the inline template
    context = {
        'inline_admin_formset': inline_instance.get_formset_kwargs(request)['formset'](instance=parent_obj),
        'original': parent_obj,
        'add': False,
        'change': True,
        'has_add_permission': inline_instance.has_add_permission(request, parent_obj),
        'has_change_permission': inline_instance.has_change_permission(request, parent_obj),
        'has_delete_permission': inline_instance.has_delete_permission(request, parent_obj),
        'has_view_permission': inline_instance.has_view_permission(request, parent_obj),
        'form_url': '',
        'opts': model_class._meta,
        'content_type_id': ContentType.objects.get_for_model(model_class).id,
        'save_as': False,
        'save_on_top': False,
        'is_popup': False,
        'app_label': app_label,
    }
    
    # Render just the inline form part
    response = TemplateResponse(
        request,
        inline_instance.template,
        context
    )
    
    return HttpResponse(response.rendered_content)
