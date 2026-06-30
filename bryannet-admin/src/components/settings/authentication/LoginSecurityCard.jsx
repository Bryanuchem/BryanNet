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

export default function LoginSecurityCard({
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
            Login Security
          </Typography>

          <Grid container spacing={3}>
            <Grid
              size={{
                xs: 12,
                md: 6,
              }}
            >
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.twoFactorAuthentication}
                    onChange={(event) =>
                      onChange(
                        "twoFactorAuthentication",
                        event.target.checked
                      )
                    }
                  />
                }
                label="Enable Two-Factor Authentication"
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
                    checked={settings.allowPasswordReset}
                    onChange={(event) =>
                      onChange(
                        "allowPasswordReset",
                        event.target.checked
                      )
                    }
                  />
                }
                label="Allow Password Reset"
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
                label="Maximum Login Attempts"
                value={settings.maximumLoginAttempts}
                onChange={(event) =>
                  onChange(
                    "maximumLoginAttempts",
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
              <TextField
                select
                fullWidth
                label="Lockout Duration"
                value={settings.lockoutDuration}
                onChange={(event) =>
                  onChange(
                    "lockoutDuration",
                    event.target.value
                  )
                }
              >
                <MenuItem value="5 Minutes">
                  5 Minutes
                </MenuItem>

                <MenuItem value="15 Minutes">
                  15 Minutes
                </MenuItem>

                <MenuItem value="30 Minutes">
                  30 Minutes
                </MenuItem>

                <MenuItem value="1 Hour">
                  1 Hour
                </MenuItem>

                <MenuItem value="24 Hours">
                  24 Hours
                </MenuItem>
              </TextField>
            </Grid>
          </Grid>
        </Stack>
      </CardContent>
    </Card>
  );
}