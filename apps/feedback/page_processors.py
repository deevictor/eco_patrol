from mezzanine.pages.page_processors import processor_for

from .forms import FeedbackForm


@processor_for('contacts')
def contacts(request, page):
    """Отображает страницу контактов

        Контексты:
        form (object): форма для отправки сообщений пользователями
        flag (bool):  если True то форма на странице не показывается
        """
    form = FeedbackForm()
    flag = False

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            flag = True

    return{
        'form': form,
        'flag': flag
    }
