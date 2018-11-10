
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.urls import reverse
from  django.views import generic
from django.utils import timezone

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list':latest_question_list
    }
    # return HttpResponse(template.render(context, request))
    return render(request, 'polls/index.html', context)
def detail(request, question_id):
    # 第一种方式
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404('Question does not exist')
    # return HttpResponse("You're looking at question %s." % question_id)
    # return render(request, 'polls/detail.html', {'question':question})
    #第二种方式
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question':question})


def results(request, question_id):
    # response = 'you are looking at the results of question %s.'
    # return HttpResponse(response % question_id)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question':question})


def vote(request, question_id):
    # return HttpResponse('you are voting on question %s.' % question_id)
    question = get_object_or_404(Question, pk=question_id)
    try:
        select_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        #重新展示投票表单
        return render(request, 'polls/detail.html', {
            'question':question,
            'error_message':'You did not select a choice.',
        })
    else:
        select_choice.votes += 1
        select_choice.save()
        #在成功发送一笔数据以后，总是返回一个HttpResponseRedict
        #这可以有效防止数据被提交两次
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five publish questions."""
        return Question.objects.filter(
            pub_date__lte = timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
