import {
  Card,
  CardContent,
  FormControlLabel,
  Grid,
  Stack,
  Switch,
  TextField,
  Typography,
} from "@mui/material";

export default function InvoiceSettingsCard({
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
            Invoice Settings
          </Typography>

          <Grid container spacing={3}>
            <Grid
              size={{
                xs: 12,
                md: 6,
              }}
            >
              <TextField
                fullWidth
                label="Invoice Prefix"
                value={settings.invoicePrefix}
                onChange={(event) =>
                  onChange(
                    "invoicePrefix",
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
                fullWidth
                type="number"
                label="Next Invoice Number"
                value={settings.nextInvoiceNumber}
                onChange={(event) =>
                  onChange(
                    "nextInvoiceNumber",
                    Number(event.target.value)
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
              <FormControlLabel
                control={
                  <Switch
                    checked={
                      settings.automaticInvoiceGeneration
                    }
                    onChange={(event) =>
                      onChange(
                        "automaticInvoiceGeneration",
                        event.target.checked
                      )
                    }
                  />
                }
                label="Enable Automatic Invoice Generation"
              />
            </Grid>

            <Grid
              size={{
                xs: 12,
                md: 6,
              }}
            >
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.includeCompanyLogo}
                    onChange={(event) =>
                      onChange(
                        "includeCompanyLogo",
                        event.target.checked
                      )
                    }
                  />
                }
                label="Include Company Logo"
              />
            </Grid>
          </Grid>
        </Stack>
      </CardContent>
    </Card>
  );
}