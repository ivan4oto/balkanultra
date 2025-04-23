// CSS
import "./main.scss"; // Main CSS

// JS
async function getTopAthletes() {
  $.ajax({
    url: `${scheme}://${host}/athlete/top-athletes/?distance=78.0`,
    method: 'GET',
    success: function(response) {
        populateTable(response);
        console.log(response);
    },
    error: function(xhr, status, error) {
        console.log(error);
    }
  })
}


function populateTable(data) {
  const tableBody = document.getElementById("table-body");
  data.forEach((item) => {
    const row = document.createElement("tr");

    Object.values(item).forEach((value) => {
      const cell = document.createElement("td");
      cell.textContent = value;
      row.appendChild(cell);
    });

    tableBody.appendChild(row);
  });
}

getTopAthletes();