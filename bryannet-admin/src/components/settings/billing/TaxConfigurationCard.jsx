import {
  Card,
  CardContent,
  FormControlLabel,
  Grid,
  MenuItem,
  Stack,
  Switch,
  TextField,
  Typography,
} from "@mui/material";

export default function TaxConfigurationCard({
  settings,
  onChange,
}) {
  return (
    <Card
      elevation={0}
      sx={{
        border: (theme) => `1px solid ${theme.palette.divider}`,
        borderRadius: 3,
      }}
    >
      <CardContent>
        <Stack spacing={3}>
          <Typography variant="h6">
            Tax Configuration
          </Typography>

          <Grid container spacing={3}>
            <Grid size={12}>
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.enableTax}
                    onChange={(event) =>
                      onChange(
                        "enableTax",
                        event.target.checked
                      )
                    }
                  />
                }
                label="Enable Tax"
              />
            </Grid>

            <Grid
              size={{
                xs: 12,
                md: 6,
              }}
            >
              <TextField
                fullWidth
                label="Tax Name"
                value={settings.taxName}
                onChange={(event) =>
                  onChange(
                    "taxName",
                    event.target.value
                  )
                }
              />
            </Grid>

            <Grid
              size={{
                xs: 12,
                md: 6,
              }}
            >
              <TextField
                select
                fullWidth
                label="Tax Rate (%)"
                value={settings.taxRate}
                onChange={(event) =>
                  onChange(
                    "taxRate",
                    Number(event.target.value)
                  )
                }
              >
                <MenuItem value={0}>0%</MenuItem>
                <MenuItem value={5}>5%</MenuItem>
                <MenuItem value={7.5}>7.5%</MenuItem>
                <MenuItem value={10}>10%</MenuItem>
                <MenuItem value={15}>15%</MenuItem>
              </TextField>
            </Grid>

            <Grid size={12}>
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.taxIncludedInPrices}
                    onChange={(event) =>
                      onChange(
                        "taxIncludedInPrices",
                        event.target.checked
                      )
                    }
                  />
                }
                label="Tax Included in Prices"
              />
            </Grid>
          </Grid>
        </Stack>
      </CardContent>
    </Card>
  );
}