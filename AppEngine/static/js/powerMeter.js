function powerMeterStart() {
  console.log('PowerMeter START!');
      //test_info_url = 'https://gradientone-test.appspot.com/u2000_traceresults/Acme/MSP/Production';
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
    //exploreTimerID = setTimeout(exploreMode,50);
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

      var configSettings = document.getElementById('settingsDisplay');
      var setChildren = configSettings.childNodes;



      //setChildren[1].children[1].innerHTML = configName;
      //setChildren[3].children[1].innerHTML = configSampleSize;
      //setChildren[1].children[3].innerHTML = traceName;
      //setChildren[3].children[3].innerHTML = configSampleRate;

      var config_url = window.location.origin + '/u2000_configinput';
      console.log('saveStatus: config_url = ',config_url);

      var configSettings = JSON.stringify({"config_name":configName,"trace_name":traceName, "correction_frequency":frequencyCorrection,
       "offset":offset, "units":units, "avg_count_auto":avgCountAuto, "range_auto":rangeAuto, "hardware_name":"Tahoe",
       "inst_name":"BitScope","company_nickname":"Acme"});
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


//POWER METER START and STOP
$("#powerMeterStartStop").click(function() {
      $(this).text(function(i, v){
      return v === 'STOP' ? 'START' : 'STOP'
      })
      var el = this;
      return (el.t = !el.t) ? powerMeterStart(el) : powerMeterStop(el);
    });