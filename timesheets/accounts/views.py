from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm, EditProfileForm, UpdateProfileForm, TimecardForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic
from django.views.generic import View
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserChangeForm
from .models import Timecard, UserProfile
from django.urls import reverse_lazy
from django.db.models import Q, Sum
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
import xlwt

def email_check(user):
    return user.email.endswith('@global.t-bird.edu')

class UserFormView(View):
    form_class = UserForm
    template_name = 'accounts/registration.html'

    #display form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    #add user
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('accounts:profile')

        return render(request, self.template_name, {'form': form})

@login_required
def profile(request):
    queryset = Timecard.objects.filter(user=request.user).order_by("-date")[:5]
    args = {'user': request.user, 'object_list':queryset}
    return render(request, 'accounts/profile.html', args)

@login_required
def edit_profile(request):

    if request.method == 'POST':
        form1 = EditProfileForm(request.POST,instance=request.user)
        form2 = UpdateProfileForm(request.POST,instance=request.user.userprofile)

        if form1.is_valid() and form2.is_valid():
            username = form1.cleaned_data['username']
            email = form1.cleaned_data['email']
            bio = form2.cleaned_data['bio']
            phone = form2.cleaned_data['phone']
            position = form2.cleaned_data['position']
            department = form2.cleaned_data['department']
            form1.save()
            form2.save()
            return redirect('/profile')

        else:
            return redirect('/profile/edit')

    else:
        form1 = EditProfileForm(instance=request.user)
        form2 = UpdateProfileForm(instance=request.user.userprofile)
        args = {'form1': form1,'form2': form2 }
        return render(request, 'accounts/edit_profile.html', args)



@login_required
def timecards(request):
    queryset = Timecard.objects.filter(user=request.user)

    stuff = []
    r = []

    date_start = request.GET.get('sdate')
    date_end = request.GET.get('edate')
    search = request.GET.get('qs')

    if date_start:
        queryset = queryset.filter(
        Q(date__gte=date_start))

    if date_end:
        queryset = queryset.filter(
        Q(date__lte=date_end))

    if search:
        queryset = queryset.filter(
        Q(project__icontains=search)|
        Q(department__icontains=search)|
        Q(comments__icontains=search))

    projectList = queryset.values_list('project', flat=True)
    projectSum = queryset.aggregate(Sum('hours'))
    request.session['query_filters'] = str(queryset)

    for p in projectList:
        stuff.append(p)
        t = queryset.filter(project__icontains=p).aggregate(Sum('hours'))
        for x in t:
            r.append(t[x])

    args = {'user': request.user, "object_list": queryset, 'r':r, 'stuff':stuff,'projectList':projectList,'projectSum':projectSum,}
    return render(request, 'accounts/timecards.html', args)


class TimeCardCreate(LoginRequiredMixin, CreateView):
    model = Timecard
    form_class = TimecardForm
    template_name = 'accounts/timecard_form.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TimeCardCreate, self).form_valid(form)


class TimeCardUpdate(UpdateView):
    model = Timecard
    form_class = TimecardForm
    template_name = 'accounts/timecard_form.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Timecard, id=id_)

    def form_valid(self, form):
        return super().form_valid(form)

class TimeCardDelete(DeleteView):
    model = Timecard
    success_url = reverse_lazy('accounts:timecards')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

@login_required
def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="timesheets.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Timesheets')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'dd/mm/yyyy'

    columns = ['Date', 'Hours', 'Project', 'Department', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Timecard.objects.filter(user=request.user).values_list('date', 'hours', 'project', 'department')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num])

    wb.save(response)
    return response

@user_passes_test(email_check)
def management(request):
    args = {'user': request.user}
    return render(request, 'accounts/management.html', args)

def export_all_xls(request):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="timesheet.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Timesheets')

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        date_format = xlwt.XFStyle()
        date_format.num_format_str = 'dd/mm/yyyy'

        columns = ['Date', 'Hours', 'Project', 'Department', ]

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        rows = Timecard.objects.all().values_list('date', 'hours', 'project', 'department')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num])

        wb.save(response)
        return response
