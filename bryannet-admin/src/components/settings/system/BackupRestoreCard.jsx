import {
  Button,
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

export default function BackupRestoreCard({
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
            Backup & Restore
          </Typography>

          <Grid container spacing={3}>
            <Grid size={12}>
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.automaticBackups}
                    onChange={(event) =>
                      onChange(
                        "automaticBackups",
                        event.target.checked
                      )
                    }
                  />
                }
                label="Enable Automatic Backups"
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
                label="Backup Frequency"
                value={settings.backupFrequency}
                onChange={(event) =>
                  onChange(
                    "backupFrequency",
                    event.target.value
                  )
                }
              >
                <MenuItem value="Hourly">
                  Hourly
                </MenuItem>

                <MenuItem value="Daily">
                  Daily
                </MenuItem>

                <MenuItem value="Weekly">
                  Weekly
                </MenuItem>

                <MenuItem value="Monthly">
                  Monthly
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
                label="Last Backup"
                value={settings.lastBackup}
                InputProps={{
                  readOnly: true,
                }}
              />
            </Grid>

            <Grid
              size={{
                xs: 12,
                md: 6,
              }}
            >
              <Button
                fullWidth
                variant="outlined"
              >
                Backup Now
              </Button>
            </Grid>

            <Grid
              size={{
                xs: 12,
                md: 6,
              }}
            >
              <Button
                fullWidth
                color="warning"
                variant="outlined"
              >
                Restore Backup
              </Button>
            </Grid>
          </Grid>
        </Stack>
      </CardContent>
    </Card>
  );
}