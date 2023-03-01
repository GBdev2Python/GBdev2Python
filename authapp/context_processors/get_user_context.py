from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Count, F

from authapp.models import CustomUser


def get_user_data(request: WSGIRequest):
    user = request.user
    if not user.is_anonymous:
        if user.is_company:
            user_query = CustomUser.objects.filter(id=user.pk)\
                .select_related('employer')\
                .annotate(
                    empl=Count("employer__id", distinct=True),
                    ttl_vac=Count('employer__vacancies__id'),
                    employer_id=F('employer__id'),
            ).only("username", "is_company", "is_staff", "is_active", "employer__id")\
                .first()
        else:
            user_query = CustomUser.objects.filter(pk=user.pk)\
                .select_related("applicants")\
                .annotate(
                    ttl_res=Count('applicants__resumes__id'),
                    appl=Count('applicants__id', distinct=True),
                    applicant_id=F('applicants__id'),
            )\
                .only('username', 'is_company', 'is_staff', 'is_active', 'applicants__id')\
                .first()
        return {'user_query': user_query}
    return {"user_query": False}
