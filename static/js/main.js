// Physics Learning Platform JavaScript

$(document).ready(function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Smooth scrolling for anchor links
    $('a[href^="#"]').on('click', function(event) {
        var target = $(this.getAttribute('href'));
        if (target.length) {
            event.preventDefault();
            $('html, body').stop().animate({
                scrollTop: target.offset().top - 80
            }, 1000);
        }
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);

    // Quiz functionality
    $('.quiz-option').on('click', function() {
        var $this = $(this);
        var questionId = $this.data('question-id');
        
        // Remove previous selection
        $('.quiz-option[data-question-id="' + questionId + '"]').removeClass('selected');
        
        // Add selection to clicked option
        $this.addClass('selected');
        
        // Enable submit button if all questions answered
        checkQuizCompletion();
    });

    // Check if all quiz questions are answered
    function checkQuizCompletion() {
        var totalQuestions = $('.quiz-question').length;
        var answeredQuestions = $('.quiz-option.selected').length;
        
        if (answeredQuestions === totalQuestions) {
            $('#submit-quiz').prop('disabled', false).removeClass('btn-secondary').addClass('btn-primary');
        }
    }

    // Simulation parameter controls
    $('.simulation-parameter').on('change', function() {
        var parameterName = $(this).attr('name');
        var parameterValue = $(this).val();
        
        // Update simulation with new parameter
        updateSimulation(parameterName, parameterValue);
    });

    // Progress tracking
    function trackProgress(elementId, progress) {
        var $element = $('#' + elementId);
        $element.attr('aria-valuenow', progress);
        $element.css('width', progress + '%');
    }

    // Topic progress tracking
    $('.start-topic').on('click', function() {
        var topicId = $(this).data('topic-id');
        var $button = $(this);
        
        $.ajax({
            url: '/topic/' + topicId + '/start/',
            method: 'POST',
            data: {
                'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                if (response.success) {
                    $button.removeClass('btn-outline-primary').addClass('btn-success');
                    $button.html('<i class="fas fa-check"></i> Started');
                    $button.prop('disabled', true);
                }
            },
            error: function() {
                alert('Error starting topic. Please try again.');
            }
        });
    });

    // Complete topic
    $('.complete-topic').on('click', function() {
        var topicId = $(this).data('topic-id');
        var $button = $(this);
        
        $.ajax({
            url: '/topic/' + topicId + '/complete/',
            method: 'POST',
            data: {
                'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                if (response.success) {
                    $button.removeClass('btn-outline-success').addClass('btn-success');
                    $button.html('<i class="fas fa-check"></i> Completed');
                    $button.prop('disabled', true);
                    
                    // Show achievement notification if applicable
                    showAchievementNotification('Topic Completed!', 'You have successfully completed this topic.');
                }
            },
            error: function() {
                alert('Error completing topic. Please try again.');
            }
        });
    });

    // Simulation session tracking
    function startSimulation(simulationId) {
        $.ajax({
            url: '/simulations/simulation/' + simulationId + '/start/',
            method: 'POST',
            data: {
                'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                if (response.success) {
                    console.log('Simulation session started');
                }
            }
        });
    }

    // Save simulation parameters
    function saveSimulationParameters(simulationId, parameters) {
        $.ajax({
            url: '/simulations/simulation/' + simulationId + '/save-parameters/',
            method: 'POST',
            data: {
                'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                'parameters': JSON.stringify(parameters)
            },
            success: function(response) {
                if (response.success) {
                    console.log('Parameters saved');
                }
            }
        });
    }

    // Achievement notifications
    function showAchievementNotification(title, message) {
        var notification = $('<div class="alert alert-success alert-dismissible fade show" role="alert">' +
            '<strong>' + title + '</strong> ' + message +
            '<button type="button" class="btn-close" data-bs-dismiss="alert"></button>' +
            '</div>');
        
        $('.container').prepend(notification);
        
        // Auto-hide after 5 seconds
        setTimeout(function() {
            notification.fadeOut();
        }, 5000);
    }

    // Search functionality
    $('#search-form').on('submit', function(e) {
        e.preventDefault();
        var query = $('#search-input').val().trim();
        
        if (query.length < 2) {
            alert('Please enter at least 2 characters to search.');
            return;
        }
        
        // Perform search
        window.location.href = '/search/?q=' + encodeURIComponent(query);
    });

    // Real-time search suggestions
    $('#search-input').on('input', function() {
        var query = $(this).val().trim();
        
        if (query.length >= 2) {
            // Implement real-time search suggestions here
            // This would typically make an AJAX call to get suggestions
        }
    });

    // Mobile menu handling
    $('.navbar-toggler').on('click', function() {
        $('.navbar-collapse').toggleClass('show');
    });

    // Close mobile menu when clicking on a link
    $('.navbar-nav .nav-link').on('click', function() {
        $('.navbar-collapse').removeClass('show');
    });

    // Lazy loading for images
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }

    // Form validation
    $('form').on('submit', function(e) {
        var $form = $(this);
        var isValid = true;
        
        // Check required fields
        $form.find('[required]').each(function() {
            if (!$(this).val().trim()) {
                $(this).addClass('is-invalid');
                isValid = false;
            } else {
                $(this).removeClass('is-invalid');
            }
        });
        
        if (!isValid) {
            e.preventDefault();
            alert('Please fill in all required fields.');
        }
    });

    // Remove validation classes on input
    $('input, textarea, select').on('input change', function() {
        $(this).removeClass('is-invalid');
    });

    // Progress bar animation
    function animateProgressBar(selector, targetValue) {
        var $progressBar = $(selector);
        var currentValue = 0;
        var increment = targetValue / 100;
        
        var timer = setInterval(function() {
            currentValue += increment;
            $progressBar.css('width', currentValue + '%');
            
            if (currentValue >= targetValue) {
                clearInterval(timer);
                $progressBar.css('width', targetValue + '%');
            }
        }, 20);
    }

    // Initialize progress bars on page load
    $('.progress-bar').each(function() {
        var targetValue = $(this).data('value') || 0;
        animateProgressBar(this, targetValue);
    });

    // Dark mode toggle
    $('#dark-mode-toggle').on('click', function() {
        $('body').toggleClass('dark-mode');
        localStorage.setItem('darkMode', $('body').hasClass('dark-mode'));
    });

    // Load dark mode preference
    if (localStorage.getItem('darkMode') === 'true') {
        $('body').addClass('dark-mode');
    }

    // Print functionality
    $('.print-btn').on('click', function() {
        window.print();
    });

    // Share functionality
    $('.share-btn').on('click', function() {
        if (navigator.share) {
            navigator.share({
                title: document.title,
                url: window.location.href
            });
        } else {
            // Fallback: copy to clipboard
            navigator.clipboard.writeText(window.location.href).then(function() {
                alert('Link copied to clipboard!');
            });
        }
    });
});
