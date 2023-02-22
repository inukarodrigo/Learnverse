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
	renderMessageToScreen({
		text: message,
		message_side: 'left',
	});

	// create AJAX request to send data to Flask route
	$.ajax({
		url: '/get_questions_for_specialPaper',
		type: 'GET',
		data: {
			lessons: JSON.stringify(lessons_need)
		},
		success: function(response) {
			// show bot message after receiving response from Flask route
			showBotLessonMessage(response.message);
		},
		error: function(error) {
			console.log(error);
		}
	});
}

function showBotLessonMessage(message, datetime) {
	renderMessageToScreen({
		text: message,
		time: datetime,
		message_side: 'left',
	});
}
let papers;
const lessons = ["introduction to computer","concept of it","data representation","data communication and networking","database management","system analysis and design","web programming","computer operating system","programming fundamentals","fundamental of digital circuits it in business","new trends and future directions of it","internet of things","web development","fundamentals of digital circuits"];
let lessons_need = [];
function getLessons(papers_numbers){
	lessons_need[0] = lessons[parseInt(papers_numbers[0])-1]
	lessons_need[1] = lessons[parseInt(papers_numbers[1])-1]

	console.log(lessons_need)
}
/**
 * Get input from user and show it on screen on button click.
 */
$('#send_button').on('click', function (e) {
	//Store the user value
	papers =$('#msg_input').val();
	let numbers = papers.split(",",2);
	console.log(numbers)
	getLessons(numbers);

	// get and show message and reset input
	showUserMessage($('#msg_input').val());
	$('#msg_input').val('');

	// show bot message
	setTimeout(function () {
		console.log(typeof papers)
		showBotMessage(lessons_need);
	}, 300);
});

function generateAListOfLessons(){
	let listOfLessons = [];
	if (papers === '1'){
		listOfLessons.concat('introduction to computer')
	}
}

/**
 * Returns a random string. Just to specify bot message to the user.
 */
function randomstring(length = 20) {
	let output = '';

	// magic function
	var randomchar = function () {
		var n = Math.floor(Math.random() * 62);
		if (n < 10) return n;
		if (n < 36) return String.fromCharCode(n + 55);
		return String.fromCharCode(n + 61);
	};

	while (output.length < length) output += randomchar();
	return output;
}

//A function to display buttons to the user
function showBotMessageButton(){
}

/**
 * Set initial bot message to the screen for the user.
 */
$(window).on('load', function () {
	showBotLessonMessage("Hello there! Please select the lessons you want questions from<br>1. introduction to computer<br>2. concept of it<br>3. data representation<br>4. data communication and networking<br>5. database management<br>6. system analysis and design<br>7. web programming<br>8. computer operating system<br>9. programming fundamentals<br>10. fundamental of digital circuits it in business<br>11. new trends and future directions of it<br>12. internet of things<br>13. web development<br>14. fundamentals of digital circuits");
});
