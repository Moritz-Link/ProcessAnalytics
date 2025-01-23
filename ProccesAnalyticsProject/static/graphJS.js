
var activities_l = []
var csrftoken = '{{ csrf_token }}';
var data_upload_status = 1
function open_close_data_upload(){


  if (data_upload_status < 0) {
    
    document.getElementById('div_choose_graph').style.display = "none";
    document.getElementById('Case_Table').style.gridRowStart = "2";
    document.getElementById('open_close_data_upload_button').innerHTML = "Open Upload";
  }
  if (data_upload_status > 0) {
    document.getElementById('Case_Table').style.gridRowStart = "3";
    document.getElementById('div_choose_graph').style.display = "block";
    document.getElementById('open_close_data_upload_button').innerHTML = "Close Upload";
    
  }
  data_upload_status = data_upload_status * -1
}

function graph(event){
  let value = event.target.value;
  
  //console.log(text)
  //value = document.getElementById("button_Choice").value
  console.log(value)
  //console.log("tet")
  load_data(value)
  
  process_step_tables(value)

}

function process_step_tables(case_id){
  console.log("process_step_tables")
  document.getElementById("id_ProcessData_CaseID").innerHTML  = case_id;
  fetch("load_graph_tables", {
    method: 'POST',
    credentials: 'same-origin',
    headers:{
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest', 
        'X-CSRFToken': csrftoken,
},
    body: JSON.stringify({'c_id':case_id}) 
})
  .then(response => response.json())
  .then(response => {
    var data = response
    //buildSimulation(data) other function
    generateTable(data)
    generate_generalData(data)
  });
}
function generate_generalData(data){
  document.getElementById("Process_Data_general_div").innerHTML = ""
  let columns = data.general_columns
  let values = data.general_values
  const tbl = document.createElement("table");
  const tblBody = document.createElement("tbody");
  const row = document.createElement("tr");

  for (let r in columns){// Columns 

    let cell = document.createElement("td");
    cell.style.fontSize ="13px";
    cell.appendChild(document.createTextNode(columns[r])); //Value of Colum
    row.appendChild(cell);
  }
  tblBody.appendChild(row);
  const row2 = document.createElement("tr");
  for (let r in values){// Columns 

    let cell = document.createElement("td");
    cell.contentEditable ="true" //contenteditable="true"
    cell.style.fontSize ="12px";
    cell.appendChild(document.createTextNode(values[r])); //Value of Colum
    row2.appendChild(cell);
  }
  tblBody.appendChild(row2);
  tbl.appendChild(tblBody);
  tbl.setAttribute('id', 'general_data_table');
  document.getElementById("Process_Data_general_div").append(tbl);
}
function generateTable(data){

  activities_l = data.activities
  let activities_data = data.activities_data
  var ul = document.getElementById("Process_Data_ul");
  while(ul.firstChild) ul.removeChild(ul.firstChild);
  ul.style.listStyleType = "none";
  for (let x in activities_l) {
    let activity = activities_l[x]
    //console.log(activity)
    var li = document.createElement("li");
    const tbl = document.createElement("table");
    tbl.setAttribute('id', activity);
    const tblBody = document.createElement("tbody");
    tbl.createCaption().innerHTML =activity;

    for (let r in activities_data[x]){
      const row = document.createElement("tr");
      //console.log(activities_data[x][r])
      let cell = document.createElement("td");
      cell.appendChild(document.createTextNode("TS"));
      row.appendChild(cell);
      cell = document.createElement("td");
      cell.contentEditable ="true"
      cell.appendChild(document.createTextNode(activities_data[x][r]));
      row.appendChild(cell);
      tblBody.appendChild(row);
    }
 
    tbl.appendChild(tblBody);
    //document.getElementById("Process_Data").append(tbl);
    li.appendChild(tbl);
    li.style.color = "black";
    li.style.float = "left";
    li.style.width = "20%";
    li.style.marginLeft = "2%";
    li.setAttribute("class", "process_table_class_li");
    ul.appendChild(li);
  }
}

