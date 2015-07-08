 // load chart lib
    google.load('visualization', '1', {packages: ['corechart','table']});
       //DECIMATED DATA PLOT
    function fetchDecData(){
       dec_base_url = 'https://gradientone-test.appspot.com/dec/';
       dec_urlPath = 'bscopedata/arduino/1435775476910';
       //dec_urlPath = decPathname;
       dec_json_url = dec_base_url + dec_urlPath;
       $.ajax({
          async: true,
          url: dec_json_url,            
          dataType: 'json',
       }).done(function (results) {
          //console.log("fetchDecData: json_url =", json_url);
         var decData = results.cha;
          //console.log("results:", decData);
         //console.log('decData Test:',decData);
         var config = results.config;
         var cleanConfig = config.substr(1, config.length-2);
         var configArray = cleanConfig.split(', ');

         var sampleSize = configArray[7].split(': ')[1];
         var sampleRate = configArray[configArray.length-1].split(': ')[1];
         //console.log('Config:',configArray);
         

         var decPointSpacing = (1/Number(sampleRate))*10;
         var offset = (sampleSize/sampleRate)/2;

         //console.log('dec point spacing should be .01:',decPointSpacing);
         //console.log('offset = ',offset);
                        //var configOptions = rawData[0].config;
            //console.log('config options: ',configOptions);
           // var formatConfig = configOptions.substr(1, configOptions.length-2);
           // var configArray = formatConfig.split(', ');
                        //sampleSize = Number(configArray[7].split(': ')[1]);
           // var sampleRate = configArray[configArray.length-1].split(': ')[1];

       data = new google.visualization.DataTable();
         data.addColumn('number', 'Time');
         data.addColumn('number', 'Ch1');

         //GETING DATA
         for (i=0; i<decData.length; i++) {
           var num = i*decPointSpacing - offset;
           num = Math.ceil(num * 100) / 100;
           console.log("fetchDecData:num=",num);
           data.addRow([
             num, 
             decData[i],
             ]);
         };
         //console.log('Data:',data);  
       //var dataTest = data;
           //console.log('DataTest:',dataTest);
      var options = {
         title: 'MMIC Amplifier @ +25degC',
         titleTextStyle: {color:'white', fontSize: 15, fontName: 'NexaBold'},
         legend: {alignment:'center', textStyle:{color:'lightgray'}},
         hAxis: {title: 'frequency',titleTextStyle:{color:'lightgray', fontName: 'NexaLight'}, textStyle:{color:'lightgray'}, baselineColor:'none', gridlines:{color: 'none', count: 5},viewWindowMode:'explicit'},
         vAxis: {title: '', titleTextStyle:{color:'lightgray'}, textStyle:{color:'lightgray'}, baselineColor:'white', gridlines:{color: 'none', count: 0}, format: '##.###', viewWindowMode:'explicit'},
         backgroundColor: {fill: 'black', stroke: 'silver', strokeWidth: 3,},              
         colors: ['rgb(2,255,253)','rgb(239,253,146)'],
         lineWidth: 2,
         curveType: 'function',
         crosshair: {trigger: 'both', selected:{opacity: 0.8}, focused:{opacity:0.8}},
         animation: {startup:true, duration: 400},
       };
      //DRAW CHART
         var chart = new google.visualization.LineChart($('#chart1').get(0));      
         chart.draw(data, options);
      //DRAW TABLE
         var table = new google.visualization.Table($('#decTable').get(0));
         table.draw(data); 
       });
    };

    //google.load("visualization", "1", {packages:["corechart"]});
    google.setOnLoadCallback(fetchDecData);

