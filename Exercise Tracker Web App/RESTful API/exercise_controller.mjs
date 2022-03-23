import * as exercises from './exercise_model.mjs';
import express from 'express';

const PORT = 3000;

const app = express();

app.use(express.static('public'));

app.use(express.urlencoded({
    extended: true
}));

app.use(express.json());

/**
 * Create a new exercise with the name, reps, weight, unit, and date provided in the body
 * The post method takes the JSON body and sends it to the createExercises function in exercis_controller.mjs
 * If there was an error then 400 was called and this coule be because of an invalid input
 */
app.post('/exercises', (req, res) => {
    exercises.createExercise(req.body.name, req.body.reps, req.body.weight, req.body.unit, req.body.date)
        .then(exercise => {
            res.status(201).json(exercise);
        })
        .catch(error => {
            console.error(error); // this will actually show the actual error code
            res.status(400).json({ Error: 'Request failed' }); // this is more of user friendly response
        });
});


/**
 * Retrive the exercise corresponding to the ID provided in the URL.
 * The id of the in the url contains the mongoDB id that is used to lookup the value
 * If the id does not exist, then a 404 is found
 * Other errors will be generalized as 400
 */
app.get('/exercises/:_id', (req, res) => {
    const exerciseId = req.params._id;
    exercises.findExerciseById(exerciseId)
        .then(exercise => {
            if (exercise !== null) {
                res.json(exercise);
            } else {
                res.status(404).json({ Error: 'Resource not found' });
            }
        })
        .catch(error => {
            console.error(error); // this will actually show the error message in the stderr which includes stderr
            res.status(400).json({ Error: 'Request failed' }); //this is more of an aesthetic 
        });
});

/**
 * Retrive exercises.                                                                           
 * If the query parameters include a year, then only the exercises for that year are returned.
 * Otherwise, all exercises are returned.
 */
app.get('/exercises', (req, res) => {
    let filter = {};
    // Is there a query parameter named year? If so add a filter based on its value.
    if (req.query.date !== undefined) {
        filter = { year: req.query.date };
    }
    exercises.findExercises(filter, '', 0)
        .then(exercises => {
            res.json(exercises);
        })
        .catch(error => {
            console.error(error); // this will actually show the error message in the stderr which includes stderr
            res.status(400).json({ Error: 'Request failed' }); //this is more of an aesthetic 
        });
});

/**
 * Update the exercises whose id is provided in the path parameter and set
 * its title, year and language to the values provided in the body.
 */
app.put('/exercises/:_id', (req, res) => {
    exercises.replaceExercise(req.params._id, req.body.name, req.body.reps, req.body.weight, req.body.unit, req.body.date)
        .then(numUpdated => {
            if (numUpdated === 1) {
                res.json({ _id: req.params._id, name: req.body.name, reps: req.body.reps, weight: req.body.weight, unit: req.body.unit, date: req.body.date })
            } else {
                res.status(404).json({ Error: 'Resource not found' });
            }
        })
        .catch(error => {
            console.error(error); // this will actually show the error message in the stderr which includes 500
            res.status(400).json({ Error: 'Request failed' }); //this is more of an aesthetic 
        });
});

/**
 * Delete the movie whose id is provided in the query parameters
 */
app.delete('/exercises/:_id', (req, res) => {
    exercises.deleteExerciseById(req.params._id)
        .then(deletedCount => {
            if (deletedCount === 1) {
                res.status(204).send();
            } else {
                res.status(404).json({ Error: 'Resource not found' });
            }
        })
        .catch(error => {
            console.error(error);
            res.send({ error: 'Request failed' });
        });
});

app.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}...`);
});