function load_data(case_id){
    const formData = new FormData();
    formData.append("case_id", case_id);
    formData.append("csrfmiddlewaretoken", csrftoken);
    fetch("load_graph", {
      method: 'POST',
      credentials: 'same-origin',
      headers:{
          'Accept': 'application/json',
          'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
          'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({'c_id':case_id}) //JavaScript object of data to POST
    })
    .then(response => response.json())
    .then(response => {
      //l = console.log(response);
      var data = response
      buildSimulation(data)
    });
}

function buildSimulation(data){
  
  var chart = "";
  document.getElementById("div_graph").innerHTML = "";
  document.getElementById("id_ProcessData_Prediction").innerHTML = "";
  // create a chart and set the data
  var chart = anychart.graph(data);
  chart.layout().type("fixed");
  var nodes = chart.nodes();

  nodes.normal().shape("box");//square
  nodes.normal().height(40);
  nodes.normal().width(60);

  chart.nodes().labels().enabled(true);
  chart.nodes().labels().format("{%activity}");
  chart.nodes().labels().fontSize(12);
  chart.nodes().labels().fontWeight(300);
  nodes.normal().fill("#ffa000");
  // set the container id
  chart.edges().normal().stroke("#ffa000", 4, "10 5", "round")
  chart.container("div_graph");

  // initiate drawing the chart
  chart.draw();
}

function clearSimulation(){
  document.getElementById("div_graph").innerHTML = ""
  document.getElementById("Process_Data_ul").innerHTML = ""
  document.getElementById("Process_Data_general_div").innerHTML = ""
  document.getElementById("id_ProcessData_CaseID").innerHTML = "Choose a case from the table"
  document.getElementById("id_ProcessData_Prediction").innerHTML = ""
}

function updata_process_instance_data(){
  const update_activities_data = []
  console.log("updata_process_instance_data")
  let general_table = document.getElementById("general_data_table");
  const general_data = read_table_info(general_table)
  //console.log(general_data)
  //console.log(activities_l)
  //for schleife durchgehen und alle Tabellen lesen + einen Eintrag erstellen
  for (activity in activities_l){
    var activity_table_data = read_table_info(document.getElementById(activities_l[activity]))
    update_activities_data.push(activity_table_data);
  }

  var send_data = {"general_data": general_data, "activities_data": update_activities_data, "activities": activities_l}
  //console.log(send_data)


  send_general_updated_data(send_data)
  //send_general_updated_data(general_data) -> Ändern damit alles gescihckt wird
  // bei Update -> zu safe ändern und dann via ID speichern
  // Predict -> Gleiche aber nicht speiccher, sondern nur predicten
}
function predict_process_instance_data(){
  const update_activities_data = []
  console.log("updata_process_instance_data")
  let general_table = document.getElementById("general_data_table");
  const general_data = read_table_info(general_table)
  //console.log(general_data)
  //console.log(activities_l)
  //for schleife durchgehen und alle Tabellen lesen + einen Eintrag erstellen
  for (activity in activities_l){
    var activity_table_data = read_table_info(document.getElementById(activities_l[activity]))
    update_activities_data.push(activity_table_data);
  }

  var send_data = {"general_data": general_data, "activities_data": update_activities_data, "activities": activities_l}
  //console.log(send_data)


  send_general_predict_data(send_data)
  //send_general_updated_data(general_data) -> Ändern damit alles gescihckt wird
  // bei Update -> zu safe ändern und dann via ID speichern
  // Predict -> Gleiche aber nicht speiccher, sondern nur predicten
}


function read_table_info(table){
  const table_data = [];
  var rowLength = table.rows.length;
  //loops through rows    
  for (i = 0; i < rowLength; i++){
    const table_data_row = [];
    //gets cells of current row
    var oCells = table.rows.item(i).cells;
    //gets amount of cells of current row
    var cellLength = oCells.length;
    
    //loops through each cell in current row
      for(var j = 0; j < cellLength; j++){
        /* get your cell info here */
        /* var cellVal = oCells.item(j).innerHTML; */
        
        table_data_row.push(oCells.item(j).innerHTML)
      }
    table_data.push(table_data_row)
    
    }
    return table_data
}
function send_general_predict_data(general_data){
  fetch("preditct_data_from_process_tables", {
    method: 'POST',
    credentials: 'same-origin',
    headers:{
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
        'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({'data':general_data}) //JavaScript object of data to POST
  })
  .then(response => response.json())
  .then(response => {
    console.log(response);
    const prediction_value =  response["graph_prediction"];
    document.getElementById("id_ProcessData_Prediction").innerHTML = "Prediction: "+prediction_value +" %";
  });
}
function send_general_updated_data(general_data){
  fetch("update_data_from_process_tables", {
    method: 'POST',
    credentials: 'same-origin',
    headers:{
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
        'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({'data':general_data}) //JavaScript object of data to POST
  })
  .then(response => response.json())
  .then(response => {
    console.log(response);
    
    
  });
}

