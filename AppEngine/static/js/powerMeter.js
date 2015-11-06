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

//CONFIG FORM SUBMIT
    function PMConfig() {
      $('#collapseConfig').collapse("hide");
      var d = document.getElementById('configSettings');
        var children = d.childNodes;
/*
      var configName = children[1].children[1].value;
      var traceName = children[3].children[1].value;
      //var configBand = children[5].children[1].value;
      var configSampleRate =  children[5].children[1].value;
      var configSampleSize = children[7].children[1].value; 
      //var configResolution = children[11].children[1].value; 
      //var configChNum = children[11].children[1].value; 

      var configSettings = document.getElementById('settingsDisplay');
        var setChildren = configSettings.childNodes;



      setChildren[1].children[1].innerHTML = configName;
      setChildren[3].children[1].innerHTML = configSampleSize;
      setChildren[1].children[3].innerHTML = traceName;
      setChildren[3].children[3].innerHTML = configSampleRate;
*/
      var config_url = 'https://gradientone-test.appspot.com/bscopeconfiginput';
      console.log('saveStatus: config_url = ',config_url);

      var configSettings = JSON.stringify({"config_name":configName,"analog_sample_rate":configSampleRate,
       "capture_buffer_size":configSampleSize,"trace_name":traceName, "hardware_name":"Tahoe",
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

$("#powerMeterStartStop").click(function() {
      $(this).text(function(i, v){
      return v === 'STOP' ? 'START' : 'STOP'
      })
      var el = this;
      return (el.t = !el.t) ? powerMeterStart(el) : powerMeterStop(el);
    });