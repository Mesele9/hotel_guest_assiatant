document.addEventListener('DOMContentLoaded', function() {
    // Star rating interaction
    document.querySelectorAll('.star-rating-label').forEach(label => {
        label.addEventListener('click', function(e) {
            const stars = this.parentElement.querySelectorAll('.star-rating-label');
            const index = Array.from(stars).indexOf(this);
            stars.forEach((star, i) => {
                i <= index ? 
                star.querySelector('.star').style.color = '#f1c40f' :
                star.querySelector('.star').style.color = '#ddd';
            });
        });
    });

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
});