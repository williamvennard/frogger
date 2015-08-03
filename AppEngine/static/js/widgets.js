

// DUT WIDGETS //
    function addWidget(type) {
        console.log('addWidget: Type = ', type);
        console.log('addDUT!');
        var testPlanHTML = "";
        var index;
        var d = document.getElementById('testPlan');
        var children = d.childNodes;
        console.log('addWidget: children.length =',children.length);
        console.log('addWidget: children =',children);
        
        for (index = 0; index < children.length; index++) {
            console.log('removeDUT: index =',index);
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
                testPlanHTML+= "<input class='appInput' style='border-top-right-radius: 5px; border-top-left-radius: 5px;' type='text' name='dut_type' value='" + dutType;
                testPlanHTML+= "'></td></tr></div>";

                testPlanHTML+= "<div style='position:relative; top:20px;' class='row appRow'><tr><td class='label'>";
                testPlanHTML+= "<p class='appLabel'>Settings:</p>"; 
                testPlanHTML+= "<input class='appInput' style='border-bottom-right-radius: 5px; border-bottom-left-radius: 5px;' type='text' name='settings' value='" + dutSettings;
                testPlanHTML+= "'></td></tr></div>";
                             
                testPlanHTML+= "</form>";
                testPlanHTML+= "</div>";
            }else if(planItemType === 'config') {
                console.log('TYPE config');
                //search
                var configName = children[index].children[0].children[1].children[0].value
                var configBand = children[index].children[0].children[1].children[1].children[1].value
                var configSampleRate = children[index].children[0].children[1].children[2].children[1].value
                var configSampleSize = children[index].children[0].children[1].children[3].children[1].value
                var configResolution = children[index].children[0].children[1].children[4].children[1].value
                var configChNum = children[index].children[0].children[1].children[5].children[1].value

                testPlanHTML+= "<div type='config' class='configBox' id='" + String(index) + "'>";
                testPlanHTML+= "<div id='configSearch' class='col-md-4'>";
                testPlanHTML+= "<h4 class='appTitle'>Instrument - <span onclick='removeWidget(" + index + ")' class='appRemove glyphicon glyphicon-remove-circle' style='left:740px;'></span></h4>";
                testPlanHTML+= "<form method='post'>";
                testPlanHTML+= "<input class='nameWidget' type='text' name='config_name' value='" + configName;
                testPlanHTML+= "' placeholder='name goes here'>";

                testPlanHTML+= "<div class='row appRow'>";
                testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Bandwidth:</p>"; 
                testPlanHTML+= "<input class='appInput' style='border-top-right-radius: 5px; border-top-left-radius: 5px;' type='text' name='analog_bandwidth' value='" + configBand;
                testPlanHTML+= "'></td></tr></div>";

                testPlanHTML+= "<div class='row appRow'>";
                testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Sample Rate:</p>"; 
                testPlanHTML+= "<input class='appInput' type='text' name='analog_sample_rate' value='" + configSampleRate;
                testPlanHTML+= "'></td></tr></div>";

                testPlanHTML+= "<div class='row appRow'>";
                testPlanHTML+= "<tr><td class='label'><p class='appLabel'> Buffer Size: </p>"; 
                testPlanHTML+= "<input class='appInput' type='text' name='capture_buffer_size' value='" + configSampleSize;
                testPlanHTML+= "'></td></tr></div>";

                testPlanHTML+= "<div class='row appRow'>";
                testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Resolution: </p>"; 
                testPlanHTML+= "<input class='appInput' type='text' name='resolution' value='" + configResolution;
                testPlanHTML+= "'></td></tr></div>";

                testPlanHTML+= "<div style='margin-bottom:10px;' class='row appRow'>";
                testPlanHTML+= "<tr><td class='label'><p class='appLabel'># of Channels: </p>"; 
                testPlanHTML+= "<input class='appInput' style='margin-bottom:0px; border-bottom-right-radius: 5px; border-bottom-left-radius: 5px;' type='text' name='capture_channels' value='" + configChNum;
                testPlanHTML+= "'></td></tr></div>";

                          
                testPlanHTML+= "</form>";
                testPlanHTML+= "</div>";

                testPlanHTML+= "<div id='configSearchResults' class='col-md-4'>";
                testPlanHTML+= "<form method='post'>";

                testPlanHTML+= "<div class='row appRow'>";
                testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Results:</p>"; 
                testPlanHTML+= "<p class='configResults'>{{ explanations }}</p></td></tr></div>";

                testPlanHTML+= "<div class='row appRow'>";
                testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Instrument Type:</p>"; 
                testPlanHTML+= "<p class='configResults' style='' type='text' name='selected_inst_type' value='{{selected_inst_type}}'></p></td></tr></div>";

                testPlanHTML+= "<div class='row appRow'>";
                testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Hardware:</p>"; 
                testPlanHTML+= "<p class='configResults' style='' type='text' name='selected_hardware' value='{{selected_hardware}}'></p></td></tr></div>";

                testPlanHTML+= "<div class='row appRow'>";
                testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Available Instruments:</p>"; 
                testPlanHTML+= "<p class='configResults'>{{avail_inst}}</p></td></tr></div>";

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
                testPlanHTML+= "<input class='appInput' style='border-top-right-radius: 5px; border-top-left-radius: 5px;' type='text' name='meas_type' placeholder='RMS' value='" + measType;
                testPlanHTML+= "'></td></div>";
                testPlanHTML+= "<div class='row appRow'>";
                testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Start Time:</p>";                   
                testPlanHTML+= "<input class='appInput' type='text' name='meas_start_time' placeholder='200 sec' value='" + measStart;
                testPlanHTML+= "'></td></div>";
                testPlanHTML+= "<div class='row appRow'>";
                testPlanHTML+= "<td class='label'><p class='appLabel'>Stop Time:</p>"
                testPlanHTML+= "<input class='appInput' style='border-bottom-right-radius: 5px; border-bottom-left-radius: 5px;' type='text' name='meas_stop_time' placeholder='400 sec' value='" + measStop;
                testPlanHTML+= "'></td></tr></div>";                                                       
                testPlanHTML+= "</form>";
                testPlanHTML+= "</div>";
            }else {
                console.log('no type match :(');
            }                          
        };
        if (type === 'dut') {              
            console.log('TYPE DUT')
            testPlanHTML+= "<div type='dut' class='appBox' id='" + String(index) + "'>";
            testPlanHTML+= "<h4 class='appTitle'>DUT - <span onclick='removeWidget(" + index + ")' class='appRemove glyphicon glyphicon-remove-circle' style='left:810px;'></span></h4>";
            testPlanHTML+= "<form method='post'>";

            testPlanHTML+= "<input class='nameWidget' type='text' name='dut_name' value='{{dut_name}}' placeholder='name goes here'>";

            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Device Under Test Type:</p>"; 
            testPlanHTML+= "<input class='appInput' style='border-top-right-radius: 5px; border-top-left-radius: 5px;' type='text' name='dut_type' value='{{dut_type}}'></td></tr></div>";

            testPlanHTML+= "<div style='position:relative; top:20px;' class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Settings:</p>"; 
            testPlanHTML+= "<input class='appInput' style='border-bottom-right-radius: 5px; border-bottom-left-radius: 5px;' type='text' name='settings' value='{{settings}}'></td></tr></div>";
                           
            testPlanHTML+= "</form>";
            testPlanHTML+= "</div>";

            document.getElementById("testPlan").innerHTML = testPlanHTML; 
            console.log('addDUT: testPlanHTML = ', testPlanHTML); 
        }else if(type === 'config') {
            console.log('TYPE Config')
            testPlanHTML+= "<div type='config' class='configBox' id='" + String(index) + "'>";
            testPlanHTML+= "<div id='configSearch' class='col-md-4'>";
            testPlanHTML+= "<h4 class='appTitle'>Instrument - <span onclick='removeWidget(" + index + ")' class='appRemove glyphicon glyphicon-remove-circle' style='left:740px;'></span></h4>";
            testPlanHTML+= "<form method='post'>";
            testPlanHTML+= "<input class='nameWidget' type='text' name='config_name' value='{{config_name}}' placeholder='name goes here'>";

            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Bandwidth:</p>"; 
            testPlanHTML+= "<input class='appInput' style='border-top-right-radius: 5px; border-top-left-radius: 5px;' type='text' name='analog_bandwidth' value='{{analog_bandwidth}}'></td></tr></div>";

            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Sample Rate:</p>"; 
            testPlanHTML+= "<input class='appInput' type='text' name='analog_sample_rate' value='{{analog_sample_rate}}'></td></tr></div>";

            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'> Buffer Size: </p>"; 
            testPlanHTML+= "<input class='appInput' type='text' name='capture_buffer_size' value='{{capture_buffer_size}}'></td></tr></div>";

            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Resolution: </p>"; 
            testPlanHTML+= "<input class='appInput' type='text' name='resolution' value='{{resolution}}'></td></tr></div>";

            testPlanHTML+= "<div style='margin-bottom:10px;' class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'># of Channels: </p>"; 
            testPlanHTML+= "<input class='appInput' style='margin-bottom:0px; border-bottom-right-radius: 5px; border-bottom-left-radius: 5px;' type='text' name='capture_channels' value='{{capture_channels}}'></td></tr></div>";
                            
            testPlanHTML+= "</form>";
            testPlanHTML+= "</div>";

            testPlanHTML+= "<div id='configSearchResults' class='col-md-4'>";
            testPlanHTML+= "<form method='post'>";

            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Results:</p>"; 
            testPlanHTML+= "<p class='configResults'>{{ explanations }}</p></td></tr></div>";

            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Instrument Type:</p>"; 
            testPlanHTML+= "<p class='configResults' style='' type='text' name='selected_inst_type' value='{{selected_inst_type}}'></p></td></tr></div>";

            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Hardware:</p>"; 
            testPlanHTML+= "<p class='configResults' style='' type='text' name='selected_hardware' value='{{selected_hardware}}'></p></td></tr></div>";

            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Available Instruments:</p>"; 
            testPlanHTML+= "<p class='configResults'>{{avail_inst}}</p></td></tr></div>";

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
            testPlanHTML+= "<input style='left:190px;' class='nameWidget' type='text' name='meas_name' value='{{meas_name}}' placeholder='name goes here'>";
            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Meas Type:</p>";                   
            testPlanHTML+= "<input class='appInput' type='text' style='border-top-right-radius: 5px; border-top-left-radius: 5px;' name='meas_type' placeholder='RMS' value='{{meas_type}}'></td></div>";
            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Start Time:</p>";                   
            testPlanHTML+= "<input class='appInput' type='text' name='meas_start_time' placeholder='200 sec' value='{{meas_start_time}}'></td></div>";
            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<td class='label'><p class='appLabel'>Stop Time:</p>";
            testPlanHTML+= "<input class='appInput' style='border-bottom-right-radius: 5px; border-bottom-left-radius: 5px;' type='text' name='meas_stop_time' placeholder='400 sec' value='{{meas_stop_time}}'></td></tr></div>";                                                         
            testPlanHTML+= "</form>";
            testPlanHTML+= "</div>";

            document.getElementById("testPlan").innerHTML = testPlanHTML; 
            console.log('addDUT: testPlanHTML = ', testPlanHTML);
        }else {
            console.log('NO TYPE MATCH')
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
        var configBand = children[i].children[0].children[1].children[1].children[1].value
        var configSampleRate = children[i].children[0].children[1].children[2].children[1].value
        var configSampleSize = children[i].children[0].children[1].children[3].children[1].value
        var configResolution = children[i].children[0].children[1].children[4].children[1].value
        var configChNum = children[i].children[0].children[1].children[5].children[1].value

        var config_search_url = '';
        var searchInput = JSON.stringify({});
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
        searchTimerID = setTimeout(getSearchResults, 1000);
        function getSearchResults() {
            console.log('getSearchResults called!!!');
            //widget_url = 'https://gradientone-dev1.appspot.com/testresults/widgets/Acme.json';
              widget_utl = window.location.origin ;
              widget_utl += "/testresults.widgets/Acme.json";
              $.ajax({
                  async: true,
                  url: widget_url,            
                  dataType: 'json',
               }).done(function (results) {
                  searchResults = results;
              });
               console.log('getSearchResults: results =', results);
            clearTimeout(searchTimerID);
        };
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

        //var initInfo_url = 'https://gradientone-dev1.appspot.com/testconfiginput';
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
        testPlanName = testSetUpInfo[3].children[0].children[1].children[0].value;
        companyName = 'Acme';
        testPlanAuthor = 'nedwards';
        startTime = testSetUpInfo[3].children[1].children[1].children[0].value;
        var startNowLogic = new Boolean(
  testSetUpInfo[3].children[1].children[1].children[3].children[1].checked);
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

                var configJsonObj = {"config_name":configName,"analog_bandwidth":configBand,"analog_sample_rate":configSampleRate,"capture_buffer_size":configSampleSize,"resolution":configResolution,"capture_channels":configChNum,};
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
        

        //var commit_url = 'https://gradientone-dev1.appspot.com/testconfiginput';
        var commit_url = window.location.origin + "/testconfiginput";
        console.log('commitBtn: indexArray = ', indexArray);
        var commitData = JSON.stringify({"testplan_name":testPlanName,"author":testPlanAuthor,"company_nickname":companyName,"start_time":startTime,"start_now":startNowLogic,"configs":configArray,"meas":measArray,"duts":dutArray,"order":indexArray});
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
