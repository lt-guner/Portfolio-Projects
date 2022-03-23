import React, { useState } from 'react';
import { useHistory } from "react-router-dom";

export const EditExercisePage = ({ exerciseToEdit }) => {

    // sets the state of the req.body are current populated
    const [name, setName] = useState(exerciseToEdit.name);
    const [reps, setReps] = useState(exerciseToEdit.reps);
    const [weight, setWeight] = useState(exerciseToEdit.weight);
    const [unit, setUnit] = useState(exerciseToEdit.unit);
    const [date, setDate] = useState(exerciseToEdit.date);

    const history = useHistory();

    // makes a call to the server to push changes and returns a promist
    // if successful it returns a status of 200 else failed
    const editExercise = async () => {
        const editedExercise = { name, reps, weight, unit, date };
        const response = await fetch(`/exercises/${exerciseToEdit._id}`, {
            method: 'PUT',
            body: JSON.stringify(editedExercise),
            headers: {
                'Content-Type': 'application/json',
            },
        });
        if (response.status === 200) {
            alert("Successfully edited the exercise");
        } else {
            alert(`Failed to edit exercise`);
        }
        history.push("/");
    };

    // the table that shows the exercise variables that can be edited
    return (
        <div>
            <h1>Edit Exercise</h1>
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
                    <td><input type="text" value={name} onChange={e => setName(e.target.value)} /></td>
                    <td><input type="number" min="1" value={reps} onChange={e => setReps(e.target.value)} /></td>
                    <td><input type="number" min="1" value={weight} onChange={e => setWeight(e.target.value)} /></td>
                    <td><input type="text" list="weightlist" value={unit} onChange={e => setUnit(e.target.value)} />
                        <datalist id = "weightlist">
                            <option value = "lbs">lbs</option>
                            <option value = "kgs">kgs</option>
                        </datalist>
                    </td>
                    <td><input type="text" minlength="8" maxlength="8" value={date} onChange={e => setDate(e.target.value)} /></td>
                </tr>
            </tbody>
            <button
                onClick={editExercise}
            >Save</button>
        </div>
    );
}

export default EditExercisePage;