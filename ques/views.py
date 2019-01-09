import datetime
import uuid

from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, HttpResponse

from ques.models import *


# Create your views here.


def welcome(request):
    if request.method == "POST":
        usr = request.POST['username']
        pwd = SUser.objects.get(user_id=request.POST['username']).password
        if pwd == request.POST['password']:
            request.session['user_id'] = usr
    if request.session.get('user_id'):
        user = SUser.objects.get(user_id=request.session.get('user_id'))
        record_list = SRecord.objects.filter(user__user_id=user.user_id, question__category=user.category).values_list(
            'question').distinct()
        finish = record_list.count()
        wrong = record_list.filter(status='0').count()
        all = TQuestion.objects.filter(category=user.category).count()
        wait = all - finish
        chapter_list = TChapter.objects.filter(category=user.category.category_id).all()
        category_list = TCategory.objects.all()
        history_list = SRecord.objects.filter(user_id=user.user_id).order_by("-create_time").values("question_id",
                                                                                                    "question__title",
                                                                                                    "status",
                                                                                                    "create_time").distinct().all()[
                       :5]
        return render(request, 'welcome.html', locals())
    return render(request, 'login.html', )


def change_category(request, category_id):
    if request.session.get('user_id'):
        user = SUser.objects.get(user_id=request.session.get('user_id'))
        user.category_id = category_id
        user.save()
        return HttpResponse("OK")
    else:
        return HttpResponse("WRONG")


def get_question_info(ques_list):
    import random
    if isinstance(ques_list, list):
        question = TQuestion.objects.get(question_id=ques_list[random.randint(0, len(ques_list) - 1)])
    else:
        question = ques_list[random.randint(0, len(ques_list) - 1)]
    option_list = TOption.objects.filter(question_id=question.question_id).all()
    answer_list = [a.option for a in TAnswer.objects.filter(question_id=question.question_id).all()]
    return question, option_list, answer_list


def change_password(request):
    if request.session.get('user_id'):
        user = SUser.objects.get(user_id=request.session.get('user_id'))
        user.password = request.POST['password']
        user.save()
        return HttpResponse("OK")
    else:
        return HttpResponse("WRONG")


def view_chapter(request, chapter_id):
    chapter = TChapter.objects.get(chapter_id=chapter_id)
    user_id = request.session.get('user_id')
    question_list = TQuestion.objects.filter(chapter=chapter_id).all()
    record_list = SRecord.objects.filter(user_id=user_id, question__chapter=chapter_id).values("question",
                                                                                               "status").distinct()
    question = {}
    for ques in question_list:
        question[ques.question_id] = 'btn-secondary'
    for record in record_list:
        if record['status'] == '0':
            question[record['question']] = 'btn-primary'
        else:
            question[record['question']] = 'btn-success'
    topic_list = []
    for key, value in question.items():
        topic_list.append({'question_id': key, 'status': value})
    limit = 42  # 每页显示的记录数
    paginator = Paginator(topic_list, limit)  # 实例化一个分页对象
    page = request.GET.get('page')  # 获取页码
    try:
        topics = paginator.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        topics = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        topics = paginator.page(paginator.num_pages)  # 取最后一页的记录
    number = int((topics.number - 1) * limit)
    return render(request, 'chapter.html', locals())


def question(request, question_id):
    question = TQuestion.objects.get(question_id=question_id)
    option_list = TOption.objects.filter(question_id=question_id).all()
    answer_list = [a.option for a in TAnswer.objects.filter(question_id=question_id).all()]
    return render(request, 'question.html', locals())


def random(request):
    if request.session.get('user_id'):
        user = SUser.objects.get(user_id=request.session.get('user_id'))
        # finish_list = list(
        #    SRecord.objects.filter(user_id=user.user_id).values_list("question", flat=True).distinct().all())
        ques_list = TQuestion.objects.filter(category=user.category_id).all()
        question, option_list, answer_list = get_question_info(ques_list)
        redirect_url = "/random"
        return render(request, "question.html", locals())
    else:
        return redirect("/welcome")


def do(request):
    question_id = request.POST['question_id']
    option_list = request.POST.getlist('option_list[]')
    user_id = request.session.get('user_id')
    status = request.POST['status']
    SRecord.objects.filter(question_id=question_id, user_id=user_id).delete()
    for opt in option_list:
        record = SRecord.objects.create(record_id=str(uuid.uuid1()), user_id=user_id,
                                        question_id=question_id, status=status, option=opt,
                                        create_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        record.save()
    return HttpResponse("OK")


def random_chapter(request, chapter):
    if request.session.get('user_id'):
        user = SUser.objects.get(user_id=request.session.get('user_id'))
        ques_list = TQuestion.objects.filter(category=user.category_id, chapter=chapter).all()
        question, option_list, answer_list = get_question_info(ques_list)
        redirect_url = "/random/" + chapter + "/"
        return render(request, "question.html", locals())
    else:
        return redirect("/welcome")


def order_chapter(request, chapter):
    if request.session.get('user_id'):
        user = SUser.objects.get(user_id=request.session.get('user_id'))
        ques_list = TQuestion.objects.filter(category=user.category_id, chapter=chapter).all()
        if not request.GET.get('index'):
            index = 0
            next_page = "/order/" + chapter + "/?index=1"
        else:
            index = int(request.GET.get('index'))
            if index > 0:
                previous_page = "/order/" + chapter + "/?index=" + str(index - 1)
        if index < len(ques_list) - 1:
            next_page = "/order/" + chapter + "/?index=" + str(index + 1)
        ques_list = [ques_list[index].question_id]
        question, option_list, answer_list = get_question_info(ques_list)

        return render(request, "question.html", locals())
    else:
        return redirect("/welcome")


def wrong(request):
    if request.session.get('user_id'):
        user = SUser.objects.get(user_id=request.session.get('user_id'))
        ques_list = list(
            SRecord.objects.filter(user_id=user.user_id, status="0", question__category=user.category_id).values_list(
                "question",
                flat=True).distinct().all())
        if not len(ques_list):
            return redirect("/welcome")
        question, option_list, answer_list = get_question_info(ques_list)
        redirect_url = "/wrong"
        return render(request, "question.html", locals())
    else:
        return redirect("/welcome")


def registry(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        SUser.objects.create(user_id=username, password=password, category_id=1)

    return render(request, "registry.html")
