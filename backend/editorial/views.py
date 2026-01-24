from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from .models import WeeklyEditorial
from django.views.decorators.csrf import csrf_exempt

@staff_member_required(login_url='/admin/login/')
def index(request):
    edit_id = request.GET.get('id')
    active = None
    if edit_id:
        active = get_object_or_404(WeeklyEditorial, id=edit_id)
    
    history = WeeklyEditorial.objects.all()
    return render(request, 'editorial/editor.html', {
        'active': active,
        'history': history
    })

@staff_member_required(login_url='/admin/login/')
def save(request):
    if request.method == "POST":
        edit_id = request.POST.get('id')
        title = request.POST.get('title')
        content = request.POST.get('content')
        is_published = request.POST.get('is_published') == 'on'
        
        if edit_id:
            entry = get_object_or_404(WeeklyEditorial, id=edit_id)
            entry.title = title
            entry.content = content
            entry.is_published = is_published
            entry.save()
        else:
            WeeklyEditorial.objects.create(
                title=title, content=content, is_published=is_published
            )
            
    return redirect('editorial:index')

@csrf_exempt
def get_weekly_content(request):
    """
    Public API to fetch the latest published weekly comment.
    """
    latest = WeeklyEditorial.objects.filter(is_published=True).first()
    if latest:
        return JsonResponse({
            'exists': True,
            'title': latest.title,
            'content': latest.content,
            'date': latest.updated_at.strftime('%d.%m.%Y')
        })
    return JsonResponse({'exists': False})
