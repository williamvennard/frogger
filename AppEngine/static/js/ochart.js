 // SETTING UP FOR LIVE DATA STREAM TEST //

  //VERTICAL KNOBS
    var vZoom = 100;
    var vPosition = 0;
    $(".vPosKnob").knob({
        'release' : function (vPos) { 
          //console.log('knob H pos value:',hPos);  
          vPosition = vPos;
          moveWindow();
      },
    }); 

    $(".vZoomKnob").knob({
      'release' : function (vRange) { 
         //console.log('knob H value:',hRange);
         vZoom = vRange;
         moveWindow();
      },
    }); 
 
  //HORIZONTAL KNOBS
    var hZoom = 1000;
    var hPosition = 0;

    $(".hZoomKnob").knob({
      'release' : function (hRange) { 
         //console.log('knob H value:',hRange);
         hZoom = hRange;
         moveWindow();
      },
    }); 

    $(".hPosKnob").knob({
        'release' : function (hPos) { 
          //console.log('knob H pos value:',hPos);  
          hPosition = hPos;
          moveWindow();
      },
    }); 

  // load chart lib
    google.load('visualization', '1', {packages: ['corechart','table']});

    var testInfo = [];
    var testSettings = [];
    var sliceNames = [];
    var resultsCache = [];
    var hMax = 0;
    var hMin = 0;
    var rawChartOptions = {};
    var totalNumPages = 0;
    var numPages = 0;
    var range = 0;
    var decData;
    var decPointSpacing;
    var decOffset;
    var base_url;
    var dec_url;
    var testSliceStart;
    var rawWidth;
    var test_info_url;
    var rawChart;
    var moveWindowData;
    var sliceSize = 0;
    var dynamicSliceEnd = 0;
    var traceModeCounter = 0;
    var rawPointSpacing;
    var step = 0;
    var traceTimerID;
    var exploreTimerID;

// EXPLORE MODE //

function exploreMode() {
  console.log('exploreMode active');
      test_info_url = 'https://gradientone-test.appspot.com/traceresults/Acme/Tahoe/Primetime';
      $.ajax({
          async: true,
          url: test_info_url,
          dataType: 'json',
       }).done(function (results) { 
        console.log('exploreMode: afterAjax results = ', results);      
        testInfo = results;  
        
        //DECIMATED DATA
        var decData = testInfo.window_bscope.cha;
        console.log('getTestInfo: decData =',decData);
        drawDecChart(decData);

        testSettings = testInfo.p_settings;
        testSliceStart = testSettings.Start_TSE;    
        //decPointSpacing = (Number(testSettings.Dec_msec_btw_samples))/1000000;
        decPointSpacing = (0.002)   
        console.log('exploreMode: decPointSpacing = ', decPointSpacing);
        instrumentName = 'Instrument: ' + testInfo.config_name;
        hardwareName = 'Hardware: ' + testInfo.hardware_name;
        document.getElementById("instrumentName").innerHTML = instrumentName;
        document.getElementById("hardwareName").innerHTML = hardwareName;
       });
    exploreTimerID = setTimeout(exploreMode,50);
};

    //LOADING URL
    //test_info_url = window.location.pathname + '.json';
    // console.log(test_info_url);

    // status updates URL =
    // https://gradientone-test.appspot.com/status/Acme/Tahoe
    var currentTestStatus;
    var statusArray = [];
