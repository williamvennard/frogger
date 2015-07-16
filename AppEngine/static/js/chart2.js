    // Load the Visualization API and the piechart package.
    google.load('visualization', '1', {'packages':['corechart']});
      
    // Set a callback to run when the Google Visualization API is loaded.
    google.setOnLoadCallback(drawChart);

    function drawChart() {
    
        var jsonData = {
          
    cols: [{id: 'freq', label: 'Frequency', type: 'number'},
           {id: 'db', label: 'CH1', type: 'number'}],
    rows: [{c:[{v: '50.0'}, {v: '25.04'}]},
           {c:[{v: '77.0'}, {v: '24.335'}]},
           {c:[{v: '104.0'}, {v: '24.332'}]},
           {c:[{v: '131.0'}, {v: '24.566'}]},
           {c:[{v: '158.0'}, {v: '24.564'}]},
           {c:[{v: '185.0'}, {v: '24.507'}]},
           {c:[{v: '212.0'}, {v: '24.533'}]},
           {c:[{v: '239.0'}, {v: '24.475'}]},
           {c:[{v: '266.0'}, {v: '24.848'}]},
           {c:[{v: '293.0'}, {v: '24.833'}]},
           {c:[{v: '320.0'}, {v: '24.832'}]},
           {c:[{v: '347.0'}, {v: '24.844'}]},
           {c:[{v: '374.0'}, {v: '24.909'}]},
           {c:[{v: '401.0'}, {v: '25.056'}]},
           {c:[{v: '428.0'}, {v: '25.217'}]},
           {c:[{v: '455.0'}, {v: '25.398'}]},
           {c:[{v: '482.0'}, {v: '25.651'}]},
           {c:[{v: '509.0'}, {v: '25.873'}]},
           {c:[{v: '536.0'}, {v: '25.991'}]},
           {c:[{v: '563.0'}, {v: '26.514'}]},
           {c:[{v: '590.0'}, {v: '26.838'}]},
           {c:[{v: '617.0'}, {v: '26.916'}]},
           {c:[{v: '644.0'}, {v: '26.816'}]},
           {c:[{v: '671.0'}, {v: '27.089'}]},
           {c:[{v: '698.0'}, {v: '27.054'}]},
           {c:[{v: '725.0'}, {v: '27.269'}]},
           {c:[{v: '752.0'}, {v: '27.578'}]},
           {c:[{v: '779.0'}, {v: '27.852'}]},
           {c:[{v: '806.0'}, {v: '28.03'}]},
           {c:[{v: '833.0'}, {v: '28.565'}]},
           {c:[{v: '860.0'}, {v: '29.032'}]},
           {c:[{v: '887.0'}, {v: '29.319'}]},
           {c:[{v: '914.0'}, {v: '29.394'}]},
           {c:[{v: '941.0'}, {v: '29.951'}]},
           {c:[{v: '968.0'}, {v: '30.123'}]},
           {c:[{v: '995.0'}, {v: '30.547'}]},
           {c:[{v: '1022.0'}, {v: '30.878'}]},
              ]
        } 
        //jsonData = readTextFile("file:///Users/william/Desktop/GoogleCharts/freqDb.txt");
        var options = {
          title: 'MMIC Amplifier @ +25degC',
          titleTextStyle: {color:'white', fontSize: 15, fontName: 'NexaBold'},
          legend: {alignment:'center', textStyle:{color:'white'}},
          hAxis: {title: 'frequency',titleTextStyle:{color:'lightgray', fontName: 'NexaLight'}, textStyle:{color:'lightgray'}, baselineColor:'none', gridlines:{color: 'none', count: 5},viewWindowMode:'explicit'},
          vAxis: {title: '', titleTextStyle:{color:'lightgray'}, textStyle:{color:'lightgray'}, baselineColor:'white', gridlines:{color: 'none', count: 0}, format: '##.###', viewWindowMode:'explicit'},
          backgroundColor: {fill: 'black', stroke: 'silver', strokeWidth: 3,},  
          colors: ['rgb(248,157,0)'],
          chartArea:{backgroundColor:'black'},
          enableInteractivity: false,
        };
        

          // Create our data table out of JSON data loaded from server.
          var data = new google.visualization.DataTable(jsonData);

          // Instantiate and draw our chart, passing in some options.
          var chart = new google.visualization.AreaChart(document.getElementById('chart2'));
          chart.draw(data, {width: 300, height: 200});
          chart.draw(data, options);
        }