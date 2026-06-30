import {
  Card,
  CardContent,
  Grid,
  MenuItem,
  Stack,
  TextField,
  Typography,
} from "@mui/material";

export default function OrganizationDetailsCard({
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
            Organization Details
          </Typography>

          <Grid container spacing={3}>
            <Grid size={12}>
              <TextField
                fullWidth
                label="Address"
                value={settings.address}
                onChange={(event) =>
                  onChange(
                    "address",
                    event.target.value
                  )
                }
              />
            </Grid>

            <Grid
              size={{
                xs: 12,
                md: 4,
              }}
            >
              <TextField
                fullWidth
                label="City"
                value={settings.city}
                onChange={(event) =>
                  onChange(
                    "city",
                    event.target.value
                  )
                }
              />
            </Grid>

            <Grid
              size={{
                xs: 12,
                md: 4,
              }}
            >
              <TextField
                fullWidth
                label="State / Province"
                value={settings.state}
                onChange={(event) =>
                  onChange(
                    "state",
                    event.target.value
                  )
                }
              />
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
                label="Country"
                value={settings.country}
                onChange={(event) =>
                  onChange(
                    "country",
                    event.target.value
                  )
                }
              >
                <MenuItem value="Nigeria">
                  Nigeria
                </MenuItem>

                <MenuItem value="Ghana">
                  Ghana
                </MenuItem>

                <MenuItem value="Kenya">
                  Kenya
                </MenuItem>

                <MenuItem value="South Africa">
                  South Africa
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
                fullWidth
                label="Postal Code"
                value={settings.postalCode}
                onChange={(event) =>
                  onChange(
                    "postalCode",
                    event.target.value
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