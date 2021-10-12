from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from .models import Note
#装饰器检验是否符合登录
def check_login(fn):
    def wrap(request,*args,**kwargs):
        if 'username' not in request.session or 'uid' not in request.session:
            c_username = request.COOKIES.get('username')
            c_uid = request.COOKIES.get('uid')
            if not c_username or not c_uid:
                return HttpResponseRedirect('/user/login')
            else:
                request.session['username'] = c_username
                request.session['uid'] = c_uid
        return fn(request,*args,**kwargs)
    return wrap
# Create your views here.
def add_note(request):
    if request.method == 'GET':
        return render(request,'note/add_note.html')
    elif request.method == 'POST':
        uid = request.session['uid']
        title = request.POST['title']
        content = request.POST['content']
        Note.objects.create(title=title,content=content,user_id=uid)

        return HttpResponseRedirect('/note/look/')

def look_note(request):

    all_note = Note.objects.filter(is_active=True)
    return render(request,'note/look_note.html',locals())


def update_note(request,note_id):
    try:
        note = Note.objects.get(id=note_id)
    except Exception as e:
        return HttpRequest('没有该笔记')
    if request.method == 'GET':
        return render(request,'note/update_note.html',locals())
    elif request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        note.title = title
        note.content = content
        note.save()
        return HttpResponseRedirect('/note/look/')


def del_note(request):
    note_id = request.GET.get('note_id')
    if not note_id:
        return HttpRequest('请求异常')
    try:
        note = Note.objects.get(id=note_id,is_active=True)

    except Exception as e:
        return HttpRequest('没有该笔记')
    # if request.method == 'GET':
    #     return HttpResponseRedirect('/note/look/')
    # elif request.method == 'POST':
    note.is_active =False
    note.save()
    return HttpResponseRedirect('/note/look/')

