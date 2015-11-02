function powerMeter() {
  console.log('PowerMeter');
      test_info_url = 'https://gradientone-test.appspot.com/traceresults/Acme/Tahoe/Primetime';
      $.ajax({
          async: true,
          url: test_info_url,
          dataType: 'json',
       }).done(function (results) { 
        console.log('Power Meter results = ', results);      
        testInfo = results;  
        
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
        //document.getElementById("hardwareName").innerHTML = hardwareName;
       });
    //exploreTimerID = setTimeout(exploreMode,50);
};