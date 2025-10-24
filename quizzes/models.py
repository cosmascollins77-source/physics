from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
from topics.models import PhysicsTopic


class Quiz(models.Model):
    """Physics quizzes aligned with CBC topics"""
    topic = models.ForeignKey(PhysicsTopic, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    instructions = models.TextField(help_text="Instructions for taking the quiz")
    time_limit = models.PositiveIntegerField(help_text="Time limit in minutes", null=True, blank=True)
    passing_score = models.PositiveIntegerField(default=70, help_text="Passing percentage")
    max_attempts = models.PositiveIntegerField(default=3, help_text="Maximum attempts allowed")
    is_randomized = models.BooleanField(default=True, help_text="Randomize question order")
    show_correct_answers = models.BooleanField(default=True, help_text="Show correct answers after completion")
    show_explanations = models.BooleanField(default=True, help_text="Show explanations for answers")
    difficulty_level = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ], default='beginner')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['topic__grade__order', 'topic__order', 'created_at']
    
    def __str__(self):
        return f"{self.topic.title} - {self.title}"


class Question(models.Model):
    """Quiz questions with different types"""
    QUESTION_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('fill_blank', 'Fill in the Blank'),
        ('short_answer', 'Short Answer'),
        ('calculation', 'Calculation'),
        ('matching', 'Matching'),
        ('ordering', 'Ordering'),
    ]
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    question_text = models.TextField()
    explanation = models.TextField(blank=True, help_text="Explanation for the correct answer")
    points = models.PositiveIntegerField(default=1)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.quiz.title} - Question {self.order}"


class Answer(models.Model):
    """Answer choices for questions"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    explanation = models.TextField(blank=True, help_text="Why this answer is correct/incorrect")
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.question.question_text[:50]}... - {self.answer_text[:30]}..."


class QuizAttempt(models.Model):
    """User quiz attempts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    time_taken = models.PositiveIntegerField(null=True, blank=True, help_text="Time taken in seconds")
    score = models.FloatField(null=True, blank=True, help_text="Score percentage")
    is_passed = models.BooleanField(default=False)
    attempt_number = models.PositiveIntegerField(default=1)
    
    class Meta:
        ordering = ['-started_at']
        unique_together = ['user', 'quiz', 'attempt_number']
    
    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} (Attempt {self.attempt_number})"


class QuizResponse(models.Model):
    """Individual question responses in quiz attempts"""
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='responses')
    selected_answers = models.ManyToManyField(Answer, blank=True, related_name='responses')
    text_response = models.TextField(blank=True, help_text="For text-based questions")
    is_correct = models.BooleanField(default=False)
    points_earned = models.FloatField(default=0)
    time_taken = models.PositiveIntegerField(null=True, blank=True, help_text="Time taken for this question in seconds")
    answered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['attempt', 'question']
    
    def __str__(self):
        return f"{self.attempt.user.username} - {self.question.question_text[:30]}..."


class QuizFeedback(models.Model):
    """Feedback and learning insights from quiz attempts"""
    attempt = models.OneToOneField(QuizAttempt, on_delete=models.CASCADE, related_name='feedback')
    difficulty_rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], 
                                                        help_text="Rate quiz difficulty (1-5)")
    helpful_rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], 
                                               help_text="Rate helpfulness (1-5)")
    concepts_understood = models.TextField(blank=True, help_text="Which concepts do you understand well?")
    concepts_confusing = models.TextField(blank=True, help_text="Which concepts need more practice?")
    suggestions = models.TextField(blank=True, help_text="Suggestions for improvement")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Feedback for {self.attempt.quiz.title} by {self.attempt.user.username}"