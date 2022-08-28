const fs = require("fs");
const request = require('request');

let interop_url = ''
let odlc_id = 0;
let cookies = '';

const submit_odlc = (odlc_data, response) =>
{
    if(interop_url === '')
    {
        const login_data = fs.readFileSync('./api/public/params.json');
        const login_json = JSON.parse(login_data);
        interop_url = `http://${login_json.ip}/api`;
    }
    if(cookies === '')
    {
        cookies = fs.readFileSync('./api/public/cookies.txt');
    }
    const options =
    {
        url: `${interop_url}/odlcs`,
        json: true,
        headers:{
            'Cookie': cookies,
            'Content-Type': 'application/json'
        },
        body: {
            ...odlc_data
        }
    };
    request.post(
        options, 
        (err, res, body) => 
        {
            if (err) 
            {
                return console.log(err);
            }
            console.log(`Status: ${res.statusCode}`);
            odlc_id = body.id;

            response.send('ODLC DATA SUBMITTED');
        }
    );
};

const submit_image = (img_data, response) =>
{
    let img = Buffer.from(img_data.split(';base64,')[1], 'base64');
    const options =
    {
        url: `${interop_url}/odlcs/${odlc_id}/image`,
        json: false,
        headers:{
            'Cookie': cookies,
            'Content-Type': 'image/png'
        },
        body: img
    };

    if(odlc_id === 0) 
    {
        response.send('ERROR');
    }
    else
    {
        // SUBMIT IMAGE WITH ODLC ID
        request.post(
            options,
            (err, res, body) => 
            {
                if (err) 
                {
                    return console.log(err);
                }
                console.log(`Status: ${res.statusCode}`);
                odlc_id = 0;
                response.send('SUBMITTED TO INTEROP');
            }
        );
    }
};

module.exports = 
{
    submit_odlc : submit_odlc,
    submit_image : submit_image
};