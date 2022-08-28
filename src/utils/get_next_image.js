const fs = require("fs");
const path = require("path");

// const rocket_images_path = './client/public/rocket_images/';
const rocket_images_path = './client/build/rocket_images/';

const get_next_image = (dir, img_idx, res, sendback) =>
{
    /* SYNCHRONOUS CODE */
    // const files = fs.readdirSync(dir);
    
    // let found = false;
    // let next_file = '';

    // img_idx = ((img_idx % files.length)===0) ? files.length : (img_idx % files.length);

    // next_file = files.filter(file => file.startsWith(`${img_idx}_`));

    // return { next_file : next_file, folder_size : files.length };

    /* ASYNCHORONOUS CODE */
    let next_file = '';
    let folder_size = 0;
    fs.readdir(
        dir,
        (err, data) =>
        {
            if(err)
            {
                console.log('ERROR READ DIRECTORY');
            }

            folder_size = data.length;
            img_idx = ((img_idx % data.length)===0) ? data.length : (img_idx % data.length);

            next_file = data.filter(file => file.startsWith(`${img_idx}_`));

            sendback(dir, next_file, folder_size, res);
            // console.log(next_file);
        }
    );
};
const send_next_image = (img_idx, res) =>
{
    get_next_image(
        rocket_images_path,
        img_idx,
        res,
        (dir, file, folder_size, res) =>
        {
            if(file === '')
            {
                res.send(
                    { end : 'IMAGE WITH THIS INDEX DOES NOT EXIST' }
                );
                return;
            }
            res.send(
                {
                    image_path : dir + file,
                    folder_size : folder_size
                }
            );
        }
    );
    
};


module.exports = send_next_image;