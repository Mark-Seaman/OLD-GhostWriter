from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, RedirectView, UpdateView

from probe.models import TestResult, Probe
from probe.probe import accept_results, approve_result, clear_probe_history, execute_probe, list_tests, reset_tests, \
    result_list, run_tests


class TestClearView(RedirectView):

    def get_redirect_url(self, **kwargs):
        pk = self.kwargs.get('pk')
        clear_probe_history(pk)
        return reverse('test_detail', args=[pk])


class TestResetView(RedirectView):

    def get_redirect_url(self, **kwargs):
        reset_tests()
        run_tests()
        return reverse('test_list')


class TestRunAllView(RedirectView):

    def get_redirect_url(self, **kwargs):
        run_tests()
        return reverse('test_list')


class TestLikeView(RedirectView):

    def get_redirect_url(self, **kwargs):
        accept_results()
        return reverse('test_list')


class TestView(RedirectView):
    url = reverse_lazy('test_list')


class TestApproveView(RedirectView):

    def get_redirect_url(self, **kwargs):
        pk = self.kwargs.get('pk')
        result = TestResult.objects.get(pk=pk)
        approve_result(result)
        return reverse('test_detail', args=[result.probe.pk])


class TestListView(ListView):
    template_name = 'test_list.html'
    model = Probe

    def get_context_data(self, **kwargs):
        return list_tests()


class TestDetailView(DetailView):
    template_name = 'test_detail.html'
    model = Probe

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        probe = kwargs['object']
        # execute_probe(probe)
        kwargs['results'] = result_list(probe)
        return kwargs


class TestResultView(DetailView):
    template_name = 'test_result.html'
    model = TestResult


class TestCreateView(LoginRequiredMixin, CreateView):
    template_name = "test_add.html"
    model = Probe
    fields = '__all__'

    def form_valid(self, form):
        form.instance.author_id = 1
        return super().form_valid(form)



class TestRunView(RedirectView):

    def get_redirect_url(self, **kwargs):
        pk = self.kwargs.get('pk')
        if pk == 0:
            for probe in Probe.objects.all():
                execute_probe(probe)
            return reverse('test_list')
        else:
            probe = Probe.objects.get(pk=pk)
            execute_probe(probe)
            return reverse('test_detail', args=[pk])


class TestUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "test_edit.html"
    model = Probe
    fields = '__all__'


class TestDeleteView(LoginRequiredMixin, DeleteView):
    model = Probe
    template_name = 'test_delete.html'
    success_url = reverse_lazy('test_list')
