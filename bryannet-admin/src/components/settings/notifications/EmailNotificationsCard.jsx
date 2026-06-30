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

export default function EmailNotificationsCard({
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
            Email Notifications
          </Typography>

          <Grid container spacing={3}>
            <Grid size={12}>
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.enableEmailNotifications}
                    onChange={(event) =>
                      onChange(
                        "enableEmailNotifications",
                        event.target.checked
                      )
                    }
                  />
                }
                label="Enable Email Notifications"
              />
            </Grid>

            <Grid size={12}>
              <TextField
                fullWidth
                type="email"
                label="Administrator Notification Email"
                value={settings.adminNotificationEmail}
                onChange={(event) =>
                  onChange(
                    "adminNotificationEmail",
                    event.target.value
                  )
                }
              />
            </Grid>

            <Grid
              size={{
                xs: 12,
                md: 4,
              }}
            >
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.notifyNewCustomerEmail}
                    onChange={(event) =>
                      onChange(
                        "notifyNewCustomerEmail",
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
                md: 4,
              }}
            >
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.notifyNewPaymentEmail}
                    onChange={(event) =>
                      onChange(
                        "notifyNewPaymentEmail",
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
                md: 4,
              }}
            >
              <FormControlLabel
                control={
                  <Switch
                    checked={
                      settings.notifySubscriptionExpiryEmail
                    }
                    onChange={(event) =>
                      onChange(
                        "notifySubscriptionExpiryEmail",
                        event.target.checked
                      )
                    }
                  />
                }
                label="Notify on Subscription Expiry"
              />
            </Grid>
          </Grid>
        </Stack>
      </CardContent>
    </Card>
  );
}