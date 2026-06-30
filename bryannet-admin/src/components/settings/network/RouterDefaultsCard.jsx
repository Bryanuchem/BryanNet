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

export default function IpAddressManagementCard({
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
            IP Address Management
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
                label="Address Pool"
                value={settings.addressPool}
                onChange={(event) =>
                  onChange(
                    "addressPool",
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
                label="Lease Duration"
                value={settings.leaseDuration}
                onChange={(event) =>
                  onChange(
                    "leaseDuration",
                    event.target.value
                  )
                }
              >
                <MenuItem value="1 Hour">
                  1 Hour
                </MenuItem>

                <MenuItem value="12 Hours">
                  12 Hours
                </MenuItem>

                <MenuItem value="24 Hours">
                  24 Hours
                </MenuItem>

                <MenuItem value="7 Days">
                  7 Days
                </MenuItem>

                <MenuItem value="Never">
                  Never
                </MenuItem>
              </TextField>
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
                    checked={settings.dhcpEnabled}
                    onChange={(event) =>
                      onChange(
                        "dhcpEnabled",
                        event.target.checked
                      )
                    }
                  />
                }
                label="Enable DHCP"
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
                    checked={settings.autoAssignAddresses}
                    onChange={(event) =>
                      onChange(
                        "autoAssignAddresses",
                        event.target.checked
                      )
                    }
                  />
                }
                label="Automatically Assign IP Addresses"
              />
            </Grid>
          </Grid>
        </Stack>
      </CardContent>
    </Card>
  );
}