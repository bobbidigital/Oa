from bullhorn.models import Category


def process_form(request, form_type):
    categories = Category.objects.all()
    if request.POST:
        form = form_type(request.POST)
        if form.is_valid():
            form.save()
            empty_form = form_type()
            template_variables = {'form': empty_form,
                                  'categories': categories,
                                  'success_message':
                                  'Record successfully created'}
        else:
            template_variables = {'form': form,
                                  'categories': categories}
    else:
        form = form_type()
        template_variables = {'form': form, 'categories': categories}
    return template_variables
