// load chart lib
    google.load('visualization', '1', {packages: ['corechart','table']});
       //DECIMATED DATA PLOT
    function fetchDecData(){
       //dec_base_url = 'https://gradientone-dev1.appspot.com/bscopedata/dec/Acme/';
       dec_base_url = window.location.origin + '/bscopedata/dec/Acme/';
       dec_urlPath = 'Tahoe/LED/1436809506690';
       //dec_urlPath = decPathname;
       dec_json_url = dec_base_url + dec_urlPath;
       $.ajax({
          async: true,
          url: dec_json_url,            
          dataType: 'json',
       }).done(function (results) {
          //console.log("fetchDecData: json_url =", json_url);
         var decData = results.cha;
          console.log("results:", decData);
         //console.log('decData Test:',decData);
         var decPointSpacing = results.p_settings[0];

         console.log('decPointSpacing:',decPointSpacing);
         

       data = new google.visualization.DataTable();
         data.addColumn('number', 'Time');
         data.addColumn('number', 'Ch1');

         //GETING DATA
         for (i=0; i<decData.length; i++) {
           var num = i*(0.01);
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
         enableInteractivity: false,
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

