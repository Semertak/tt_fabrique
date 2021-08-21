from django.contrib.auth.decorators import user_passes_test

with_admin_token = user_passes_test(lambda user: user.is_active)


def admin_role_required(view_func):
    decorated_view_func = with_admin_token(view_func)
    return decorated_view_func
