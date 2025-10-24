from django.contrib import admin
from .models import Quiz, Question, Answer, QuizAttempt, QuizResponse, QuizFeedback


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'difficulty_level', 'passing_score', 'is_active']
    list_filter = ['difficulty_level', 'is_active', 'topic__grade']
    search_fields = ['title', 'description']
    list_editable = ['is_active']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'quiz', 'question_type', 'points', 'order', 'is_active']
    list_filter = ['question_type', 'is_active', 'quiz__topic__grade']
    search_fields = ['question_text', 'explanation']
    list_editable = ['order', 'is_active']
    inlines = [AnswerInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['answer_text', 'question', 'is_correct', 'order']
    list_filter = ['is_correct', 'question__quiz__topic__grade']
    search_fields = ['answer_text', 'explanation']
    list_editable = ['is_correct', 'order']


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'started_at', 'score', 'is_passed', 'attempt_number']
    list_filter = ['is_passed', 'quiz__topic__grade']
    search_fields = ['user__username', 'quiz__title']
    readonly_fields = ['started_at']


@admin.register(QuizResponse)
class QuizResponseAdmin(admin.ModelAdmin):
    list_display = ['attempt', 'question', 'is_correct', 'points_earned', 'answered_at']
    list_filter = ['is_correct', 'attempt__quiz__topic__grade']
    search_fields = ['attempt__user__username', 'question__question_text']


@admin.register(QuizFeedback)
class QuizFeedbackAdmin(admin.ModelAdmin):
    list_display = ['attempt', 'difficulty_rating', 'helpful_rating', 'created_at']
    list_filter = ['difficulty_rating', 'helpful_rating']
    search_fields = ['attempt__user__username', 'attempt__quiz__title']
    readonly_fields = ['created_at']