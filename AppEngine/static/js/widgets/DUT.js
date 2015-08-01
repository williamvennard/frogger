
// DUT WIDGETS //
    function addWidget(type) {
        console.log('addWidget: Type = ', type);
        console.log('addDUT!');
        var testPlanHTML = "";
        var index;
        var d = document.getElementById('testPlan');
        var children = d.childNodes;
        console.log('addDUT: children.length =',children.length);
        console.log('addDUT: children =',children);
        
        for (index = 0; index < children.length; index++) {
            console.log('removeDUT: index =',index);
            var planItemType = children[index].getAttribute('type');
            console.log('addDUT: type DUI? ',planItemType === 'DUT')
            console.log('addDUT: planItemType =',planItemType);
            if (planItemType === 'DUT') {
                console.log('TYPE DUT');
                console.log('addDUT: planItemType =',planItemType);
                var theName = children[index].children[1].children[0].value;
                var typeDUT = children[index].children[1].children[1].children[1].value;

                testPlanHTML+= "<div type='DUT' class='appBox' id='" + String(index) + "'>";
                testPlanHTML+= "<h4 class='appTitle'>DUT - <span onclick='removeDUT(" + index + ")' class='appRemove glyphicon glyphicon-remove-circle'></span></h4>";
                testPlanHTML+= "<form method='post'>";
                testPlanHTML+= "<input id='name" + index;
                testPlanHTML+= "' class='nameWidget' type='text' name='dut_name' value='" + theName;
                testPlanHTML+= "' placeholder='name goes here'>";
                testPlanHTML+= "<div class='row appRow'><tr><td class='label'>";
                testPlanHTML+= "<p class='appLabel'>Device Under Test Type:</p>"; 
                testPlanHTML+= "<input class='appInput' id='type" + index;
                testPlanHTML+= "' style='border-top-right-radius: 5px; border-top-left-radius: 5px;' type='text' name='dut_type' value='" + typeDUT;
                testPlanHTML+= "'></td></tr></div>";
                testPlanHTML+= "<input id='appSubmitBtn' type='submit' value='SUBMIT'>";                              
                testPlanHTML+= "</form>";
                testPlanHTML+= "<p id=order" + index + "></p>"; //HERE FOR TESTING
                testPlanHTML+= "</div>";
            }else if(planItemType === 'config') {
                console.log('TYPE config');
            }else if(planItemType === 'measurement') {
                console.log('TYPE meas');
            }else {
                console.log('no type match :(')
            }                          
        };
        if (type === 'DUT') {              
            console.log('TYPE DUT')
            testPlanHTML+= "<div type='DUT' class='appBox' id='" + String(index) + "'>";
            testPlanHTML+= "<h4 class='appTitle'>DUT - <span onclick='removeDUT(" + index + ")' class='appRemove glyphicon glyphicon-remove-circle'></span></h4>";
            testPlanHTML+= "<form method='post'>";
            testPlanHTML+= "<input id='name" + index;
            testPlanHTML+= "' class='nameWidget' type='text' name='dut_name' value='{{dut_name}}' placeholder='name goes here'>";
            testPlanHTML+= "<div class='row appRow'><tr><td class='label'>";
            testPlanHTML+= "<p class='appLabel'>Device Under Test Type:</p>"; 
            testPlanHTML+= "<input class='appInput' id='type" + index;
            testPlanHTML+= "' style='border-top-right-radius: 5px; border-top-left-radius: 5px;' type='text' name='dut_type' value='{{dut_type}}'></td></tr></div>";
            testPlanHTML+= "<input id='appSubmitBtn' type='submit' value='SUBMIT'>"                              
            testPlanHTML+= "</form>"
            testPlanHTML+= "<p id=order" + index + "></p>"; //HERE FOR TESTING
            testPlanHTML+= "</div>";

            document.getElementById("testPlan").innerHTML = testPlanHTML; 
            console.log('addDUT: testPlanHTML = ', testPlanHTML); 
        }else if(type === 'Config') {
            console.log('TYPE Config')
            testPlanHTML+= "<div class='appBox' id='" + index + "'>";
            testPlanHTML+= "<h4 class='appTitle'>Instrument - <span onclick='removeOscope(" + index + ")' class='appRemove glyphicon glyphicon-remove-circle'></span></h4>";
            testPlanHTML+= "<form method='post'>";
            testPlanHTML+= "<input class='nameWidget' type='text' name='config_name' value='{{config_name}}' placeholder='name goes here'>";
            testPlanHTML+= "<div class='row appOrder'><tr><td class='label'>";
            testPlanHTML+= "<select id='orderSelect' class='form-control' style='position:relative; bottom:10px;'>";
            testPlanHTML+= "<option value='1'>1</option>";
            testPlanHTML+= "<option value='2'>2</option>";
            testPlanHTML+= "<option value='3'>3</option>";
            testPlanHTML+= "<option value='4'>4</option>";
            testPlanHTML+= "</select></td></tr></div>";
            testPlanHTML+= "<div class='row appRow'><tr><td class='label'>";
            testPlanHTML+= "<p class='appLabel'>Instrument:</p>"; 
            testPlanHTML+= "<input class='appInput' style='border-top-right-radius: 5px; border-top-left-radius: 5px;' type='text' name='instrument_name' value='{{instrument_name}}'></td></tr></div>";                           
            testPlanHTML+= "<input id='appSubmitBtn' type='submit' value='SUBMIT'>"                              
            testPlanHTML+= "</form>"
            testPlanHTML+= "</div>";

            document.getElementById("testPlan").innerHTML = testPlanHTML; 
            console.log('addDUT: testPlanHTML = ', testPlanHTML); 
        }else if(type === 'measurement') {

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
    function removeDUT(index) {
      d = document.getElementById('testPlan');
      
      console.log('removeDUT: d.haschildnodes =',d.hasChildNodes());
      console.log('removeDUT: d.firstchild =',d.firstChild);
      var olddiv = document.getElementById(index);
      d.removeChild(olddiv);
      //d.removeChild(d.firstChild);
      var children = d.childNodes;
      for (var i = 0; i < children.length; i++) {
        console.log('removeDUT: i =',i);
      }
    };
    //ADD WIDGET BUTTON CONTROL
    $("#newDUT").click(function () {
      addWidget('DUT');
    });
    $("#newConfig").click(function () {
      addWidget('Config');
    });
//CANVAS ORDER
    $(document).ready(function() {
    $(".droppable").sortable({
      update: function( event, ui ) {
        Dropped();
        console.log('indexArray = ', indexArray);
        indexArray=[];
        console.log("New position: ", ui.item.index());
        index ='dev 1  Position:' + ui.item.index();
        
      }
    });    
  });
    var indexArray = [];
  function Dropped(event, ui){
    var apps = document.getElementsByClassName("appBox");
    console.log('Dropped: apps.length =',apps.length);
        for(var i = 0;i<apps.length;i++) {
            var d = document.getElementById('testPlan');
            var children = d.childNodes;
            var planItemType = children[i].getAttribute('type');
            var planItemName = children[i].children[1].children[0].value;
            
            var orderInfo = planItemType + ':' + planItemName + ':' + i;
            indexArray.push(orderInfo); 

        }
    $(".draggable").each(function(){        
    });
  }  