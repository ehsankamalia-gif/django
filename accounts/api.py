import json
from functools import wraps

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from .models import User
from .permissions import assignable_permissions


def staff_permission_required_json(perm):
    """Requires is_staff AND the given permission; returns JSON 401/403 instead of redirecting."""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return JsonResponse({'detail': 'Authentication required.'}, status=401)
            if not (request.user.is_staff and request.user.has_perm(perm)):
                return JsonResponse({'detail': 'Permission denied.'}, status=403)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def superuser_required_json(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'detail': 'Authentication required.'}, status=401)
        if not request.user.is_superuser:
            return JsonResponse({'detail': 'Permission denied.'}, status=403)
        return view_func(request, *args, **kwargs)
    return wrapper


def _serialize_user(user):
    return {
        'id': user.id,
        'phone_number': user.phone_number,
        'full_name': user.full_name,
        'role': user.role,
        'is_active': user.is_active,
    }


def _serialize_permission(permission):
    return {
        'id': permission.id,
        'label': permission.name,
        'codename': permission.codename,
        'app_label': permission.content_type.app_label,
        'model': permission.content_type.model,
    }


@staff_permission_required_json('accounts.view_user')
@require_http_methods(['GET'])
def user_list(request):
    users = User.objects.filter(is_superuser=False).order_by('phone_number')
    return JsonResponse({'users': [_serialize_user(u) for u in users]})


@superuser_required_json
@require_http_methods(['GET', 'POST'])
def user_permissions(request, pk):
    target = get_object_or_404(User, pk=pk, is_superuser=False)
    available = assignable_permissions()

    if request.method == 'POST':
        payload = json.loads(request.body or '{}')
        requested_ids = {int(i) for i in payload.get('permission_ids', [])}
        valid_ids = set(available.values_list('id', flat=True))
        target.user_permissions.set(requested_ids & valid_ids)
        return JsonResponse({'status': 'ok'})

    assigned_ids = list(target.user_permissions.values_list('id', flat=True))
    return JsonResponse({
        'available': [_serialize_permission(p) for p in available],
        'assigned_ids': assigned_ids,
    })


@superuser_required_json
@require_http_methods(['POST'])
def user_role(request, pk):
    target = get_object_or_404(User, pk=pk, is_superuser=False)
    payload = json.loads(request.body or '{}')
    target.is_staff = bool(payload.get('is_staff'))
    if not target.is_staff:
        target.user_permissions.clear()
    target.save(update_fields=['is_staff'])
    return JsonResponse({'status': 'ok', 'user': _serialize_user(target)})