/*    
    function getTestStatus() {
      //status_url = 'https://gradientone-test.appspot.com/testlibrary/Acme/NyquistB/1437712799600.json';
      status_url = 'https://gradientone-test.appspot.com/status/Acme/Tahoe';
      $.ajax({
          async: true,
          url: status_url,            
          dataType: 'json',
       }).done(function (results) {
          currentTestStatus = results.status.status;
          testStatusTime = results.status.time;
          // have key start, finish, current, config change
          // check value of key current with whats in status history 
          console.log('getTestStatus: currentTestStatus = ',currentTestStatus);
          document.getElementById("currentStatus").innerHTML = currentTestStatus;      
      });
       setTimeout(getTestStatus,200);
    };
    getTestStatus();
*/    
    //Continuously polling at: 
    //https://gradientone-test.appspot.com/testresults/Acme/Tahoe/LED
    function traceMode() {
      console.log('traceMode active');
      test_info_url = 'https://gradientone-test.appspot.com/traceresults/Acme/Tahoe/Primetime';
      $.ajax({
          async: true,
          url: test_info_url,
          dataType: 'json',
       }).done(function (results) {       
        testInfo = results;  

        //testSettings = testInfo;
        //console.log('getTestInfo: testInfo =',testInfo);
        testSettings = testInfo.p_settings;
        //URLS RAW
        raw_urlPath = testInfo.raw_data_url;
        //Test Info RAW
        //testSliceStart = testSettings.start_tse;
        testSliceStart = testSettings.Start_TSE;       
        totalNumPages = testSettings.Total_Slices;
        numPages = Number(testSettings.Total_Slices); //not live version

        rawPointSpacing = (testSettings.Raw_msec_btw_samples)/1000000;  //convert micro s to seconds
        sliceSize = Number(testSettings.Slice_Size_msec);
        console.log('raw_urlPath = ',raw_urlPath);
        rawUrlSplit = raw_urlPath.split(testSliceStart);
        base_url = rawUrlSplit[0];
        sliceEnd = (Number(testSliceStart) + (numPages*sliceSize)) -10;

        rawOffset = Number(testSliceStart) + ((Number(numPages) * Number(sliceSize))/2);
        rawWidth = (Number(numPages) * Number(sliceSize)) * rawPointSpacing;

        instrumentName = 'Instrument: ' + testInfo.config_name;
        hardwareName = 'Hardware: ' + testInfo.hardware_name;
        document.getElementById("instrumentName").innerHTML = instrumentName;
        document.getElementById("hardwareName").innerHTML = hardwareName;

        //if(traceModeCounter < numPages) {
          dynamicSliceEnd = sliceEnd;
          console.log('traceMode: dynamicSliceEnd =',dynamicSliceEnd);
          //(Number(testSliceStart) + getTestInfoCounter*sliceSize );
        //};

        buildSliceNames(Number(testSliceStart),dynamicSliceEnd,sliceSize);
        traceModeCounter++;
      
        name = String(sliceEnd);
        delete resultsCache.name;
        fetchSliceNames();

        console.log('slice names = ',sliceNames);
        //console.log('decOffset = ',decOffset);
        //console.log('getTestInfo: testInfo = ', testInfo);              
        //console.log('getTestInfo: testInfo.Total_Slices = ', numPages);
        //console.log('getTestInfo: testInfo.Dec_msec_btw_samples = ', decPointSpacing);  
        //console.log('getTestInfo: sliceSize = ', sliceSize);   
        //console.log('getTestInfo: rawPointSpacing =',rawPointSpacing);  
       });
         traceTimerID = setTimeout(traceMode,1000);
    };
    
    // DEC CHART CODE //

    // BUILD DEC DATA TABLE AND DRAW DEC CHART
    function drawDecChart(decData) {
        var data = new google.visualization.DataTable();
        data.addColumn('number', 'Time');
        data.addColumn('number', 'Ch1');
        console.log('drawDecChart: decData =',decData.length);
        console.log('drawDecChart: decPointSpacing =',decPointSpacing);

        for (i=0; i<decData.length; i++) {
           var num = i*decPointSpacing;
          //console.log('drawDecChart: num =', num);
           num = Math.ceil(num * 100) / 100;
           data.addRow([
             num, 
             decData[i],
             ]);
        };
        console.log('drawDecChart: data=',data);
        decChartOptions = {
         title: '',
         titleTextStyle: {color:'lightgray', fontSize: 18, fontName: 'NexaLight'},
         legend: 'none', //{alignment:'center', textStyle:{color:'lightgray'}},
         hAxis: {title: 'Time(sec)',titleTextStyle:{color:'lightgray', fontName: 'NexaLight'}, textStyle:{color:'lightgray'}, baselineColor:'white', gridlines:{color: 'gray', count: 6}, minorGridlines:{color: 'gray', count: 1}, viewWindowMode:'explicit'}, //viewWindow:{max: hMax, min: hMin}},
         vAxis: {title: '', titleTextStyle:{color:'lightgray'}, textStyle:{color:'lightgray'}, baselineColor:'white', gridlines:{color: 'gray', count: 6}, minorGridlines:{color: 'gray', count: 1}, format: '##.###', viewWindowMode:'explicit', },
         backgroundColor: {fill:'none', stroke: 'black', strokeWidth: 0,},                 
         colors: ['rgb(2,255,253)','rgb(239,253,146)'],
         chartArea:{backgroundColor:'', height:350, width:445},
         lineWidth: 2.5,
         curveType: 'function',
         crosshair: {trigger: 'both', selected:{opacity: 0.8}, focused:{opacity:0.8}},
         explorer: {maxZoomOut: 5, maxZoomIn: 0.125},
        };
      //DRAW CHART
         var chart = new google.visualization.LineChart($('#oChart').get(0));      
         chart.draw(data, decChartOptions);
      //DRAW TABLE
         var table = new google.visualization.Table($('#oTable').get(0));
         table.draw(data); 
    };

