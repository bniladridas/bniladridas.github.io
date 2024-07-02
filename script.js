$(document).ready(function() {
    // Initialize Dialogflow API
    const dialogflow = require('dialogflow');
    const sessionId = 'your-session-id';
    const languageCode = 'en-US';
    const dialogflowAgent = new dialogflow.SessionsClient();
  
    // Set up chatbot input and send button
    const chatbotInput = $('#chatbot-input');
    const chatbotSend = $('#chatbot-send');
  
    // Set up chatbot messages container
    const chatbotMessages = $('#chatbot-messages');
  
    // Function to send message to Dialogflow API
    function sendMessageToDialogflow(message) {
      const request = {
        session: sessionId,
        queryInput: {
          text: {
            text: message,
            languageCode: languageCode,
          },
        },
      };
  
      dialogflowAgent.detectIntent(request)
        .then(response => {
          const intent = response.queryResult.intent;
          const responseText = response.queryResult.fulfillmentText;
          handleDialogflowResponse(intent, responseText);
        })
        .catch(error => {
          console.error('Error sending message to Dialogflow:', error);
        });
    }
  
    // Function to handle Dialogflow response
    function handleDialogflowResponse(intent, responseText) {
      const botResponse = responseText;
      chatbotMessages.append('<div class="chatbot-message bot">' + botResponse + '</div>');
    }
  
    // Send button click event handler
    chatbotSend.on('click', function() {
      const message = chatbotInput.val();
      if (message !== '') {
        chatbotMessages.append('<div class="chatbot-message user">' + message + '</div>');
        chatbotInput.val('');
        sendMessageToDialogflow(message);
      }
    });
  });