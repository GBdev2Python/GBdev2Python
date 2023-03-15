import re
from collections import defaultdict
from typing import Union

from applicantapp.models import Experience, Resumes


def validate_experience_subform(post_request: dict, return_list: bool = True) -> Union[list, dict]:
    form_data = defaultdict(lambda: [0, 0])
    re_number = re.compile('(form-)|(-company)|(-description)')

    for k, v in post_request.items():
        if k.startswith('form-') and 'id' not in k:
            form_order_number = int(re_number.sub('', k))
            form_data[form_order_number][k.endswith('description')] = v

    if return_list:
        return [form_data.get(k) for k in form_data if form_data.get(k)[0]]

    return {k: form_data.get(k) for k in form_data if form_data.get(k)[0]}


def save_experience_data(valid_fields_data: list, resume: Resumes):
    experience_objects = []

    for company, description in valid_fields_data:
        experience_objects.append(Experience(resume=resume, company=company, description=description))

    return len(Experience.objects.bulk_create(experience_objects))


def update_experience_data(post_request: dict, resume: Resumes) -> dict:
    experiences = Experience.objects.filter(resume=resume).order_by('id')

    valid_data = validate_experience_subform(post_request=post_request, return_list=False)
    update_objects = []
    created, deleted, updated = 0, 0, 0

    for idx, exp in enumerate(experiences):
        dict_object = valid_data.pop(idx, None)
        if dict_object is not None:
            exp.company = dict_object[0]
            exp.description = dict_object[1]
            update_objects.append(exp)
        else:
            exp.delete()
            deleted += 1

    updated = Experience.objects.bulk_update(update_objects, fields=['company', 'description'])
    if valid_data:
        created = save_experience_data(list(valid_data.values()), resume=resume)

    return {"c": created, "u": updated, "d": deleted}
