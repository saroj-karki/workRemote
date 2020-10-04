from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Post, JobApplication
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.urls import reverse
from bootstrap_datepicker_plus import DatePickerInput
from .forms import JobApplyForm
from django.utils.encoding import uri_to_iri



# Create your views here.


def home(request):

    
    context = {
        'posts': Post.objects.all(),
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'end_date']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_form(self):
        form = super().get_form()
        form.fields['end_date'].widget = DatePickerInput()
        return form

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


class JobApplyView(LoginRequiredMixin, CreateView):
    model = JobApplication
    
    template_name = 'blog/job_apply.html'
    form_class = JobApplyForm

    def form_valid(self, form):
        form.instance.user = self.request.user
    
        post = Post.objects.get(pk=self.kwargs['pk'])
        form.instance.post = post
        # form.save()
        super().form_valid(form)
        messages.success(self.request, "Job application submitted successfully!")
        return redirect(reverse('post-detail', kwargs={
            'pk': form.instance.post.pk
        }))
   

class JobSearchView(ListView):
    template_name = 'blog/search.html'
    model = Post
    context_object_name = 'allPosts'

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            if len(query)>70:
                allPosts = Post.objects.none()
                messages.warning(self.request, "No search results found. Please search valid content.")
            else:
                allPostsTitle = self.model.objects.filter(title__icontains=query)
                allPostsContent = self.model.objects.filter(content__icontains=query)
                allPosts = allPostsTitle.union(allPostsContent)
                if allPosts.count() == 0:
                    messages.warning(self.request, "No search results found. Please search valid content.")
        else:
            allPosts = self.model.objects.none()
        return allPosts


class DashboardView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'blog/job_apply.html'

    def get(self, request, **kwargs):
        
        post = Post.objects.get(pk=self.kwargs['pk'])
        job_applicants = JobApplication.objects.filter(post=post)
    
        total_applicants = job_applicants.count()

        pending_count = JobApplication.objects.filter(post=post, status='pending').count()
        approved_count = JobApplication.objects.filter(post=post, status='approved').count()

        context = { 'job_applicant': job_applicants,
                    'total_applicants': total_applicants,
                    'pending_count': pending_count,
                    'approved_count': approved_count
                    }
        return render(request, 'blog/dashboard.html', context)

    def test_func(self):
        post = Post.objects.get(pk=self.kwargs['pk'])
        if self.request.user == post.author:
            return True
        return False

class ApplicantDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = JobApplication
    template_name = 'blog/applicant_detail.html'
    context_object_name = 'applicant_detail'

    def get_object(self, **kwargs):
        sno = self.kwargs.get('sno')
        return get_object_or_404(JobApplication, sno=sno)

    def test_func(self):
        # post = self.kwargs.get('post')
        post = Post.objects.get(pk=self.kwargs['pk'])
        if self.request.user == post.author:
            return True
        return False


def job_applicant_delete(request, pk, sno):

    if request.method == 'POST':
        post = Post.objects.filter(pk=pk).first()
        

        applicant = JobApplication.objects.filter(sno=sno).first()
        applicant.delete()
        messages.success(request, "Applicant successfully deleted.")
        job_applicant = JobApplication.objects.filter(post=post)
    
        total_applicants = job_applicant.count()
        pending_count = JobApplication.objects.filter(post=post, status='pending').count()
        approved_count = JobApplication.objects.filter(post=post, status='approved').count()


        context = {'job_applicant': job_applicant,
                    'total_applicants': total_applicants,
                    'pending_count': pending_count,
                    'approved_count': approved_count
                }
        return render(request, 'blog/dashboard.html', context)

    else:
        return render(request, 'blog/application_confirm_delete.html')

    return render(request, 'blog/dashboard.html', context)


def job_applicant_approve(request, pk, sno):

    if request.method == 'POST':
        post = Post.objects.filter(pk=pk).first()
        
        applicant = JobApplication.objects.filter(sno=sno).update(status='approved')
        # applicant.update(status='approved')
        messages.success(request, "Applicant approved successfully.")

        job_applicant = JobApplication.objects.filter(post=post)
    
        total_applicants = job_applicant.count()
        pending_count = JobApplication.objects.filter(post=post, status='pending').count()
        approved_count = JobApplication.objects.filter(post=post, status='approved').count()



        context = {'job_applicant': job_applicant,
                    'total_applicants': total_applicants,
                    'pending_count': pending_count,
                    'approved_count': approved_count
                }
        return render(request, 'blog/dashboard.html', context)

    else:
        return render(request, 'blog/application_approve.html')

    return render(request, 'blog/dashboard.html', context)


