import "./main.scss"; 

const tableHtml = `
<table class="table">
        <thead>
            <tr>
                <th scope="col">#</th>
                <th scope="col">Име</th>
                <th scope="col">Фамилия</th>
                <th scope="col">Време</th>
            </tr>
        </thead>
    <tbody id='table-body'>
    </tbody>
</table>
`

$(function() {

    $.ajax({
        url: `http://127.0.0.1:8000/results/json`, // the endpoint
        type: "GET", // http method
        success: [         
            function(json) {
                var years_mapping = ["first", "second"] // Bootstrap doesn't allow numbers to be used as ids for some reason...
                
                for (let y = 0; y < Object.keys(json).length; y ++){
                    var year = Object.keys(json)[y];
                    
                    for (let r = 0; r < Object.keys(json[year]).length; r ++) {
                        var race = Object.keys(json[year])[r]
                        var raceCyrilic = race == 'ultra' ? 'Ултра' : 'Скай'
                        $(`#${years_mapping[y]}`).append(`
                        <div class="d-flex justify-content-center">
                        <h3 id='type-label'>${raceCyrilic}</h3>
                        </div>
                        `)
                        $(`#${years_mapping[y]}`).append(tableHtml)
                        $('#table-body').attr('id', `table-${year}-${race}`)

                        
                        for (let i = 0; i < json[year][race].length; i++) {
                            var athleteProps = json[year][race][i]
                            $(`#table-${year}-${race}`).append(`
                            <tr>
                                <th scope="row">${athleteProps['Ranking']}</th>
                                <td>${athleteProps['First name']}</td>
                                <td>${athleteProps['Family name']}</td>
                                <td>${athleteProps['Time']}</td>
                            </tr>
                            `)
                        }

                    }

                }                
        }],

        error: function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
})