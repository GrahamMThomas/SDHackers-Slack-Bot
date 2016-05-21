var RtmClient = require('slack-client').RtmClient;
var RTM_EVENTS = require('slack-client').RTM_EVENTS;
var CLIENT_EVENTS = require('slack-client').CLIENT_EVENTS;
var RTM_CLIENT_EVENTS = require('slack-client').CLIENT_EVENTS.RTM;
var PythonShell = require('python-shell');
var waiting = false;
var mainChannel = 'C0NATP5B8'
var announcementChannel = 'C0W07UEUF'
var rtm = new RtmClient("token", {logLevel: 'none'});;

//This channel is the direct message between me/bot
//var mainChannel = 'D0TKTGN05'


//Meetups
var meetups = ["","","","",""];

//Since the Python Shell module is weird,
//I use this variable as a method of "return"
var pythonOutput = 'pythonOutput';


console.log("Booting up hackerbot...");

// fs.readFile("Txts/magical.txt", 'utf8', function(err, data) {
//   if (err) throw err;
//   tokens.token = data;
//   console.log(tokens.token)  
// });

var rtm = new RtmClient(process.argv[2], {logLevel: 'none'}); 
console.log("RTM Started:" + process.argv[2]);


rtm.start(); 


/*
Usage:  Call with python file name + directory
		and receive the first print statement
		from the python program.
*/
function runPythonScript(file)
{
	
	waiting = true;
	PythonShell.run(file, function (err, results) 
	{
		
		//If an error occurs send a slack message containing it and kill the bot.
		if (err) 
			{
				sendToSlack('Something broke...', mainChannel);
				//Have to give the program 3 seconds to send the error to slack.
				setTimeout(function(){ throw err; }, 3000);
				
			}

		//return the first print statement from the python program.
		try
		{	
			//Set pythonOutput so other methods can pull this var
			setPythonOutput(results[0]);		
			console.log(pythonOutput);
		}
		catch(err){}
	});
	waiting = false;

}

/*
PLEASE NOTE THIS METHOD--------------
	Either the PythonShell module really sucks
	or I am using it wrong. I created a very dirty work
	around... Had my make a global variable and call this 
	functions to set it. Please PM me if you can find a fix.
*/
function setPythonOutput(variable)
{
	pythonOutput = variable;
}

/*
Usage:  Give message and channel to 
		send message to Slack
*/
function sendToSlack(messageToSend, channel)
{
	//Using slack api, send the message to the designated channel
	rtm.sendMessage(messageToSend, channel, function messageSent() { });
}

/*
Usage:  When a person joins a channel
		print welcome message and then a quote
*/
function onChannelJoin(message)
{
	console.log("Welcoming Newbie...\n");

	runPythonScript('Python/retriever_comments.py');
	setTimeout(function()
	{ 
		var messageToSend = "  Welcome <@" + message.user + ">! " + pythonOutput;
		sendToSlack(messageToSend, message.channel);
	}, 250);
		
}

/*
Usage:  Call python file and receive
		a quote. Then send to slack.
*/
function startSendQuote(message)
{
	runPythonScript('Python/retriever_comments.py');
	setTimeout(function()
	{ 
		sendQuote(message, pythonOutput);
	}, 250);
}
function sendQuote(commandMessage, quote)
{
	//Need to give time to access the python file before printing.
	sendToSlack(quote, mainChannel);		
}

/*
Usage:  If a message is in the main Channel, tell
		the user to not insult in my channel, because
		that is rude. If the user did not add a user
		to insult, call them crazy. If neither of those,
		call a python file to receive an insult. Give a 1
		in 5 chance to reveal the insulter. Send final
		message to slack.
*/
function startSendInsult(message)
{
	//If the user says the command in 
	//a channel other than the main channel
	if(message.channel != mainChannel)
	{
		runPythonScript('Python/retriever_insults.py');
		setTimeout(function()
		{ 
			sendInsult(message, pythonOutput);
		}, 250);
	}
	else
	{
		messageToSend = "<@" + message.user + "> tried to insult in public.";
		sendToSlack(messageToSend, mainChannel);
	}
	
}
function sendInsult(commandMessage, insult)
{
	var messageToSend;
	//If there is text after the command.
	if(commandMessage.text.length > 8)
	{
		//Make a one in five chance to reveal the insulter
		var randnum = Math.random()*5;
		var culprit = '';
		if (Math.floor(randnum) == 0)
		{
			culprit = "  Sender: <@" + commandMessage.user + ">";
		}
		console.log("uutp " + pythonOutput)
		
		messageToSend = commandMessage.text.substring(7,20) + " " + insult + culprit;
		sendToSlack(messageToSend, mainChannel);
		
	}
	else
	{
		messageToSend = "<@" + commandMessage.user + "> tried to insult the wall.";
		sendToSlack(messageToSend, mainChannel);
	}
}

/*
Usage:  Add meetup to the meetups array. Make
		the added meetup at the top of the list
		and push the rest to the bottom
*/
function addMeetup(message)
{
	for(i = 5; i > 0; i--)
	{
		meetups[i] = meetups[i-1];
	}
	meetups[0] = message.text.substring(10);
}

/*
Usage:  Send the meetups array to slack in a
		nice format. Only send meetups that 
		exist.
*/
function sendMeetup(message)
{
	var messageToSend = ''
	for(i = 0; i < 5; i++)
	{
		//If meetup was added...
		if(meetups[i] != "")
		{
			messageToSend = messageToSend + (i+1) + ". " + meetups[i] + "\n";
		}
	}
	sendToSlack(messageToSend, mainChannel);		    	
}

/*
Usage:  Automatically redirect messages sent
		to the Annoucement channel into the 
		main channel.
*/
function sendAnnouncement(message)
{
	sendToSlack("*ANNOUNCEMENT!*\n <@" + message.user + ">: " + message.text, mainChannel);
}

rtm.on(RTM_EVENTS.MESSAGE, function (message) {
	console.log("Got Message");
    console.log(message);
    if (!waiting)
    {
    	try
    	{
    		if(message.channel != announcementChannel)
    		{
		    	if(message.subtype == 'channel_join')
			    {
			  		onChannelJoin(message);
			    }

			    if(message.text == "!quote")
			    {
			    	console.log("Finding Quote....\n");
			  		startSendQuote(message);
			    }

			    if(message.text.substring(0,7) == "!insult")
			    {
			    	console.log("Finding Insult....\n");
			    	startSendInsult(message);	
			    }

			    if(message.text.substring(0,10) == "!meetupadd")
			    {
			    	addMeetup(message);	
			    }

			    if(message.text.substring(0,11) == "!getstarted")
			    {
			    	sendToSlack("Getting Started: https://github.com/SDHackers/Start-here", mainChannel);
			    }

			    if(message.text.substring(0,13) == "!walkthroughs")
			    {
			    	sendToSlack("Walkthroughs: https://github.com/SDHackers/Walkthroughs", mainChannel);
			    }

			    if(message.text.substring(0,5) == "!help")
			    {
			    	sendToSlack("!quote - Random Quote \n
					    		!insult - Random Insult \n
					    		!meetup - List recent meetups \n
					    		!meetupadd - Add Meetup to !meetup command\n
					    		!getstarted - Get Started with SDHackers Github \n
					    		!walkthroughs - Get Walkthroughs with SDHackers Github", mainChannel);
			    }

			    if(message.text.substring(0,7) == "!meetup" )
			    {
			    	sendMeetup(message);
			    }
			}
			else
			{
				sendAnnouncement(message);	
			}
		}
		catch(err)
		{
			//console.log(err)
		}
	}
});