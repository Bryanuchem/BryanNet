import {
  Button,
  Card,
  CardContent,
  Chip,
  FormControlLabel,
  Grid,
  Stack,
  Switch,
  TextField,
  Typography,
} from "@mui/material";

export default function TelegramIntegrationCard({
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
            Telegram Bot
          </Typography>

          <Grid container spacing={3}>
            <Grid size={12}>
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.telegramEnabled}
                    onChange={(event) =>
                      onChange(
                        "telegramEnabled",
                        event.target.checked
                      )
                    }
                  />
                }
                label="Enable Telegram Bot"
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
                label="Bot Username"
                value={settings.telegramBotUsername}
                onChange={(event) =>
                  onChange(
                    "telegramBotUsername",
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
              <Stack spacing={1}>
                <Typography
                  variant="body2"
                  color="text.secondary"
                >
                  Webhook Status
                </Typography>

                <Chip
                  label={settings.telegramWebhookStatus}
                  color={
                    settings.telegramWebhookStatus ===
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