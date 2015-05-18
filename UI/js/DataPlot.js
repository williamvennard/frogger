    // Load the Visualization API and the piechart package.
    google.load('visualization', '1', {'packages':['corechart']});
      
    // Set a callback to run when the Google Visualization API is loaded.
    google.setOnLoadCallback(drawChart);

    function readTextFile(file)
    {
        var allText;
        var rawFile = new XMLHttpRequest();
        rawFile.open("GET", file, false);
        rawFile.onreadystatechange = function ()
        {
            if(rawFile.readyState === 4)
            {
                if(rawFile.status === 200 || rawFile.status == 0)
                {
                    var allText = rawFile.responseText;
                    //alert(allText);
                }
            }
        }
        rawFile.send(null);
        return allText;
    }  

    function drawChart() {
    
        var jsonData = {
          
    cols: [{id: 'freq', label: 'Frequency', type: 'number'},
           {id: 'db11', label: 'DB11', type: 'number'},{id: 'db12', label: 'DB12', type: 'number'}],
    rows: [{c:[{v: '50.0'}, {v: '-25.04'}, {v: '-16.754'}]},
           {c:[{v: '77.0'}, {v: '-24.335'}, {v: '-16.754'}]},
           {c:[{v: '104.0'}, {v: '-24.332'}, {v: '-16.757'}]},
           {c:[{v: '131.0'}, {v: '-24.566'}, {v: '-16.752'}]},
           {c:[{v: '158.0'}, {v: '-24.564'}, {v: '-16.764'}]},
           {c:[{v: '185.0'}, {v: '-24.507'}, {v: '-16.751'}]},
           {c:[{v: '212.0'}, {v: '-24.533'}, {v: '-16.743'}]},
           {c:[{v: '239.0'}, {v: '-24.475'}, {v: '-16.755'}]},
           {c:[{v: '266.0'}, {v: '-24.848'}, {v: '-16.746'}]},
           {c:[{v: '293.0'}, {v: '-24.833'}, {v: '-16.752'}]},
           {c:[{v: '320.0'}, {v: '-24.832'}, {v: '-16.756'}]},
           {c:[{v: '347.0'}, {v: '-24.844'}, {v: '-16.76'}]},
           {c:[{v: '374.0'}, {v: '-24.909'}, {v: '-16.766'}]},
           {c:[{v: '401.0'}, {v: '-25.056'}, {v: '-16.751'}]},
           {c:[{v: '428.0'}, {v: '-25.217'}, {v: '-16.758'}]},
           {c:[{v: '455.0'}, {v: '-25.398'}, {v: '-16.746'}]},
           {c:[{v: '482.0'}, {v: '-25.651'}, {v: '-16.76'}]},
           {c:[{v: '509.0'}, {v: '-25.873'}, {v: '-16.753'}]},
           {c:[{v: '536.0'}, {v: '-25.991'}, {v: '-16.75'}]},
           {c:[{v: '563.0'}, {v: '-26.514'}, {v: '-16.751'}]},
           {c:[{v: '590.0'}, {v: '-26.838'}, {v: '-16.758'}]},
           {c:[{v: '617.0'}, {v: '-26.916'}, {v: '-16.754'}]},
           {c:[{v: '644.0'}, {v: '-26.816'}, {v: '-16.754'}]},
           {c:[{v: '671.0'}, {v: '-27.089'}, {v: '-16.76'}]},
           {c:[{v: '698.0'}, {v: '-27.054'}, {v: '-16.767'}]},
           {c:[{v: '725.0'}, {v: '-27.269'}, {v: '-16.753'}]},
           {c:[{v: '752.0'}, {v: '-27.578'}, {v: '-16.765'}]},
           {c:[{v: '779.0'}, {v: '-27.852'}, {v: '-16.756'}]},
           {c:[{v: '806.0'}, {v: '-28.03'}, {v: '-16.751'}]},
           {c:[{v: '833.0'}, {v: '-28.565'}, {v: '-16.771'}]},
           {c:[{v: '860.0'}, {v: '-29.032'}, {v: '-16.77'}]},
           {c:[{v: '887.0'}, {v: '-29.319'}, {v: '-16.769'}]},
           {c:[{v: '914.0'}, {v: '-29.394'}, {v: '-16.775'}]},
           ]
        } 
        //jsonData = readTextFile("file:///Users/william/Desktop/GoogleCharts/freqDb.txt");

          // Create our data table out of JSON data loaded from server.
          var data = new google.visualization.DataTable(jsonData);

          // Instantiate and draw our chart, passing in some options.
          var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
          chart.draw(data, {width: 400, height: 240});
        }

