//PM CONFIG FORM SUBMIT
var configName;
var traceName;

function loadConfig(type, savedSettings){
      console.log('loadConfig: Type = ', type);
      if (type == 'sU2001A') {
        var sconfigName = savedSettings.config_name;
        var scorrectionFreq = savedSettings.correction_frequency;
        var soffset = savedSettings.offset;
        var sunits = savedSettings.units;
        var savgCountAuto = savedSettings.averaging_count_auto;
        var srangeAuto = savedSettings.range_auto;
        var spassFail = savedSettings.pass_fail;
        var sminPass = savedSettings.min_value;
        var smaxPass = savedSettings.max_value;
        var d = document.getElementById('PMConfigSettings');

        var children = d.childNodes;
        console.log('PMConfig: children = ', children);

        children[1].children[1].value = sconfigName;
        children[3].children[1].value = 'DefaultTraceName'

        children[5].children[1].value = scorrectionFreq;
        children[7].children[1].value = soffset; 
        children[9].children[1].value = sunits;
        console.log("averaging_count_auto: ", savgCountAuto)
        avgCountAuto = children[11].children[1].checked = (savgCountAuto === 'True'); 
        rangeAuto = children[13].children[1].checked = (srangeAuto === 'True');
      } else {
        console.log('No type match')
      };
      $('#collapsePMConfig').collapse("show");
};
function PMConfig() {
      $('#collapsePMConfig').collapse("hide");

      var d = document.getElementById('PMConfigSettings');
      var children = d.childNodes;
      console.log('PMConfig: children = ', children);

      configName = children[1].children[1].value;
      traceName = children[3].children[1].value;
      
      var company = document.getElementById('company_nickname').value;
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
       "offset":offset, "units":units, "avg_count_auto":avgCountAuto, "range_auto":rangeAuto, "hardware_name": gConfigVars.hardwareName,
       "inst_name":"U2001A","company_nickname":company, });

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


function PMtraceStart(el){
      console.log('traceStart !!!!!')
      //formatStartUrl = raw_urlPath.split('/');
      var startValue = 'Start_Trace';
      var start_url = window.location.origin + '/panelcontrol/' + 'Acme' + '/' + 'Tahoe' + '/' + configName + '/' + traceName;// + formatStartUrl[formatStartUrl.length-2];
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
      var start_url = window.location.origin + '/panelcontrol/' + 'Acme' + 
      '/' + 'Tahoe' + '/' + configName + '/' + traceName;
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
      clearTimeout(PMtraceTimerID);
    };

function PMruntraceStart(el){
      console.log('runStart !!!!!')
      //formatStartUrl = raw_urlPath.split('/');
      var startValue = 'Start_Run';
      var start_url = window.location.origin + '/panelcontrol/' + 'Acme' + 
      '/' + 'Tahoe' + '/' + configName + '/' + traceName;
      console.log('runStart: start_url =',start_url);

      var startData = JSON.stringify({"command":startValue});
      console.log('runStart: startData =', startData);
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
    }
    function PMruntraceStop(el){
      console.log('runStop!!!!!')
      //formatStartUrl = raw_urlPath.split('/');
      
      var startValue = 'Stop_Run';
      var start_url = window.location.origin + '/panelcontrol/' + 'Acme' + 
      '/' + 'Tahoe' + '/' + configName + '/' + traceName;
      console.log('runStart: start_url =',start_url);

      var startData = JSON.stringify({"command":startValue});
      console.log('runStart: startData =', startData);
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
      clearTimeout(PMtraceTimerID);
    };

//POWER METER RUN START and STOP
$("#powerMeterRunStartStop").click(function() {
      $(this).text(function(i, v){
      return v === 'STOP' ? 'RUN' : 'STOP'
      })
      var el = this;
      return (el.t = !el.t) ? PMruntraceStart(el) : PMruntraceStop(el);
    });

//POWER METER START and STOP
$("#powerMeterStartStop").click(function() {
      $(this).text(function(i, v){
      return v === 'STOP' ? 'CAPTURE' : 'STOP'
      })
      var el = this;
      return (el.t = !el.t) ? PMtraceStart(el) : PMtraceStop(el);
    });


var resultsTrigger;
function powerMeterData() {
  console.log('PowerMeter START!');
      test_info_url = window.location.origin + '/u2000_traceresults/' + 'Acme' + '/' + 'Tahoe' + '/' + configName ; //unhard code company and hardware asap
      $.ajax({
          async: true,
          url: test_info_url,
          dataType: 'json',
       }).done(function (results) { 
        console.log('powerMeterStart: Power Meter results = ', results);      
        var testInfo = results;  
        resultsTrigger = results;

        var measurement = testInfo.cha;
        var start_tse = testInfo.start_tse;
        var company_nickname = "Acme";
        var hardware_name = 'Tahoe';
/*        var config_name = configName;
        var trace_name = configName;*/

        console.log('powerMeterStart: cha', measurement);
        console.log('start_tse: cha', start_tse);

        // needed for comments on results
        var start_tse = testInfo.start_tse
        console.log('powerMeterStart: start_tse', start_tse);
        document.getElementById('start_tse').value = start_tse;

        //def get(self,company_nickname="", hardware_name="",config_name="",start_tse=""):
        //u2000data
        
        document.getElementById("measurementValue").innerHTML = measurement;
        document.getElementById("start_tse").value = start_tse;
        document.getElementById("company_nickname").value = company_nickname;
        document.getElementById("hardware_name").value = hardware_name;
        document.getElementById("config_name").value = configName;
        document.getElementById("trace_name").value = traceName;
       });
    PMtraceTimerID = setTimeout(powerMeterData,1000);
    //stop when there is data
    if (!(resultsTrigger = 'none')) {
      clearTimeout(PMtraceTimerID);
   };
};

function PMSaveStatus(status) {
     document.getElementById("traceSave").disabled = true; 
      console.log('saveStatus: SAVED!!');
      

      var saveValue = status;
      var save_url = window.location.origin + '/datamgmt/u2000' + '/' + '{{profile.company_nickname}}' + '/' + gConfigVars.hardwareName;  //unhard code company and hardware asap
      console.log('saveStatus: save_url = ',save_url);

      var formData = JSON.stringify({"save_status":saveValue,"totalNumPages":totalNumPages,"sliceSize":sliceSize});
      console.log('saveStatus: formData =', formData);
     $.ajax({
        type: "POST",
        url: save_url,
        data: formData,
        dataType: 'json',
        success: function(data, textStatus, jqXHR)
        {
            console.log('saveStatus: Ajax post was a success!');
        },
      }); 

};
