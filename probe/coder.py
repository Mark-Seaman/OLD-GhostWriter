from publish.files import read_file, write_file


models = '''
class Professor(models.Model):
    address = models.TextField(null=True, verbose_name=_("Address"))
    phone = models.CharField(max_length=100, null=True, verbose_name=_("Phone"))

    def get_fields(self):
        return [(field.verbose_name, getattr(self, field.name)) for field in self._meta.fields]

    def detail_link(self):
        return button_html(f'/professor/{self.pk}', 'View Record')

    def delete_link(self):
        return button_html(f'/professor/{self.pk}/delete', 'Delete Record')

    def edit_link(self):
        return button_html(f'/professor/{self.pk}/', 'Edit Record')

    @classmethod
    def get_model_label(cls):
        return cls._meta.verbose_name_plural

    class Meta:
        verbose_name = _("Professor")
        verbose_name_plural = _("Professors")

'''


urls = '''
from .views_professor import (
    ProfessorListView,
    ProfessorDetailView,
    ProfessorCreateView,
    ProfessorUpdateView,
    ProfessorDeleteView,
)

    # Professor
    path('professor/',                    ProfessorListView.as_view(),   name='professor_list'),
    path('professor/<int:pk>',            ProfessorDetailView.as_view(), name='professor_detail'),
    path('professor/add',                 ProfessorCreateView.as_view(), name='professor_add'),
    path('professor/<int:pk>/',           ProfessorUpdateView.as_view(), name='professor_edit'),
    path('professor/<int:pk>/delete',     ProfessorDeleteView.as_view(), name='professor_delete'),

'''

views = '''
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from .models import Professor, button_html


class ProfessorListView(ListView):
    model = Professor
    template_name = 'list.html'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        model_label = self.model.get_model_label()
        data = {
            'title': f'List of {model_label}',
            'add_button': button_html("/professor/add", f'Add {model_label}'),
            'list_button': button_html('/professor/', f'{model_label} List'),
        }
        kwargs.update(data)
        return kwargs


class ProfessorDetailView(DetailView):
    model = Professor
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        model_label = self.model.get_model_label()
        data = {
            'title': f'{model_label} details',
            'edit_button': button_html(f"/professor/{self.get_object().pk}/", f'Edit Record' ),
            'list_button': button_html('/professor/', f'{model_label} List'),
        }
        kwargs.update(data)
        return kwargs


class ProfessorUpdateView(UpdateView):
    model = Professor
    template_name = 'edit.html'
    fields = '__all__'
    success_url = reverse_lazy('professor_list')  

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        model_label = self.model.get_model_label()
        object = self.get_object()
        data = dict(title=f'Edit {model_label}', 
                    view_button=object.detail_link(),
                    delete_button=object.delete_link(),
                    list_button=button_html('/professor/', f'{model_label} List'))
        kwargs.update(data)
        return kwargs


class ProfessorCreateView(CreateView):
    model = Professor
    template_name = 'add.html'
    fields = '__all__'
    success_url = reverse_lazy('professor_list') 

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        model_label = self.model.get_model_label()
        data = {
            'title': f'Add {model_label}',
            'list_button': button_html('/professor/', f'{model_label} List'),
        }
        kwargs.update(data)
        return kwargs

class ProfessorDeleteView(DeleteView):
    model = Professor
    template_name = 'delete.html'
    success_url = reverse_lazy('professor_list') 

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        model_label = self.model.get_model_label()
        data = {
            'title': f'Delete {model_label}',
            'list_button': button_html('/professor/', f'{model_label} List'),
        }
        kwargs.update(data)
        return kwargs


'''


def coder():
    print('Code Generator')

    f1 = '/Users/seaman/Github/ProMETA/register/views_professor.py'
    f2 = '/Users/seaman/Github/ProMETA/register/views_section.py'
    # text = transform(read_file(f1))

    transform(urls)
    transform(models)
    text = transform(views)
    write_file(f2, text)


def transform(text):
    subs = (('Professor', 'Campus'), ('professor', 'campus'))
    subs = (('Professor', 'Course'), ('professor', 'course'))
    subs = (('Professor', 'CourseSection'), ('professor', 'section'))
    for s in subs:
        text = text.replace(s[0], s[1])
    print(text)
    return text
    
