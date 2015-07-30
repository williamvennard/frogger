// INSTRUMENT(config) WIDGETS //    
    var testPlan = "";
    var index;
    function addOscope() {
        console.log('addOscope!');
        var numi = document.getElementById('theValue');
        //index + 1 when widget is added
        index = (document.getElementById('theValue').value -1) +2;
        numi.value = index;
        console.log('addOscope: index =', index);

        testPlan+= "<div class='appBox' id='" + index + "'>";
        testPlan+= "<h4 class='appTitle'>Instrument - Oscilloscope <span onclick='removeOscope(" + index + ")' class='appRemove glyphicon glyphicon-remove-circle'></span></h4>";
        testPlan+= "<form method='post'>";
        testPlan+= "<div class='row appOrder'><tr><td class='label'>";
        testPlan+= "<select id='orderSelect' class='form-control' style='position:relative; bottom:10px;'>";
        testPlan+= "<option value='1'>1</option>";
        testPlan+= "<option value='2'>2</option>";
        testPlan+= "<option value='3'>3</option>";
        testPlan+= "<option value='4'>4</option>";
        testPlan+= "</select></td></tr></div>";
        testPlan+= "<div class='row appRow'><tr><td class='label'>";
        testPlan+= "<p class='appLabel'>Instrument:</p>"; 
        testPlan+= "<input class='appInput' style='border-top-right-radius: 5px; border-top-left-radius: 5px;' type='text' name='instrument_name' value='{{instrument_name}}'></td></tr></div>";                           
    /*
                            <div class="row appRow">
                                <tr>
                                    <td class="label">
                                        <p class="appLabel">Sample Rate (Hz):</p>  
                                        <input class="appInput" type="text" name="sample_rate" value="{{sample_rate}}">
                                    </td>
                                </tr>
                            </div>
                            <div class="row appRow">
                                <tr>
                                    <td class="label">
                                        <p class="appLabel">Num. of Samples:</p>  
                                        <input class="appInput" style="border-bottom-right-radius: 5px; border-bottom-left-radius: 5px;" type="text" name="number_of_samples" value="{{number_of_samples}}">
                                    </td>
                                </tr>
                            </div>
    */
        testPlan+= "<input id='appSubmitBtn' type='submit' value='SUBMIT'>"                              
        testPlan+= "</form>"
        testPlan+= "</div>";

        document.getElementById("testPlan").innerHTML = testPlan; 
        console.log('addOscope: testPlan = ', testPlan);

        $(document).ready(function () { 
              $(".collapseStartTest").fadeIn("fast");           
        });         
    };

var d;
    function removeOscope(index) { 

        d = document.getElementById('testPlan');
        var olddiv = document.getElementById(index);
        d.removeChild(olddiv);
        //d = null;
        console.log('removeOscope: testPlan = ', testPlan);

        // index - 1 when widget is removed
        var sub = document.getElementById('theValue');
        index = (document.getElementById('theValue').value -1);
        sub.value = index;
        console.log('index=', index);

    };
    $("#OScope").click(function () {
      addOscope();
    });