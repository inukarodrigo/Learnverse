/**
 * Returns the current datetime for the message creation.
 */
function getCurrentTimestamp() {
	return new Date();
}

/**
 * Renders a message on the chat screen based on the given arguments.
 * This is called from the `showUserMessage` and `showBotMessage`.
 */
function renderMessageToScreen(args) {
	// local variables
	let displayDate = (args.time || getCurrentTimestamp()).toLocaleString('en-IN', {
		month: 'short',
		day: 'numeric',
		hour: 'numeric',
		minute: 'numeric',
	});
	let messagesContainer = $('.messages');

	// init element
	let message = $(`
	<li class="message ${args.message_side}">
		<div class="avatar"></div>
		<div class="text_wrapper">
			<div class="text">${args.text}</div>
			<div class="timestamp">${displayDate}</div>
		</div>
	</li>
	`);

	// add to parent
	messagesContainer.append(message);

	// animations
	setTimeout(function () {
		message.addClass('appeared');
	}, 0);
	messagesContainer.animate({ scrollTop: messagesContainer.prop('scrollHeight') }, 300);
}

/**
 * Displays the user message on the chat screen. This is the right side message.
 */
function showUserMessage(message, datetime) {
	renderMessageToScreen({
		text: message,
		time: datetime,
		message_side: 'right',
	});
}

/**
 * Displays the chatbot message on the chat screen. This is the left side message.
 */
function showBotMessage(message, datetime) {
	setTimeout(function() {
		renderMessageToScreen({
			text: message,
			message_side: 'left',
		});
	}, 2000); // delay in milliseconds
}

function showBotLessonMessage(message, datetime) {
	renderMessageToScreen({
		text: message,
		time: datetime,
		message_side: 'left',
	});
}
window.papersForTheExam = [];
/**
 * Get input from user and show it on screen on button click.
 */
$('#send_button').on('click', function (e) {
  // Store the user input
  const papers = $('#msg_input').val();

  // Get the lesson text
  const lessonTextList = getLessonText(papers);
  showUserMessage(papers);
  showBotMessage("Your paper has been generated successfully and is now available for viewing. You can access it by using the URL provided below.<br> <a href='http://127.0.0.1:5000/specialPaper'>http://127.0.0.1:5000/specialPaper</a>");

  // Convert the lessonTextList array to a comma-separated string
  const lessonTextString = lessonTextList.join(',');

  // Reset the input
  $('#msg_input').val('');

  // Make an AJAX request to the get_questions_for_specialPaper endpoint
    $.ajax({
        url: '/get_questions_for_specialPaper',
        method: 'GET',
        data: {listOfLessons: lessonTextString},
        success: function(response) {
            // Handle the response from the server
            window.papersForTheExam = response;
            console.log(Object.values(papersForTheExam));
            localStorage.setItem('listOfQuestions',JSON.stringify(response));
        },
        error: function(jqXHR, textStatus, errorThrown) {
            // Handle any errors that occur during the request
            console.log(textStatus, errorThrown);
        }
    });
});
window.papersForTheExam = localStorage.getItem('listOfQuestions');

function getLessonText(papers) {
  // Split the user input into an array of numbers
  const numbers = papers.split(/[ ,]+/).map(Number);

  // Create an empty list to store the text
  const lessonTextList = [];

  // Iterate through the array of numbers and add the respective text to the list
  numbers.forEach(number => {
    switch(number) {
      case 1:
        lessonTextList.push("introduction to computer");
        break;
      case 2:
        lessonTextList.push("concept of it");
        break;
      case 3:
        lessonTextList.push("data representation");
        break;
      case 4:
        lessonTextList.push("data communication and networking");
        break;
      case 5:
        lessonTextList.push("database management");
        break;
      case 6:
        lessonTextList.push("system analysis and design");
        break;
      case 7:
        lessonTextList.push("web programming");
        break;
      case 8:
        lessonTextList.push("computer operating system");
        break;
      case 9:
        lessonTextList.push("programming fundamentals");
        break;
      case 10:
        lessonTextList.push("fundamental of digital circuits it in business");
        break;
      case 11:
        lessonTextList.push("new trends and future directions of it");
        break;
      case 12:
        lessonTextList.push("internet of things");
        break;
      case 13:
        lessonTextList.push("web development");
        break;
      case 14:
        lessonTextList.push("fundamentals of digital circuits");
        break;
      default:
        break;
    }
  });

  // Return the list of text
  return lessonTextList;
}

/**
 * Set initial bot message to the screen for the user.
 */
$(window).on('load', function () {
	showBotLessonMessage("Hello there! Please select the lessons you want questions from<br>1. introduction to computer<br>2. concept of it<br>3. data representation<br>4. data communication and networking<br>5. database management<br>6. system analysis and design<br>7. web programming<br>8. computer operating system<br>9. programming fundamentals<br>10. fundamental of digital circuits it in business<br>11. new trends and future directions of it<br>12. internet of things<br>13. web development<br>14. fundamentals of digital circuits");
});
