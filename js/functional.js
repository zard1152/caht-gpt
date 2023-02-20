async function callCHATGPT(language,targetElementId='chatgpt-response_D') {
    // var responseText1 = document.getElementById("chatgpt-response");
    var responseText1 = document.getElementById(targetElementId);
    responseText1.innerHTML = ""
    function printMessage(message) {
      var responseText = document.getElementById(targetElementId);
      var index = 0;

      // 创建一个定时器，每隔一段时间打印一个字符
      var interval = setInterval(function() {
        responseText.innerHTML += message[index];
        index++;

        // 当打印完成时，清除定时器
        if (index >= message.length) {
          clearInterval(interval);
        }
      },
      150); // 每隔50毫秒打印一个字符
    }
    var xhr = new XMLHttpRequest();
    // var url = "https://api.openai.com/v1/completions";
    var inputText = document.getElementById("chat-gpt-input").value;
    var url = "http://artclass.eu.org:18081/GetContent";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.setRequestHeader("Authorization", "Bearer 123456");
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4 && xhr.status === 200) {
        var json = JSON.parse(xhr.responseText);
        // var response = json.choices[0].text;
        var response = json.text
        // 将CHATGPT的返回值输出到文本框
        var responseText = document.getElementById(targetElementId);
        var index = 0;

        // 创建一个定时器，每隔一段时间打印一个字符
        var interval = setInterval(function() {
          responseText.innerHTML += response[index];
          index++;

          // 当打印完成时，清除定时器
          if (index >= response.length) {
            clearInterval(interval);
          }
        },
        50); // 每隔50毫秒打印一个字符
      }
    };

    var data = JSON.stringify({
      "prompt": inputText,
      "salf_cdoe": "12354",
      "language_type": language
      // "max_tokens": 2048,
      // "temperature": 0.5,
      // "top_p": 1,
      // "frequency_penalty": 0,
      // "presence_penalty": 0,
      // "model": "text-davinci-003"
    });
    console.log(data);
    await printMessage('正在思考，请等待......');
    await xhr.send(data);
  }

  
function showDiv(textarea_module) {
    var div = document.getElementById(textarea_module);
    div.style.display = "block";
    // if (textarea_module === "div_auto_display_P") {
    //     var div = document.getElementById(textarea_module);
    //     div.style.display = "block";
    //   }
    // else if (textarea_module === "div_auto_display_Si") {
    //     var div = document.getElementById(textarea_module);
    //     div.style.display = "block";
    //   }
    // else if (textarea_module === "div_auto_display_S") {
    //     var div = document.getElementById(textarea_module);
    //     div.style.display = "block";
    //   }
    // else if (textarea_module === "div_auto_display_W") {
    //     var div = document.getElementById(textarea_module);
    //     div.style.display = "block";
    //   }
    // else if (textarea_module === "div_auto_display_C") {
    //     var div = document.getElementById(textarea_module);
    //     div.style.display = "block";
    //   }

    }