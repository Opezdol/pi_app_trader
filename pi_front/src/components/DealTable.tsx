import { useEffect, useState } from 'react';
import { DataGrid } from '@mui/x-data-grid'; // Import the DataGrid component
import axios from 'axios'


interface Route {
  name: string;
  id: number;
}
interface DealPublic {
  side: string;
  instAmount: number;
  baseAmount: number;
  id: number;
  route: Route;
  price: number | null;
  myprice: number | null;
  coeff: number | null;

}

interface PriceUpdate {
  instId: string
  bidPx: number,
  askPx: number,
  ts: number,
}


const DealGrid = () => {
  const [items, setData] = useState<DealPublic[]>([]);
  const [prices, setPrices] = useState<PriceUpdate[]>([]);
  useEffect(() => {
    axios.get('http://127.0.0.1:8000/db/trans')
      .then(function (response) {
        console.log(response);
        let data = response.data;
        setData(data);
      })
      .catch(function (error) {
        console.log(error);
      })

    const eventSource = new EventSource('http://127.0.0.1:8000/sse');
    eventSource.onmessage = (event) => {
      const new_data = JSON.parse(event.data);
      console.log(new_data);

      setPrices(new_data);
    };


    return () => {
      eventSource.close();
    };
  }, []);



  const getPrice = (side: string, name: string) => {
    for (var price of prices) {
      if (name == price.instId) {
        return side == 'buy' ? price.askPx : price.bidPx;
      }
    }
  }


  useEffect(() => {
    let data = items;
    data.map((obj: DealPublic) => {
      const res = getPrice(obj.side, obj.route.name);
      // in case of undefined
      obj.price = res ? res : 69;
      obj.myprice = obj.instAmount / obj.baseAmount;
      obj.coeff = obj.myprice / obj.price;
    })
    setData(data);

  }, [prices]);





  // Define the columns for the table based on your SpotData model
  const columns = [
    {
      field: 'route', headerName: 'Inst Type',
      valueGetter: (route: Route) => {
        return route.name;
      },

    },
    {
      field: 'id', headerName: 'ID', valueGetter: (route: Route) => {
        return route.id;
      }
    },
    { field: 'instAmount', headerName: 'instAmount' },
    { field: 'baseAmount', headerName: 'baseAmount' },
    { field: 'side', headerName: 'Side' },
    { field: 'price', headerName: 'Price' },
    { field: 'myprice', headerName: 'My Price' },
    {
      field: 'coeff', headerName: 'Coeff', width: 250,
    },]

  return (
    <div style={{ width: "100%", height: "600px" }}>
      <DataGrid
        rows={items}
        columns={columns}
        getRowId={(rows) => rows.id} // Optional: provide a unique ID for each row if necessary
        density="compact" // Optional: Adjust the table density (options: 'comfort', 'compact')
      />
    </div >
  );
};

export default DealGrid




