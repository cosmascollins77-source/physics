from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from topics.models import CBCGrade, PhysicsTopic, TopicContent, TopicFormula, TopicExperiment
from simulations.models import Simulation
from quizzes.models import Quiz, Question, Answer
from progress.models import Achievement, UserProfile
from django.utils.text import slugify

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate the database with sample physics data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create CBC Grades
        self.create_grades()
        
        # Create Physics Topics
        self.create_topics()
        
        # Create Simulations
        self.create_simulations()
        
        # Create Quizzes
        self.create_quizzes()
        
        # Create Achievements
        self.create_achievements()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data!')
        )

    def create_grades(self):
        grades_data = [
            {'name': 'Grade 7', 'description': 'Introduction to Physics', 'order': 1},
            {'name': 'Grade 8', 'description': 'Basic Physics Concepts', 'order': 2},
            {'name': 'Grade 9', 'description': 'Intermediate Physics', 'order': 3},
            {'name': 'Grade 10', 'description': 'Advanced Physics', 'order': 4},
            {'name': 'Grade 11', 'description': 'Pre-University Physics', 'order': 5},
            {'name': 'Grade 12', 'description': 'University Preparation Physics', 'order': 6},
        ]
        
        for grade_data in grades_data:
            grade, created = CBCGrade.objects.get_or_create(
                name=grade_data['name'],
                defaults=grade_data
            )
            if created:
                self.stdout.write(f'Created grade: {grade.name}')

    def create_topics(self):
        # Get grades
        grade_7 = CBCGrade.objects.get(name='Grade 7')
        grade_8 = CBCGrade.objects.get(name='Grade 8')
        grade_9 = CBCGrade.objects.get(name='Grade 9')
        grade_10 = CBCGrade.objects.get(name='Grade 10')
        
        topics_data = [
            {
                'title': 'Introduction to Motion',
                'grade': grade_7,
                'difficulty_level': 'beginner',
                'description': 'Learn the basics of motion, speed, and velocity.',
                'learning_outcomes': 'Students will understand the concepts of motion, speed, velocity, and acceleration.',
                'estimated_duration': 45
            },
            {
                'title': 'Forces and Newton\'s Laws',
                'grade': grade_8,
                'difficulty_level': 'intermediate',
                'description': 'Explore the fundamental forces and Newton\'s three laws of motion.',
                'learning_outcomes': 'Students will understand forces, Newton\'s laws, and their applications.',
                'estimated_duration': 60
            },
            {
                'title': 'Electricity and Circuits',
                'grade': grade_9,
                'difficulty_level': 'intermediate',
                'description': 'Introduction to electrical concepts, circuits, and basic electronics.',
                'learning_outcomes': 'Students will understand electrical concepts, circuit analysis, and basic electronics.',
                'estimated_duration': 75
            },
            {
                'title': 'Light and Optics',
                'grade': grade_8,
                'difficulty_level': 'intermediate',
                'description': 'Study of light behavior, reflection, refraction, and optical instruments.',
                'learning_outcomes': 'Students will understand light properties, reflection, refraction, and optical systems.',
                'estimated_duration': 50
            },
            {
                'title': 'Waves and Sound',
                'grade': grade_9,
                'difficulty_level': 'intermediate',
                'description': 'Understanding wave properties, sound waves, and wave behavior.',
                'learning_outcomes': 'Students will understand wave properties, sound characteristics, and wave phenomena.',
                'estimated_duration': 55
            },
            {
                'title': 'Thermodynamics',
                'grade': grade_10,
                'difficulty_level': 'advanced',
                'description': 'Heat, temperature, energy transfer, and thermodynamic processes.',
                'learning_outcomes': 'Students will understand heat, temperature, energy transfer, and thermodynamic principles.',
                'estimated_duration': 80
            }
        ]
        
        for topic_data in topics_data:
            topic, created = PhysicsTopic.objects.get_or_create(
                title=topic_data['title'],
                defaults={
                    **topic_data,
                    'slug': slugify(topic_data['title'])
                }
            )
            if created:
                self.stdout.write(f'Created topic: {topic.title}')
                
                # Create topic content
                self.create_topic_content(topic)
                self.create_topic_formulas(topic)
                self.create_topic_experiments(topic)

    def create_topic_content(self, topic):
        content_data = [
            {
                'content_type': 'theory',
                'title': 'Introduction',
                'content': f'This topic covers the fundamental concepts of {topic.title.lower()}. Students will learn through interactive content, simulations, and practical examples.',
                'is_essential': True
            },
            {
                'content_type': 'formula',
                'title': 'Key Formulas',
                'content': f'Important formulas and equations related to {topic.title.lower()} that students need to memorize and understand.',
                'is_essential': True
            },
            {
                'content_type': 'example',
                'title': 'Worked Examples',
                'content': f'Step-by-step solutions to common problems in {topic.title.lower()} to help students understand problem-solving techniques.',
                'is_essential': True
            }
        ]
        
        for content_data_item in content_data:
            TopicContent.objects.get_or_create(
                topic=topic,
                title=content_data_item['title'],
                defaults=content_data_item
            )

    def create_topic_formulas(self, topic):
        if 'Motion' in topic.title:
            formulas_data = [
                {
                    'name': 'Speed Formula',
                    'formula': 'v = \\frac{d}{t}',
                    'description': 'Speed equals distance divided by time',
                    'variables': {'v': 'speed', 'd': 'distance', 't': 'time'},
                    'units': 'm/s',
                    'is_essential': True
                },
                {
                    'name': 'Acceleration Formula',
                    'formula': 'a = \\frac{v_f - v_i}{t}',
                    'description': 'Acceleration equals change in velocity divided by time',
                    'variables': {'a': 'acceleration', 'v_f': 'final velocity', 'v_i': 'initial velocity', 't': 'time'},
                    'units': 'm/s²',
                    'is_essential': True
                }
            ]
        elif 'Forces' in topic.title:
            formulas_data = [
                {
                    'name': 'Newton\'s Second Law',
                    'formula': 'F = ma',
                    'description': 'Force equals mass times acceleration',
                    'variables': {'F': 'force', 'm': 'mass', 'a': 'acceleration'},
                    'units': 'N',
                    'is_essential': True
                }
            ]
        else:
            formulas_data = [
                {
                    'name': 'Basic Formula',
                    'formula': 'E = mc^2',
                    'description': 'Energy-mass equivalence',
                    'variables': {'E': 'energy', 'm': 'mass', 'c': 'speed of light'},
                    'units': 'J',
                    'is_essential': True
                }
            ]
        
        for formula_data in formulas_data:
            TopicFormula.objects.get_or_create(
                topic=topic,
                name=formula_data['name'],
                defaults=formula_data
            )

    def create_topic_experiments(self, topic):
        experiments_data = [
            {
                'title': f'Virtual {topic.title} Experiment',
                'objective': f'To demonstrate key concepts in {topic.title.lower()}',
                'materials_needed': 'Computer with internet connection',
                'procedure': f'1. Open the simulation\n2. Adjust parameters\n3. Observe results\n4. Record observations',
                'expected_results': f'Students will observe {topic.title.lower()} phenomena',
                'is_virtual': True
            }
        ]
        
        for experiment_data in experiments_data:
            TopicExperiment.objects.get_or_create(
                topic=topic,
                title=experiment_data['title'],
                defaults=experiment_data
            )

    def create_simulations(self):
        topics = PhysicsTopic.objects.all()
        
        for topic in topics:
            simulation_data = {
                'title': f'{topic.title} Simulation',
                'description': f'Interactive simulation for {topic.title.lower()}',
                'simulation_type': 'motion' if 'Motion' in topic.title else 'electricity' if 'Electricity' in topic.title else 'optics',
                'html_content': f'<div class="simulation-container"><h3>{topic.title} Interactive Simulation</h3><p>Use the controls below to explore {topic.title.lower()} concepts.</p></div>',
                'learning_objectives': f'Students will understand {topic.title.lower()} through hands-on experimentation',
                'instructions': 'Adjust the parameters and observe the changes in the simulation',
                'difficulty_level': topic.difficulty_level,
                'estimated_duration': 15
            }
            
            simulation, created = Simulation.objects.get_or_create(
                topic=topic,
                title=simulation_data['title'],
                defaults=simulation_data
            )
            if created:
                self.stdout.write(f'Created simulation: {simulation.title}')

    def create_quizzes(self):
        topics = PhysicsTopic.objects.all()
        
        for topic in topics:
            quiz_data = {
                'title': f'{topic.title} Quiz',
                'description': f'Test your understanding of {topic.title.lower()}',
                'instructions': 'Answer all questions carefully. You have multiple attempts.',
                'time_limit': 30,
                'passing_score': 70,
                'max_attempts': 3,
                'difficulty_level': topic.difficulty_level
            }
            
            quiz, created = Quiz.objects.get_or_create(
                topic=topic,
                title=quiz_data['title'],
                defaults=quiz_data
            )
            
            if created:
                self.stdout.write(f'Created quiz: {quiz.title}')
                self.create_quiz_questions(quiz)

    def create_quiz_questions(self, quiz):
        questions_data = [
            {
                'question_type': 'multiple_choice',
                'question_text': f'What is the main focus of {quiz.topic.title}?',
                'explanation': f'This question tests basic understanding of {quiz.topic.title.lower()}.',
                'points': 1
            },
            {
                'question_type': 'true_false',
                'question_text': f'Is {quiz.topic.title} an important topic in physics?',
                'explanation': f'{quiz.topic.title} is indeed an important topic in physics.',
                'points': 1
            }
        ]
        
        for i, question_data in enumerate(questions_data):
            question, created = Question.objects.get_or_create(
                quiz=quiz,
                question_text=question_data['question_text'],
                defaults={
                    **question_data,
                    'order': i + 1
                }
            )
            
            if created:
                self.create_question_answers(question)

    def create_question_answers(self, question):
        if question.question_type == 'multiple_choice':
            answers_data = [
                {'answer_text': 'Option A', 'is_correct': True, 'order': 1},
                {'answer_text': 'Option B', 'is_correct': False, 'order': 2},
                {'answer_text': 'Option C', 'is_correct': False, 'order': 3},
                {'answer_text': 'Option D', 'is_correct': False, 'order': 4}
            ]
        else:  # true_false
            answers_data = [
                {'answer_text': 'True', 'is_correct': True, 'order': 1},
                {'answer_text': 'False', 'is_correct': False, 'order': 2}
            ]
        
        for answer_data in answers_data:
            Answer.objects.get_or_create(
                question=question,
                answer_text=answer_data['answer_text'],
                defaults=answer_data
            )

    def create_achievements(self):
        achievements_data = [
            {
                'name': 'First Steps',
                'description': 'Complete your first topic',
                'achievement_type': 'topic_completion',
                'criteria': {'topics_completed': 1},
                'points': 10,
                'icon': 'fas fa-baby'
            },
            {
                'name': 'Quiz Master',
                'description': 'Score 100% on a quiz',
                'achievement_type': 'quiz_mastery',
                'criteria': {'quiz_score': 100},
                'points': 25,
                'icon': 'fas fa-trophy'
            },
            {
                'name': 'Simulation Explorer',
                'description': 'Complete 5 simulations',
                'achievement_type': 'simulation_explorer',
                'criteria': {'simulations_completed': 5},
                'points': 30,
                'icon': 'fas fa-flask'
            },
            {
                'name': 'Learning Streak',
                'description': 'Study for 7 consecutive days',
                'achievement_type': 'streak',
                'criteria': {'streak_days': 7},
                'points': 50,
                'icon': 'fas fa-fire'
            }
        ]
        
        for achievement_data in achievements_data:
            Achievement.objects.get_or_create(
                name=achievement_data['name'],
                defaults=achievement_data
            )
