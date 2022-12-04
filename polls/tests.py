import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for question whoes pub date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date = time)
        self.assertIs(future_question.was_published_recently(), False)
    
    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for question who is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1)
        future_question = Question(pub_date = time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for question who is published within 1 day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59)
        future_question = Question(pub_date = time)
        self.assertIs(future_question.was_published_recently(), True)


def create_question(question_text, days):
    """
    Create a question with the given 'question_text' and publish given number of 'days
    offset to now (negative for questions in the past, positive for questions that have yet to be
    published).
    """
    time =  timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no question exists, an appropiate message will be displayed.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Question with a pub_date in the past are displayed on the index page.
        """
        quesiton = create_question(question_text = "Past question.", days=-3)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question]
        )

    def test_future_question(self):
        """
        Question with a pub_date in the future aren't displayed on the index page.
        """
        create_question(question_text="Future question.", days=3)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future question exits, only past and the present questions 
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-3)
        create_question(question_text="Future question.", days=3)
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [question]
        )

    def two_past_questions(self):
        """
        The question index may be displayed multiple questions.
        """
        question1 = create_question(question_text="Past question.", days=-3)
        question2 = create_question(question_text="Past question.", days=-3)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [question1, question2]
        )



