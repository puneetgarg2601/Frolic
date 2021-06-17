from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic, View
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from . import models
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import SearchForm, CustomerRegistrationForm, BlogCreationForm, VideoCastCreationForm, PodCastCreationForm, EditProfileForm, SkillCreationForm


class Index(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        context = {
            'last_blog': models.Blog.objects.order_by('-pk').filter(publish=True)[:1],
            'skills': models.Skill.objects.all(),
            'blogs': models.Blog.objects.order_by('-pk').filter(publish=True)[1:5],
            'videocasts': models.Videocast.objects.order_by('-pk').filter(publish=True)[:4]
        }
        return render(request, self.template_name, context)


class Search(View):
    template_name = 'search.html'

    def get(self, request, *args, **kwargs):
        form = SearchForm(self.request.GET)
        if form.is_valid():
            print('valid')
            query = form.cleaned_data['query']
            context = {
                'blogs': models.Blog.objects.order_by('-pk').filter(
                    Q(title__icontains=query) | Q(content__icontains=query)
                ),
                'videocasts': models.Videocast.objects.order_by('-pk').filter(
                    Q(title__icontains=query) | Q(content__icontains=query)
                ),
                'podcasts': models.Podcast.objects.order_by('-pk').filter(
                    Q(title__icontains=query) | Q(content__icontains=query)
                )
            }
        else:
            return redirect('content:index')
        return render(request, self.template_name, context)

@method_decorator(login_required, name='dispatch')
class BlogCategoryCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = models.BlogCategory
    fields = '__all__'
    success_message = 'Blog category was created successfully'

    def get_success_url(self):
        return reverse('content:blog_category_create')


class Blog(generic.ListView):
    def get(self, request):
        blog = models.Blog.objects.order_by('-pk').filter(publish=True)
        return render(request, 'blog_archive.html', {'object_list':blog})
            

@method_decorator(login_required, name='dispatch')       
class BlogCreateView(View):
    def get(self, request):
        form = BlogCreationForm()
        return render(request, 'content/blog_form.html', {'form':form})
        
    def post(self, request):
        form = BlogCreationForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            a = title.split()
            slug = '-'.join(a)
            reg =form.save(commit=False)
            reg.user = request.user
            reg.slug = slug
            reg.save()
            form.save_m2m()
            
            messages.success(request, 'Congratulations!! Blog Added Successfully.')
        return render(request, 'content/blog_form.html', {'form':form})


class BlogArchiveByCategoryPK(generic.ListView):
    model = models.Blog
    template_name = 'blog_archive.html'

    def get_queryset(self):
        return self.model.objects.filter(category=self.kwargs['pk'])


class BlogSingle(generic.DetailView):
    model = models.Blog
    template_name = 'single.html'   

    def get_queryset(self):
        return self.model.objects.filter(Q(slug=self.kwargs['slug']) and Q(id=self.kwargs['id']))


@method_decorator(login_required, name='dispatch')
class VideocastCategoryCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = models.VideocastCategory
    fields = '__all__'
    success_message = 'Video cast category was created successfully'

    def get_success_url(self):
        return reverse('content:videocast_category_create')


class Videocast(generic.ListView):
    def get(self, request):
        video = models.Videocast.objects.order_by('-pk').filter(publish=True)
        return render(request, 'videocast_archive.html', {'object_list':video})


@method_decorator(login_required, name='dispatch')
class VideocastCreateView(View):
    def get(self, request):
        form = VideoCastCreationForm()
        return render(request, 'content/videocast_form.html', {'form':form})
        
    def post(self, request):
        form = VideoCastCreationForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            a = title.split()
            slug = '-'.join(a)
            reg =form.save(commit=False)
            reg.user = request.user
            reg.slug = slug
            reg.save()
            form.save_m2m()
            
            messages.success(request, 'Congratulations!! Video Added Successfully.')
        return render(request, 'content/videocast_form.html', {'form':form})


class VideocastArchiveByCategoryPK(generic.ListView):
    model = models.Videocast
    template_name = 'videocast_archive.html'

    def get_queryset(self):
        return self.model.objects.filter(category=self.kwargs['pk'])


class VideocastSingle(generic.DetailView):
    model = models.Videocast
    template_name = 'single.html'

    def get_queryset(self):
        return self.model.objects.filter(Q(slug=self.kwargs['slug']) and Q(id=self.kwargs['id']))


@method_decorator(login_required, name='dispatch')
class PodcastCategoryCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = models.PodcastCategory
    fields = '__all__'
    success_message = 'Podcast category was created successfully'

    def get_success_url(self):
        return reverse('content:podcast_category_create')


class Podcast(generic.ListView):
    def get(self, request):
        audio = models.Podcast.objects.order_by('-pk').filter(publish=True)
        return render(request, 'podcast_archive.html', {'object_list':audio})


@method_decorator(login_required, name='dispatch')
class PodcastCreateView(View):
    def get(self, request):
        form = PodCastCreationForm()
        return render(request, 'content/podcast_form.html', {'form':form})
        
    def post(self, request):
        form = PodCastCreationForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            a = title.split()
            slug = '-'.join(a)
            reg =form.save(commit=False)
            reg.user = request.user
            reg.slug = slug
            reg.save()
            form.save_m2m()
            
            messages.success(request, 'Congratulations!! Audio Added Successfully.')
        return render(request, 'content/podcast_form.html', {'form':form})


class PodArchiveByCategoryPK(generic.ListView):
    model = models.Podcast
    template_name = 'podcast_archive.html'

    def get_queryset(self):
        return self.model.objects.filter(category=self.kwargs['pk'])


class PodSingle(generic.DetailView):
    model = models.Podcast
    template_name = 'single.html'

    def get_queryset(self):
        return self.model.objects.filter(Q(slug=self.kwargs['slug']) and Q(id=self.kwargs['id']))


@method_decorator(login_required, name='dispatch')
class SkillCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    def get(self, request):
        form = SkillCreationForm()
        return render(request, 'content/skill_form.html', {'form':form})
        
    def post(self, request):
        form = SkillCreationForm(request.POST)
        if form.is_valid():
            reg =form.save(commit=False)
            reg.user = request.user
            reg.save()
            messages.success(request, 'Congratulations!! Skill Added Successfully.')
        return render(request, 'content/skill_form.html', {'form':form})


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'registration/customerregistration.html', {'form':form})
    
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! Registered Successfully.')
            form.save()
        return render(request, 'registration/customerregistration.html', {'form':form})

    def get_success_url(self):
        return reverse('login')

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request, id, query):
        usr = User.objects.get(pk=id)
        if query == 'blog':
            blogs = models.Blog.objects.filter(user=usr)
            return render(request, 'content/profile_blog.html', {'user':usr, 'object_list':blogs, 'blog':'active'})
        if query == 'video':
            videos = models.Videocast.objects.filter(user=usr)
            return render(request, 'content/profile_videocast.html', {'user':usr, 'object_list':videos, 'video':'active'})
        if query == 'audio':
            audios = models.Podcast.objects.filter(user=usr)
            return render(request, 'content/profile_podcast.html', {'user':usr, 'object_list':audios, 'audio':'active'})
        if query == 'skill':
            skills = models.Skill.objects.filter(user=usr)
            return render(request, 'content/profile_skill.html', {'user':usr, 'skills':skills, 'skill':'active'})

