import './App.css'
import { useEffect, useState } from "react";
import axios from "axios";
//import { HStack } from "@chakra-ui/react"
import { Flex } from "@chakra-ui/react"
import Dealer, { Route } from "./components/Dealer.tsx"
import DealGrid from './components/DealTable.tsx';

const usdtMarketUrl = "http://127.0.0.1:8000/market_usdt";

function App() {
  const [routeSelect, setRoutes] = useState<Route[] | null>(null);
  useEffect(() => {
    axios.get(usdtMarketUrl)
      .then((response) => {
        setRoutes(response.data);
      })
      .catch((error) => {
        console.log("Error reciveing Routes from backend");
        setRoutes(null);

      });
  }, []);
  return (
    <>
      <Flex>
        <div>
          <Dealer routes={routeSelect} />
        </div>
        <DealGrid />
      </Flex>
    </>
  )
}

export default App
