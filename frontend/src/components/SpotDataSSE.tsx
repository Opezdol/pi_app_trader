
import React, { useEffect, useState } from 'react';
import { createArrayDataSource } from '@mui/x-data-grid'; // Import the createArrayDataSource utility for DataGrid
import { DataGrid } from '@mui/x-data-grid'; // Import the DataGrid component
const SpotDataSSE = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    const eventSource = new EventSource('/sse');

    eventSource.onmessage = (event) => {
      const new_data = JSON.parse(event.data);
      setData(new_data.data);
    };

    return () => {
      eventSource.close();
    };
  }, []);

  // Define the columns for the table based on your SpotData model
  const columns = [
    { field: 'instType', headerName: 'Inst Type' },
    { field: 'instId', headerName: 'Inst ID' },
    { field: 'last', headerName: 'Last Price' },
    // Add more columns as needed.
  ];

  return (
    <div>
      <DataGrid
        rows={data}
        columns={columns}
        getRowId={(rows) => rows.index} // Optional: provide a unique ID for each row if necessary
        disableSelectionOnClick={true} // Optional: Prevent row selection on click
        density="compact" // Optional: Adjust the table density (options: 'comfort', 'compact')
      />
    </div>
  );
};

export default SpotDataSSE;