@method_decorator(login_required, name='dispatch')
class EditProfileView(View):
    def get(self, request, id):
        if request.user.id == id:
            form = EditProfileForm(instance=request.user)
            return render(request, 'content/edit_profile.html', {'form':form})

    def post(self, request, id):
        if request.user.id == id:
            form = EditProfileForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile Updated Successfully!! ')
            return render(request, 'content/edit_profile.html', {'form':form})

@method_decorator(login_required, name='dispatch')
class EditBlogView(View):
    def get(self, request, slug, id):
        blog = models.Blog.objects.get(Q(id=id) and Q(slug=slug))
        if blog.user == request.user:
            form = BlogCreationForm(instance=blog)
            return render(request, 'content/edit_blog.html', {'form':form})
        
    def post(self, request, slug, id):
        blog = models.Blog.objects.get(Q(id=id) and Q(slug=slug))
        if blog.user == request.user:
            form = BlogCreationForm(request.POST, request.FILES, instance=blog)
            if form.is_valid():
                title = form.cleaned_data['title']
                a = title.split()
                slug = '-'.join(a)
                reg =form.save(commit=False)
                reg.user = request.user
                reg.slug = slug
                reg.save()
                form.save_m2m()
                
                messages.success(request, 'Congratulations!! Blog Updated Successfully.')
            return render(request, 'content/edit_blog.html', {'form':form})

