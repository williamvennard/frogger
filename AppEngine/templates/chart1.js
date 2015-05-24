<script type="text/javascript">
    // Load the Visualization API and the corechart package.
    google.load('visualization', '1', {'packages':['corechart']});
      
    // Set a callback to run when the Google Visualization API is loaded.
    google.setOnLoadCallback(drawChart);
 
    function drawChart() {
    
        var jsonData = {
          
    cols: [{id: 'freq', label: 'Frequency', type: 'number'},
           {id: 'db11', label: 'S11', type: 'number'},{id: 'db12', label: 'S22', type: 'number'}],
    rows: [ 
            {% for d in datasets %}  
              {c:[{v: {{d.frequency}}}, {v: {{d.S11dB}}}, {v: {{d.S12dB}}}]},
            {% endfor %}
            ]
        } 

          var options = {
            title: 'MMIC Amplifier @ +85degC',
            titleTextStyle: {color:'black', fontSize: 16},
            legend: {alignment:'center'},
            hAxis: {title: 'Frequency'},
            vAxis: {title: 'dB'},
            backgroundColor: {color: 'white', stroke: 'silver', strokeWidth: 3,},                 
            colors: ['rgb(248,157,0)','rgb(75,19,115)'],
          }

          // Create our data table out of JSON data loaded from server.
          var data = new google.visualization.DataTable(jsonData);

          // Instantiate and draw our chart, passing in some options.
          var chart = new google.visualization.LineChart(document.getElementById('chart1'));
          chart.draw(data, {width: 300, height: 200});
          chart.draw(data, options);
        }
</script>
