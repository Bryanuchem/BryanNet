import {
  Card,
  CardContent,
  FormControlLabel,
  Grid,
  Stack,
  Switch,
  Typography,
} from "@mui/material";

export default function SystemAlertsCard({
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
            System Alerts
          </Typography>

          <Grid container spacing={3}>
            <Grid size={12}>
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.enableSystemAlerts}
                    onChange={(event) =>
                      onChange(
                        "enableSystemAlerts",
                        event.target.checked
                      )
                    }
                  />
                }
                label="Enable System Alerts"
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
                    checked={settings.maintenanceAlerts}
                    onChange={(event) =>
                      onChange(
                        "maintenanceAlerts",
                        event.target.checked
                      )
                    }
                  />
                }
                label="Maintenance Alerts"
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
                    checked={settings.securityAlerts}
                    onChange={(event) =>
                      onChange(
                        "securityAlerts",
                        event.target.checked
                      )
                    }
                  />
                }
                label="Security Alerts"
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
                    checked={settings.backupAlerts}
                    onChange={(event) =>
                      onChange(
                        "backupAlerts",
                        event.target.checked
                      )
                    }
                  />
                }
                label="Backup Alerts"
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
                    checked={settings.highPriorityEvents}
                    onChange={(event) =>
                      onChange(
                        "highPriorityEvents",
                        event.target.checked
                      )
                    }
                  />
                }
                label="High Priority Events"
              />
            </Grid>
          </Grid>
        </Stack>
      </CardContent>
    </Card>
  );
}