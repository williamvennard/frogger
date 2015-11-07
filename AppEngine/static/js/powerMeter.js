function PMtraceStart(el){
      console.log('traceStart !!!!!')
      //formatStartUrl = raw_urlPath.split('/');
      //https://gradientone-test.appspot.com/panelcontrol/Acme/Tahoe/Primetime
      var startValue = 'Start_Trace';
      var start_url = window.location.origin + '/panelcontrol/Acme/Tahoe/Primetime';// + formatStartUrl[formatStartUrl.length-2];
      console.log('exploreStart: start_url =',start_url);
      var startData = JSON.stringify({"command":startValue});
      console.log('exploreStart: startData =', startData);
     $.ajax({
        type: "POST",
        url: start_url,
        data: startData,
        dataType: 'json',
        success: function(data, textStatus, jqXHR)
        {
          console.log('saveStatus: Ajax post was a success!');
        },
      });
      powerMeterData();
    };
    function PMtraceStop(el){
      console.log('traceStop !!!!!')
      
      var startValue = 'Stop_Trace';
      var start_url = window.location.origin + '/panelcontrol/Acme/Tahoe/Primetime';// + formatStartUrl[formatStartUrl.length-2];
      console.log('exploreStart: start_url =',start_url);

      var startData = JSON.stringify({"command":startValue});
      console.log('exploreStart: startData =', startData);
     $.ajax({
        type: "POST",
        url: start_url,
        data: startData,
        dataType: 'json',
        success: function(data, textStatus, jqXHR)
        {
          console.log('saveStatus: Ajax post was a success!');
        },
      });
      clearTimeout(traceTimerID);
    };


//POWER METER START and STOP
$("#powerMeterStartStop").click(function() {
      $(this).text(function(i, v){
      return v === 'STOP' ? 'START' : 'STOP'
      })
      var el = this;
      return (el.t = !el.t) ? PMtraceStart(el) : PMtraceStop(el);
    });



function powerMeterData() {
  console.log('PowerMeter START!');
      //test_info_url = 'https://gradientone-test.appspot.com/u2000_traceresults/Acme/MSP/Tahoe';
      test_info_url = window.location.origin + '/u2000_traceresults/Acme/MSP/Production';
      $.ajax({
          async: true,
          url: test_info_url,
          dataType: 'json',
       }).done(function (results) { 
        console.log('powerMeterStart: Power Meter results = ', results);      
        var testInfo = results;  

        var measurement = testInfo.cha;
        console.log('powerMeterStart: cha', measurement);

        //def get(self,company_nickname="", hardware_name="",config_name="",start_tse=""):
        //u2000data
        
        document.getElementById("measurementValue").innerHTML = measurement;
       });
    traceTimerID = setTimeout(traceMode,1000);
};








//PM CONFIG FORM SUBMIT
    function PMConfig() {
      $('#collapseConfig').collapse("hide");
      var d = document.getElementById('PMConfigSettings');

      var children = d.childNodes;
      console.log('PMConfig: children = ', children);
      var configName = children[1].children[1].value;
      var traceName = children[3].children[1].value;

      var frequencyCorrection =  children[5].children[1].value;
      var offset = children[7].children[1].value; 
      var units = children[9].children[1].value; 
      var avgCountAuto = children[11].children[1].checked; 
      var rangeAuto = children[13].children[1].checked;

      var configSettings = document.getElementById('PMSettingsDisplay');
      var setChildren = configSettings.childNodes;



      setChildren[1].children[1].innerHTML = configName;
      setChildren[3].children[1].innerHTML = frequencyCorrection;
      setChildren[1].children[3].innerHTML = traceName;
      setChildren[3].children[3].innerHTML = offset;

      document.getElementById("PMUnits").innerHTML = units;
    

      var config_url = window.location.origin + '/u2000_configinput';
      console.log('saveStatus: config_url = ',config_url);

      var configSettings = JSON.stringify({"config_name":configName,"trace_name":traceName, "correction_frequency":frequencyCorrection,
       "offset":offset, "units":units, "avg_count_auto":avgCountAuto, "range_auto":rangeAuto, "hardware_name":"Tahoe",
       "inst_name":"U2001A","company_nickname":"Acme"});

      console.log('instConfig: configSettings = ',configSettings);

     $.ajax({
        type: "POST",
        url: config_url,
        data: configSettings,
        dataType: 'json',
        success: function(data, textStatus, jqXHR)
        {
            console.log('saveStatus: Ajax post was a success!');
        },
      }); 
    };


