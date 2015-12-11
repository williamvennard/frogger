//PM CONFIG FORM SUBMIT
var configName;
var traceName;
var company = '{{profile.company_nickname}}';
var hardware = gConfigVars.hardwareName;

function OPConfig(instrument_config) {

      configName = instrument_config.configName;
      traceName = instrument_config.traceName;
      frequencyCorrection = instrument_config.frequencyCorrection;
      offset = instrument_config.offset;
      units = instrument_config.units;
      avgCountAuto = instrument_config.avgCountAuto;
      rangeAuto = instrument_config.rangeAuto;

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
       "offset":offset, "units":units, "avg_count_auto":avgCountAuto, "range_auto":rangeAuto, "hardware_name": hardware,
       "inst_name":"U2001A","company_nickname":"{{profile.company_nickname}}"});

      console.log('instConfig: configSettings = ',configSettings);

     // $.ajax({
     //    type: "POST",
     //    url: config_url,
     //    data: configSettings,
     //    dataType: 'json',
     //    success: function(data, textStatus, jqXHR)
     //    {
     //        console.log('saveStatus: Ajax post was a success!');
     //    },
     //  }); 
    };  

function PMtraceStart(el){
      console.log('traceStart !!!!!')
      //formatStartUrl = raw_urlPath.split('/');
      var startValue = 'Start_Trace';
      var start_url = window.location.origin + '/panelcontrol/' + company + '/' + hardware + '/' + configName + '/' + traceName;// + formatStartUrl[formatStartUrl.length-2];
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
      var start_url = window.location.origin + '/panelcontrol/' + company + '/' + hardware + '/' + configName + '/' + traceName;
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


//POWER METER START and STOP
$("#powerMeterStartStop").click(function() {
      $(this).text(function(i, v){
      return v === 'STOP' ? 'START' : 'STOP'
      })
      var el = this;
      return (el.t = !el.t) ? PMtraceStart(el) : PMtraceStop(el);
    });


var resultsTrigger;
function powerMeterData() {
  console.log('PowerMeter START!');
      test_info_url = window.location.origin + '/u2000_traceresults/' + company + '/' + hardware + '/' + configName;
      $.ajax({
          async: true,
          url: test_info_url,
          dataType: 'json',
       }).done(function (results) { 
        console.log('powerMeterStart: Power Meter results = ', results);      
        var testInfo = results;
        resultsTrigger = results;

        var measurement = testInfo.cha;
        console.log('powerMeterStart: cha', measurement);

        var start_tse = testInfo.start_tse
        console.log('powerMeterStart: start_tse', start_tse);

        document.getElementById('start_tse').value = start_tse;
        document.getElementById("measurementValue").innerHTML = measurement;
        
        var max_pass_value = document.getElementById("max_pass_value").value;
        var min_pass_value = document.getElementById("min_pass_value").value;
        var pass_fail
        if (min_pass_value <= measurement && measurement <= max_pass_value){
          pass_fail = "PASS"
          document.getElementById('pass_feedback').innerHTML = pass_fail
          document.getElementById('fail_feedback').innerHTML = ""
        } else {
          pass_fail = "FAIL"
          document.getElementById('fail_feedback').innerHTML = pass_fail;
          document.getElementById('pass_feedback').innerHTML = "";
        };
        var results_data = JSON.stringify({"config_name":configName,
          "trace_name":traceName, "start_tse":start_tse, "pass_fail":pass_fail,
          "max_pass_value":max_pass_value, "min_pass_value":min_pass_value,});
        ResultsUpdate(results_data)
       });
    PMtraceTimerID = setTimeout(powerMeterData,1000);
    //stop when there is data
    if (!(resultsTrigger = 'none')) {
      clearTimeout(PMtraceTimerID);
   };

};

function ResultsUpdate(results_data) {
      var update_url = window.location.origin + '/u2000_update_results';
      console.log('saveStatus: update_url = ',update_url);
      console.log('instResults: results_data = ',results_data);

     $.ajax({
        type: "POST",
        url: update_url,
        data: results_data,
        dataType: 'json',
        success: function(data, textStatus, jqXHR)
        {
            console.log('saveStatus: Update results post was a success!');
        },
      }); 
    };  
// function updateTestResults() {
//     var runner = new XMLHttpRequest();
//     runner.open('POST', 'URL', true);
//     runner.send();
//     return runner;
// }
