
    var timerVar;
    var compl;

    var JSONpreface = '{ "version" : "AS.1", "action" : ';

    function iframeToParent(message){
      window.parent.postMessage(message, "https://www.assistments.org");
      }

    function iframeLoaded(){
      iframeToParent(JSONpreface + '"loaded" }');

      timerVar = window.setInterval("iframeHeartbeat()", 10000);
      }

    // Sends the "heartbeat" message
    function iframeHeartbeat() {
      iframeToParent(JSONpreface +  '"heartbeat"}');
    }

    function close_session(){
        $.getJSON('/_cleanup');
    };

    function iframeCompleted(answer) {
        var score = 1;
        var ans = "Student worked hard on this problem."

        if (answer){
            ans = answer
        }

        iframeToParent(JSONpreface + '"completed", '+ '"answer" : "<b>'
                + ans +'</b>",'+ '"score" : ' + score +' }');

        window.clearTimeout(timerVar);
        window.clearTimeout(compl);
    }
