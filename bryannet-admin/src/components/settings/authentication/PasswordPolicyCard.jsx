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

export default function PasswordPolicyCard({
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
            Password Policy
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
                type="number"
                label="Minimum Password Length"
                value={settings.minimumPasswordLength}
                onChange={(event) =>
                  onChange(
                    "minimumPasswordLength",
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
                label="Password Expiry"
                value={settings.passwordExpiry}
                onChange={(event) =>
                  onChange(
                    "passwordExpiry",
                    event.target.value
                  )
                }
              >
                <MenuItem value="30 Days">
                  30 Days
                </MenuItem>

                <MenuItem value="60 Days">
                  60 Days
                </MenuItem>

                <MenuItem value="90 Days">
                  90 Days
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
                    checked={settings.requireUppercase}
                    onChange={(event) =>
                      onChange(
                        "requireUppercase",
                        event.target.checked
                      )
                    }
                  />
                }
                label="Require Uppercase Letters"
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
                    checked={settings.requireLowercase}
                    onChange={(event) =>
                      onChange(
                        "requireLowercase",
                        event.target.checked
                      )
                    }
                  />
                }
                label="Require Lowercase Letters"
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
                    checked={settings.requireNumbers}
                    onChange={(event) =>
                      onChange(
                        "requireNumbers",
                        event.target.checked
                      )
                    }
                  />
                }
                label="Require Numbers"
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
                      settings.requireSpecialCharacters
                    }
                    onChange={(event) =>
                      onChange(
                        "requireSpecialCharacters",
                        event.target.checked
                      )
                    }
                  />
                }
                label="Require Special Characters"
              />
            </Grid>
          </Grid>
        </Stack>
      </CardContent>
    </Card>
  );
}