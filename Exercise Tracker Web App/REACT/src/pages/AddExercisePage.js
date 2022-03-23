import React, { useState } from 'react';
import { useHistory } from "react-router-dom";

export const AddExercisePage = () => {

    // sets the state before the reques.body is received
    const [name, setName] = useState('');
    const [reps, setReps] = useState('');
    const [weight, setWeight] = useState('');
    const [unit, setUnit] = useState('');
    const [date, setDate] = useState('');

    const history = useHistory();

    // adds an exercise based on JSON object that is passed to the server
    // if successful then 201 is passed else failed
    const addExercise = async () => {
        const newExercise = { name, reps, weight, unit, date };
        const response = await fetch('/exercises', {
            method: 'POST',
            body: JSON.stringify(newExercise),
            headers: {
                'Content-Type': 'application/json',
            },
        });
        if (response.status === 201) {
            alert("Successfully added the exercises");
        } else {
            alert(`Failed to add exercises`);
        }
        history.push("/");
    };

    // table that shows the different variables that can be added
    return (
        <div>
            <h1>Add Exercises</h1>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Reps</th>
                    <th>Weight</th>
                    <th>Unit</th>
                    <th>Date</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><input type="text" placeholder="Enter exercise name" value={name} onChange={e => setName(e.target.value)} /></td>
                    <td><input type="number" min="1" value={reps} placeholder="Enter # of reps" onChange={e => setReps(e.target.value)} /></td>
                    <td><input type="number" min="1" value={weight} placeholder="Enter weight used" onChange={e => setWeight(e.target.value)} /></td>
                    <td><input type="text" placeholder="Enter unit type" list="weightlist" value={unit} onChange={e => setUnit(e.target.value)} />
                        <datalist id = "weightlist">
                            <option value = "lbs">lbs</option>
                            <option value = "kgs">kgs</option>
                        </datalist>
                    </td>
                    <td><input type="text" minlength="8" maxlength="8" placeholder="Enter date MM-DD-YY" value={date} onChange={e => setDate(e.target.value)} /></td>
                </tr>
            </tbody>
            <button onClick={addExercise}>Add</button>
        </div>
    );
}

export default AddExercisePage;