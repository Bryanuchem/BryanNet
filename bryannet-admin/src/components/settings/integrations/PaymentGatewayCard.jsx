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

export default function PaymentGatewayCard({
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
            Payment Gateway
          </Typography>

          <Grid container spacing={3}>
            <Grid size={12}>
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.paymentGatewayEnabled}
                    onChange={(event) =>
                      onChange(
                        "paymentGatewayEnabled",
                        event.target.checked
                      )
                    }
                  />
                }
                label="Enable Payment Gateway"
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
                label="Gateway Provider"
                value={settings.paymentProvider}
                onChange={(event) =>
                  onChange(
                    "paymentProvider",
                    event.target.value
                  )
                }
              >
                <MenuItem value="Paystack">
                  Paystack
                </MenuItem>

                <MenuItem value="Flutterwave">
                  Flutterwave
                </MenuItem>

                <MenuItem value="Monnify">
                  Monnify
                </MenuItem>

                <MenuItem value="Stripe">
                  Stripe
                </MenuItem>
              </TextField>
            </Grid>

            <Grid
              size={{
                xs: 12,
                md: 3,
              }}
            >
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.sandboxMode}
                    onChange={(event) =>
                      onChange(
                        "sandboxMode",
                        event.target.checked
                      )
                    }
                  />
                }
                label="Sandbox Mode"
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
                  Connection Status
                </Typography>

                <Chip
                  label={settings.paymentConnectionStatus}
                  color={
                    settings.paymentConnectionStatus ===
                    "Connected"
                      ? "success"
                      : "default"
                  }
                />
              </Stack>
            </Grid>

            <Grid
              size={12}
              display="flex"
              justifyContent="flex-end"
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