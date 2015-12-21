var configName;
var traceName;

function loadConfig(type, savedSettings, savedU2000Settings, show){
      console.log('loadConfig: Type = ', type);
      if (type == 'sU2001A') {
        var sconfigName = savedU2000Settings.config_name;
        var scorrectionFreq = savedU2000Settings.correction_frequency;
        var soffset = savedU2000Settings.offset;
        var sunits = savedU2000Settings.units;
        var savgCountAuto = savedU2000Settings.averaging_count_auto;
        var srangeAuto = savedU2000Settings.range_auto;
        var spassFail = savedU2000Settings.pass_fail;
        var sminPass = savedU2000Settings.min_value;
        var smaxPass = savedU2000Settings.max_value;
        var d = document.getElementById('PMConfigSettings');

        var children = d.childNodes;
        console.log('PMConfig: children = ', children);

        children[1].children[1].value = savedSettings.active_testplan_name;
        children[3].children[1].value = sconfigName;
        children[5].children[1].value = scorrectionFreq;
        children[7].children[1].value = soffset; 
        children[9].children[1].value = sunits;
        console.log("averaging_count_auto: ", savgCountAuto)
        avgCountAuto = children[11].children[1].checked = (savgCountAuto === 'True'); 
        rangeAuto = children[13].children[1].checked = (srangeAuto === 'True');
      } else {
        console.log('No type match')
      };
      if (sconfigName != 'working') {
        $('#collapsePMConfig').collapse("show");
      }
};

//PM CONFIG FORM SUBMIT
function PMConfig() {
      $('#collapsePMConfig').collapse("hide");

      var d = document.getElementById('PMConfigSettings');
      var children = d.childNodes;
      console.log('PMConfig: children = ', children);

      traceName = children[1].children[1].value;
      configName = children[3].children[1].value;
      traceName = validateInput(traceName);
      configName = validateInput(configName);

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


function validateInput(input) {
        console.log(input);
        console.log("TYPE: ", typeof input);
        input = input.replace(/ +$/, "");
        input = input.replace(/\s+/g, '-');
        return input;
    };


function PMtraceStart(el){
      console.log('traceStart !!!!!')
      //formatStartUrl = raw_urlPath.split('/');
      var startValue = 'Start_Trace';
      var company = document.getElementById('company_nickname').value;
      var start_url = window.location.origin + '/panelcontrol/' + company + '/' + gConfigVars.hardwareName + '/' + configName + '/' + traceName;// + formatStartUrl[formatStartUrl.length-2];
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
      var company = document.getElementById('company_nickname').value;
      var start_url = window.location.origin + '/panelcontrol/' + company + 
      '/' + gConfigVars.hardwareName + '/' + configName + '/' + traceName;
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
      var company = document.getElementById('company_nickname').value;
      var start_url = window.location.origin + '/panelcontrol/' + company + 
      '/' + gConfigVars.hardwareName + '/' + configName + '/' + traceName;
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
      var company = document.getElementById('company_nickname').value;
      var start_url = window.location.origin + '/panelcontrol/' + company + 
      '/' + gConfigVars.hardwareName + '/' + configName + '/' + traceName;
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
      PMtraceStart()
    });
    //   $(this).text(function(i, v){
    //   return v === 'STOP' ? 'CAPTURE' : 'STOP'
    //   })
    //   var el = this;
    //   return (el.t = !el.t) ? PMtraceStart(el) : PMtraceStop(el);
    // });


var resultsTrigger;
function powerMeterData() {
  console.log('PowerMeter START!');
      var company = document.getElementById('company_nickname').value;
      test_info_url = window.location.origin + '/u2000_traceresults/' + company + '/' + gConfigVars.hardwareName + '/' + configName ; //unhard code company and hardware asap
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
        var company_nickname = company;
        var hardware_name = gConfigVars.hardwareName;
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
        
        // For comment form 
        document.getElementById("measurementValue").innerHTML = measurement;
        document.getElementById("start_tse").value = start_tse;
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
      
      var company = document.getElementById('company_nickname').value;
      var saveValue = status;
      var save_url = window.location.origin + '/datamgmt/u2000' + '/' + company + '/' + gConfigVars.hardwareName;
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

function PMStatusUpdate(){
      var company = document.getElementById('company_nickname').value;
      var status_url = window.location.origin + '/status/' + company + '/' + gConfigVars.hardwareName;
      // console.log('STATUS CHECK URL: ', status_url);
      $.ajax({
          type: "GET",
          url: status_url,
          dataType: 'json',
       }).done(function (results) {
        var statusUpdate
        if (results) { 
          console.log('STATUS: ', results.status);
          statusUpdate = results.status;
        }
        else { 
          console.log("NO STATUS UPDATE!");
          statusUpdate = "NULL"
        }
        document.getElementById("PMcurrentStatus").innerHTML = statusUpdate;
      });
}
