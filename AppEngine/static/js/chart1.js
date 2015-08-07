    // Load the Visualization API and the piechart package.
    google.load('visualization', '1', {'packages':['corechart']});
      
    // Set a callback to run when the Google Visualization API is loaded.
    google.setOnLoadCallback(drawChart);

    function drawChart() {
    
        var jsonData = {
          
    cols: [{id: 'freq', label: 'Frequency', type: 'number'},
           {id: 'db', label: 'CH1', type: 'number'}],
    rows: [{c:[{v: '50.0'}, {v: '15.04'}]},
           {c:[{v: '77.0'}, {v: '14.335'}]},
           {c:[{v: '104.0'}, {v: '14.332'}]},
           {c:[{v: '131.0'}, {v: '14.566'}]},
           {c:[{v: '158.0'}, {v: '14.564'}]},
           {c:[{v: '185.0'}, {v: '14.507'}]},
           {c:[{v: '212.0'}, {v: '14.533'}]},
           {c:[{v: '239.0'}, {v: '14.475'}]},
           {c:[{v: '266.0'}, {v: '14.848'}]},
           {c:[{v: '293.0'}, {v: '16.833'}]},
           {c:[{v: '320.0'}, {v: '17.832'}]},
           {c:[{v: '347.0'}, {v: '18.844'}]},
           {c:[{v: '374.0'}, {v: '18.909'}]},
           {c:[{v: '401.0'}, {v: '19.056'}]},
           {c:[{v: '428.0'}, {v: '20.217'}]},
           {c:[{v: '455.0'}, {v: '21.398'}]},
           {c:[{v: '482.0'}, {v: '20.651'}]},
           {c:[{v: '509.0'}, {v: '17.873'}]},
           {c:[{v: '536.0'}, {v: '16.991'}]},
           {c:[{v: '563.0'}, {v: '15.514'}]},
           {c:[{v: '590.0'}, {v: '14.838'}]},
           {c:[{v: '617.0'}, {v: '14.916'}]},
           {c:[{v: '644.0'}, {v: '14.816'}]},
           {c:[{v: '671.0'}, {v: '14.089'}]},
           {c:[{v: '698.0'}, {v: '14.054'}]},
           {c:[{v: '725.0'}, {v: '14.269'}]},
           {c:[{v: '752.0'}, {v: '14.578'}]},
           {c:[{v: '779.0'}, {v: '14.852'}]},
           {c:[{v: '806.0'}, {v: '15.03'}]},
           {c:[{v: '833.0'}, {v: '14.565'}]},
           {c:[{v: '860.0'}, {v: '13.032'}]},
           {c:[{v: '887.0'}, {v: '14.319'}]},
           {c:[{v: '914.0'}, {v: '15.394'}]},
           {c:[{v: '941.0'}, {v: '14.951'}]},
           {c:[{v: '968.0'}, {v: '14.123'}]},
           {c:[{v: '995.0'}, {v: '14.547'}]},
           {c:[{v: '1022.0'}, {v: '14.878'}]},
              ]
        } 
        //jsonData = readTextFile("file:///Users/william/Desktop/GoogleCharts/freqDb.txt");
          var options = {
            title: 'MMIC Amplifier @ -45degC',
            titleTextStyle: {color:'white', fontSize: 15, fontName: 'NexaBold'},
            legend: {alignment:'center', textStyle:{color:'lightgray'}},
            hAxis: {title: 'frequency',titleTextStyle:{color:'lightgray', fontName: 'NexaLight'}, textStyle:{color:'lightgray'}, baselineColor:'none', gridlines:{color: 'none', count: 5},viewWindowMode:'explicit'},
            vAxis: {title: '', titleTextStyle:{color:'lightgray'}, textStyle:{color:'lightgray'}, baselineColor:'white', gridlines:{color: 'none', count: 0}, format: '##.###', viewWindowMode:'explicit'},
            backgroundColor: {fill: 'black', stroke: 'silver', strokeWidth: 3,},               
            colors: ['rgb(2,255,253)'], 
            curveType: 'function',
            lineWidth: 2,
            enableInteractivity: false,         
          };



          // Create our data table out of JSON data loaded from server.
          var data = new google.visualization.DataTable(jsonData);

          // Instantiate and draw our chart, passing in some options.
          var chart = new google.visualization.LineChart(document.getElementById('chart1'));
          chart.draw(data, {width: 300, height: 200});
          chart.draw(data, options);
        }

