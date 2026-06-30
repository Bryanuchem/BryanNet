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

export default function SessionManagementCard({
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
            Session Management
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
                label="Session Timeout"
                value={settings.sessionTimeout}
                onChange={(event) =>
                  onChange(
                    "sessionTimeout",
                    event.target.value
                  )
                }
              >
                <MenuItem value="15 Minutes">
                  15 Minutes
                </MenuItem>

                <MenuItem value="30 Minutes">
                  30 Minutes
                </MenuItem>

                <MenuItem value="1 Hour">
                  1 Hour
                </MenuItem>

                <MenuItem value="2 Hours">
                  2 Hours
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
                label="Maximum Concurrent Sessions"
                value={settings.maximumConcurrentSessions}
                onChange={(event) =>
                  onChange(
                    "maximumConcurrentSessions",
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
                    checked={settings.rememberMe}
                    onChange={(event) =>
                      onChange(
                        "rememberMe",
                        event.target.checked
                      )
                    }
                  />
                }
                label="Enable Remember Me"
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
                    checked={settings.automaticLogout}
                    onChange={(event) =>
                      onChange(
                        "automaticLogout",
                        event.target.checked
                      )
                    }
                  />
                }
                label="Automatic Logout on Inactivity"
              />
            </Grid>
          </Grid>
        </Stack>
      </CardContent>
    </Card>
  );
}