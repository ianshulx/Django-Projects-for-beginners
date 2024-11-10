from random import shuffle
from .models import Profile,Post,Liked_Post,Comment,Follow
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from django.contrib import auth
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def search(request):
    my_profile=Profile.objects.get(user=request.user)
    character=request.POST["username"]
    all_objects=Profile.objects.all()
    search_users=[]
    for objects in all_objects:
        if character in objects.user.username:
            search_users.append({
                'profile':objects,
                'bio':objects.bio[0:83]
            })

    return render(request,"search.html",{"my_profile":my_profile,"search_users":search_users,"caption":character})

@login_required(login_url='login')
def post(request,post_id):
    post=Post.objects.get(post_id=post_id)
    return render(request,"post.html",{"post":post,'is_liked':Liked_Post.objects.filter(Username=request.user.username,post_id=post_id).exists()})

@login_required(login_url='login')
def comment(request):
    if request.method=="POST":
        post_id=request.POST["post_id"]
        reqd_post=Post.objects.get(post_id=post_id)
        content=request.POST["content"]
        profile=Profile.objects.get(user=request.user)
        new_object= Comment.objects.create(post_id=reqd_post,content=content,author=profile)
        new_object.save()
        print("Rhino:",request.META.get('HTTP_REFERER'))
        if request.META.get('HTTP_REFERER')=='http://127.0.0.1:8000/':
            redirect_url='/'
        else:
            redirect_url=f"/post/{post_id}"

    return redirect(redirect_url)

@login_required(login_url='login')
def profile(request,username):
    current_user=User.objects.get(username=username)
    Profile_obj=Profile.objects.get(user=current_user)
    posts=Post.objects.filter(Profile=Profile_obj)
    if Follow.objects.filter(current_user=request.user,followed=Profile_obj).exists():
        value="Unfollow"
    else:
        value="Follow"
    follower_list=Follow.objects.filter(followed=Profile_obj)
    follower_profile=[]
    for follower in follower_list:
        follower_profile.append(Profile.objects.get(user=follower.current_user))
    following_list=Follow.objects.filter(current_user=current_user)
    return render(request,"profile.html",{'profile':Profile_obj,'posts':posts,'num_posts':len(posts),'follow_status':value,"follower_list":follower_profile,"following_list":following_list})

@login_required(login_url='login')
def upload(request):
    current_user=request.user
    img=request.FILES.get('image')
    caption=request.POST["Caption"]
    my_profile=Profile.objects.get(user=current_user)
    my_post=Post.objects.create(Profile=my_profile,Img=img,caption=caption)
    my_post.save()
    return redirect('/')

@login_required(login_url='login')
def settings(request):
    current_user=request.user
    my_profile=Profile.objects.get(user=current_user)
    if request.method=="POST":
        if request.FILES.get('image')==None:
            my_img=my_profile.profile_img
        else:
            my_img=request.FILES.get('image')
        new_bio=request.POST["bio"]
        new_loc=request.POST["loc"]
        my_profile.profile_img=my_img
        my_profile.bio=new_bio
        my_profile.location=new_loc
        my_profile.save()

    return render(request,"setting.html",{'my_profile':my_profile})

@login_required(login_url='login')
def index(request):
    current_user = request.user
    my_profile = Profile.objects.get(user=current_user)
    my_following=Follow.objects.filter(current_user=current_user)
    posts=[]
    for following in my_following:
        current_posts=Post.objects.filter(Profile=following.followed)
        posts.extend(current_posts)
    shuffle(posts)
    liked_posts=[]
    for post in posts:
        liked_posts.append({
            'Post':post,
            'is_liked':post.is_liked_by(current_user)
        })

    all_objects=Follow.objects.filter(followed=my_profile)
    recommendation_list=[]
    for follower in all_objects:
        profile=Profile.objects.get(user=follower.current_user)
        if not Follow.objects.filter(current_user=request.user,followed=profile).exists():
            recommendation_list.append(profile)
            
    second_list=set()
    users_following=Follow.objects.filter(current_user=request.user)
    for following in users_following:
        for new_rec in Follow.objects.filter(current_user=following.followed.user):
            second_list.add(new_rec.followed)

    final_list=list(second_list)
    really_final=[]
    print("Hippo:",len(final_list))
    for element in final_list:
        print('hi')
        if  element.user!=my_profile.user and not Follow.objects.filter(current_user=request.user,followed=element).exists():
            really_final.append(element)

    recommendation_list.extend(really_final)
    return render(request, "index.html", {'my_profile': my_profile, 'posts': liked_posts, 'reccomendation_list':recommendation_list})

def signup(request):
    if request.method=="POST":
        username=request.POST["username"]
        mail=request.POST['Email']
        pwd1=request.POST["password"]
        pwd2=request.POST["password2"]

        if pwd1!=pwd2:
            messages.info(request,"Password doesn't match")
            redirect('signup')

        else:
            if User.objects.filter(email=mail).exists():
                messages.info(request,"Sorry! Email already registered")
                return redirect ('signup')
            else:
                new_user=User.objects.create_user(username=username,email=mail,password=pwd1)
                new_user.save()

                current_user=User.objects.get(email=mail)
                new_profile=Profile.objects.create(user=current_user)
                new_profile.save()
                return redirect('login')

    return render(request,'signup.html')

def login(request):
    if request.method=="POST":
        username=request.POST["username"]
        pwd=request.POST["password"]
        user=auth.authenticate(username=username,password=pwd)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,"Invalid Credentials")
            return redirect('login')
    return render(request,'login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def Like_post(request):
    current_user=request.user
    post_id=request.GET.get('post_id')
    profile_obj=Post.objects.get(post_id=post_id)
    if request.META.get('HTTP_REFERER')=='http://127.0.0.1:8000/':
        redirect_url='/'
    else:
        redirect_url=f"/post/{post_id}"
    if Liked_Post.objects.filter(Username=current_user.username,post_id=post_id).exists():
        current_obj=Liked_Post.objects.get(Username=current_user.username,post_id=post_id)
        current_obj.delete()
        profile_obj.likes=profile_obj.likes-1
        profile_obj.save()
        return redirect(redirect_url)
    else:
        current_obj=Liked_Post.objects.create(Username=current_user.username,post_id=post_id)
        current_obj.save()
        profile_obj.likes=profile_obj.likes+1
        profile_obj.save()
        return redirect(redirect_url)

@login_required(login_url='login')
def follow(request,username):
    current_user=request.user
    follower=User.objects.get(username=username)
    follower_profile=Profile.objects.get(user=follower)
    check=Follow.objects.filter(current_user=current_user,followed=follower_profile).exists()
    following_profile=Profile.objects.get(user=current_user)
    if check:
        followx=Follow.objects.get(current_user=current_user,followed=follower_profile)
        followx.delete()
        follower_profile.followers=follower_profile.followers-1
        follower_profile.save()
        following_profile.following-=1
        following_profile.save()
    else:
        new_obj=Follow.objects.create(current_user=current_user,followed=follower_profile)
        new_obj.save()
        follower_profile.followers=follower_profile.followers+1
        follower_profile.save()
        following_profile.following+=1
        following_profile.save()
    

    if request.META.get('HTTP_REFERER')=='http://127.0.0.1:8000/':
        return redirect('/')
    return redirect(f'/profile/{username}')

    