import {
  Card,
  CardContent,
  Grid,
  Stack,
  TextField,
  Typography,
} from "@mui/material";

export default function PlatformInformationCard({
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
            Platform Information
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
                label="Platform Name"
                value={settings.platformName}
                onChange={(event) =>
                  onChange(
                    "platformName",
                    event.target.value
                  )
                }
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
                label="Company Name"
                value={settings.companyName}
                onChange={(event) =>
                  onChange(
                    "companyName",
                    event.target.value
                  )
                }
              />
            </Grid>

            <Grid size={12}>
              <TextField
                fullWidth
                multiline
                minRows={3}
                label="Platform Description"
                value={settings.platformDescription}
                onChange={(event) =>
                  onChange(
                    "platformDescription",
                    event.target.value
                  )
                }
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
                label="Company Email"
                type="email"
                value={settings.companyEmail}
                onChange={(event) =>
                  onChange(
                    "companyEmail",
                    event.target.value
                  )
                }
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
                label="Company Phone"
                value={settings.companyPhone}
                onChange={(event) =>
                  onChange(
                    "companyPhone",
                    event.target.value
                  )
                }
              />
            </Grid>
          </Grid>
        </Stack>
      </CardContent>
    </Card>
  );
}