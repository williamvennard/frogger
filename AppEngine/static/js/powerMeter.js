function powerMeterStart() {
  console.log('PowerMeter START!');
      //test_info_url = 'https://gradientone-test.appspot.com/u2000_testresults/Acme/batch1/Production';
      test_info_url = window.location.origin + '/u2000_testresults/Acme/batch1/Production';
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
        
        //DECIMATED DATA
        //var decData = testInfo.window_bscope.cha;
        //console.log('getTestInfo: decData =',decData);
        //drawDecChart(decData);

        //testSettings = testInfo.p_settings;
        //testSliceStart = testSettings.Start_TSE;    
        //decPointSpacing = (Number(testSettings.Dec_msec_btw_samples))/1000000;
        //decPointSpacing = (0.002)   
        //console.log('exploreMode: decPointSpacing = ', decPointSpacing);
        //instrumentName = 'Instrument: ' + testInfo.config_name;
        //hardwareName = 'Hardware: ' + testInfo.hardware_name;
        //document.getElementById("instrumentName").innerHTML = instrumentName;
        document.getElementById("measurementValue").innerHTML = measurement;
       });
    //exploreTimerID = setTimeout(exploreMode,50);
};

$("#powerMeterStartStop").click(function() {
      $(this).text(function(i, v){
      return v === 'STOP' ? 'START' : 'STOP'
      })
      var el = this;
      return (el.t = !el.t) ? powerMeterStart(el) : powerMeterStop(el);
    });