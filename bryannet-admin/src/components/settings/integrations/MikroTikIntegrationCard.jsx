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

export default function MikroTikIntegrationCard({
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
            MikroTik Router
          </Typography>

          <Grid container spacing={3}>
            <Grid size={12}>
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.mikrotikEnabled}
                    onChange={(event) =>
                      onChange(
                        "mikrotikEnabled",
                        event.target.checked
                      )
                    }
                  />
                }
                label="Enable MikroTik Integration"
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
                label="Default Router"
                value={settings.defaultRouter}
                onChange={(event) =>
                  onChange(
                    "defaultRouter",
                    event.target.value
                  )
                }
              >
                <MenuItem value="Main Router">
                  Main Router
                </MenuItem>

                <MenuItem value="Branch Router">
                  Branch Router
                </MenuItem>

                <MenuItem value="Test Router">
                  Test Router
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
                  label={settings.routerConnectionStatus}
                  color={
                    settings.routerConnectionStatus ===
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
                md: 3,
              }}
              display="flex"
              alignItems="flex-end"
            >
              <Button
                fullWidth
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