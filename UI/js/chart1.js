    // Load the Visualization API and the piechart package.
    google.load('visualization', '1', {'packages':['corechart']});
      
    // Set a callback to run when the Google Visualization API is loaded.
    google.setOnLoadCallback(drawChart);
 
    function drawChart() {
    
        var jsonData = {
          
    cols: [{id: 'freq', label: 'Frequency', type: 'number'},
           {id: 'db11', label: 'S11', type: 'number'},{id: 'db12', label: 'S22', type: 'number'}],
    rows: [{c:[{v: '50.0'}, {v: '25.04'}, {v: '20.154'}]},
           {c:[{v: '77.0'}, {v: '24.335'}, {v: '19.554'}]},
           {c:[{v: '104.0'}, {v: '24.332'}, {v: '19.357'}]},
           {c:[{v: '131.0'}, {v: '24.566'}, {v: '19.652'}]},
           {c:[{v: '158.0'}, {v: '24.564'}, {v: '19.764'}]},
           {c:[{v: '185.0'}, {v: '24.507'}, {v: '20.151'}]},
           {c:[{v: '212.0'}, {v: '24.533'}, {v: '20.343'}]},
           {c:[{v: '239.0'}, {v: '24.475'}, {v: '20.555'}]},
           {c:[{v: '266.0'}, {v: '24.848'}, {v: '20.646'}]},
           {c:[{v: '293.0'}, {v: '24.833'}, {v: '20.752'}]},
           {c:[{v: '320.0'}, {v: '24.832'}, {v: '20.956'}]},
           {c:[{v: '347.0'}, {v: '24.844'}, {v: '21.176'}]},
           {c:[{v: '374.0'}, {v: '24.909'}, {v: '21.266'}]},
           {c:[{v: '401.0'}, {v: '25.056'}, {v: '21.451'}]},
           {c:[{v: '428.0'}, {v: '25.217'}, {v: '21.658'}]},
           {c:[{v: '455.0'}, {v: '25.398'}, {v: '22.746'}]},
           {c:[{v: '482.0'}, {v: '25.651'}, {v: '22.76'}]},
           {c:[{v: '509.0'}, {v: '25.873'}, {v: '22.853'}]},
           {c:[{v: '536.0'}, {v: '25.991'}, {v: '22.95'}]},
           {c:[{v: '563.0'}, {v: '26.514'}, {v: '23.251'}]},
           {c:[{v: '590.0'}, {v: '26.838'}, {v: '23.458'}]},
           {c:[{v: '617.0'}, {v: '26.916'}, {v: '23.554'}]},
           {c:[{v: '644.0'}, {v: '26.816'}, {v: '24.564'}]},
           {c:[{v: '671.0'}, {v: '27.089'}, {v: '24.66'}]},
           {c:[{v: '698.0'}, {v: '27.054'}, {v: '24.767'}]},
           {c:[{v: '725.0'}, {v: '27.269'}, {v: '24.753'}]},
           {c:[{v: '752.0'}, {v: '27.578'}, {v: '24.865'}]},
           {c:[{v: '779.0'}, {v: '27.852'}, {v: '24.956'}]},
           {c:[{v: '806.0'}, {v: '28.03'}, {v: '24.991'}]},
           {c:[{v: '833.0'}, {v: '28.565'}, {v: '25.371'}]},
           {c:[{v: '860.0'}, {v: '29.032'}, {v: '25.77'}]},
           {c:[{v: '887.0'}, {v: '29.319'}, {v: '26.369'}]},
           {c:[{v: '914.0'}, {v: '29.394'}, {v: '26.775'}]},
           ]
        } 

          var options = {
            title: 'MMIC Amplifier @ +85degC',
            titleTextStyle: {color:'white', fontSize: 15},
            legend: {alignment:'center', textStyle:{color:'white'}},
            hAxis: {title: 'Frequency',titleTextStyle:{color:'white'}, textStyle:{color:'white'}, baselineColor:'white', gridlines:{color: 'white', count: 6}, minorGridlines:{color: 'white', count: 1}, viewWindowMode:'pretty'},
            vAxis: {title: 'dB', titleTextStyle:{color:'white'}, textStyle:{color:'white'}, baselineColor:'white', gridlines:{color: 'white', count: 6}, minorGridlines:{color: 'white', count: 1}},
            backgroundColor: {fill:'rgb(59,96,120)', stroke: 'silver', strokeWidth: 3,},                 
            colors: ['rgb(254,241,10)','rgb(231,61,35)'],
            chartArea:{backgroundColor:''},
            lineWidth: 1.5,
            curveType: 'function',
          }
        //jsonData = readTextFile("file:///Users/william/Desktop/GoogleCharts/freqDb.txt");

          // Create our data table out of JSON data loaded from server.
          var data = new google.visualization.DataTable(jsonData);

          // Instantiate and draw our chart, passing in some options.
          var chart = new google.visualization.LineChart(document.getElementById('chart1'));
          chart.draw(data, {width: 300, height: 200});
          chart.draw(data, options);
        }

