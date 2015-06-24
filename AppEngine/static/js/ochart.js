//VERTICAL KNOBS
    var vZoom = 100;
    var vPosition = 0;
    $(".vPosKnob").knob({
        'release' : function (vPos) { 
          //console.log('knob H pos value:',hPos);  
          vPosition = vPos;
          doPoll();
      },
    }); 

    $(".vZoomKnob").knob({
      'release' : function (vRange) { 
         //console.log('knob H value:',hRange);
         vZoom = vRange;
         doPoll();
      },
    }); 
//HORIZONTAL KNOBS
    var hZoom = 100;
    var hPosition = 0;
    $(".hPosKnob").knob({
        'release' : function (hPos) { 
          //console.log('knob H pos value:',hPos);  
          hPosition = hPos;
          doPoll();
      },
    }); 

    $(".hZoomKnob").knob({
      'release' : function (hRange) { 
         //console.log('knob H value:',hRange);
         hZoom = hRange;
         doPoll();
      },
    }); 

 // load chart lib
    google.load('visualization', '1', {
      packages: ['corechart','table']
    });
       var doPollCounter = 0;
       var sliceNames = [];
       var resultsCache = [];
       var autoMaxPosition = 0;
       var autoMinPosition = 0;
       var hMax = 0;
       var hMin = 0;
       var chartOptions = {};
       function fetchData(base_url,sliceName,use_async){
          json_url = base_url + sliceName;
          $.ajax({
             async: use_async,
             url: json_url,            
             dataType: 'json',
          }).done(function (results) {
             //console.log("fetchData: json_url =", json_url);
             //console.log("fetchData: sliceName =", sliceName);
             //console.log("fetchData: results =", results);
             resultsCache[sliceName] = results;
             //console.log("61:resultsCache[sliceName] =", resultsCache[sliceName]);
          })  // need error handler
       };

       function doPoll(){
          doPollCounter++;
          var data = new google.visualization.DataTable();
          data.addColumn('number', 'Time');
          data.addColumn('number', 'Ch1');
          //data.addColumn('number', 'Ch2');

          //var startTime = Date.now();
     
          function gatherData(base_url,sliceNames,first,last){
            var sliceName = sliceNames[first];
            if (!(sliceName in resultsCache)) {
                 json_url = base_url + sliceName;
                 //console.log("gatherData: cache miss: json_url =", json_url);
                 fetchData(base_url,sliceName,false);
               };
            var gatheredResults = resultsCache[sliceName];
            var firstRow = gatheredResults['data'][0];

            if (autoMinPosition == 0) {
              console.log('auto min and max:',firstRow.TIME)
              console.log('range for auto max:',range);
              autoMinPosition = Number(firstRow.TIME);
              autoMaxPosition = Number(firstRow.TIME)+range;
              hMax = autoMaxPosition;
              hMin = autoMinPosition;
              console.log("chart options viewWindow:", chartOptions.hAxis.viewWindow);
              chartOptions.hAxis.viewWindow.max = hMax;
              chartOptions.hAxis.viewWindow.min = hMin;
            };
            for (idx = first; idx < last; idx++) {
               sliceName = sliceNames[idx];
               //console.log("gatherData: sliceName =", sliceName);
               //console.log("gatherData: idx =", idx);
               if (!(sliceName in resultsCache)) {
                 json_url = base_url + sliceName;
                 //console.log("gatherData: cache miss: json_url =", json_url);
                 fetchData(base_url,sliceName,false);
               };
               gatheredResults = resultsCache[sliceName];
               //console.log("gatherData: resultsCache =", resultsCache);
               //console.log("gatherData: gatheredResults =", gatheredResults);
               //console.log("gatherData: idx = ", idx);
               //GETING DATA
               $.each(gatheredResults['data'], function (i, row) {
                 data.addRow([
                   parseFloat(row.TIME),
                   parseFloat(row.CH1),
                   //parseFloat(row.CH2), 
                 ]);
               });
            };
    
            //var endTime = Date.now();
            //console.log('Timer:', endTime - startTime);

            //DRAW CHART
            var chart = new google.visualization.LineChart($('#ochart').get(0));      
            chart.draw(data, chartOptions);
            //DRAW TABLE
            var table = new google.visualization.Table($('#oTable').get(0));
            table.draw(data, tableOptions);  
          };

            console.log('auto MAX position:',autoMaxPosition);
            console.log('auto MIN position:',autoMinPosition);
            var center = hPosition + (autoMinPosition + autoMaxPosition)/2;
            var width = (autoMaxPosition - autoMinPosition)*(100.0/hZoom);
            console.log('h zoom:',hZoom);

            console.log('window width:', width);
            console.log('window center:',center);

            console.log('do poll counter:',doPollCounter);
            
            hMax = center + width/2 + range;
            hMin = center - width/2;

            console.log('hMax:',hMax);
            console.log('hMin:',hMin);
            //console.log('horizontal Zoom dial:',hZoom);
            //console.log('horizontal position dial:',hPosition);
            
        chartOptions = {
            title: 'Oscope Data',
            titleTextStyle: {color:'lightgray', fontSize: 18, fontName: 'NexaLight'},
            legend: {alignment:'center', textStyle:{color:'lightgray'}},
            hAxis: {title: 'Time(sec)',titleTextStyle:{color:'lightgray', fontName: 'NexaLight'}, textStyle:{color:'lightgray'}, baselineColor:'white', gridlines:{color: 'gray', count: 6}, minorGridlines:{color: 'gray', count: 1}, viewWindowMode:'explicit', viewWindow:{max: hMax, min:hMin}},
            vAxis: {title: '', titleTextStyle:{color:'lightgray'}, textStyle:{color:'lightgray'}, baselineColor:'white', gridlines:{color: 'gray', count: 6}, minorGridlines:{color: 'gray', count: 1}, format: '##.###', viewWindowMode:'explicit', viewWindow:{max:2.5, min:-2.5} },
            backgroundColor: {fill:'none', stroke: 'black', strokeWidth: 0,},                 
            colors: ['rgb(2,255,253)','rgb(239,253,146)'],
            chartArea:{backgroundColor:'', height:300, width:445},
            lineWidth: 2,
            curveType: 'function',
            crosshair: {trigger: 'both', selected:{opacity: 0.8}, focused:{opacity:0.8}},
          };
          var tableOptions = {
            showRowNumber: true,
          };

          //console.log("calling gatherData with name = ",sliceNames);
          //console.log("calling gatherData with length = ",sliceNames.length);

          //Drawing data test:
          gatherData(base_url,sliceNames,0,doPollCounter);

          //gatherData(base_url,sliceNames,0,sliceNames.length);

          //var pagingTest = (doPollCounter+1)*10;
          //console.log('do poll paging test:', pagingTest);
          var sliceBuild = Number('1435092471100');

          sliceStop = sliceBuild + 51*100;

          for (msec = sliceBuild+200; msec < sliceStop;msec += 100) {
            name = String(msec);
            if ($.inArray(name, sliceNames) == -1) {
              sliceNames.push(String(msec));
            };
          };
          //put var range here for back to how it was
          if (doPollCounter < 52) {
            range = (Number(sliceNames[doPollCounter]) - Number(sliceNames[0]))/1000;
            console.log('Range in Number:',range);
          }else{
            range = 0;
          };
      //console.log('sliceNames for range:',sliceNames);

          //gatherData used to go here

          //console.log('slice names:',sliceNames);
          //console.log("after gatherData length = ",sliceNames.length);
          for (idx in sliceNames) {
            if (!(sliceNames[idx] in resultsCache)) {
              fetchData(base_url,sliceNames[idx],true);
            };
          };
          // use last TIME inplace of -495.00
          if(doPollCounter < 52) {
            setTimeout(doPoll,50);
          };
       };

// POLL FOR CURRENT TIME TO START PLOTTING DATA

     // var formatTime = (Math.round(Date.now()/100))*100;
     // console.log('current timestamp:',formatTime);
// BUILD SLICES GIVEN current Time
      console.log('this runs first!');
      sliceNames.push('1435092471100');
      sliceNames.push(String(Number('1435092471100')+100));

       var base_url = 'http://gradientone-test.appspot.com/oscopedata/amplifier/';
       fetchData(base_url,sliceNames[0],true);
       fetchData(base_url,sliceNames[1],true);

      var range = (Number(sliceNames[sliceNames.length-1]) - Number(sliceNames[0]))/1000;
      console.log('Range in Number:',range);
      console.log('sliceNames for range:',sliceNames);
  

       google.setOnLoadCallback(doPoll);
       
      
