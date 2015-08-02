
//function that listens to Socket and do something when notification comes
function listen() {
    var source = new WebSocket('ws://' + window.location.host + '/ws');
    var parent = document.getElementById("mycol")
    source.onmessage = function(msg) {
    var message = JSON.parse(msg.data);
    console.log(message);
    //Return random color for superhero
    
    var child = document.createElement("DIV");
    child.className = 'ui red message';
    
    var text = message['new_val']['name'].toUpperCase() + ' joined the league on  '+ Date(); 
    var content = document.createTextNode(text);
    child.appendChild(content);
    parent.appendChild(child);
    return false;
    }
}

$(document).ready(function(){
console.log('I am ready'); 
listen();
});
