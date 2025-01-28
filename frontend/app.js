import { useEffect, useState } from "react";

function App() {
    const [data, setData] = useState(null);

    useEffect(() => {
        fetch("http://127.0.0.1:8000/simulate")
            .then(response => response.json())
            .then(data => setData(data));
    }, []);

    return (
        <div>
            <h1>HVAC Simulation</h1>
            <p>Simulation Result: {data ? JSON.stringify(data) : "Loading..."}</p>
        </div>
    );
}

export default App;