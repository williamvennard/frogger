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
    var hZoom = 100;
    var hPosition = 0;
    var hPosStep = 0.05;

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

    function buildSliceNames(start,end,interval) {
        for (msec = start; msec <= end;msec += interval) {
          name = String(msec);
          if ($.inArray(name, sliceNames) == -1) {
            sliceNames.push(name);
          };
        };  
    };

    //LOADING URL
    //test_info_url = window.location.pathname + '.json';
    // console.log(test_info_url);

    //Continuously polling at: 
    //https://gradientone-dev1.appspot.com/testresults/Acme/Tahoe/LED
    var sliceSize = 0;
    var counter = 0;
    function getTestInfo() {
      counter++;
      //test_info_url = 'https://gradientone-dev1.appspot.com/testlibrary/Acme/manufacturing/1436809506690.json';
      test_info_url = 'https://gradientone-test.appspot.com/testresults/Acme/Tahoe/Primetime';
      console.log('test_info_url', test_info_url);
      $.ajax({
          async: true,
          url: test_info_url,
          dataType: 'json',
       }).done(function (results) {       
        //testInfo = results.data[0];  //live version
        testInfo = results;     //nonLive
        //console.log('getTestInfo: results = ',results);
        
        console.log('testInfo p_settings = ', testInfo.p_settings);
        console.log('sting or no?', typeof testInfo.p_settings);

        testSettings = testInfo.p_settings;
        //URLS DEC/RAW
        dec_url = testInfo.dec_data_url;
        raw_urlPath = testInfo.raw_data_url;
        //Test Info DEC/RAW
        testSliceStart = testSettings.Start_TSE;    
        decPointSpacing = (Number(testSettings.Dec_msec_btw_samples))/1000;    
        totalNumPages = testSettings.Total_Slices;
        //numPages = testInfo.Current_slice_count;
        numPages = Number(testSettings.Total_Slices); //not live version
        //numPages = 5;
        rawPointSpacing = (testSettings.Raw_msec_btw_samples)/1000;
        sliceSize = Number(testSettings.Slice_Size_msec);

        rawUrlSplit = raw_urlPath.split(testSliceStart);
        base_url = rawUrlSplit[0];
        sliceEnd = (Number(testSliceStart) + (numPages*sliceSize)) -10;

        decOffset = (((Number(numPages) * Number(sliceSize))/10) * decPointSpacing)/2;
        rawOffset = Number(testSliceStart) + ((Number(numPages) * Number(sliceSize))/2);
        rawWidth = (Number(numPages) * Number(sliceSize)) * rawPointSpacing;
        //move to function called buildSliceNames(start,end,sliceSize)
        //give slice start and a number
        //buildSliceNames(Number(testSliceStart),sliceEnd,10);
        for (msec = Number(testSliceStart); msec <= sliceEnd;msec += sliceSize) {
          name = String(msec);
          if ($.inArray(name, sliceNames) == -1) {
            sliceNames.push(name);
          };
        };

        fetchDecData();
        name = String(sliceEnd);
        delete resultsCache.name;
        fetchSliceNames();
        console.log('slice names = ',sliceNames);
        console.log('decOffset = ',decOffset);
        console.log('getTestInfo: testInfo = ', testInfo);
        console.log('getTestInfo: sliceEnd = ', sliceEnd);        
        console.log('getTestInfo: testInfo.Total_Slices = ', numPages);
        console.log('getTestInfo: testInfo.Dec_msec_btw_samples = ', decPointSpacing);  
        console.log('getTestInfo: sliceSize = ', sliceSize);     
       });
       setTimeout(getTestInfo,500);   // change to 100 later
       console.log('Counter = ',counter);
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

       for (idx = 0; idx < numPages; idx++) {
            sliceName = sliceNames[idx];
            if (!(sliceName in resultsCache)) { return; }
            var gatheredResults = resultsCache[sliceName];
            //console.log('drawRawChart: gatheredResults = ',resultsCache[sliceName]);
            console.log('drawRawChart: gatheredResults =', gatheredResults)
            var rawData = gatheredResults;
            console.log('drawRawChart: rawData = ', rawData);
            //var rawCha = rawData[0].cha;
            var rawCha = rawData.cha;

            
            //BUILD DATA TABLE ADDING ROWS TIME AND CHA
           for (i = 0; i < rawCha.length; i++) {
             data.addRow([
               ((Number(sliceName) - rawOffset) + i)/1000,
               parseFloat(rawCha[i]),
               ]);
           };
         };
      
         range = (Number(sliceNames[numPages]) - Number(sliceNames[0]))/1000;
         hMax = range/2;
         hMin = (- rawWidth/2); 

      rawChartOptions = {
         title: 'Raw Data',
         titleTextStyle: {color:'lightgray', fontSize: 18, fontName: 'NexaLight'},
         legend: {alignment:'center', textStyle:{color:'lightgray'}},
         hAxis: {title: 'Time(sec)',titleTextStyle:{color:'lightgray', fontName: 'NexaLight'}, textStyle:{color:'lightgray'}, baselineColor:'white', gridlines:{color: 'gray', count: 6}, minorGridlines:{color: 'gray', count: 1}, viewWindowMode:'explicit', viewWindow:{max: hMax, min: hMin}},
         vAxis: {title: '', titleTextStyle:{color:'lightgray'}, textStyle:{color:'lightgray'}, baselineColor:'white', gridlines:{color: 'gray', count: 6}, minorGridlines:{color: 'gray', count: 1}, format: '##.###', viewWindowMode:'explicit', },
         backgroundColor: {fill:'none', stroke: 'black', strokeWidth: 0,},                 
         colors: ['rgb(2,255,253)','rgb(239,253,146)'],
         //chartArea:{backgroundColor:'', height:300, width:445},
         lineWidth: 2.5,
         curveType: 'function',
         crosshair: {trigger: 'both', selected:{opacity: 0.8}, focused:{opacity:0.8}},
      };
      var tableOptions = {
         showRowNumber: true,
      };   
          moveWindowData = data;
          console.log('drawRawChart: data=',data)
         //DRAW CHART
         rawChart = new google.visualization.LineChart($('#oChart').get(0));      
         rawChart.draw(data, rawChartOptions);
         //DRAW TABLE
         var table = new google.visualization.Table($('#oTable').get(0));
         table.draw(data, tableOptions);  
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
      console.log('saveStatus: testSliceStart = ',testSliceStart);
      console.log('saveStatus: sliceSize = ',sliceSize);
      console.log('saveStatus: totalNumPages = ',totalNumPages);
      console.log('saveStatus: raw_urlPath = ',raw_urlPath);

      var saveValue = '"' + status + '"';
      var save_url = 'https://gradientone-test.appspot.com/datamgmt/' + testSliceStart;
      console.log('saveStatus: save_url = ',save_url);

      var formData = {save_status:saveValue,totalNumPages:totalNumPages,sliceSize:sliceSize};
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
    /*
    function moveWindow(){
        var width = rawWidth*(100/hZoom);
        
    console.log('hPosStep = ',hPosStep);
        hMax = hPosition + width/2;
        hMin = hPosition - width/2;
 
        hPosStep = 5.0 / hZoom;
        console.log('hPosStep = ', hPosStep);
        console.log('moveWindow: H position = ',hPosition);
        console.log('moveWindow: H zoom = ',hZoom);
        rawChartOptions.hAxis.viewWindow.max = hMax;
        rawChartOptions.hAxis.viewWindow.min = hMin;

        rawChart.draw(moveWindowData, rawChartOptions); // REDRAW CHART
        console.log('moveWindow: vew window =',rawChartOptions.hAxis.viewWindow);
    }; 
    // replay button
    function replay() {
      step = (- rawWidth/2);
      var windowSize = rawWidth*(100/hZoom);
      timerID = setInterval(increment, 10);
      function increment () {
        if (step <= rawWidth/2) {
          step = step + 0.01
        }else {
         clearInterval(timerID); 
        }  
        rhMax = step + windowSize/2;
        rhMin = step - windowSize/2; 
        rawChartOptions.hAxis.viewWindow.max = rhMax;
        rawChartOptions.hAxis.viewWindow.min = rhMin;

        rawChart.draw(moveWindowData, rawChartOptions);
      };
    };
    // pause / start / rewind
    function start() {   
      var windowSize = rawWidth*(100/hZoom);
      timerID = setInterval(increment, 10);
      function increment () {
        if (step <= rawWidth/2) {
          step = step + 0.01
        }else {
         clearInterval(timerID); 
        }  
        rhMax = step + windowSize/2;
        rhMin = step - windowSize/2; 
        rawChartOptions.hAxis.viewWindow.max = rhMax;
        rawChartOptions.hAxis.viewWindow.min = rhMin;

        rawChart.draw(moveWindowData, rawChartOptions);
      };
    };

    function rewind() {  
      var windowSize = rawWidth*(100/hZoom); 
      timerID = setInterval(increment, 10);
      function increment () {
        if (step >= (-rawWidth/2)) {
          step = step - 0.01
        }else {
         clearInterval(timerID); 
        }; 
        rhMax = step + windowSize/2;
        rhMin = step - windowSize/2; 
        rawChartOptions.hAxis.viewWindow.max = rhMax;
        rawChartOptions.hAxis.viewWindow.min = rhMin;

        rawChart.draw(moveWindowData, rawChartOptions);
      };
    };
// BUTTON CONTROLS
  $(document).ready(function(){
    $('#Replay').click(function(){
       replay();
    });
    $('#Pause').click(function(){ 
       clearInterval(timerID);
    });
    $('#Start').click(function(){
       start();
    });
    $('#Rewind').click(function(){
       rewind();
    });
  });
  */
  $("#save").click(function () {
      saveStatus('save');
  });
  $("#startStop").click(function () {
    $(this).text(function(i, v){
      return v === 'STOP' ? 'START' : 'STOP'
    })
  });