@method_decorator(login_required, name='dispatch')
class EditVideocastView(View):
    def get(self, request, slug, id):
        video = models.Videocast.objects.get(Q(id=id) and Q(slug=slug))
        if video.user == request.user:
            form = VideoCastCreationForm(instance=video)
            return render(request, 'content/edit_videocast.html', {'form':form})
        
    def post(self, request, slug, id):
        video = models.Videocast.objects.get(Q(id=id) and Q(slug=slug))
        if video.user == request.user:
            form = VideoCastCreationForm(request.POST, request.FILES, instance=video)
            if form.is_valid():
                title = form.cleaned_data['title']
                a = title.split()
                slug = '-'.join(a)
                reg =form.save(commit=False)
                reg.user = request.user
                reg.slug = slug
                reg.save()
                form.save_m2m()
                
                messages.success(request, 'Congratulations!! Videocast Updated Successfully.')
            return render(request, 'content/edit_videocast.html', {'form':form})

@method_decorator(login_required, name='dispatch')
class EditPodcastView(View):
    def get(self, request, slug, id):
        podcast = models.Podcast.objects.get(Q(id=id) and Q(slug=slug))
        if podcast.user == request.user:
            form = PodCastCreationForm(instance=podcast)
            return render(request, 'content/edit_podcast.html', {'form':form})
        
    def post(self, request, slug, id):
        podcast = models.Podcast.objects.get(Q(id=id) and Q(slug=slug))
        if podcast.user == request.user:
            form = PodCastCreationForm(request.POST, request.FILES, instance=podcast)
            if form.is_valid():
                title = form.cleaned_data['title']
                a = title.split()
                slug = '-'.join(a)
                reg =form.save(commit=False)
                reg.user = request.user
                reg.slug = slug
                reg.save()
                form.save_m2m()
                
                messages.success(request, 'Congratulations!! Podcast Updated Successfully.')
            return render(request, 'content/edit_podcast.html', {'form':form})

@method_decorator(login_required, name='dispatch')
class EditSkillView(View):
    def get(self, request, id):
        skill = models.Skill.objects.get(id=id)
        if skill.user == request.user:
            form = SkillCreationForm(instance=skill)
            return render(request, 'content/edit_skill.html', {'form':form})
        
    def post(self, request, id):
        skill = models.Skill.objects.get(id=id)
        if skill.user==request.user:
            form = SkillCreationForm(request.POST, instance=skill)
            if form.is_valid():
                reg =form.save(commit=False)
                reg.user = request.user
                reg.save()
                
                messages.success(request, 'Congratulations!! Skill Updated Successfully.')
            return render(request, 'content/edit_skill.html', {'form':form})

@method_decorator(login_required, name='dispatch')
class DeleteBlogView(View):
    def post(self, request, slug, id):
        pi = models.Blog.objects.get(Q(id=id) and Q(slug=slug))
        if pi.user == request.user:
            pi.delete()
            messages.success(request, 'Blog Deleted Successfully!!')
            return redirect('content:profile', id= request.user.id, query= 'blog')

    def get(self, request, slug, id):
        pi = models.Blog.objects.get(Q(id=id) and Q(slug=slug))
        if pi.user == request.user:
            return render(request, 'content/delete_blog.html')

@method_decorator(login_required, name='dispatch')
class DeleteVideocastView(View):
    def post(self, request, slug, id):
        pi = models.Videocast.objects.get(Q(id=id) and Q(slug=slug))
        if pi.user == request.user:
            pi.delete()
            messages.success(request, 'Videocast Deleted Successfully!!')
            return redirect('content:profile', id= request.user.id, query= 'video')

    def get(self, request, slug, id):
        pi = models.Videocast.objects.get(Q(id=id) and Q(slug=slug))
        if pi.user == request.user:
            return render(request, 'content/delete_videocast.html')

@method_decorator(login_required, name='dispatch')
class DeletePodcastView(View):
    def post(self, request, slug, id):
        pi = models.Podcast.objects.get(Q(id=id) and Q(slug=slug))
        if pi.user==request.user:
            pi.delete()
            messages.success(request, 'Podcast Deleted Successfully!!')
            return redirect('content:profile', id= request.user.id, query= 'audio')

    def get(self, request, slug, id):
        pi = models.Podcast.objects.get(Q(id=id) and Q(slug=slug))
        if pi.user == request.user:
            return render(request, 'content/delete_podcast.html')

@method_decorator(login_required, name='dispatch')
class DeleteSkillView(View):
    def post(self, request, id):
        pi = models.Skill.objects.get(id=id)
        if pi.user == request.user:
            pi.delete()
            messages.success(request, 'Skill Deleted Successfully!!')
            return redirect('content:profile', id= request.user.id, query= 'skill')

    def get(self, request, id):
        pi = models.Skill.objects.get(id=id)
        if pi.user == request.user:
            return render(request, 'content/delete_skill.html')