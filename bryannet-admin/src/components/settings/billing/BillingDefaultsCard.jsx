import {
  Card,
  CardContent,
  Grid,
  MenuItem,
  Stack,
  TextField,
  Typography,
} from "@mui/material";

export default function BillingDefaultsCard({
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
            Billing Defaults
          </Typography>

          <Grid container spacing={3}>
            <Grid
              size={{
                xs: 12,
                md: 6,
              }}
            >
              <TextField
                select
                fullWidth
                label="Currency"
                value={settings.currency}
                onChange={(event) =>
                  onChange(
                    "currency",
                    event.target.value
                  )
                }
              >
                <MenuItem value="NGN">
                  Nigerian Naira (NGN)
                </MenuItem>

                <MenuItem value="USD">
                  US Dollar (USD)
                </MenuItem>

                <MenuItem value="EUR">
                  Euro (EUR)
                </MenuItem>

                <MenuItem value="GBP">
                  British Pound (GBP)
                </MenuItem>
              </TextField>
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
                label="Billing Cycle"
                value={settings.billingCycle}
                onChange={(event) =>
                  onChange(
                    "billingCycle",
                    event.target.value
                  )
                }
              >
                <MenuItem value="Weekly">
                  Weekly
                </MenuItem>

                <MenuItem value="Monthly">
                  Monthly
                </MenuItem>

                <MenuItem value="Quarterly">
                  Quarterly
                </MenuItem>

                <MenuItem value="Yearly">
                  Yearly
                </MenuItem>
              </TextField>
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
                label="Grace Period"
                value={settings.gracePeriod}
                onChange={(event) =>
                  onChange(
                    "gracePeriod",
                    event.target.value
                  )
                }
              >
                <MenuItem value="0 Days">
                  0 Days
                </MenuItem>

                <MenuItem value="3 Days">
                  3 Days
                </MenuItem>

                <MenuItem value="7 Days">
                  7 Days
                </MenuItem>

                <MenuItem value="14 Days">
                  14 Days
                </MenuItem>
              </TextField>
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
                label="Default Due Days"
                value={settings.defaultDueDays}
                onChange={(event) =>
                  onChange(
                    "defaultDueDays",
                    Number(event.target.value)
                  )
                }
              />
            </Grid>
          </Grid>
        </Stack>
      </CardContent>
    </Card>
  );
}
