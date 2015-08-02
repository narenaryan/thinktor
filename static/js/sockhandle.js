
//function that listens to Socket and also sets on message handler
function listen() {
    var source = new WebSocket('ws://' + window.location.host + '/ws');
    var parent = document.getElementById("myul")
    source.onmessage = function(msg) {
    var message = JSON.parse(msg.data);
    console.log(message);
    //Create list element
    var child = document.createElement("LI");
    //Append it to UL
    var text = message['new_val']['name'].toUpperCase() + ' joined the league on  '+ Date(); 
    var content = document.createTextNode(text);
    child.appendChild(content);
    parent.appendChild(child)
    return false;
    }
}

$(document).ready(function(){
console.log('I am ready');
listen();
});
