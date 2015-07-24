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
    var getTestInfoCounter = 0;
    var rawPointSpacing;

    function fetchDecData(){
       dec_json_url = dec_url;
       $.ajax({
          async: true,
          url: dec_json_url,            
          dataType: 'json',
       }).done(function (results) {
         var chaData = results.cha;
         drawDecChart(chaData);
      });
    };

    //LOADING URL
    //test_info_url = window.location.pathname + '.json';
    // console.log(test_info_url);

    // status updates URL =
    // https://gradientone-test.appspot.com/status/Acme/Tahoe
    var currentTestStatus;
    var statusArray = [];
    function getTestStatus() {
      status_url = 'https://gradientone-test.appspot.com/status/Acme/Tahoe';
      console.log('getTestStatus: RUNNING',status_url)
      $.ajax({
          async: true,
          url: status_url,            
          dataType: 'json',
       }).done(function (results) {
          currentTestStatus = results.status.status;
          testStatusTime = results.status.time;
          console.log('getTestStatus: currentTestStatus = ',currentTestStatus);
          console.log('getTestStatus =  ', $.inArray(testStatusTime, statusArray) == -1);
          document.getElementById("currentStatus").innerHTML = currentTestStatus;
          if ($.inArray(testStatusTime, statusArray) == -1) {
            var jsonStatus = {"status":currentTestStatus, "time":testStatusTime};
            statusArray.push(jsonStatus);
            statusArray.push(testStatusTime);
          };          
          console.log('statusArray = ',statusArray);
      });
    };
    
    //Continuously polling at: 
    //https://gradientone-dev1.appspot.com/testresults/Acme/Tahoe/LED
    function getTestInfo() {

      //test_info_url = 'https://gradientone-dev1.appspot.com/testlibrary/Acme/manufacturing/1436809506690.json';
      test_info_url = 'https://gradientone-test.appspot.com/testresults/Acme/Tahoe/Primetime';
      console.log('test_info_url', test_info_url);
      $.ajax({
          async: true,
          url: test_info_url,
          dataType: 'json',
       }).done(function (results) {       
        testInfo = results;  

        testSettings = testInfo.p_settings;
        //URLS DEC/RAW
        dec_url = testInfo.dec_data_url;
        raw_urlPath = testInfo.raw_data_url;
        //Test Info DEC/RAW
        testSliceStart = testSettings.Start_TSE;    
        decPointSpacing = (Number(testSettings.Dec_msec_btw_samples))/1000;    
        totalNumPages = testSettings.Total_Slices;
        numPages = Number(testSettings.Total_Slices); //not live version

        rawPointSpacing = (testSettings.Raw_msec_btw_samples)/1000000;
        sliceSize = Number(testSettings.Slice_Size_msec);
        rawUrlSplit = raw_urlPath.split(testSliceStart);
        base_url = rawUrlSplit[0];
        sliceEnd = (Number(testSliceStart) + (numPages*sliceSize)) -10;

        decOffset = (((Number(numPages) * Number(sliceSize))/10) * decPointSpacing)/2;
        rawOffset = Number(testSliceStart) + ((Number(numPages) * Number(sliceSize))/2);
        rawWidth = (Number(numPages) * Number(sliceSize)) * rawPointSpacing;

        instrumentName = 'Instrument: ' + testInfo.instrument_name;
        hardwareName = 'Hardware: ' + testInfo.hardware_name;
        document.getElementById("instrumentName").innerHTML = instrumentName;
        document.getElementById("hardwareName").innerHTML = hardwareName;

        //move to function called buildSliceNames(start,end,sliceSize)
        //give slice start and a number
        //console.log('getTestInfo: hMaxMs =', hMaxMs);
        //console.log('getTestInfo: dynamicSliceEnd <= sliceEnd ',dynamicSliceEnd <= sliceEnd);
        //console.log('getTestInfo: sliceEnd = ', sliceEnd); 
        //console.log('getTestInfo: dynamicSliceEnd = ', dynamicSliceEnd);
        //console.log('getTestInfo:counter <= numPages ',getTestInfoCounter <= numPages);

        //console.log('getTestInfoCounter =',getTestInfoCounter);
        if(getTestInfoCounter < numPages) {
          dynamicSliceEnd = (Number(testSliceStart) + getTestInfoCounter*sliceSize );
        }else;
        buildSliceNames(Number(testSliceStart),dynamicSliceEnd,sliceSize);
        getTestInfoCounter++;
/*
        for (msec = Number(testSliceStart); msec <= sliceEnd;msec += sliceSize) {
          name = String(msec);
          if ($.inArray(name, sliceNames) == -1) {
            sliceNames.push(name);
          };
        };
*/
        getTestStatus()       
        name = String(sliceEnd);
        delete resultsCache.name;
        fetchSliceNames();

        //fetchDecData();  //DEC DATA

        console.log('slice names = ',sliceNames);
        //console.log('decOffset = ',decOffset);
        //console.log('getTestInfo: testInfo = ', testInfo);              
        //console.log('getTestInfo: testInfo.Total_Slices = ', numPages);
        //console.log('getTestInfo: testInfo.Dec_msec_btw_samples = ', decPointSpacing);  
        //console.log('getTestInfo: sliceSize = ', sliceSize);   
        //console.log('getTestInfo: rawPointSpacing =',rawPointSpacing);  
       });

          setTimeout(getTestInfo,10000);

       //setTimeout(getTestInfo,200);   // change to 100 later
    };
    //getTestInfo();  // called by googe setOnLoadCallback method
    
    // DEC CHART CODE //

    // BUILD DEC DATA TABLE AND DRAW DEC CHART
    function drawDecChart(decData) {
        var data = new google.visualization.DataTable();
        data.addColumn('number', 'Time');
        data.addColumn('number', 'Ch1');

        for (i=0; i<decData.length; i++) {
           var num = i*decPointSpacing - decOffset;
           //console.log('drawDecChart: num =', decOffset);
           num = Math.ceil(num * 100) / 100;
           data.addRow([
             num, 
             decData[i],
             ]);
        };

        decChartOptions = {
         title: '',
         titleTextStyle: {color:'lightgray', fontSize: 18, fontName: 'NexaLight'},
         legend: {alignment:'center', textStyle:{color:'lightgray'}},
         hAxis: {title: 'Time(sec)',titleTextStyle:{color:'lightgray', fontName: 'NexaLight'}, textStyle:{color:'lightgray'}, baselineColor:'white', gridlines:{color: 'gray', count: 6}, minorGridlines:{color: 'gray', count: 1}, viewWindowMode:'explicit', viewWindow:{max: hMax, min: hMin}},
         vAxis: {title: '', titleTextStyle:{color:'lightgray'}, textStyle:{color:'lightgray'}, baselineColor:'white', gridlines:{color: 'gray', count: 6}, minorGridlines:{color: 'gray', count: 1}, format: '##.###', viewWindowMode:'explicit', },
         backgroundColor: {fill:'none', stroke: 'black', strokeWidth: 0,},                 
         colors: ['rgb(2,255,253)','rgb(239,253,146)'],
         lineWidth: 2.5,
         curveType: 'function',
         crosshair: {trigger: 'both', selected:{opacity: 0.8}, focused:{opacity:0.8}},
        };
      //DRAW CHART
         var chart = new google.visualization.LineChart($('#decChart').get(0));      
         chart.draw(data, decChartOptions);
      //DRAW TABLE
         var table = new google.visualization.Table($('#decTable').get(0));
         table.draw(data); 
    };

    //google.setOnLoadCallback(fetchDecData);

