$(document).ready(function() {
  // Add float labels functionality
  $('.form-field input').on('focus', function() {
    $(this).siblings('label').addClass('float');
  });

  $('.form-field input').on('blur', function() {
    if ($(this).val().length === 0) {
      $(this).siblings('label').removeClass('float');
    }
  });

  // Handle form submission
  $('.form').on('submit', function(event) {
    event.preventDefault();

    // Get the entered username and password
    var username = $('#email').val();
    var password = $('#password').val();

    // Validate the username and password
    if (username === 'your_username' && password === 'your_password') {
      // Successful login, redirect to a new page or perform other actions
      alert('Login successful!');
    } else {
      // Invalid login, display an error message
      alert('Invalid username or password!');
    }
  });
});
