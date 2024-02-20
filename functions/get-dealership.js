const express = require('express');
const app = express();
const port = process.env.PORT || 3000;
const Cloudant = require('@cloudant/cloudant');

async function dbCloudantConnect(){
    /* try to initialize connection with IAM authentication to dealerships database
    */
    try{ //attempt connection
        const cloudant = Cloudant({ //create cloudant constant with API key and url
            plugins: { iamauth: {iamApiKey: 'OZXFODn3EjIAN1B7SLt6BnwQi1WhLroIRfWmjI20qiE2' }},
            url: 'https://78bfea69-47f6-42c2-ab2a-fec36de36077-bluemix.cloudantnosqldb.appdomain.cloud',
        });

        const db = cloudant.use('dealerships'); //create db constant from dealerships cloudant database
        console.info('Connection Successful! Connected to DB.'); //log successful connection
        return db; //return db
    } catch(err){ //catch any errors that occur
        console.error('Connection Failed: '+err.message+' for Cloudant DB'); //log error message in console
        throw err; //throw error
    }
}

let db;

(async () => { //async to attempt to connect to database
    db = await dbCloudantConnect(); //wait on database response
})();

app.use(express.json());

app.get('/dealerships/get', (req, res) =>{ //define route to get all dealerships with optional state and id filters
    const {state,id} = req.query;
    const capstate = (state.at(0).toUpperCase()+state.slice(1));

    const selector = {}; //create selector dictionary to populate with query params
    if(state){ //if state is not null...
        selector.state = capstate; //populate selector.state with state from query
    }

    if(id){ //if id is not null...
        selector.id = parseInt(id); //populate selector.id with id from query
    }

    const queryOptions = { //create a query options dictionary
        selector, //include selectors
        limit: 10, //limit to 10 documents returned
    };

    db.find(queryOptions, (err, body) =>{ //query database with query options and ...
        if(err) { //if there is an error...
            console.error('Error fetching dealerships:', err); //log error in concole
            res.status(500).json({error: 'An error occured while fetching dealerships.'}); //send 500 response          
        }else{ //if ther is no error...
            const dealerships = body.docs; //create dealership and populate with query result
            res.json(dealerships); //send response containing dealership.
        }
    });
});

app.listen(port, () => { //server listen on port 3000
    console.log('Server is running on port '+port); //log when server starts up in console
});