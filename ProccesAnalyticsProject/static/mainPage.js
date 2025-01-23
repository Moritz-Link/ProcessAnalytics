
let div_sidebar_widt = 0

const template = document.createElement('template');
template.innerHTML ='<div class="sidebar", id="div_sidebar"><button id="btn-sidebar" onclick="btn_sidebar()">X</button >';
document.getElementById("wrapper_id").appendChild(template.content);
var sidebar_item = document.getElementsByClassName("item");
function btn_sidebar() {
    if (div_sidebar_widt < 1) {
        document.getElementById('div_sidebar').style.width = "2%";
        document.getElementById('div_main_content').style.width = "98%";
        document.getElementById('btn-sidebar').style.width = "100%";
        //document.getElementById('test_h1').style.display  = "none";
        for(var i = (sidebar_item.length - 1); i >= 0; i--)
        {
            sidebar_item[i].style.display  = "none";
        };
        div_sidebar_widt = 1;
      }
      else {
        document.getElementById('div_sidebar').style.width = "10%";
        document.getElementById('div_main_content').style.width = "90%";
        document.getElementById('btn-sidebar').style.width = "40%";
        for(var i = (sidebar_item.length - 1); i >= 0; i--)
        {
            sidebar_item[i].style.display  = "";
        };
        div_sidebar_widt = 0;

        }

  }
