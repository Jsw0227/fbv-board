from django.shortcuts import render, redirect, reverse

# Create your views here.
def index(request):
    return render(request, 'board/index.html')

from .models import Board

def list(request):
    board_list = Board.objects.all().order_by('-id')
    context = {
        'board_list':board_list,
    }
    return render(
        request,
        'board/list.html',
        context
    )

def read(request, id):
    board = Board.objects.get(pk=id)
    board.incrementReadCount()
    return render(request, 'board/read.html', {'board' :board})

def regist(request):
    if request.method == 'POST':
        title = request.POST['title']
        writer = request.POST.get('writer')
        content = request.POST['content']
        Board(title=title, writer=writer, content=content).save()
        return redirect(reverse('board:list'))        
    else:
        return render(request, 'board/regist.html')


def edit(request, id):
    board = Board.objects.get(pk=id)
    if request.method == 'POST':
        board.title = request.POST['title']
        board.writer = request.POST.get('writer')
        board.content = request.POST['content']
        board.save()
        return redirect(reverse('board:read', args=(id,)))        
    else:
        return render(request, 'board/edit.html', {'board':board})
    
def remove(request, id):
    board = Board.objects.get(pk=id)
    if request.method == 'POST':
        board.delete()
        return redirect(reverse('board:list'))        
    else:
        return render(request, 'board/remove.html', {'board':board})
