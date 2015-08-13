
// DUT WIDGETS //
    function addWidget(type,savedSettings) {
        console.log('addWidget: Type = ', type);
        console.log('addWidget!');

        var testPlanHTML = "";
        var index;
        var d = document.getElementById('testPlan');
        var children = d.childNodes;
        console.log('addWidget: children.length =',children.length);
        console.log('addWidget: children =',children);
        
        for (index = 0; index < children.length; index++) {
            //console.log('removeDUT: index =',index);
            var planItemType = children[index].getAttribute('type');
            console.log('addWidget: type DUT? ',planItemType === 'dut')
            console.log('addWidget: planItemType =',planItemType);
            if (planItemType === 'dut') {
                console.log('TYPE DUT');
                
                var dutName = children[index].children[1].children[0].value;
                var dutType = children[index].children[1].children[1].children[1].value;
                var dutSettings = children[index].children[1].children[2].children[1].value;

                testPlanHTML+= "<div type='dut' class='appBox' id='" + String(index) + "'>";
                testPlanHTML+= "<h4 class='appTitle'>DUT - <span onclick='removeWidget(" + index + ")' class='appRemove glyphicon glyphicon-remove-circle' style='left:810px;'></span></h4>";
                testPlanHTML+= "<form method='post'>";

                testPlanHTML+= "<input class='nameWidget' type='text' name='dut_name' value='" + dutName;
                testPlanHTML+= "' placeholder='name goes here'>";

                testPlanHTML+= "<div class='row appRow'><tr><td class='label'>";
                testPlanHTML+= "<p class='appLabel'>Device Under Test Type:</p>"; 
                testPlanHTML+= "<input autocomplete='off' class='appInput' style='border-top-right-radius: 5px; border-top-left-radius: 5px;' type='text' name='dut_type' value='" + dutType;
                testPlanHTML+= "'></td></tr></div>";

                testPlanHTML+= "<div style='position:relative; top:20px;' class='row appRow'><tr><td class='label'>";
                testPlanHTML+= "<p class='appLabel'>Settings:</p>"; 
                testPlanHTML+= "<input autocomplete='off' class='appInput' style='border-bottom-right-radius: 5px; border-bottom-left-radius: 5px;' type='text' name='settings' value='" + dutSettings;
                testPlanHTML+= "'></td></tr></div>";
                             
                testPlanHTML+= "</form>";
                testPlanHTML+= "</div>";
            }else if(planItemType === 'config') {
                console.log('TYPE config');
                
                var configName = children[index].children[0].children[1].children[0].value
                var configBand = children[index].children[0].children[1].children[1].children[1].value
                var configSampleRate = children[index].children[0].children[1].children[2].children[1].value
                var configSampleSize = children[index].children[0].children[1].children[3].children[1].value
                var configResolution = children[index].children[0].children[1].children[4].children[1].value
                var configChNum = children[index].children[0].children[1].children[5].children[1].value
                //Search results
                var configResults = children[index].children[1].children[0].children[0].children[1].innerHTML;
                var configInstType = children[index].children[1].children[0].children[1].children[1].innerHTML;
                var configHardware = children[index].children[1].children[0].children[2].children[1].innerHTML;
                var configAvail = children[index].children[1].children[0].children[3].children[1].innerHTML;

                testPlanHTML+= "<div type='config' class='configBox' id='" + String(index) + "'>";
                testPlanHTML+= "<div id='configSearch' class='col-md-4'>";
                testPlanHTML+= "<h4 class='appTitle'>Config - <span onclick='removeWidget(" + index + ")' class='appRemove glyphicon glyphicon-remove-circle' style='left:777px;'></span></h4>";
                testPlanHTML+= "<form method='post'>";
                testPlanHTML+= "<input class='nameWidget' type='text' name='config_name' value='" + configName;
                testPlanHTML+= "' placeholder='name goes here'>";
                
                testPlanHTML+= "<div class='row appRow'>";
                testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Bandwidth(Hz):</p>"; 
                testPlanHTML+= "<input autocomplete='off' class='appInput' style='border-top-right-radius: 5px; border-top-left-radius: 5px;' type='text' name='analog_bandwidth' placeholder='20,000,000' value='" + configBand;
                testPlanHTML+= "'></td></tr></div>";

                testPlanHTML+= "<div class='row appRow'>";
                testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Sample Rate(sps):</p>"; 
                testPlanHTML+= "<input autocomplete='off' class='appInput' type='text' name='analog_sample_rate' placeholder='20,000,000' value='" + configSampleRate;
                testPlanHTML+= "'></td></tr></div>";

                testPlanHTML+= "<div class='row appRow'>";
                testPlanHTML+= "<tr><td class='label'><p class='appLabel'> Buffer Size: </p>"; 
                testPlanHTML+= "<input autocomplete='off' class='appInput' type='text' name='capture_buffer_size' placeholder='12,000' value='" + configSampleSize;
                testPlanHTML+= "'></td></tr></div>";

                testPlanHTML+= "<div class='row appRow'>";
                testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Resolution: </p>"; 
                testPlanHTML+= "<input autocomplete='off' class='appInput' type='text' name='resolution' placeholder='12' value='" + configResolution;
                testPlanHTML+= "'></td></tr></div>";

                testPlanHTML+= "<div style='margin-bottom:10px;' class='row appRow'>";
                testPlanHTML+= "<tr><td class='label'><p class='appLabel'># of Channels: </p>"; 
                testPlanHTML+= "<input autocomplete='off' class='appInput' style='margin-bottom:0px; border-bottom-right-radius: 5px; border-bottom-left-radius: 5px;' type='text' placeholder='2' name='capture_channels' value='" + configChNum;
                testPlanHTML+= "'></td></tr></div>";

                          
                testPlanHTML+= "</form>";
                testPlanHTML+= "</div>";

                testPlanHTML+= "<div id='configSearchResults' class='col-md-4'>";
                testPlanHTML+= "<form method='post'>";

                testPlanHTML+= "<div class='row appRow'>";
                testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Results:</p>"; 
                testPlanHTML+= "<p class='configResults' style='width: 180px;' id='results" + index;
                testPlanHTML+= "'>" + configResults;
                testPlanHTML+= "</p></td></tr></div>";

                testPlanHTML+= "<div class='row appRow'>";
                testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Instrument Type:</p>"; 
                testPlanHTML+= "<p class='configResults' style='' type='text' name='selected_inst_type' value='' id='instType" + index;
                testPlanHTML+= "'>" + configInstType;
                testPlanHTML+= "</p></td></tr></div>";

                testPlanHTML+= "<div class='row appRow'>";
                testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Hardware:</p>"; 
                testPlanHTML+= "<p class='configResults' style='' type='text' name='selected_hardware' value='' id='hardware" + index;
                testPlanHTML+= "'>" + configHardware;
                testPlanHTML+= "</p></td></tr></div>";

                testPlanHTML+= "<div class='row appRow'>";
                testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Available Instruments:</p>"; 
                testPlanHTML+= "<p class='configResults' id='avail" + index;
                testPlanHTML+= "''>" + configAvail;
                testPlanHTML+= "</p></td></tr></div>";

                testPlanHTML+= "</form>";
                testPlanHTML+= "</div>";
                testPlanHTML+= "<button id='configSearchBtn' onclick='configSearch(" + index + ")'>SEARCH</button>";   
                testPlanHTML+= "</div>";

                //$('#configSearchBtn').trigger('click'); 
            }else if(planItemType === 'measurement') {
                console.log('TYPE meas');
                var measName = children[index].children[1].children[0].value;
                var measType = children[index].children[1].children[1].children[1].value     
                var measStart = children[index].children[1].children[2].children[1].value;
                var measStop = children[index].children[1].children[3].children[1].value
                console.log('rmsStart = ', measStart);
                console.log('rmsStop = ', measStop);

                testPlanHTML+= "<div type='measurement' class='appBox' id='" + String(index) + "'>";
                testPlanHTML+= "<h4 class='appTitle'>RMS Measurement - <span onclick='removeWidget(" + index + ")' class='appRemove glyphicon glyphicon-remove-circle' style='left:685px;'></span></h4>";
                testPlanHTML+= "<form method='post'>";
                testPlanHTML+= "<input style='left:190px;' class='nameWidget' type='text' name='meas_name' value='" + measName;
                testPlanHTML+= "' placeholder='name goes here'>";
                testPlanHTML+= "<div class='row appRow'>";
                testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Meas Type:</p>";                   
                testPlanHTML+= "<input autocomplete='off' class='appInput' style='border-top-right-radius: 5px; border-top-left-radius: 5px;' type='text' name='meas_type' placeholder='RMS' value='" + measType;
                testPlanHTML+= "'></td></div>";
                testPlanHTML+= "<div class='row appRow'>";
                testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Start Time(sec):</p>";                   
                testPlanHTML+= "<input autocomplete='off' class='appInput' type='text' name='meas_start_time' placeholder='200' value='" + measStart;
                testPlanHTML+= "'></td></div>";
                testPlanHTML+= "<div class='row appRow'>";
                testPlanHTML+= "<td class='label'><p class='appLabel'>Stop Time(sec):</p>"
                testPlanHTML+= "<input autocomplete='off' class='appInput' style='border-bottom-right-radius: 5px; border-bottom-left-radius: 5px;' type='text' name='meas_stop_time' placeholder='400' value='" + measStop;
                testPlanHTML+= "'></td></tr></div>";                                                       
                testPlanHTML+= "</form>";
                testPlanHTML+= "</div>";
            }else {
                console.log('no type match :(');
            };                          
        };
        if (type === 'dut') {              
            console.log('TYPE DUT')
            testPlanHTML+= "<div type='dut' class='appBox' id='" + String(index) + "'>";
            testPlanHTML+= "<h4 class='appTitle'>DUT - <span onclick='removeWidget(" + index + ")' class='appRemove glyphicon glyphicon-remove-circle' style='left:810px;'></span></h4>";
            testPlanHTML+= "<form method='post'>";

            testPlanHTML+= "<input class='nameWidget' type='text' name='dut_name' value='' placeholder='name goes here'>";

            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Device Under Test Type:</p>"; 
            testPlanHTML+= "<input autocomplete='off' class='appInput' style='border-top-right-radius: 5px; border-top-left-radius: 5px;' type='text' name='dut_type' value=''></td></tr></div>";

            testPlanHTML+= "<div style='position:relative; top:20px;' class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Settings:</p>"; 
            testPlanHTML+= "<input autocomplete='off' class='appInput' style='border-bottom-right-radius: 5px; border-bottom-left-radius: 5px;' type='text' name='settings' value=''></td></tr></div>";
                           
            testPlanHTML+= "</form>";
            testPlanHTML+= "</div>";

            document.getElementById("testPlan").innerHTML = testPlanHTML; 
            console.log('addDUT: testPlanHTML = ', testPlanHTML); 
        }else if(type === 'config') {
            console.log('TYPE Config')
            testPlanHTML+= "<div type='config' class='configBox' id='" + String(index) + "'>";
            testPlanHTML+= "<div id='configSearch' class='col-md-4'>";
            testPlanHTML+= "<h4 class='appTitle'>Config - <span onclick='removeWidget(" + index + ")' class='appRemove glyphicon glyphicon-remove-circle' style='left:777px;'></span></h4>";
            testPlanHTML+= "<form method='post'>";
            testPlanHTML+= "<input class='nameWidget' type='text' name='config_name' value='' placeholder='name goes here'>";

            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Bandwidth(Hz):</p>"; 
            testPlanHTML+= "<input autocomplete='off' class='appInput' style='border-top-right-radius: 5px; border-top-left-radius: 5px;' type='text' placeholder='20,000,000' name='analog_bandwidth' value=''></td></tr></div>";

            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Sample Rate(sps):</p>"; 
            testPlanHTML+= "<input autocomplete='off' class='appInput' type='text' placeholder='20,000,000' name='analog_sample_rate' value=''></td></tr></div>";

            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'> Buffer Size: </p>"; 
            testPlanHTML+= "<input autocomplete='off' class='appInput' type='text' placeholder='12,000' name='capture_buffer_size' value=''></td></tr></div>";

            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Resolution: </p>"; 
            testPlanHTML+= "<input autocomplete='off' class='appInput' type='text' placeholder='12' name='resolution' value=''></td></tr></div>";

            testPlanHTML+= "<div style='margin-bottom:10px;' class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'># of Channels: </p>"; 
            testPlanHTML+= "<input class='appInput' style='margin-bottom:0px; border-bottom-right-radius: 5px; border-bottom-left-radius: 5px;' type='text' placeholder='2' name='capture_channels' autocomplete='off' value=''></td></tr></div>";
                            
            testPlanHTML+= "</form>";
            testPlanHTML+= "</div>";

            testPlanHTML+= "<div id='configSearchResults' class='col-md-4'>";
            testPlanHTML+= "<form method='post'>";

            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Results:</p>"; 
            testPlanHTML+= "<p class='configResults' style='width: 180px;' id='results" + index;
            testPlanHTML+= "'></p></td></tr></div>";

            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Instrument Type:</p>"; 
            testPlanHTML+= "<p class='configResults' style='' type='text' name='selected_inst_type' value='' id='instType" + index;
            testPlanHTML+= "'></p></td></tr></div>";

            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Hardware:</p>"; 
            testPlanHTML+= "<p class='configResults' style='' type='text' name='selected_hardware' value='' id='hardware" + index;
            testPlanHTML+= "'></p></td></tr></div>";

            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Available Instruments:</p>"; 
            testPlanHTML+= "<p class='configResults' id='avail" + index;
            testPlanHTML+= "''></p></td></tr></div>";

            testPlanHTML+= "</form>";
            testPlanHTML+= "</div>";
            testPlanHTML+= "<button id='configSearchBtn' onclick='configSearch(" + index + ")'>SEARCH</button>"; 
            testPlanHTML+= "</div>";

            document.getElementById("testPlan").innerHTML = testPlanHTML; 
            console.log('addDUT: testPlanHTML = ', testPlanHTML); 
        }else if(type === 'measurement') {
            testPlanHTML+= "<div type='measurement' class='appBox' id='" + String(index) + "'>";
            testPlanHTML+= "<h4 class='appTitle'>RMS Measurement - <span onclick='removeWidget(" + index + ")' class='appRemove glyphicon glyphicon-remove-circle' style='left:685px;'></span></h4>";
            testPlanHTML+= "<form method='post'>";
            testPlanHTML+= "<input style='left:190px;' class='nameWidget' type='text' name='meas_name' value='' placeholder='name goes here'>";
            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Meas Type:</p>";                   
            testPlanHTML+= "<input autocomplete='off' class='appInput' type='text' style='border-top-right-radius: 5px; border-top-left-radius: 5px;' name='meas_type' placeholder='RMS' value=''></td></div>";
            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Start Time(sec):</p>";                   
            testPlanHTML+= "<input autocomplete='off' class='appInput' type='text' name='meas_start_time' placeholder='200' value=''></td></div>";
            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<td class='label'><p class='appLabel'>Stop Time(sec):</p>";
            testPlanHTML+= "<input autocomplete='off' class='appInput' style='border-bottom-right-radius: 5px; border-bottom-left-radius: 5px;' type='text' name='meas_stop_time' placeholder='400' value=''></td></tr></div>";                                                         
            testPlanHTML+= "</form>";
            testPlanHTML+= "</div>";

            document.getElementById("testPlan").innerHTML = testPlanHTML; 
            console.log('addDUT: testPlanHTML = ', testPlanHTML);
        }else if(type === 'sdut') {
            
            var sdutName = savedSettings.dut_name;
            var sdutType = savedSettings.dut_type
            var sdutSettings = savedSettings.settings;

            testPlanHTML+= "<div type='dut' class='appBox' id='" + String(index) + "'>";
            testPlanHTML+= "<h4 class='appTitle'>DUT - <span onclick='removeWidget(" + index + ")' class='appRemove glyphicon glyphicon-remove-circle' style='left:810px;'></span></h4>";
            testPlanHTML+= "<form method='post'>";

            testPlanHTML+= "<input class='nameWidget' type='text' name='dut_name' value='" + sdutName;
            testPlanHTML+= "' placeholder='name goes here'>";

            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Device Under Test Type:</p>"; 
            testPlanHTML+= "<input autocomplete='off' class='appInput' style='border-top-right-radius: 5px; border-top-left-radius: 5px;' type='text' name='dut_type' value='" + sdutType;
            testPlanHTML+= "'></td></tr></div>";

            testPlanHTML+= "<div style='position:relative; top:20px;' class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Settings:</p>"; 
            testPlanHTML+= "<input autocomplete='off' class='appInput' style='border-bottom-right-radius: 5px; border-bottom-left-radius: 5px;' type='text' name='settings' value='" + sdutSettings;
            testPlanHTML+= "'></td></tr></div>";
                           
            testPlanHTML+= "</form>";
            testPlanHTML+= "</div>";
            document.getElementById("testPlan").innerHTML = testPlanHTML;  
        }else if(type === 'sconfig') {
            console.log('addWidget: savedSettings sconfig= ',savedSettings);

        };
        $(document).ready(function () { 
              $(".collapseCommitTest").fadeIn("fast");           
        });         
    };

    (function($) {
        $.fn.getAttributes = function() {
            var attributes = {}; 

            if( this.length ) {
                $.each( this[0].attributes, function( index, attr ) {
                    attributes[ attr.name ] = attr.value;
                } ); 
            }
            return attributes;
        };
    })(jQuery);

    var d;
    function removeWidget(index) {
      d = document.getElementById('testPlan');
      
      console.log('removeWidget: d.haschildnodes =',d.hasChildNodes());
      console.log('removeWidget: d.firstchild =',d.firstChild);
      var olddiv = document.getElementById(index);
      d.removeChild(olddiv);
      //d.removeChild(d.firstChild);
      var children = d.childNodes;
      for (var i = 0; i < children.length; i++) {
        console.log('removeWidget: i =',i);
      }
    };


    //ADD WIDGET BUTTON CONTROL
    $("#newDUT").click(function () {
      addWidget('dut');
    });
    $("#newConfig").click(function () {
      addWidget('config');
    });
    $("#RMS").click(function () {
      addWidget('measurement');
    });
    $("#configSearchBtn").click(function () {
        configSearch();
    });
    $("#commitBtn").click(function () {
        commitBtn();
    });