// RAW CHART CODE //
    var savedData = 0;
// BUILD RAW DATA TABLE AND DRAW RAW CHART+TABLE
    function drawRawChart(){   
      var data = new google.visualization.DataTable();
      savedData = data;
      data.addColumn('number', 'Time');
      data.addColumn('number', 'Ch1');

      for (idx = 0; idx < sliceNames.length; idx++) {
        sliceName = sliceNames[idx];
        //console.log('drawRawChart: SHOULD CHANGE sliceName = ', sliceName);
        if (!(sliceName in resultsCache)) { break; }
        var gatheredResults = resultsCache[sliceName];
        //console.log('drawRawChart: gatheredResults =', gatheredResults)
        var rawData = gatheredResults;
        var rawCha = rawData.cha;
        //console.log('drawRawChart: rawCha=', rawCha);

        //BUILD DATA TABLE ADDING ROWS TIME AND CHA
        for (i = 0; i < rawCha.length; i++) {

          data.addRow([
           (((Number(sliceName) - testSliceStart)/1000) + i*rawPointSpacing),
           parseFloat(rawCha[i]),
          ]);
        };
      };
      //console.log('drawRawChart: THIS SHOULD SHOW UP data =', data);
       //range = (Number(sliceNames[numPages]) - Number(sliceNames[0]))/1000;
       //hMax = range/2;
       //hMin = (- rawWidth/2); 
      var width = rawWidth*(100/hZoom);  
      hMax = hPosition + width;
      hMin = hPosition;

      rawChartOptions = {
         title: '',
         titleTextStyle: {color:'lightgray', fontSize: 18, fontName: 'NexaLight'},
         legend: 'none', //{alignment:'center', textStyle:{color:'lightgray'}},
         hAxis: {title: 'Time(sec)',titleTextStyle:{color:'lightgray', fontName: 'NexaLight'}, textStyle:{color:'lightgray'}, baselineColor:'white', gridlines:{color: 'gray', count: 6}, minorGridlines:{color: 'gray', count: 1}, viewWindowMode:'explicit', viewWindow:{max: hMax, min: hMin}},
         vAxis: {title: '', titleTextStyle:{color:'lightgray'}, textStyle:{color:'lightgray'}, baselineColor:'white', gridlines:{color: 'gray', count: 6}, minorGridlines:{color: 'gray', count: 1}, format: '##.###', viewWindowMode:'explicit', },
         backgroundColor: {fill:'none', stroke: 'black', strokeWidth: 0,},                 
         colors: ['rgb(2,255,253)','rgb(239,253,146)'],
         chartArea:{backgroundColor:'', height:350, width:445},
         lineWidth: 2.5,
         curveType: 'function',
         crosshair: {trigger: 'both', selected:{opacity: 0.8}, focused:{opacity:0.8}},
         explorer: {maxZoomOut: 10, maxZoomIn: 0.125},
      };
      var tableOptions = {
         showRowNumber: true,
      };   
      moveWindowData = data;
      //console.log('drawRawChart: data=',data)
      //DRAW CHART
      rawChart = new google.visualization.LineChart($('#oChart').get(0));      
      rawChart.draw(data, rawChartOptions);
      //DRAW TABLE
      var table = new google.visualization.Table($('#oTable').get(0));
      table.draw(data, tableOptions);  
    };
    function buildSliceNames(start,end,interval) {
      //console.log('buildSliceNames',start);
        for (msec = start; msec <= end;msec += interval) {
          name = String(msec);
          if ($.inArray(name, sliceNames) == -1) {
            sliceNames.push(name);
          };
        };  
    };

    function fetchSliceNames() {
      console.log('fetchSliceNames: sliceNames = ',sliceNames);
        for (idx in sliceNames) {
            if (!(sliceNames[idx] in resultsCache)) {
               fetchData(base_url,sliceNames[idx],true);
           };
        };
    };
    //google.setOnLoadCallback(getTestInfo);   STOP from CALLING on AUTO
    // FETCH RAW DATA 
    function fetchData(base_url,sliceName,use_async){

        json_url = base_url + sliceName;
        //console.log('fetchData: json_url',json_url)
        $.ajax({
          async: use_async,
          url: json_url,            
          dataType: 'json',
        }).done(function (results) {
          resultsCache[sliceName] = results;
          //console.log('fetchData: results =',results)
          drawRawChart();
        });  
    };
    //want save button to create this url and post true or
    //https://gradientone-test.appspot.com/datamgmt/bscopedata/Acme/Tahoe/wildwood/1436937598030

    //CONFIG FORM SUBMIT
    function instConfig() {
      var d = document.getElementById('configSettings');
        var children = d.childNodes;

      var configName = children[1].children[1].value;
      var configBand = children[3].children[1].value;
      var configSampleRate =  children[5].children[1].value;
      var configSampleSize = children[7].children[1].value; 
      var configResolution = children[9].children[1].value; 
      var configChNum = children[11].children[1].value; 

      var configSettings = document.getElementById('settingsDisplay');
        var setChildren = configSettings.childNodes;



      setChildren[1].children[1].innerHTML = configBand;
      setChildren[3].children[1].innerHTML = configSampleRate;
      setChildren[1].children[3].innerHTML = configSampleSize;
      setChildren[3].children[3].innerHTML = configResolution;

      var config_url = 'https://gradientone-test.appspot.com/bscopeconfiginput';
      console.log('saveStatus: config_url = ',config_url);

      var configSettings = JSON.stringify({"config_name":configName,"analog_bandwidth":configBand,
            "analog_sample_rate":configSampleRate, "capture_buffer_size":configSampleSize,
             "capture_channels":configChNum, "resolution":configResolution,"timepost":false});
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


    function saveStatus(status) {
     document.getElementById("traceSave").disabled = true; 
      console.log('saveStatus: SAVED!!');
      $('#collapseSave').collapse("hide");
      formatSaveUrl = raw_urlPath.split('/');


      var saveValue = status;
      var save_url = 'https://gradientone-test.appspot.com/datamgmt/' + formatSaveUrl[formatSaveUrl.length-5] + '/' + formatSaveUrl[formatSaveUrl.length-4] + '/' + formatSaveUrl[formatSaveUrl.length-3] + '/' + formatSaveUrl[formatSaveUrl.length-2] + '/' + formatSaveUrl[formatSaveUrl.length-1];
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

    // Connected to knobs
    // WILL BE USED TO MOVE THE PLOT WINDOW TO GIVE THE FEELING OF MOVEMENT
   
    function moveWindow(){
        var width = rawWidth*(100/hZoom);
        
        hMax = hPosition + width;
        hMin = hPosition;
        console.log('moveWindow: hMax = ', hMax);
        console.log('moveWindow: hMin = ', hMin);

        console.log('moveWindow: H position = ',hPosition);
        console.log('moveWindow: H zoom = ',hZoom);
        rawChartOptions.hAxis.viewWindow.max = hMax;
        rawChartOptions.hAxis.viewWindow.min = hMin;

        rawChart.draw(moveWindowData, rawChartOptions); // REDRAW CHART
        console.log('moveWindow: vew window =',rawChartOptions.hAxis.viewWindow);
    }; 
     
    // replay button
  
      // replay button
    var step = 0;
    var windowSize = 0;
    var incrementTimerID;
    function increment () {
        if (step <= rawWidth) {
          step = step + rawPointSpacing;
        }else {
          console.log('increment: out of data');
          return;
         //clearInterval(timerID); 
        };
        rhMax = step + windowSize;
        rhMin = step; 
        rawChartOptions.hAxis.viewWindow.max = rhMax;
        rawChartOptions.hAxis.viewWindow.min = rhMin;

        rawChart.draw(moveWindowData, rawChartOptions);
        incrementTimerID = setTimeout(increment,2);
        console.log('increment: incrementTimerID=',incrementTimerID);
      };
    function reverseIncrement () {
        if (step >= 0) {
          step = step - rawPointSpacing;
        }else {
          return;
        }; 
        rhMax = step + windowSize;
        rhMin = step; 
        rawChartOptions.hAxis.viewWindow.max = rhMax;
        rawChartOptions.hAxis.viewWindow.min = rhMin;

        rawChart.draw(moveWindowData, rawChartOptions);
        incrementTimerID = setTimeout(reverseIncrement,2);
      };


    function replay() {
      console.log('rawPointSpacing!!!!!! =',rawPointSpacing);
      step = 0;
      windowSize = rawWidth*(100/hZoom);
      //timerID = setInterval(increment, 100); 
      increment();
    };
    // pause / start / rewind
    function start() {   
      windowSize = rawWidth*(100/hZoom);
      //timerID = setInterval(increment, 100);
      increment();

    };

    function backward() {  
      windowSize = rawWidth*(100/hZoom);
      reverseIncrement(); 
      //timerID = setInterval(increment, 100);
    };
// BUTTON CONTROLS
$(document).ready(function(){
//REPLAY BUTTONS
  
    $('#backward').click(function(){
      clearTimeout(incrementTimerID);
      backward();
    });
    $('#pause').click(function(){ 
      clearTimeout(incrementTimerID);
    });
    $('#start').click(function(){
      clearTimeout(incrementTimerID);
      replay();
    });
    $('#forward').click(function(){
      clearTimeout(incrementTimerID);
      start();
    });

    $('#replay').click(function(){

       replay();
    });
   
//OPTION BUTTONS
  //EXPLORE MODE
  $("#exploreBtns").hide();
  $("#exploreMode").click(function () {
    clearTimeout(traceTimerID);
    $("#traceMode").css("background-color", "rgb(150,150,150)"); //turn off color
    $("#exploreMode").css("background-color", "rgb(124,175,46)"); //turn on color
    $("#exploreBtns").fadeIn("fast");
    $("#traceBtns").hide();
    //exploreMode();
  });
  $("#exploreSave").click(function () {
      saveStatus('save');
  });

    function exploreStart(el){
      console.log('exploreStart !!!!!')
      //formatStartUrl = raw_urlPath.split('/');
      var startValue = 'Start_Explore';
      var start_url = 'https://gradientone-test.appspot.com/' + 'panelcontrol/Acme/Tahoe/Primetime';// + formatStartUrl[formatStartUrl.length-2];
      console.log('exploreStart: start_url =',start_url);

      var startData = JSON.stringify({"start_status":startValue});
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
      exploreMode();
    }
    function exploreStop(el){
      console.log('exploreStop!!!!!')
      //formatStartUrl = raw_urlPath.split('/');
      
      var startValue = 'Stop_Explore';
      var start_url = 'https://gradientone-test.appspot.com/' + 'panelcontrol/Acme/Tahoe/Primetime';// + formatStartUrl[formatStartUrl.length-2];
      console.log('exploreStart: start_url =',start_url);

      var startData = JSON.stringify({"start_status":startValue});
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
      clearTimeout(exploreTimerID);
    };
    $("#exploreStartStop").click(function() {
      $(this).text(function(i, v){
      return v === 'STOP' ? 'START' : 'STOP'
      })
      var el = this;
      return (el.t = !el.t) ? exploreStart(el) : exploreStop(el);
    });

    function exploreResume(el){
      console.log('exploreResume !!!!!')
      exploreMode();
    };
    function explorePause(el){
      console.log('explorePause!!!!!')
      clearTimeout(exploreTimerID);
    };
    $("#explorePause").click(function() {
      $(this).text(function(i, v){
      return v === 'Resume' ? 'Pause' : 'Resume'
      })
      var el = this;
      return (el.t = !el.t) ?  explorePause(el) : exploreResume(el);
    });

  //TRACE MODE //  
    $("#traceBtns").hide();
    $("#traceMode").click(function () {
      clearTimeout(exploreTimerID);
      $("#exploreMode").css("background-color", "rgb(150,150,150)"); //turn off color
      $("#traceMode").css("background-color", "rgb(124,175,46)"); //turn on color
      $("#traceBtns").fadeIn("fast");
      $("#exploreBtns").hide();
      //traceMode();
    });
    //$("#traceSave").click(function () {
    //  saveStatus('save');

   // });
    $("#traceDelete").click(function () {
      saveStatus('delete');
      statusArray = [];
    });
    function traceStart(el){
      console.log('traceStart !!!!!')
      //formatStartUrl = raw_urlPath.split('/');
      //https://gradientone-test.appspot.com/panelcontrol/Acme/Tahoe/Primetime
      var startValue = 'Start_Trace';
      var start_url = 'https://gradientone-test.appspot.com/' + 'panelcontrol/Acme/Tahoe/Primetime';// + formatStartUrl[formatStartUrl.length-2];
      console.log('exploreStart: start_url =',start_url);

      var startData = JSON.stringify({"start_status":startValue});
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
      traceMode();
    };
    function traceStop(el){
      console.log('traceStop!!!!!')
      //formatStartUrl = raw_urlPath.split('/');
      
      var startValue = 'Stop_Trace';
      var start_url = 'https://gradientone-test.appspot.com/' + 'panelcontrol/Acme/Tahoe/Primetime';// + formatStartUrl[formatStartUrl.length-2];
      console.log('exploreStart: start_url =',start_url);

      var startData = JSON.stringify({"start_status":startValue});
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
    $("#traceStartStop").click(function() {
      $(this).text(function(i, v){
      return v === 'STOP' ? 'START' : 'STOP'
      })
      var el = this;
      return (el.t = !el.t) ? traceStart(el) : traceStop(el);
    });
             
});