// DUT WIDGETS //
    var testPlan = "";
    var index;
    function addDUT() {
        console.log('addDUT!');
        var numi = document.getElementById('theValue');
        //index + 1 when widget is added
        index = (document.getElementById('theValue').value -1) +2;
        numi.value = index;
        console.log('addDUT: index =', index);

        testPlan+= "<div class='appBox' id='" + index + "'>";
        testPlan+= "<h4 class='appTitle'>DUT <span onclick='removeDUT(" + index + ")' class='appRemove glyphicon glyphicon-remove-circle'></span></h4>";
        testPlan+= "<form method='post'>";
        testPlan+= "<div class='row appOrder'><tr><td class='label'>";
        testPlan+= "<select id='orderSelect' class='form-control' style='position:relative; bottom:10px;'>";
        testPlan+= "<option value='1'>1</option>";
        testPlan+= "<option value='2'>2</option>";
        testPlan+= "<option value='3'>3</option>";
        testPlan+= "<option value='4'>4</option>";
        testPlan+= "</select></td></tr></div>";
        testPlan+= "<div class='row appRow'><tr><td class='label'>";
        testPlan+= "<p class='appLabel'>Device Under Test Type:</p>"; 
        testPlan+= "<input class='appInput' style='border-top-right-radius: 5px; border-top-left-radius: 5px;' type='text' name='dut_type' value='{{dut_type}}'></td></tr></div>";                           
    /*
                            <form method="post">
      <table>
          <tr>
          <td class="label">
            Test Plan Name:  
          </td>
          <td>
            <input type="text" name="testplan_name" value="{{testplan_name}}">
          </td>
        </tr>
        <tr>
          <td class="label">
            Device Under Test Type:  
          </td>
          <td>
            <input type="text" name="dut_type" value="{{dut_type}}">
          </td>
        </tr>
        <tr>
        <td class="label">
            Device Under Test Name:
        </td>

          <td>
            <input type="text" name="dut_name" value="{{dut_name}}">
            <input type="hidden" name="company_nickname" value="Acme">
            <input type="hidden" name="testplan_name" value="Smiley">
            <input type="hidden" name="author" value="nedwards">
            <input type="hidden" name="dutpost" value=True>
          </td>
          <tr>
          <td class="label">
            Settings:  
          </td>
          <td>
            <input type="text" name="settings" value="{{settings}}">
          </td>
        </tr>

      <tr>
          <td class="label">
          DUT  Test Order:  
          </td>
          <td>
            <input type="text" name="dut_test_order" value="{{dut_test_order}}">
          </td>
        </tr>
      <input type="submit">
    </form>
    */
        testPlan+= "<input id='appSubmitBtn' type='submit' value='SUBMIT'>"                              
        testPlan+= "</form>"
        testPlan+= "</div>";

        document.getElementById("testPlan").innerHTML = testPlan; 
        console.log('addDUT: testPlan = ', testPlan);  

        $(document).ready(function () { 
              $(".collapseStartTest").fadeIn("fast");           
        });         
    };

var d;
    function removeDUT(index) { 

        d = document.getElementById('testPlan');
        var olddiv = document.getElementById(index);
        d.removeChild(olddiv);
        //d = null;
        console.log('removeDUT: testPlan = ', testPlan);

        // index - 1 when widget is removed
        var sub = document.getElementById('theValue');
        index = (document.getElementById('theValue').value -1);
        sub.value = index;
        console.log('index=', index);

    };
    $("#DUT").click(function () {
      addDUT();
    });