//CONFIG SEARCH BUTTON
    var searchTimerID;
    function configSearch(i) {
        console.log('configSearch!!!!!');
        var d = document.getElementById('testPlan');
        var children = d.childNodes;

        var configName = children[i].children[0].children[1].children[0].value
        var configBand = new Number(children[i].children[0].children[1].children[1].children[1].value);
        var configSampleRate = new Number(children[i].children[0].children[1].children[2].children[1].value);
        var configSampleSize = new Number(children[i].children[0].children[1].children[3].children[1].value);
        var configResolution = new Number(children[i].children[0].children[1].children[4].children[1].value);
        var configChNum = new Number(children[i].children[0].children[1].children[5].children[1].value);

        var testSetUp = document.getElementById('testSetup');
        var testSetUpInfo = testSetUp.childNodes;
        var companyName = 'Acme';
        var testPlanName = testSetUpInfo[1].children[0].children[1].children[0].value;
        
        var config_search_url = 'https://gradientone-test.appspot.com';
        //var config_search_url = window.location.origin;
        config_search_url += "/instlookup/";
        config_search_url += companyName + "/" + testPlanName + "/";
        config_search_url += configName;
        console.log('configSearch: config_search_url = ',config_search_url);

        var searchInput = JSON.stringify({"analog_bandwidth":configBand,
            "analog_sample_rate":configSampleRate, "capture_buffer_size":configSampleSize,
             "capture_channels":configChNum, "resolution":configResolution,"timepost":false});
        console.log('configSearch: searchInput = ',searchInput);
        $.ajax({
        type: "POST",
        url: config_search_url,
        data: searchInput,
        dataType: 'json',

        success: function(data, textStatus, jqXHR)
        {
            console.log('commitBtn: Ajax post was a success!');
        },
        });   
        //searchTimerID = setTimeout(getSearchResults, 3000);
        function getSearchResults() {
            console.log('getSearchResults called!!!');
            //widget_url = 'https://gradientone-test.appspot.com/testresults/widgets/Acme.json'
              //var search_results_url = window.location.origin;
              var search_results_url = 'https://gradientone-test.appspot.com';
              search_results_url += "/instlookup/" + companyName + "/";
              search_results_url += testPlanName + "/";
              search_results_url += configName;
              console.log('getSearchResults: search_results_url =',search_results_url);
              $.ajax({
                  async: true,
                  url: search_results_url,            
                  dataType: 'json',
               }).done(function (results) {
                  var searchResults = results;
                  console.log('getSearchResults: results =', results);
                  console.log('getSearchResults: i = ', i);

                  var configResults = searchResults.explanations;
                  console.log('configResults = ',configResults);
                  var configInstType = searchResults.selected_inst_type;
                  console.log('configInstType = ',configInstType);
                  var configHardware = searchResults.selected_hardware;
                  console.log('configHardware = ',configHardware);
                  var configAvail = searchResults.avail_inst;
                  console.log('configAvail = ',configAvail);

                  console.log('SEARCHING');
                  console.log('after searching =results.length ',results.length)

                  var resultsTextNode = document.createTextNode(configResults);
                  var typeTextNode = document.createTextNode(configInstType);
                  var hardwareTextNode = document.createTextNode(configHardware);
                  var availTextNode = document.createTextNode(configAvail);
                  var d = document.getElementById('testPlan');
                  var children = d.childNodes;
                  for (var j=0;j<4;j++){
                    children[i].children[1].children[0].children[j].children[1].innerHTML = "";
                  };
                  children[i].children[1].children[0].children[0].children[1].appendChild(resultsTextNode);
                  children[i].children[1].children[0].children[1].children[1].appendChild(typeTextNode);
                  children[i].children[1].children[0].children[2].children[1].appendChild(hardwareTextNode);
                  children[i].children[1].children[0].children[3].children[1].appendChild(availTextNode);
              });  
              //console.log('STOP POLLING FOR SEARCH RESULTS!!');
              //clearTimeout(searchTimerID);   
        };
        getSearchResults(); 
    };

