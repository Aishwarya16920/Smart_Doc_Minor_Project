var number = 0;

//Function that replies back
function botAns(userInput) {
    //split the input into an array of strings whenever a blank space is encountered
    const arr = userInput.split(" ");

    //loop through each element of the array and capitalize the first letter
    for (var i = 0; i < arr.length; i++) {
        arr[i] = arr[i].charAt(0).toUpperCase() + arr[i].slice(1);

    }

    //Join all the elements of the array back into a string using a blankspace as a separator 
    const modInput = arr.join(" ");

    //div element which holds the input
    var user = document.createElement('div');
    var bot = document.createElement('div');

    //Assigning the class
    user.className = 'msg user';
    bot.className = 'msg bot';

    //TextNode to display the input given by user 
    var userEntry = document.createTextNode(userInput);
    document.getElementById('sub').appendChild(user);
    let x = document.getElementsByClassName('user');
    x[number].appendChild(userEntry);
    number += 1;

    //Passing the input entered by user to Flask app
    $.get('/get', { msg: modInput }).done(function(data) {
        //TextNode to display the reply given by bot
        readOutLoud(data);
        botRpl = document.createTextNode(data);
        document.getElementById('sub').appendChild(bot);
        let y = document.getElementsByClassName('bot');
        y[number].appendChild(botRpl);

        //Clearing the textbox after sending the message
        document.getElementById('send').value = '';
    })
}
//Function that reads out loud 
function readOutLoud(speak) {
    let speech = new SpeechSynthesisUtterance();

    speech.lang = "en-US";
    speech.text = speak;
    speech.volume = 1;
    speech.rate = 1;
    speech.pitch = 1;

    window.speechSynthesis.speak(speech);
}


//Function that Gets the input given by user
function myKeypress(e) {
    if (window.event) {
        if (e.keyCode == 13) {

            //Auto Scroll
            $('#sub').scrollTop($('#sub').scrollTop() + 100);

            var entry = document.getElementById('send').value;
            //Passing the data given by user to a function that will reply back
            botAns(entry)
        }
    }
}

//Making the microphone work
function myClick(e) {
    document.getElementById('microphoneAction').style.display = 'flex';
    document.getElementById('stop').style.display = 'flex';

    //Speech recognition object
    var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition;
    var recognition = new SpeechRecognition();

    //Runs when the speech recognition starts
    recognition.onstart = function() {
        document.getElementById('microphoneAction').innerHTML = "Listening..Please Speak!";
    };

    //Runs When user is done speaking
    recognition.onspeechend = function() {
        recognition.stop();
        document.getElementById('microphoneAction').style.display = 'none';
        document.getElementById('stop').style.display = 'none';
    }

    //Runs when the speech recognition returns result
    recognition.onresult = function(event) {
        var userMicrophone = event.results[0][0].transcript;
        //Getting the ans from the bot
        botAns(userMicrophone);

    };

    // Start recognition
    recognition.start();

    //Stop recognition
    document.getElementById('stop').addEventListener('click', (e) => {
        recognition.stop();
        document.getElementById('microphoneAction').style.display = 'none';
        document.getElementById('stop').style.display = 'none';

    });
}