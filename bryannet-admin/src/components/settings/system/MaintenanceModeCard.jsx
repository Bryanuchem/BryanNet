import {
  Card,
  CardContent,
  FormControlLabel,
  Grid,
  Stack,
  Switch,
  TextField,
  Typography,
} from "@mui/material";

export default function MaintenanceModeCard({
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
            Maintenance Mode
          </Typography>

          <Grid container spacing={3}>
            <Grid size={12}>
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.maintenanceMode}
                    onChange={(event) =>
                      onChange(
                        "maintenanceMode",
                        event.target.checked
                      )
                    }
                  />
                }
                label="Enable Maintenance Mode"
              />
            </Grid>

            <Grid size={12}>
              <TextField
                fullWidth
                multiline
                minRows={3}
                label="Maintenance Message"
                value={settings.maintenanceMessage}
                onChange={(event) =>
                  onChange(
                    "maintenanceMessage",
                    event.target.value
                  )
                }
              />
            </Grid>

            <Grid size={12}>
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.allowAdminAccess}
                    onChange={(event) =>
                      onChange(
                        "allowAdminAccess",
                        event.target.checked
                      )
                    }
                  />
                }
                label="Allow Administrator Access During Maintenance"
              />
            </Grid>
          </Grid>
        </Stack>
      </CardContent>
    </Card>
  );
}