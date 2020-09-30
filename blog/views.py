from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, JobApplication
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from django.urls import reverse

# Create your views here.


def home(request):
    
    context = {
        'posts': Post.objects.all()
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
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

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

def job_apply(request, pk):
    if request.method=="POST" and request.FILES['myfile']:

        myfile = request.FILES['myfile']
        # fs = FileSystemStorage()
        # filename = fs.save(myfile.name, myfile)
        # uploaded_file_url = fs.url(filename)

        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        work_experience = request.POST.get("wexperience")
        user = request.user
        post = Post.objects.filter(pk=pk).first()

        apply_job = JobApplication(name=name, email=email, phone=phone, work_experience=work_experience, user=user, post=post, resume= myfile)
        apply_job.save()
        messages.success(request, "Your application has been posted successfully!!")

    return render(request, 'blog/job_apply.html',)

def job_search(request):
    query = request.GET['query']
    
    if len(query)>70:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)

        paginator = Paginator(allPosts, 25) 

    if allPosts.count() == 0:
        messages.warning(request, "No search results found. Please search valid content.")    
    context = {'allPosts': allPosts}

    return render(request, 'blog/search.html', context)

def job_dashboard(request, pk):
    post = Post.objects.filter(pk=pk).first()
    job_applicant = JobApplication.objects.filter(post=post)
    
    total_applicants = job_applicant.count()
    # print(total_applicants)

    context = {'job_applicant': job_applicant,
                'total_applicants': total_applicants
                }
    return render(request, 'blog/dashboard.html', context)


def applicant_detail(request, pk, sno):
    post = Post.objects.filter(pk=pk).first()
    job_applicant = JobApplication.objects.filter(post=post)

    applicant_detail = JobApplication.objects.filter(sno=sno).first()
    # print(applicant_detail)
    # print(applicant_detail.name)
    # print(applicant_detail.email)

    context = {
        'applicant_detail': applicant_detail
    }

    return render(request, 'blog/applicant_detail.html', context)


def job_applicant_delete(request, pk, sno):

    if request.method == 'POST':
        post = Post.objects.filter(pk=pk).first()
        

        applicant = JobApplication.objects.filter(sno=sno).first()
        applicant.delete()
        messages.success(request, "Applicant successfully deleted.")
        job_applicant = JobApplication.objects.filter(post=post)
    
        total_applicants = job_applicant.count()


        context = {'job_applicant': job_applicant,
                'total_applicants': total_applicants
                }
        return render(request, 'blog/dashboard.html', context)

    else:
        return render(request, 'blog/application_confirm_delete.html')

    return render(request, 'blog/dashboard.html', context)

