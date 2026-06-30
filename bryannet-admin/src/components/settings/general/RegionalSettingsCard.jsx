import {
  Card,
  CardContent,
  Grid,
  MenuItem,
  Stack,
  TextField,
  Typography,
} from "@mui/material";

export default function RegionalSettingsCard({
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
            Regional Settings
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
                label="Time Zone"
                value={settings.timeZone}
                onChange={(event) =>
                  onChange(
                    "timeZone",
                    event.target.value
                  )
                }
              >
                <MenuItem value="Africa/Lagos">
                  Africa/Lagos
                </MenuItem>

                <MenuItem value="UTC">
                  UTC
                </MenuItem>

                <MenuItem value="Europe/London">
                  Europe/London
                </MenuItem>

                <MenuItem value="America/New_York">
                  America/New_York
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
                label="Language"
                value={settings.language}
                onChange={(event) =>
                  onChange(
                    "language",
                    event.target.value
                  )
                }
              >
                <MenuItem value="English">
                  English
                </MenuItem>

                <MenuItem value="French">
                  French
                </MenuItem>

                <MenuItem value="Spanish">
                  Spanish
                </MenuItem>
              </TextField>
            </Grid>

            <Grid
              size={{
                xs: 12,
                md: 4,
              }}
            >
              <TextField
                select
                fullWidth
                label="Date Format"
                value={settings.dateFormat}
                onChange={(event) =>
                  onChange(
                    "dateFormat",
                    event.target.value
                  )
                }
              >
                <MenuItem value="DD/MM/YYYY">
                  DD/MM/YYYY
                </MenuItem>

                <MenuItem value="MM/DD/YYYY">
                  MM/DD/YYYY
                </MenuItem>

                <MenuItem value="YYYY-MM-DD">
                  YYYY-MM-DD
                </MenuItem>
              </TextField>
            </Grid>

            <Grid
              size={{
                xs: 12,
                md: 4,
              }}
            >
              <TextField
                select
                fullWidth
                label="Time Format"
                value={settings.timeFormat}
                onChange={(event) =>
                  onChange(
                    "timeFormat",
                    event.target.value
                  )
                }
              >
                <MenuItem value="24 Hour">
                  24 Hour
                </MenuItem>

                <MenuItem value="12 Hour">
                  12 Hour
                </MenuItem>
              </TextField>
            </Grid>

            <Grid
              size={{
                xs: 12,
                md: 4,
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
          </Grid>
        </Stack>
      </CardContent>
    </Card>
  );
}