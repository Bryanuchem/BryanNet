import {
  Card,
  CardContent,
  FormControlLabel,
  Grid,
  Stack,
  Switch,
  Typography,
} from "@mui/material";

export default function TelegramNotificationsCard({
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
            Telegram Notifications
          </Typography>

          <Grid container spacing={3}>
            <Grid size={12}>
              <FormControlLabel
                control={
                  <Switch
                    checked={
                      settings.enableTelegramNotifications
                    }
                    onChange={(event) =>
                      onChange(
                        "enableTelegramNotifications",
                        event.target.checked
                      )
                    }
                  />
                }
                label="Enable Telegram Notifications"
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
                      settings.notifyNewCustomerTelegram
                    }
                    onChange={(event) =>
                      onChange(
                        "notifyNewCustomerTelegram",
                        event.target.checked
                      )
                    }
                  />
                }
                label="Notify on New Customer"
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
                      settings.notifyNewPaymentTelegram
                    }
                    onChange={(event) =>
                      onChange(
                        "notifyNewPaymentTelegram",
                        event.target.checked
                      )
                    }
                  />
                }
                label="Notify on New Payment"
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
                      settings.notifyRouterEventsTelegram
                    }
                    onChange={(event) =>
                      onChange(
                        "notifyRouterEventsTelegram",
                        event.target.checked
                      )
                    }
                  />
                }
                label="Notify on Router Events"
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
                      settings.notifySystemErrorsTelegram
                    }
                    onChange={(event) =>
                      onChange(
                        "notifySystemErrorsTelegram",
                        event.target.checked
                      )
                    }
                  />
                }
                label="Notify on System Errors"
              />
            </Grid>
          </Grid>
        </Stack>
      </CardContent>
    </Card>
  );
}