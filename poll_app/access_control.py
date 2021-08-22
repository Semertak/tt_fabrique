from poll_app.models import Users


def is_request_by_admin(request):
    """
    Обладает ли отправивший запрас правами админа
    Предполагается, что все пользователя анонимные и токены есть только у админов.

    :return: bool
    """
    token = request.headers.get('Handmade-Token', None)
    return Users.objects.filter(token=token).exists()
