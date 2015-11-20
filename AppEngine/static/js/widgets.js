
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
                testPlanHTML+= "<h4 class='appTitle'>BitScope - <span onclick='removeWidget(" + index + ")' class='appRemove glyphicon glyphicon-remove-circle' style='left:777px;'></span></h4>";
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
                testPlanHTML+= "'>" + configAvail;
                testPlanHTML+= "</p></td></tr></div>";

                testPlanHTML+= "</form>";
                testPlanHTML+= "</div>";
                testPlanHTML+= "<button id='configSearchBtn' onclick='configSearch(" + index + ")'>SEARCH</button>";   
                testPlanHTML+= "</div>";

            }else if(planItemType === 'U2001A') {
                console.log('U2001A!!')

                var U2001AName = children[index].children[0].children[1].children[0].value
                var freqCorrection = children[index].children[0].children[1].children[1].children[1].value
                var offset = children[index].children[0].children[1].children[2].children[1].value
                var units = children[index].children[0].children[1].children[3].children[1].value

                if (children[index].children[0].children[1].children[4].children[1].checked==true) {
                    var avgCountAuto = 'checked'
                }else{
                    var avgCountAuto = ''
                };

                if (children[index].children[0].children[1].children[5].children[1].checked==true) {
                    var rangeAuto = 'checked'
                }else{
                    var rangeAuto = ''
                };

                if (children[index].children[0].children[1].children[6].children[1].checked==true) {
                    var passFail = 'checked'
                }else{
                    var passFail = ''
                }; 

                var passFailMax = children[index].children[0].children[1].children[7].children[1].value
                var passFailMin = children[index].children[0].children[1].children[8].children[1].value

                //Search results
                var configResults = children[index].children[1].children[0].children[0].children[1].innerHTML;
                var configInstType = children[index].children[1].children[0].children[1].children[1].innerHTML;
                var configHardware = children[index].children[1].children[0].children[2].children[1].innerHTML;
                var configAvail = children[index].children[1].children[0].children[3].children[1].innerHTML;


                testPlanHTML+= "<div type='U2001A' class='U2001ABox' id='" + String(index) + "'>";
                testPlanHTML+= "<div id='configSearch' class='col-md-4'>";
                testPlanHTML+= "<h4 class='appTitle'>U2001A - <span onclick='removeWidget(" + index + ")' class='appRemove glyphicon glyphicon-remove-circle' style='left:777px;'></span></h4>";
                testPlanHTML+= "<form method='post'>";
                testPlanHTML+= "<input class='nameWidget' type='text' name='config_name' value='" + U2001AName;
                testPlanHTML+= "' placeholder='name goes here'>";

                testPlanHTML+= "<div class='row appRow'>";
                testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Freq Correction:</p>"; 
                testPlanHTML+= "<input autocomplete='off' class='appInput' style='border-top-right-radius: 5px; border-top-left-radius: 5px;' type='text' placeholder='' name='analog_bandwidth' value='" + freqCorrection;
                testPlanHTML+= "'></td></tr></div>";

                testPlanHTML+= "<div class='row appRow'>";
                testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Offset:</p>"; 
                testPlanHTML+= "<input autocomplete='off' class='appInput' type='text' placeholder='' name='analog_sample_rate' value='" + offset;
                testPlanHTML+= "'></td></tr></div>";

                testPlanHTML+= "<div class='row appRow'>";
                testPlanHTML+= "<tr><td class='label'><p class='appLabel'> Units: </p>"; 
                testPlanHTML+= "<input autocomplete='off' class='appInput' style='margin-bottom:0px; border-bottom-right-radius: 5px; border-bottom-left-radius: 5px;' type='text' placeholder='' name='capture_buffer_size' value='" + units;
                testPlanHTML+= "'></td></tr></div>";

                testPlanHTML+= "<div class='row appRow'>";
                testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Avg Count Auto: </p>"; 
                testPlanHTML+= "<input autocomplete='off' class='appInput' type='checkbox'  name='resolution' value=''" + avgCountAuto + "></td></tr></div>";

                testPlanHTML+= "<div style='' class='row appRow'>";
                testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Range Auto: </p>"; 
                testPlanHTML+= "<input class='appInput' type='checkbox' name='' autocomplete='off' value=''" + rangeAuto + "></td></tr></div>";
                                
                testPlanHTML+= "<div class='row appRow'>";
                testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Pass/Fail: </p>";
                testPlanHTML+= "<input class='appInput' type='checkbox' name='' autocomplete='off' value=''" + passFail + "></td></tr></div>"; 

                testPlanHTML+= "<div class='row appRow'>";
                testPlanHTML+= "<tr><td class='label'><p class='appLabel'> Max: </p>"; 
                testPlanHTML+= "<input autocomplete='off' class='appInput' type='text' placeholder='12,000' name='capture_buffer_size' value='" + passFailMax;
                testPlanHTML+= "'></td></tr></div>";

                testPlanHTML+= "<div class='row appRow'>";
                testPlanHTML+= "<tr><td class='label'><p class='appLabel'> Min: </p>"; 
                testPlanHTML+= "<input autocomplete='off' class='appInput' type='text' placeholder='12,000' name='capture_buffer_size' value='" + passFailMin;
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
                testPlanHTML+= "'>" + configAvail;
                testPlanHTML+= "</p></td></tr></div>";

                testPlanHTML+= "</form>";
                testPlanHTML+= "</div>";
                testPlanHTML+= "<button id='configSearchBtn' onclick='configSearch(" + index + ")'>SEARCH</button>";   
                testPlanHTML+= "</div>";



                //$('#configSearchBtn').trigger('click');
            }else if(planItemType === 'measure') {
                console.log('TYPE meas');
                var measName = children[index].children[1].children[0].value;
  
                if (children[index].children[1].children[1].children[1].checked==true) {
                    var passFail = 'checked'
                }else{
                    var passFail = ''
                }; 

                var passFailMax = children[index].children[1].children[2].children[1].value;
                var passFailMin = children[index].children[1].children[3].children[1].value
                

                testPlanHTML+= "<div type='measure' class='appBox' id='" + String(index) + "'>";
                testPlanHTML+= "<h4 class='appTitle'>Measure - <span onclick='removeWidget(" + index + ")' class='appRemove glyphicon glyphicon-remove-circle' style='left:685px;'></span></h4>";
                testPlanHTML+= "<form method='post'>";
                testPlanHTML+= "<input style='left:190px;' class='nameWidget' type='text' name='meas_name' value='" + measName;
                testPlanHTML+= "' placeholder='name goes here'>";
                testPlanHTML+= "<div class='row appRow'>";
                testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Pass/Fail:</p>";                   
                testPlanHTML+= "<input class='appInput' type='checkbox' name='' autocomplete='off' value=''" + passFail + "></td></div>";
                testPlanHTML+= "<div class='row appRow'>";
                testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Max:</p>";                   
                testPlanHTML+= "<input autocomplete='off' class='appInput' style='border-top-right-radius: 5px; border-top-left-radius: 5px;' type='text' name='' placeholder='200' value='" + passFailMax;
                testPlanHTML+= "'></td></div>";
                testPlanHTML+= "<div class='row appRow'>";
                testPlanHTML+= "<td class='label'><p class='appLabel'>Min:</p>";
                testPlanHTML+= "<input autocomplete='off' class='appInput' style='border-bottom-right-radius: 5px; border-bottom-left-radius: 5px;' type='text' name='' placeholder='100' value='" + passFailMin;
                testPlanHTML+= "'></td></tr></div>";                                                         
                testPlanHTML+= "</form>";
                testPlanHTML+= "</div>";

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
        }else if(type === 'config') {       //BitScope
            console.log('TYPE Config')
            testPlanHTML+= "<div type='config' class='configBox' id='" + String(index) + "'>";
            testPlanHTML+= "<div id='configSearch' class='col-md-4'>";
            testPlanHTML+= "<h4 class='appTitle'>BitScope - <span onclick='removeWidget(" + index + ")' class='appRemove glyphicon glyphicon-remove-circle' style='left:777px;'></span></h4>";
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
        }else if(type === 'U2001A') {           //Power Meter
            console.log('TYPE U2001A')
            testPlanHTML+= "<div type='U2001A' class='U2001ABox' id='" + String(index) + "'>";
            testPlanHTML+= "<div id='configSearch' class='col-md-4'>";
            testPlanHTML+= "<h4 class='appTitle'>U2001A - <span onclick='removeWidget(" + index + ")' class='appRemove glyphicon glyphicon-remove-circle' style='left:777px;'></span></h4>";
            testPlanHTML+= "<form method='post'>";
            testPlanHTML+= "<input class='nameWidget' type='text' name='config_name' value='' placeholder='name goes here'>";

            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Freq Correction:</p>"; 
            testPlanHTML+= "<input autocomplete='off' class='appInput' style='border-top-right-radius: 5px; border-top-left-radius: 5px;' type='text' placeholder='' name='analog_bandwidth' value=''></td></tr></div>";

            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Offset:</p>"; 
            testPlanHTML+= "<input autocomplete='off' class='appInput' type='text' placeholder='' name='analog_sample_rate' value=''></td></tr></div>";

            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'> Units: </p>"; 
            testPlanHTML+= "<input autocomplete='off' class='appInput' type='text' placeholder='' name='capture_buffer_size' value=''></td></tr></div>";

            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Avg Count Auto: </p>"; 
            testPlanHTML+= "<input autocomplete='off' class='appInput' type='checkbox'  name='resolution' value=''></td></tr></div>";

            testPlanHTML+= "<div style='' class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Range Auto: </p>"; 
            testPlanHTML+= "<input class='appInput' style='margin-bottom:0px; border-bottom-right-radius: 5px; border-bottom-left-radius: 5px;' type='checkbox' name='' autocomplete='off' value=''></td></tr></div>";
                            
            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Pass/Fail: </p>";
            testPlanHTML+= "<input class='appInput' type='checkbox' name='' autocomplete='off' value=''></td></tr></div>"; 

            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'> Max: </p>"; 
            testPlanHTML+= "<input autocomplete='off' class='appInput' type='text' placeholder='12,000' name='capture_buffer_size' value=''></td></tr></div>";

            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'> Min: </p>"; 
            testPlanHTML+= "<input autocomplete='off' class='appInput' type='text' placeholder='12,000' name='capture_buffer_size' value=''></td></tr></div>";

            testPlanHTML+= "</form>";
            testPlanHTML+= "</div>";

            testPlanHTML+= "<div id='configSearchResults' class='col-md-4' style='left:100px;'>";
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

        }else if(type === 'measure') {
            testPlanHTML+= "<div type='measure' class='appBox' id='" + String(index) + "'>";
            testPlanHTML+= "<h4 class='appTitle'>Measure - <span onclick='removeWidget(" + index + ")' class='appRemove glyphicon glyphicon-remove-circle' style='left:685px;'></span></h4>";
            testPlanHTML+= "<form method='post'>";
            testPlanHTML+= "<input style='left:190px;' class='nameWidget' type='text' name='meas_name' value='' placeholder='name goes here'>";
            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Pass/Fail:</p>";                   
            testPlanHTML+= "<input class='appInput' type='checkbox' name='' autocomplete='off' value=''></td></div>";
            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Max:</p>";                   
            testPlanHTML+= "<input autocomplete='off' class='appInput' style='border-top-right-radius: 5px; border-top-left-radius: 5px;' type='text' name='' placeholder='200' value=''></td></div>";
            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<td class='label'><p class='appLabel'>Min:</p>";
            testPlanHTML+= "<input autocomplete='off' class='appInput' style='border-bottom-right-radius: 5px; border-bottom-left-radius: 5px;' type='text' name='' placeholder='100' value=''></td></tr></div>";                                                         
            testPlanHTML+= "</form>";
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

            var sconfigName = savedSettings.config_name;
            var sconfigBand = savedSettings.analog_bandwidth;
            var sconfigSampleRate = savedSettings.analog_sample_rate;
            var sconfigSampleSize = savedSettings.capture_buffer_size;
            var sconfigResolution = savedSettings.resolution;
            var sconfigNumChannels = savedSettings.capture_channels;

            testPlanHTML+= "<div type='config' class='configBox' id='" + String(index) + "'>";
            testPlanHTML+= "<div id='configSearch' class='col-md-4'>";
            testPlanHTML+= "<h4 class='appTitle'>Config - <span onclick='removeWidget(" + index + ")' class='appRemove glyphicon glyphicon-remove-circle' style='left:777px;'></span></h4>";
            testPlanHTML+= "<form method='post'>";
            testPlanHTML+= "<input class='nameWidget' type='text' name='config_name' value='" + sconfigName;
            testPlanHTML+= "' placeholder='name goes here'>";

            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Bandwidth(Hz):</p>"; 
            testPlanHTML+= "<input autocomplete='off' class='appInput' style='border-top-right-radius: 5px; border-top-left-radius: 5px;' type='text' placeholder='20,000,000' name='analog_bandwidth' value='" + sconfigBand;
            testPlanHTML+= "'></td></tr></div>";

            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Sample Rate(sps):</p>"; 
            testPlanHTML+= "<input autocomplete='off' class='appInput' type='text' placeholder='20,000,000' name='analog_sample_rate' value='" + sconfigSampleRate;
            testPlanHTML+= "'></td></tr></div>";

            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'> Buffer Size: </p>"; 
            testPlanHTML+= "<input autocomplete='off' class='appInput' type='text' placeholder='12,000' name='capture_buffer_size' value='" + sconfigSampleSize;
            testPlanHTML+= "'></td></tr></div>";

            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Resolution: </p>"; 
            testPlanHTML+= "<input autocomplete='off' class='appInput' type='text' placeholder='12' name='resolution' value='" + sconfigResolution;
            testPlanHTML+= "'></td></tr></div>";

            testPlanHTML+= "<div style='margin-bottom:10px;' class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'># of Channels: </p>"; 
            testPlanHTML+= "<input class='appInput' style='margin-bottom:0px; border-bottom-right-radius: 5px; border-bottom-left-radius: 5px;' type='text' placeholder='2' name='capture_channels' autocomplete='off' value='" + sconfigNumChannels;
            testPlanHTML+= "'></td></tr></div>";
                            
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
       }else if(type === 'sU2001A') {           //Saved Power Meter

            console.log('addWidget: savedSettings sU2001A= ',savedSettings);

            var sconfigName = savedSettings.config_name;
            var scorrectionFreq = savedSettings.correction_frequency;
            var soffset = savedSettings.offset;
            var sunits = savedSettings.units;
            var savgCountAuto = savedSettings.averaging_count_auto;
            var srangeAuto = savedSettings.range_auto;
            var spassFail = savedSettings.pass_fail;
            var sminPass = savedSettings.min_value;
            var smaxPass = savedSettings.max_value;

            testPlanHTML+= "<div type='U2001A' class='U2001ABox' id='" + String(index) + "'>";
            testPlanHTML+= "<div id='configSearch' class='col-md-4'>";
            testPlanHTML+= "<h4 class='appTitle'>U2001A - <span onclick='removeWidget(" + index + ")' class='appRemove glyphicon glyphicon-remove-circle' style='left:777px;'></span></h4>";
            testPlanHTML+= "<form method='post'>";
            testPlanHTML+= "<input class='nameWidget' type='text' name='config_name' placeholder='name goes here' value='" + sconfigName + "'>";

            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Freq Correction:</p>"; 
            testPlanHTML+= "<input autocomplete='off' class='appInput' style='border-top-right-radius: 5px; border-top-left-radius: 5px;' type='text' placeholder='' name='analog_bandwidth' value='" + scorrectionFreq;
            testPlanHTML+= "'></td></tr></div>";

            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Offset:</p>";
            testPlanHTML+= "<input autocomplete='off' class='appInput' type='text' placeholder='' name='analog_sample_rate' value='" + soffset + "'></td></tr></div>";

            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'> Units: </p>"; 
            testPlanHTML+= "<input autocomplete='off' class='appInput' type='text' placeholder='' name='capture_buffer_size' value='" + sunits + "'></td></tr></div>";

            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Avg Count Auto: </p>"; 
            testPlanHTML+= "<input autocomplete='off' class='appInput' type='checkbox'  name='resolution' value='" + savgCountAuto + "'></td></tr></div>";

            testPlanHTML+= "<div style='' class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Range Auto: </p>"; 
            testPlanHTML+= "<input class='appInput' style='margin-bottom:0px; border-bottom-right-radius: 5px; border-bottom-left-radius: 5px;' type='checkbox' name='' autocomplete='off' value='" + srangeAuto;
            testPlanHTML+= "'></td></tr></div>";
                            
            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'>Pass/Fail: </p>";
            testPlanHTML+= "<input class='appInput' type='checkbox' name='' autocomplete='off' value='" + spassFail + "'></td></tr></div>"; 

            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'> Max: </p>"; 
            testPlanHTML+= "<input autocomplete='off' class='appInput' type='text' placeholder='12,000' name='capture_buffer_size' value='" + smaxPass + "'></td></tr></div>";

            testPlanHTML+= "<div class='row appRow'>";
            testPlanHTML+= "<tr><td class='label'><p class='appLabel'> Min: </p>"; 
            testPlanHTML+= "<input autocomplete='off' class='appInput' type='text' placeholder='12,000' name='capture_buffer_size' value='" + sminPass + "'></td></tr></div>";

            testPlanHTML+= "</form>";
            testPlanHTML+= "</div>";

            testPlanHTML+= "<div id='configSearchResults' class='col-md-4' style='left:100px;'>";
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
            console.log('addU2001A: testPlanHTML = ', testPlanHTML); 
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
    $("#newU2001A").click(function () {
      addWidget('U2001A');
    });
    $("#measure").click(function () {
      addWidget('measure');
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
        
        //var config_search_url = 'https://gradientone-test.appspot.com';
        var config_search_url = window.location.origin;
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
              var search_results_url = window.location.origin;
              //var search_results_url = 'https://gradientone-test.appspot.com';
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
            console.log(' = ', indexArray);
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
    var indexArray = []; 

    function postInitInfo() {
        console.log('postInitInfo called!!!!');
        var testSetUp = document.getElementById('testSetup');
        var testSetUpInfo = testSetUp.childNodes;
        testPlanName = testSetUpInfo[3].children[0].children[1].children[0].value;
        companyName = 'Acme';
        hardwareName = 'Tahoe';
        testPlanAuthor = 'nedwards';
        startTime = testSetUpInfo[3].children[1].children[1].children[0].value;
        d = new Date(startTime);
        var startMS = d.getTime();
        startNowLogic = new Boolean(
       testSetUpInfo[3].children[1].children[1].children[3].children[1].checked);

        //var initInfo_url = 'https://gradientone-test.appspot.com/testconfiginput';
        var initInfo_url = window.location.origin;
        initInfo_url += "/testconfiginput";
        var initData = JSON.stringify({"testplan_name":testPlanName,"author":testPlanAuthor,"company_nickname":companyName,"hardware_name":hardwareName,"start_time":startMS,"start_now":startNowLogic});
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
        var configArray = [];
        var U2001Array = [];
        var measArray = [];
        var dutArray = [];
        var testSetUp = document.getElementById('testSetup');
        var testSetUpInfo = testSetUp.childNodes;
        testPlanName = testSetUpInfo[1].children[0].children[1].children[0].value;
        var opsStart = new Boolean(document.getElementById('opsStartCheck').checked);
        companyName = 'Acme';
        testPlanAuthor = 'nedwards';
        hardwareName = 'Tahoe';
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
            }else if(planItemType === 'U2001A') {
                var U2001AName = children[index].children[0].children[1].children[0].value
                var freqCorrection = children[index].children[0].children[1].children[1].children[1].value
                var offset = children[index].children[0].children[1].children[2].children[1].value
                var units = children[index].children[0].children[1].children[3].children[1].value
                var avgCountAuto = new Boolean(children[index].children[0].children[1].children[4].children[1].checked)
                var rangeAuto = new Boolean(children[index].children[0].children[1].children[5].children[1].checked)
                var passFail = new Boolean(children[index].children[0].children[1].children[6].children[1].checked)
                var passFailMin = 0.0
                var passFailMax = 0.0
                if (passFail){
                    passFailMin = children[index].children[0].children[1].children[7].children[1].value
                    passFailMax = children[index].children[0].children[1].children[8].children[1].value
                }

                var U2001AJsonObj = {"config_name":U2001AName, "correction_frequency": freqCorrection, "offset":offset, "units":units, 
                "instrument_type": "U2001A", "hardware": "Tahoe", "averaging_count_auto": avgCountAuto, "range_auto": rangeAuto, 
                "pass_fail":passFail, "min_value": passFailMin, "max_value": passFailMax}
                configArray.push(U2001AJsonObj);

            }else if(planItemType === 'measure') {
                var measName = children[index].children[1].children[0].value;
                var passFail = new Boolean(children[index].children[1].children[1].children[1].checked)    
                var passFailMax = children[index].children[1].children[2].children[1].value
                var passFailMin = children[index].children[1].children[3].children[1].value  

                var measureJsonObj = {"meas_name":measName,"pass_fail":passFail,"max_value": passFailMax,"min_value": passFailMin};

                measArray.push(measureJsonObj);
            }else if(planItemType === 'measurement') {
                var measName = children[index].children[1].children[0].value;
                var measType = children[index].children[1].children[1].children[1].value     
                var measStart = children[index].children[1].children[2].children[1].value
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
        var commitData = JSON.stringify({"testplan_name":testPlanName,"author":testPlanAuthor,"company_nickname":companyName,"hardware_name":hardwareName,"start_time":startMS,"start_now":startNowLogic,"configs":configArray,"meas":measArray,"duts":dutArray,"order":indexArray,"ops_start": opsStart});
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
        //clear old test plan
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
                if (planItemType == 'config' ||  'U2001A') {
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
