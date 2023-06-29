
from django.urls import path

from probe.views_probe import (TestApproveView, TestClearView, TestCreateView, TestDeleteView, TestDetailView,
                               TestLikeView, TestListView, TestResetView, TestResultView, TestRunAllView, TestRunView,
                               TestUpdateView)

urlpatterns = [

    # Test
    path('',                       TestListView.as_view(),      name='test_list'),
    path('<int:pk>',               TestDetailView.as_view(),    name='test_detail'),
    path('add',                    TestCreateView.as_view(),    name='test_add'),
    path('<int:pk>/',              TestUpdateView.as_view(),    name='test_edit'),
    path('<int:pk>/delete',        TestDeleteView.as_view(),    name='test_delete'),

    # Results
    path('<int:pk>/result',        TestResultView.as_view(),    name='test_result'),
    path('<int:pk>/run',           TestRunView.as_view(),       name='test_run'),
    path('<int:pk>/approve',       TestApproveView.as_view(),   name='test_approve'),
    path('<int:pk>/clear',         TestClearView.as_view(),     name='test_clear'),

    # All Tests
    path('reset',                  TestResetView.as_view(),     name='test_reset'),
    path('run',                    TestRunAllView.as_view(),    name='test_run_all'),
    path('like',                   TestLikeView.as_view(),      name='test_like'),

]
