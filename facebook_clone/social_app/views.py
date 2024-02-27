from datetime import datetime
from django.shortcuts import render, redirect
from .models import Post, Comment
from friend_app.models import FriendsList
import json
from django.http import JsonResponse
#import os
from django.conf import settings
#from django.core.files.storage import FileSystemStorage
import base64
from django.core import files
from django.core.files.base import ContentFile

# Create your views here.


#TEMP_PROFILE_IMAGE_NAME = "temp_profile_image.png"


'''
All Users Post
'''


def index(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        friend = FriendsList.objects.get(user = user)
        friends_list = friend.friends.all()

        '''
        List of post according to User friend
        '''
        post_list = Post.objects.filter(user__in = list(friends_list) + [user,]).order_by('-date_post')
        context['post_list'] = post_list
    else:
        return redirect('login')
    return render(request, 'home.html', context)




'''
All Users Post with Json
'''


def postList(request):
    payload = {}
    p_list = []
    user = request.user
    if user.is_authenticated:
        post_list = Post.objects.all().order_by('-date_post')
        for i in post_list:
            payload['user'] = i.user.username
            payload['user_post'] = i.user_post
            payload['image'] = i.image.url
            payload['date_post'] = i.date_post
            p_list.append(payload)
    else:
        payload['response'] = 'User not authenticated'
    return JsonResponse(json.dumps(payload), content_type="application/json")



'''
Image from base 64 Encoding
'''


def save_post_image_form_base64String(imageString):
    format, imgstr = imageString.split(';base64,')
    ext = format.split('/')[-1]
    img = base64.b64decode(imgstr)
    file_data = ContentFile(img)
    file_name = "'myphoto." + ext
    return file_name, file_data

'''
Create a post with json
'''

def create_post(request):
    payload = {}
    user = request.user
    if user.is_authenticated:
        ns = json.loads(request.body)
        inputPostValue = ns.get('inputPostValue')
        imgPostValue = ns.get('imgPostValue')

        if inputPostValue and imgPostValue:
            post = Post.objects.create(
                user=user, user_post=inputPostValue)
            print(post)
            file_name, file_data = save_post_image_form_base64String(
                imgPostValue)
            #print(post.file.save(file_name, file_data))
            post.file.save(file_name, file_data)
            payload['response'] = 'Post created Successfully'
        else:
            if inputPostValue:
                post = Post.objects.create(
                    user=user, user_post=inputPostValue)
                print(post)
                payload['response'] = 'Post created Successfully'
            else:
                post = Post.objects.create(
                    user=user)
                print(post)
                file_name, file_data = save_post_image_form_base64String(
                    imgPostValue)
                #print(post.image.save(file_name, file_data))
                post.file.save(file_name, file_data)
                payload['response'] = 'Post created Successfully'
       
    else:
        payload['response'] = 'User has to be authenticated'
    return JsonResponse(json.dumps(payload), content_type="application/json", safe=False)


'''
User like post with Json
'''


def like_post(request, id):
    payload = {}
    user = request.user
    if user.is_authenticated:
        post_id = Post.objects.get(id=id)
        if user in post_id.user_like_post.all():
            post_id.user_like_post.remove(user)
            like_count = post_id.user_like_post.all().count()
            payload['response'] = 'Unlike User'
            payload['like_count'] = like_count
        else:
            post_id.user_like_post.add(user)
            like_count = post_id.user_like_post.all().count()
            payload['response'] = 'Like User'
            payload['like_count'] = like_count

    else:
        payload['response'] = 'User Needs to be authenticated'
    return JsonResponse(payload, content_type="application/json", safe=False)


'''
Get like count for each post with json
'''


def get_like_count(request, id):
    payload = {}
    user = request.user
    if user.is_authenticated:
        post_id = Post.objects.get(id=id)
        like_count = post_id.user_like_post.all().count()
        payload['response'] = 'Unlike User'
        payload['like_count'] = like_count

    else:
        payload['response'] = 'User Needs to be authenticated'
    return JsonResponse(payload, content_type="application/json", safe=False)


'''
User comment on post with Json
'''


def user_comment(request, id):
    payload = {}
    comment_list = []
    user = request.user
    if user.is_authenticated:
        post_id = Post.objects.get(id=id)
        ns = json.loads(request.body)
        inputValue = ns['inputValue']
        if request.method == 'POST':
            comment = Comment.objects.create(
                user=user, post_id=post_id, comment=inputValue)
            payload['response'] = 'Comment Successful'

            all_comment_list = Comment.objects.filter(post_id=post_id)
            if all_comment_list:
                for i in all_comment_list:
                    comment_list.append({
                        'user': i.user.username,
                        'comment': i.comment
                    })
                str_time = datetime.strftime(comment.date_comment, "%I:%M %p")
                str_time = str_time.strip("0")
                payload['comment_list'] = comment_list
                payload['comment_count'] = len(comment_list)
                payload['user'] = user.username
                payload['comment'] = comment.comment
                payload['date'] = str_time
                
            else:
                payload['response'] = 'No Input value'
    else:
        payload['response'] = 'User has to be Authenticated'

    return JsonResponse((payload), content_type="application/json", safe=False)


'''
Comment Count for each post
'''


def comment_count(request, id):
    payload = {}
    user = request.user
    if user.is_authenticated:
        post_id = Post.objects.get(id=id)
        va = Comment.objects.filter(post_id=post_id).count()
        payload['response'] = va

    return JsonResponse(payload, content_type="application/json", safe=False)


''' 
User Share Post
'''
def userSharePost(request, id):
    user = request.user
    post_id = Post.objects.get(id = id)
    user_post = post_id.user_post
    image = post_id.file
    posted_by = post_id.user
    Post.objects.create(user = user, user_post = user_post, file = image, posted_by = posted_by) 
    return redirect('index')



