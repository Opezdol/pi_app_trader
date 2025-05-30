import React from "react";
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';

export default function SubscribeForm() {
  let selectables = [
    "BTC",
    "LTC",
    "ETH",
    "Someshit"
  ]
  const [value, setValue] = React.useState<string | null>(null);

  return (
    <Box p={3} bgcolor='lightgray' width='25%'>
    <Stack spacing={2} width="200px">
      <Typography variant="h5" gutterBottom>
        Tracer
      </Typography>
      <Autocomplete
          openOnFocus
          fullWidth
          autoComplete
          options={selectables}
          onChange={(event, newValue) => {
              setValue(newValue);
              console.log(newValue);
          }}
          renderInput={ (params) => <TextField {...params} 
          label="Route" />  }
      />
      <Button onClick={(e) =>{
          console.log("Clicked!!!");
          console.log(value);
          setValue(null);
        }} >Add to Monitor</Button>
  </Stack>
  </Box>
  )
}



