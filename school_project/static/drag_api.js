const button = document.getElementById('the_button')
let contestants = []
async function apicall() {
    var response = await fetch("https://sheet2api.com/wiki-api/List_of_Drag_Race_contestants/en/Contestants+of+RuPaul%2527s+Drag+Race+and+their+backgrounds");
    var coderData = await response.json();

    for (let i = 0; i <= coderData.length - 1; i++) {
        if (coderData[i]['Hometown']) {
            hometown = coderData[i]['Hometown'].split(', ');
            HometownData = { city: hometown[0], state: hometown[1] }

            console.log(HometownData)
        }

        else {
            HometownData = 'null'
        }

        contestant_name = coderData[i]['Contestant'].split(' '),
            last_name = (contestant_name.length > 1) ? contestant_name[1] : '';
        name_data = {
            first_name: contestant_name[0],
            last_name: last_name
        }

        ContestantData = {
            Season: coderData[i]['Season'],
            Contestant: name_data,
            Age: coderData[i]['Age'],
            Hometown: HometownData,
            Outcome: coderData[i]['Outcome'].replace(/\[[^\]]*\]/g, "")
        }
        contestants.push(ContestantData)
        console.log(contestants)

    }

    return contestants

}
apicall()

function insert() {
    // $.post("/insert_queen", {
    //     data: contestants
    // })

    fetch("/insert_queen",
        {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'Accept': 'application/json'
            },

            body: JSON.stringify(contestants)
        }).then(res => {
            if (res.ok) {
                return res.json()
            } else {
                alert("something is wrong")
            }
        }).then(jsonResponse => {

            // Log the response data in the console
            console.log(jsonResponse)
        }
        ).catch((err) => console.error(err));
    //                 
}


// fetch("/insert_queen", {
//     method: "POST",
//     body: JSON.stringify(contestants),
//     headers: {
// "Content-type": "application/json; charset=UTF-8"
//     }
// });
