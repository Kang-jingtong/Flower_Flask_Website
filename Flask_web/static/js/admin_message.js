//发送按钮点击
function sendMessageBt(){
    var input = document.getElementsByClassName('chat-input')[0];
    var text = input.value;
    if(text==''){
        alert("Reponse can not be empty");
    }
    //console.log(text);
    else{
        
        input.value='';
    }
}

//将消息添加到聊天界面
function addMessage(text){
    var message = document.createElement('p');
    var chat_line = document.getElementsByClassName('chat-line')[0];
    message.innerText = text;
    chat_line.appendChild(message);
    
}

//输入框的按下事件
function inputKeyDown(event){
    //console.log(event);
    //判断是否按下回车键
    if(event.keyCode == 13){
        var input = event.target;
        var text = input.value;
        if(event.ctrlKey){
            // Ctrl + Enter 换行
            input.value = text + '\n';
        }
        else{
            //组织默认行为
            event.preventDefault();
            // Enter 发送消息
            sendMessageBt();
        }
    }
}