
    //LOAD KNOB VALUES
function values(val) {
        //console.log('Knob HValue:',val);
        hValue = val;
        //console.log('TEST',hVal);
            };

// Load the Visualization API and the piechart package.
    google.load('visualization', '1', {'packages':['corechart']});
      
    // Set a callback to run when the Google Visualization API is loaded.
    google.setOnLoadCallback(drawChart);


    function drawChart(val) {
      
        var jsonData = {
          
    cols: [{id: 'freq', label: 'Frequency', type: 'number'},
           {id: 'db', label: 'CH1', type: 'number'}],
    rows: [{c:[{v: '0.0'}, {v: '0.04'}]},
           {c:[{v: '7.0'}, {v: '2.335'}]},
           {c:[{v: '10.0'}, {v: '4.332'}]},
           {c:[{v: '13.0'}, {v: '5.566'}]},
           {c:[{v: '15.0'}, {v: '6.564'}]},
           {c:[{v: '18.0'}, {v: '5.507'}]},
           {c:[{v: '21.0'}, {v: '3.533'}]},
           {c:[{v: '23.0'}, {v: '2.475'}]},
           {c:[{v: '26.0'}, {v: '1.848'}]},
           {c:[{v: '29.0'}, {v: '-2.833'}]},
           {c:[{v: '32.0'}, {v: '-3.832'}]},
           {c:[{v: '34.0'}, {v: '-4.844'}]},
           {c:[{v: '37.0'}, {v: '-4.909'}]},
           {c:[{v: '40.0'}, {v: '-5.056'}]},
           {c:[{v: '42.0'}, {v: '-5.217'}]},
           {c:[{v: '45.0'}, {v: '-4.398'}]},
           {c:[{v: '48.0'}, {v: '-3.651'}]},
           {c:[{v: '50.0'}, {v: '-2.873'}]},
           {c:[{v: '53.0'}, {v: '0.991'}]},
           {c:[{v: '56.0'}, {v: '2.514'}]},
           {c:[{v: '59.0'}, {v: '2.838'}]},
           {c:[{v: '61.0'}, {v: '3.916'}]},
           {c:[{v: '64.0'}, {v: '2.816'}]},
           {c:[{v: '67.0'}, {v: '2.089'}]},
           {c:[{v: '69.0'}, {v: '4.054'}]},
           {c:[{v: '72.0'}, {v: '6.269'}]},
           {c:[{v: '75.0'}, {v: '7.578'}]},
           {c:[{v: '77.0'}, {v: '7.852'}]},
           {c:[{v: '80.0'}, {v: '8.03'}]},
           {c:[{v: '83.0'}, {v: '8.565'}]},
           {c:[{v: '86.0'}, {v: '9.032'}]},
           {c:[{v: '88.0'}, {v: '9.319'}]},
           {c:[{v: '91.0'}, {v: '9.394'}]},
           {c:[{v: '94.0'}, {v: '9.951'}]},
           {c:[{v: '96.0'}, {v: '5.123'}]},
           {c:[{v: '99.0'}, {v: '2.547'}]},
           {c:[{v: '102.0'}, {v: '0.878'}]},
              ]
        } 
        //jsonData = readTextFile("file:///Users/william/Desktop/GoogleCharts/freqDb.txt");
         
         
          //var hVal = {val};
          //hVal = eval(hVal);
          var hVal = val;
console.log('Knob HValue TEST:',hVal);
          var options = {
            title: '',
            titleTextStyle: {color:'black', fontSize: 15},
            legend: 'none',
            
            hAxis: {title: '', baselineColor:'black', gridlines:{color: 'gray', count: 5}, minorGridlines:{color: 'gray', count: 1}, viewWindow:{max:hVal, min:0}},

            vAxis: {title: 'Amp', baselineColor:'black', gridlines:{color: 'gray', count: 5}, minorGridlines:{color: 'gray', count: 1}, viewWindow:{max:10, min:-10}},

            backgroundColor: {fill: 'none', stroke: 'silver', strokeWidth: 3,},  
            colors: ['rgb(129,255,212)'], 
            chartArea:{backgroundColor:'',left:50,top:50,width:425,height:300},
            lineWidth: 2, 
            explorer: { actions: ['dragToZoom', 'rightClickToReset'] },  
            crosshair: {trigger: 'both', selected:{opacity: 0.8}, focused:{opacity:0.8}},   
          };


          // Create our data table out of JSON data loaded from server.
          var data = new google.visualization.DataTable(jsonData);

          // Instantiate and draw our chart, passing in some options.
          var chart = new google.visualization.LineChart(document.getElementById('ochart'));
          chart.draw(data, options);
        };


