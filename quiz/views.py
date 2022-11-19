from django.shortcuts import render, redirect, HttpResponse
from .models import Question, Quiz, Report, Response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .forms import QuestionForm
import json
from django.db.models import Q

@login_required(login_url='/auth')
def create_question(request):
    if request.method == 'POST':
        slug = request.POST.get('slug')
        quiz = Quiz.objects.filter(slug=slug)[0]
        question = request.POST.get('question')
        a = request.POST.get('a')
        b = request.POST.get('b')
        c = request.POST.get('c')
        d = request.POST.get('d')
        answer = request.POST.get('answer')
        marks = int(request.POST.get('mark'))
        neg = int(request.POST.get('neg'))
        if neg > 0:
            neg = neg*-1
        response_data = {}
        question = Question(quiz=quiz, question=question, option1 = a, option2 = b, option3 = c, option4=d, answer=answer, marks=marks, negative=neg)
        question.save()
        response_data['status'] = 'Sucess : question added!'
        response_data['question'] = question.question
        response_data['id'] = question.id
        response_data['a'] = question.option1
        response_data['b'] = question.option2
        response_data['c'] = question.option3
        response_data['d'] = question.option4
        response_data['answer'] = question.answer
        response_data['marks'] = question.marks
        response_data['negative'] = question.negative
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

@login_required(login_url='/auth')
def home(request):
    # Search Implementation
    q = request.GET.get('q') if request.GET.get('q')!=None else ''
    quizes = Quiz.objects.filter(
        Q(title__icontains=q) | Q(author__username__icontains=q)
        )
    quiz_count = quizes.count()
    my_quizes = Quiz.objects.filter(author=request.user)
    reports = Report.objects.filter(student=request.user)
    # Quiz Creation 
    if request.method == 'POST':
        title = request.POST.get('title')
        quiz = Quiz(title=title, author=request.user)
        quiz.save()
        return redirect('home')
    
    return render(request, 'quiz/home.html', {'quizes': quizes, 'quiz_count': quiz_count, 'my_quizes': my_quizes, 'reports':reports})

@login_required(login_url='/auth')
def question_list(request, slug):
    quiz = Quiz.objects.get(slug=str(slug))
    questions = Question.objects.filter(quiz=quiz)
    my_quizes = Quiz.objects.filter(author=request.user)
    reports = Report.objects.filter(quiz=quiz)
    return render(request, 'quiz/questions.html', {'reports':reports, 'questions': questions, 'my_quizes': my_quizes, 'slug':slug, 'quiz':quiz})

@login_required(login_url='/auth')
def response_page(request, slug, userid):
    quiz = Quiz.objects.filter(slug=slug)[0]
    user = User.objects.filter(id=userid)[0]
    response = Response.objects.filter(quiz=quiz, student=user)
    return render(request, 'quiz/records.html', {'response' : response, 'student':user})


@login_required(login_url='/auth')
def exam_view(request, slug):
    quiz = Quiz.objects.filter(slug=str(slug))[0]
    questions = Question.objects.filter(quiz=quiz)
    if request.method == 'POST':
        score = 0
        for question in questions:
            id = str(question.id)
            if( request.POST.get(id) == question.answer):
                score += question.marks
                try:
                    response = Response(quiz=quiz, student=request.user, question=question, is_correct=True, answer=request.POST.get(id))
                    response.save()
                except:
                    response = Response.objects.filter(quiz=quiz, question=question, student=request.user)[0]
                    attempt = response.attempt + 1
                    response_another = Response(quiz=quiz, student=request.user, question=question, is_correct=True, answer=request.POST.get(id), attempt=attempt)
                    response_another.save()
            else:
                score += question.negative
                try:
                    response = Response(quiz=quiz, student=request.user, question=question, is_correct=False, answer=request.POST.get(id))
                    response.save()
                except:
                    response = Response.objects.filter(quiz=quiz, question=question, student=request.user)[0]
                    attempt = response.attempt + 1
                    response_another = Response(quiz=quiz, student=request.user, question=question, is_correct=False, answer=request.POST.get(id), attempt=attempt)
                    response_another.save()
        try:
            report = Report(quiz=quiz, student=request.user, score=score)
            report.save()
        except:
            report = Report.objects.filter(quiz=quiz, student=request.user)[0]
            report.score=score
            report.attempt+=1
            report.save()

        return redirect('home')

    else:
        reports = Report.objects.filter(quiz=quiz)
        return render(request, 'quiz/exam.html', {'questions': questions, 'slug':slug, 'reports': reports, 'quiz':quiz})

class QuestionCreate(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        quiz = Quiz.objects.filter(slug=slug)[0]
        context["quiz"] = quiz
        return context

    def form_valid(self, form):
        slug = self.kwargs['slug']
        quiz = Quiz.objects.filter(slug=slug)[0]
        form.instance.quiz = quiz
        return super().form_valid(form)


class QuestionUpdate(LoginRequiredMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    success_url = reverse_lazy('home')
    template_name_suffix= '_update_form'


class QuestionDelete(LoginRequiredMixin, DeleteView):
    model = Question
    fields = '__all__'
    success_url = reverse_lazy('home')

class QuizDelete(LoginRequiredMixin, DeleteView):
    model = Quiz
    fields = '__all__'
    success_url = reverse_lazy('home')
