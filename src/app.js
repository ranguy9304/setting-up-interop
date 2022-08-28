const fs = require('fs');
const path = require('path');
const request = require('request');
const express = require('express');
const cookieParser = require('cookie-parser');
const cors = require('cors');

const send_next_image = require('./utils/get_next_image');
const submit = require('./utils/submit_interop');
const { json } = require('express');

const app = express();
app.use(express.json());
app.use(cookieParser());
app.use(cors());
const port = process.env.PORT || 8000;
let interop_url = '';

/**
 * @author Aditya Choubey
 * @description GET function. Fetch from this URL to get path to next image in folder.
 */

app.get(
    '/image',
    (req,res) =>
    {
        send_next_image(req.query.img_idx, res);
    }
);

/**
 * @author Aditya Choubey and Darshan K S
 * @description POST function. Get b64 encoded data and upload to interop server as decoded png image.
 */
app.post(
    '/upload_img',
    (req, res) =>
    {
        submit.submit_image(req.body.raw_img_data, res);
    }
);

/**
 * @author Aditya Choubey and Darshan K S
 * @description POST function. Get details object and upload to interop server.
 */
app.post(
    '/upload_odlc',
    (req, res) =>
    {
        const odlc_data =
        {
            mission: req.body.mission,
            type: req.body.type_data,
            latitude: req.body.lat_data,
            longitude: req.body.long_data,
            orientation: req.body.orientation_data,
            shape: req.body.shape_data,
            shapeColor: req.body.shape_color_data,
            alphanumeric: req.body.an_data,
            alphanumericColor: req.body.an_color_data,
            autonomous: false
        };
        submit.submit_odlc(odlc_data, res);
    }
);

/**
 * @author Aditya Choubey and Darshan K S
 * @description POST function. Get emergent details object and upload to interop server.
 */
app.post(
    '/upload_emergent',
    (req, res) =>
    {
        const odlc_data =
        {
            mission: req.body.mission,
            type: req.body.type_data,
            latitude: req.body.lat_data,
            longitude: req.body.long_data,
            description: req.body.desc,
            autonomous: false,
            // orientation: null,
            // shape: null,
            // shapeColor: null,
            // alphanumeric: null,
            // alphanumericColor: null,

        }
        submit.submit_odlc(odlc_data, res);
    }
)


app.listen(
    port,
    () =>
    {
        console.log('Starting server on Port ' + port);

        const login_data = fs.readFileSync('./api/public/params.json');
        const login_json = JSON.parse(login_data);
        interop_url = `http://${login_json.ip}/api`;

        request.post(
            {
                headers: {'Content-Type': 'application/json'},
                url: `${interop_url}/login`,
                body: 
                JSON.stringify(
                    {
                        username: login_json.username,
                        password: login_json.password 
                    }
                )
            }, 
            (error, response, body) =>
            {
                if(error)
                {
                
                    console.log(error);
                }
                else
                {
                    console.log('LOGIN SUCCESSFUL');
                    const cookies = response.headers['set-cookie'][0].split(';')[0];
                    console.log(cookies);
                    fs.writeFileSync('./api/public/cookies.txt', cookies);
                }
                
            }
        );
    }
);