// RAW CHART CODE //

// BUILD RAW DATA TABLE AND DRAW RAW CHART+TABLE
    function drawRawChart(){   
      var data = new google.visualization.DataTable();
       data.addColumn('number', 'Time');
       data.addColumn('number', 'Ch1');

       for (idx = 0; idx < sliceNames.length; idx++) {
            sliceName = sliceNames[idx];
            //console.log('drawRawChart: SHOULD CHANGE sliceName = ', sliceName);
            if (!(sliceName in resultsCache)) { return; }
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
         title: 'Raw Data',
         titleTextStyle: {color:'lightgray', fontSize: 18, fontName: 'NexaLight'},
         legend: 'none', //{alignment:'center', textStyle:{color:'lightgray'}},
         hAxis: {title: 'Time(sec)',titleTextStyle:{color:'lightgray', fontName: 'NexaLight'}, textStyle:{color:'lightgray'}, baselineColor:'white', gridlines:{color: 'gray', count: 6}, minorGridlines:{color: 'gray', count: 1}, viewWindowMode:'explicit', viewWindow:{max: hMax, min: hMin}},
         vAxis: {title: '', titleTextStyle:{color:'lightgray'}, textStyle:{color:'lightgray'}, baselineColor:'white', gridlines:{color: 'gray', count: 6}, minorGridlines:{color: 'gray', count: 1}, format: '##.###', viewWindowMode:'explicit', },
         backgroundColor: {fill:'none', stroke: 'black', strokeWidth: 0,},                 
         colors: ['rgb(2,255,253)','rgb(239,253,146)'],
         chartArea:{backgroundColor:'', height:300, width:445},
         lineWidth: 2.5,
         curveType: 'function',
         crosshair: {trigger: 'both', selected:{opacity: 0.8}, focused:{opacity:0.8}},
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
    google.setOnLoadCallback(getTestInfo);
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

    function saveStatus(status) {
      console.log('saveStatus: sliceSize = ',sliceSize);
      console.log('saveStatus: totalNumPages = ',totalNumPages);
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
    var step = 0;
    function Forward() {
      //console.log('rawPointSpacing!!!!!! =',rawPointSpacing);   
      var windowSize = rawWidth*(100/hZoom);
      timerID = setInterval(increment, 100);
      function increment () {
        if (step <= rawWidth) {
          step = step + rawPointSpacing*2
        }else {
         clearInterval(timerID); 
        }  
        rhMax = step + windowSize;
        rhMin = step; 
        rawChartOptions.hAxis.viewWindow.max = rhMax;
        rawChartOptions.hAxis.viewWindow.min = rhMin;

        rawChart.draw(moveWindowData, rawChartOptions);
      };
    };
    function fastForward() {   
      var windowSize = rawWidth*(100/hZoom);
      timerID = setInterval(increment, 100);
      function increment () {
        if (step <= rawWidth) {
          step = step + rawPointSpacing*20
        }else {
         clearInterval(timerID); 
        }  
        rhMax = step + windowSize;
        rhMin = step; 
        rawChartOptions.hAxis.viewWindow.max = rhMax;
        rawChartOptions.hAxis.viewWindow.min = rhMin;

        rawChart.draw(moveWindowData, rawChartOptions);
      };
    };
    // pause / start / rewind
    function start() {   
      var windowSize = rawWidth*(100/hZoom);
      timerID = setInterval(increment, 100);
      function increment () {
        if (step <= rawWidth) {
          step = step + rawPointSpacing*2
        }else {
         clearInterval(timerID); 
        }  
        rhMax = step + windowSize;
        rhMin = step; 
        rawChartOptions.hAxis.viewWindow.max = rhMax;
        rawChartOptions.hAxis.viewWindow.min = rhMin;

        rawChart.draw(moveWindowData, rawChartOptions);
      };
    };


    function backward() {  
      var windowSize = rawWidth*(100/hZoom); 
      timerID = setInterval(increment, 100);
      function increment () {
        if (step >= 0) {
          step = step - rawPointSpacing*2
        }else {
         clearInterval(timerID); 
        }; 
        rhMax = step + windowSize;
        rhMin = step; 
        rawChartOptions.hAxis.viewWindow.max = rhMax;
        rawChartOptions.hAxis.viewWindow.min = rhMin;

        rawChart.draw(moveWindowData, rawChartOptions);
      };
    };
    function fastBackward() {  
      var windowSize = rawWidth*(100/hZoom); 
      timerID = setInterval(increment, 100);
      function increment () {
        if (step >= 0) {
          step = step - rawPointSpacing*20
        }else {
         clearInterval(timerID); 
        }; 
        rhMax = step + windowSize;
        rhMin = step; 
        rawChartOptions.hAxis.viewWindow.max = rhMax;
        rawChartOptions.hAxis.viewWindow.min = rhMin;

        rawChart.draw(moveWindowData, rawChartOptions);
      };
    };
// BUTTON CONTROLS
  $(document).ready(function(){
    $('#replay').click(function(){
       replay();
    });
    $('#fastBackward').click(function(){
       fastBackward();
    });
    $('#backward').click(function(){
       backward();
    });
    $('#pause').click(function(){ 
       clearInterval(timerID);
    });
    $('#start').click(function(){
       start();
    });
    $('#forward').click(function(){
       Forward();
    });
    $('#fastForward').click(function(){
       fastForward();
    });
  });
 


  $("#save").click(function () {
      saveStatus('save');
  });
  $("#delete").click(function () {
      saveStatus('delete');
      statusArray = [];
  });
  $("#startStop").click(function () {
    $(this).text(function(i, v){
      return v === 'STOP' ? 'START' : 'STOP'
    })
  });