//CANVAS ORDER
    $(document).ready(function() {
        $(".droppable").sortable({
          update: function( event, ui ) {
            Dropped();
            console.log('indexArray = ', indexArray);
            //indexArray=[];
            console.log("New position: ", ui.item.index());
            index ='dev 1  Position:' + ui.item.index();
            
           }
        });    
    });


    var testPlanName;
    var startTime;
    var testPlanAuthor;
    var companyName;
    var configArray = [];
    var measArray = [];
    var dutArray = [];
    var indexArray = [];

    function postInitInfo() {
        console.log('postInitInfo called!!!!');
        var testSetUp = document.getElementById('testSetup');
        var testSetUpInfo = testSetUp.childNodes;
        testPlanName = testSetUpInfo[3].children[0].children[1].children[0].value;
        companyName = 'Acme';
        testPlanAuthor = 'nedwards';
        startTime = testSetUpInfo[3].children[1].children[1].children[0].value;
        d = new Date(startTime);
        var startMS = d.getTime();
        startNowLogic = new Boolean(
       testSetUpInfo[3].children[1].children[1].children[3].children[1].checked);

        //var initInfo_url = 'https://gradientone-test.appspot.com/testconfiginput';
        var initInfo_url = window.location.origin;
        initInfo_url += "/testconfiginput";
        var initData = JSON.stringify({"testplan_name":testPlanName,"author":testPlanAuthor,"company_nickname":companyName,"start_time":startMS,"start_now":startNowLogic});
        console.log('postInitInfo: initData = ', initData);
        $.ajax({
        type: "POST",
        url: initInfo_url,
        data: initData,
        dataType: 'json',
        success: function(data, textStatus, jqXHR)
        {
            console.log('commitBtn: Ajax post was a success!');
        },
        });
    };

    function commitBtn() {
        Dropped(); //get order 
        var testSetUp = document.getElementById('testSetup');
        var testSetUpInfo = testSetUp.childNodes;
        testPlanName = testSetUpInfo[1].children[0].children[1].children[0].value;
        companyName = 'Acme';
        testPlanAuthor = 'nedwards';
        startTime = testSetUpInfo[1].children[1].children[1].children[0].value;
        d = new Date(startTime);
        var startMS = d.getTime();
        var startNowLogic = new Boolean(
  testSetUpInfo[1].children[1].children[1].children[3].children[1].checked);
        //LOOP FOR WIDGET SETTINGS 
        var d = document.getElementById('testPlan');
        var children = d.childNodes;
        commitData = [];
        for (index = 0; index < children.length; index++) {
            console.log('removeDUT: index =',index);
            var planItemType = children[index].getAttribute('type');
            if (planItemType === 'dut') {
                var dutName = children[index].children[1].children[0].value;
                var dutType = children[index].children[1].children[1].children[1].value;
                var dutSettings = children[index].children[1].children[2].children[1].value;

                var dutJsonObj = {"dut_name":dutName,"dut_type":dutType,"settings":dutSettings};

                dutArray.push(dutJsonObj);
            }else if(planItemType === 'config') {
                var configName = children[index].children[0].children[1].children[0].value
                var configBand = children[index].children[0].children[1].children[1].children[1].value
                var configSampleRate = children[index].children[0].children[1].children[2].children[1].value
                var configSampleSize = children[index].children[0].children[1].children[3].children[1].value
                var configResolution = children[index].children[0].children[1].children[4].children[1].value
                var configChNum = children[index].children[0].children[1].children[5].children[1].value
                //config search results
               // var configResults = children[index].children[1].children[0].children[0].children[1].innerHTML;
                var configInstType = children[index].children[1].children[0].children[1].children[1].innerHTML;
                var configHardware = children[index].children[1].children[0].children[2].children[1].innerHTML;
               // var configAvail = children[index].children[1].children[0].children[3].children[1].innerHTML;

                var configJsonObj = {"config_name":configName,"analog_bandwidth":configBand,"analog_sample_rate":configSampleRate,"capture_buffer_size":configSampleSize,"resolution":configResolution,"capture_channels":configChNum,"instrument_type":configInstType,"hardware":configHardware};
                configArray.push(configJsonObj);
            }else if(planItemType === 'measurement') {
                var measName = children[index].children[1].children[0].value;
                var measType = children[index].children[1].children[1].children[1].value     
                var measStart = children[index].children[1].children[2].children[1].value;
                var measStop = children[index].children[1].children[3].children[1].value  

                var measJsonObj = {"meas_name":measName,"meas_type":measType,"meas_start_time":measStart,"meas_stop_time":measStop};

                measArray.push(measJsonObj);
            }else { 
                console.log('commitBtn: no widget type match!');
            }
        };   
        

        //var commit_url = 'https://gradientone-test.appspot.com/testconfiginput';
        var commit_url = window.location.origin + "/testconfiginput";
        console.log('commitBtn: indexArray = ', indexArray);
        var commitData = JSON.stringify({"testplan_name":testPlanName,"author":testPlanAuthor,"company_nickname":companyName,"start_time":startMS,"start_now":startNowLogic,"configs":configArray,"meas":measArray,"duts":dutArray,"order":indexArray});
        console.log('commitBtn: commitData = ', commitData);
        $.ajax({
        type: "POST",
        url: commit_url,
        data: commitData,
        dataType: 'json',
        success: function(data, textStatus, jqXHR)
        {
            console.log('commitBtn: Ajax post was a success!');
        },
        });
        alert('Test Plan Commited');

        d.innerHTML = '';
        testSetUpInfo[1].children[0].children[1].children[0].value = '';
        testSetUpInfo[1].children[1].children[1].children[0].value = '';
        $(".collapseNewTest").hide();
        $(".collapseCommitTest").hide();
        $("#accordion").hide();
    };
   
    function Dropped(event, ui){
        indexArray = [];
        var apps = document.getElementsByClassName("appBox");
        var d = document.getElementById('testPlan');
        var children = d.childNodes;
        console.log('Dropped: children.length =',children.length);

            for(var i = 0;i<children.length;i++) {
                
                var planItemType = children[i].getAttribute('type');
                if (planItemType == 'config') {
                    var planItemName = children[i].children[0].children[1].children[0].value;
                }else {
                    var planItemName = children[i].children[1].children[0].value;
                }

                var orderInfo = planItemType + ':' + planItemName + ':' + i;
                indexArray.push(orderInfo); 

            }
        $(".draggable").each(function(){        
        });
    }  
