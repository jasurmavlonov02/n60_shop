from django.shortcuts import redirect


def require_email(strategy, details, user=None, *args, **kwargs):
    email = details.get('email')

    if not email:
        return redirect('users:email_required')  # Email so‘rash uchun maxsus sahifa
    return {'email': email}
