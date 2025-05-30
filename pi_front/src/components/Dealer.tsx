
import React from 'react'
import Select from 'react-select'
import axios from 'axios'
import {
  Button,
  Center,
  Field,
  Fieldset,
  NumberInput,
  Stack,
} from "@chakra-ui/react"
//
//

type Side = 'buy' | 'sell';

type Deal = {
  route: string | null;
  instAmount: number | null;
  baseAmount: number | null;
  side: Side | null;
}
const defValue: Deal = { route: null, instAmount: null, baseAmount: null, side: null };

export type Route =
  {
    "baseCcy": string,
    "instId": string,
    "instType": string,
    "lotSz": number,
    "minSz": number,
    "quoteCcy": string,
    "state": string,
    "tickSz": number
  }



const Dealer = ({ routes }: { routes: Route[] | null }) => {

  const [state, setState] = React.useState<Deal>(defValue);

  const handleSubmit = () => {
    console.log("Posting submit:");
    axios.post('http://127.0.0.1:8000/db/trans', state)
      .then(function (response) {
        console.log(response.data);
      })
      .catch(function (error) {
        console.log(error);
      });



    setState({
      ...defValue,
      route: state.route,
    });
    console.log(state);

  };
  // Input fields function handles onChange
  const valueChangeHandler = (e: React.ChangeEvent<HTMLInputElement>) => {
    setState({
      ...state,
      [e.target.name]: e.target.value,
    })
  };
  // Buttons <Bye | Sell > onClick function
  const sideButtonHandler = (e: React.MouseEvent<HTMLButtonElement>) => {
    setState({
      ...state,
      side: e.target.name,
    })
  }

  //bgColor on select 

  const buttonStyles = {
    variant: "outline",
    transition: "background 0.5s ease-in-out",
  }
  //
  const selectables = routes?.map((val: Route) => ({ value: val.instId, label: val.instId }));

  return (
    <Fieldset.Root bg='blue.200' color='black' p={3} rounded='sm' size="md" maxW="20%" >
      <Center><Stack>
        <Fieldset.Legend >Dealer</Fieldset.Legend>
      </Stack>
      </Center>

      <Fieldset.Content>

        <hr />
        <Select
          options={selectables}
          name='route'
          placeholder='Route'
          onChange={(e) => {
            setState({
              ...state,
              route: e ? e.value : null,
            });
            console.log(state);
          }} />
        <hr />

        <Field.Root alignItems={'center'}>

          <Stack align="flex-start" direction="row" gap="10"   >
            <Button
              tabIndex={0}
              name='buy'
              onClick={sideButtonHandler}
              css={buttonStyles}
              bgColor={state?.side == "buy" ? "green.500" : "gray.400"}
            >
              Buy
            </Button>
            <Button
              tabIndex={0}
              name='sell'
              onClick={sideButtonHandler}
              css={buttonStyles}
              bgColor={state?.side == "sell" ? "red.500" : "gray.400"}
            >
              Sell
            </Button>

          </Stack>
        </Field.Root>

        <Field.Root>
          <Field.Label>{state?.route ? state.route : "instAmount"}</Field.Label>

          <NumberInput.Root name='instAmount' required
            value={String(state?.instAmount)}
            onChange={valueChangeHandler}>
            <NumberInput.Input />
          </NumberInput.Root>

        </Field.Root>

        <Field.Root>
          <Field.Label>baseAmount</Field.Label>
          <NumberInput.Root name='baseAmount' required
            value={String(state?.baseAmount)}
            onChange={valueChangeHandler}>
            <NumberInput.Input />
          </NumberInput.Root>
        </Field.Root>
      </Fieldset.Content>

      <Center>
        <Button type="submit"
          tabIndex={0}
          alignSelf="flex-start"
          onClick={handleSubmit}
          disabled={!state.instAmount || !state.baseAmount || !state.side || !state.route}
        >
          Submit
        </Button>
      </Center>
    </Fieldset.Root >

  );
};

export default Dealer

