import {
  Button,
  Card,
  CardContent,
  Chip,
  Grid,
  Stack,
  TextField,
  Typography,
} from "@mui/material";

export default function SystemHealthCard({
  settings,
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
            System Health
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
                label="Platform Version"
                value={settings.platformVersion}
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
              <Stack spacing={1}>
                <Typography
                  variant="body2"
                  color="text.secondary"
                >
                  Database Status
                </Typography>

                <Chip
                  label={settings.databaseStatus}
                  color={
                    settings.databaseStatus === "Healthy"
                      ? "success"
                      : "error"
                  }
                />
              </Stack>
            </Grid>

            <Grid
              size={{
                xs: 12,
                md: 6,
              }}
            >
              <TextField
                fullWidth
                label="Storage Usage"
                value={settings.storageUsage}
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
              <Stack spacing={1}>
                <Typography
                  variant="body2"
                  color="text.secondary"
                >
                  Background Services
                </Typography>

                <Chip
                  label={settings.backgroundServices}
                  color={
                    settings.backgroundServices === "Running"
                      ? "success"
                      : "warning"
                  }
                />
              </Stack>
            </Grid>

            <Grid size={12}>
              <Button
                variant="outlined"
                fullWidth
              >
                Run Diagnostics
              </Button>
            </Grid>
          </Grid>
        </Stack>
      </CardContent>
    </Card>
  );
}