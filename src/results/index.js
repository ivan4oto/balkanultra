import "./main.scss";
import ultra2020 from "./2020ultra.json"
import ultra2021 from "./2021ultra.json"
import sky2021 from "./2021sky.json"
import ultra2022 from "./2022ultra.json"
import sky2022 from "./2022sky.json"
import ultra2023 from "./2023ultra.json"
import sky2023 from "./2023sky.json"

// Map with results
const resultsMap = {
  'ultra2020': ultra2020,
  'ultra2021': ultra2021,
  'sky2021': sky2021,
  'ultra2022': ultra2022,
  'sky2022': sky2022,
  'ultra2023': ultra2023,
  'sky2023': sky2023
}

// Function to populate table with data
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

// Function to load JSON data
async function loadJsonData(filename) {
  const response = await fetch(filename);
  if (!response.ok) {
    throw new Error(`Error loading ${filename}: ${response.statusText}`);
  }
  return await response.json();
}

// Function to clear the table content
function clearTable() {
  const tableBody = document.getElementById("table-body");
  while (tableBody.firstChild) {
    tableBody.removeChild(tableBody.firstChild);
  }
}

// Function to update the table with the selected data
async function updateTable() {
  const year = document.getElementById("year-select").value;
  const type = document.getElementById("type-select").value;

  // Load the JSON data
  const staticPath = document.getElementById("results-container").getAttribute("data-static-path");
  const filename = `${type}${year}`;
  try {
    const jsonData = resultsMap[filename] // await loadJsonData(filename);
    clearTable();
    populateTable(jsonData);
  } catch (error) {
    console.error(error);
  }
}

// Add event listeners to the dropdowns
document.getElementById("year-select").addEventListener("change", updateTable);
document.getElementById("type-select").addEventListener("change", updateTable);

// Call the function to load the initial data and populate the table
updateTable();
