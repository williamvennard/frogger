
function OPConfig(instrument_config) {

      configName = instrument_config.configName;
      traceName = instrument_config.traceName;
      frequencyCorrection = instrument_config.frequencyCorrection;
      offset = instrument_config.offset;
      units = instrument_config.units;
      avgCountAuto = instrument_config.avgCountAuto;
      rangeAuto = instrument_config.rangeAuto;

      var configSettings = document.getElementById('PMSettingsDisplay');
      var setChildren = configSettings.childNodes;

      setChildren[1].children[1].innerHTML = configName;
      setChildren[3].children[1].innerHTML = frequencyCorrection;
      setChildren[1].children[3].innerHTML = traceName;
      setChildren[3].children[3].innerHTML = offset;

      document.getElementById("PMUnits").innerHTML = units;
    

      var config_url = window.location.origin + '/u2000_configinput';
      console.log('saveStatus: config_url = ',config_url);

      var configSettings = JSON.stringify({"config_name":configName,"trace_name":traceName, "correction_frequency":frequencyCorrection,
       "offset":offset, "units":units, "avg_count_auto":avgCountAuto, "range_auto":rangeAuto, "hardware_name":"Tahoe",
       "inst_name":"U2001A","company_nickname":"Acme"});

      console.log('instConfig: configSettings = ',configSettings);

     $.ajax({
        type: "POST",
        url: config_url,
        data: configSettings,
        dataType: 'json',
        success: function(data, textStatus, jqXHR)
        {
            console.log('saveStatus: Ajax post was a success!');
        },
      }); 
    };  
