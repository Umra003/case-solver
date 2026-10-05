from django.shortcuts import render, redirect, get_object_or_404
from .models import Case, Question, CaseAttempt


# =========================
# HOME
# =========================

def home(request):
    return render(request, 'home.html')


# =========================
# PLAYER
# =========================

def player(request):

    if request.method == 'POST':

        name = request.POST.get('player_name')
        character = request.POST.get('character')

        request.session['player_name'] = name
        request.session['character'] = character

        return redirect('dashboard')

    return render(request, 'player.html')


# =========================
# DASHBOARD
# =========================

def dashboard(request):

    player_name = request.session.get('player_name')

    attempts = CaseAttempt.objects.filter(
        player_name=player_name
    ).select_related(
        'case'
    ).order_by(
        '-completed_at'
    )

    # Total number of cases in database
    total_cases = Case.objects.count()

    # Number of unique cases completed
    solved_cases = attempts.values(
        'case'
    ).distinct().count()

    # Best score
    best_score = 0

    if attempts.exists():

        best_score = max(
            attempt.score
            for attempt in attempts
        )

    # Progress percentage
    if total_cases > 0:

        progress = int(
            (solved_cases / total_cases) * 100
        )

    else:

        progress = 0

    return render(
        request,
        'dashboard.html',
        {
            'attempts': attempts,
            'total_cases': total_cases,
            'solved_cases': solved_cases,
            'best_score': best_score,
            'progress': progress,
        }
    )


# =========================
# MY PROGRESS
# =========================

def progress(request):

    player_name = request.session.get(
        'player_name'
    )

    attempts = CaseAttempt.objects.filter(
        player_name=player_name
    ).select_related(
        'case'
    ).order_by(
        '-completed_at'
    )

    # Total cases
    total_cases = Case.objects.count()

    # Unique cases solved
    solved_cases = attempts.values(
        'case'
    ).distinct().count()

    # Progress percentage
    if total_cases > 0:

        progress_percentage = int(
            (solved_cases / total_cases) * 100
        )

    else:

        progress_percentage = 0

    # Best score
    best_score = 0

    if attempts.exists():

        best_score = max(
            attempt.score
            for attempt in attempts
        )

    return render(
        request,
        'progress.html',
        {
            'attempts': attempts,
            'total_cases': total_cases,
            'solved_cases': solved_cases,
            'progress_percentage': progress_percentage,
            'best_score': best_score,
        }
    )


# =========================
# MYSTERY / ALL CASES
# =========================

def mystery(request):

    cases = Case.objects.all().order_by(
        'id'
    )

    return render(
        request,
        'mystery.html',
        {
            'cases': cases
        }
    )


# =========================
# CASE DETAILS
# =========================

def case_detail(request, case_id):

    case = get_object_or_404(
        Case,
        id=case_id
    )

    return render(
        request,
        'case_detail.html',
        {
            'case': case
        }
    )


# =========================
# QUESTIONS
# =========================

def question(
    request,
    case_id,
    question_number
):

    # Get selected case
    case = get_object_or_404(
        Case,
        id=case_id
    )

    # Get all questions for this case
    questions = Question.objects.filter(
        case=case
    ).order_by(
        'id'
    )

    total_questions = questions.count()

    # If there are no more questions,
    # go to result page
    if question_number > total_questions:

        return redirect('result')


    # Get current question
    current_question = questions[
        question_number - 1
    ]


    # =========================
    # START NEW INVESTIGATION
    # =========================

    if (
        request.method == 'GET'
        and question_number == 1
    ):

        request.session['score'] = 0

        request.session['current_case'] = case_id


    # =========================
    # CHECK ANSWER
    # =========================

    if request.method == 'POST':

        answer = request.POST.get(
            'answer'
        )

        score = request.session.get(
            'score',
            0
        )

        # Correct answer
        if (
            answer
            == current_question.correct_answer
        ):

            score += current_question.points

        request.session['score'] = score


        # Go to next question
        return redirect(
            'question',
            case_id=case_id,
            question_number=question_number + 1
        )


    # Display question
    return render(
        request,
        'question.html',
        {
            'case': case,
            'question': current_question,
            'question_number': question_number,
            'total_questions': total_questions,
        }
    )


# =========================
# RESULT
# =========================

def result(request):

    score = request.session.get(
        'score',
        0
    )

    case_id = request.session.get(
        'current_case'
    )

    # Make sure a case exists
    if not case_id:

        return redirect('mystery')


    case = get_object_or_404(
        Case,
        id=case_id
    )

    player_name = request.session.get(
        'player_name'
    )


    # =========================
    # SAVE INVESTIGATION
    # =========================

    # Prevent duplicate records when
    # refreshing the result page

    already_saved = CaseAttempt.objects.filter(
        player_name=player_name,
        case=case,
        score=score
    ).exists()


    if not already_saved:

        CaseAttempt.objects.create(
            player_name=player_name,
            case=case,
            score=score
        )


    # Display result
    return render(
        request,
        'result.html',
        {
            'score': score,
            'case': case
        }
    )
