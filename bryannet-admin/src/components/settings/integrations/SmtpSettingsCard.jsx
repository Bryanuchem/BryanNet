import {
  Button,
  Card,
  CardContent,
  Chip,
  FormControlLabel,
  Grid,
  MenuItem,
  Stack,
  Switch,
  TextField,
  Typography,
} from "@mui/material";

export default function SmtpSettingsCard({
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
            SMTP Email
          </Typography>

          <Grid container spacing={3}>
            <Grid size={12}>
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.smtpEnabled}
                    onChange={(event) =>
                      onChange(
                        "smtpEnabled",
                        event.target.checked
                      )
                    }
                  />
                }
                label="Enable SMTP"
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
                label="SMTP Host"
                value={settings.smtpHost}
                onChange={(event) =>
                  onChange(
                    "smtpHost",
                    event.target.value
                  )
                }
              />
            </Grid>

            <Grid
              size={{
                xs: 12,
                md: 3,
              }}
            >
              <TextField
                fullWidth
                type="number"
                label="SMTP Port"
                value={settings.smtpPort}
                onChange={(event) =>
                  onChange(
                    "smtpPort",
                    Number(event.target.value)
                  )
                }
              />
            </Grid>

            <Grid
              size={{
                xs: 12,
                md: 3,
              }}
            >
              <TextField
                select
                fullWidth
                label="Encryption"
                value={settings.smtpEncryption}
                onChange={(event) =>
                  onChange(
                    "smtpEncryption",
                    event.target.value
                  )
                }
              >
                <MenuItem value="None">
                  None
                </MenuItem>

                <MenuItem value="SSL">
                  SSL
                </MenuItem>

                <MenuItem value="TLS">
                  TLS
                </MenuItem>
              </TextField>
            </Grid>

            <Grid
              size={{
                xs: 12,
                md: 3,
              }}
            >
              <Stack spacing={1}>
                <Typography
                  variant="body2"
                  color="text.secondary"
                >
                  Connection Status
                </Typography>

                <Chip
                  label={settings.smtpConnectionStatus}
                  color={
                    settings.smtpConnectionStatus ===
                    "Connected"
                      ? "success"
                      : "default"
                  }
                />
              </Stack>
            </Grid>

            <Grid
              size={{
                xs: 12,
                md: 9,
              }}
              display="flex"
              justifyContent="flex-end"
              alignItems="flex-end"
            >
              <Button
                variant="outlined"
              >
                Test Connection
              </Button>
            </Grid>
          </Grid>
        </Stack>
      </CardContent>
    </Card>
  );
}